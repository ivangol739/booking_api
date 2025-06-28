from fastapi import APIRouter, Depends, status, HTTPException
from app.backend.db_depends import get_db
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import insert
from app.schemas.booking import BookingCreate, BookingResponse, BookingUpdate
from app.models.bookings import Booking
from app.models.flight import Flight
from slugify import slugify
from datetime import datetime
from app.routers.auth import get_current_user


router = APIRouter(prefix='/bookings', tags=['bookings'])

@router.get('/')
async def all_bookings(db: Annotated[AsyncSession, Depends(get_db)]):
    bookings = await db.scalars(select(Booking))
    return bookings.all()

@router.post('/')
async def create_booking(db: Annotated[AsyncSession, Depends(get_db)], booking_data: BookingCreate, get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user.get('is_admin') or get_user.get('is_supplier'):
        flight = await db.scalar(select(Flight).where(Flight.id == booking_data.flight_id))
        if flight is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Flight not found')
        if flight.available_seats < booking_data.seats:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not enough seats available')

        slug = slugify(f"booking-{get_user.get('id')}-{flight.id}-{datetime.utcnow().timestamp()}")

        await db.execute(insert(Booking).values(
            user_id=get_user.get('id'),
            flight_id=booking_data.flight_id,
            seats=booking_data.seats,
            slug=slug,
            status="confirmed",
        ))

        flight.available_seats -= booking_data.seats

        await db.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You have not enough permission for this action'
        )


@router.get('/{flight_slug}')
async def booking_by_flight(db: Annotated[AsyncSession, Depends(get_db)], flight_slug: str):
    flight = await db.scalar(select(Flight).where(Flight.slug == flight_slug))
    if flight is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Flight not found')

    bookings = await db.scalars(select(Booking).where(Booking.flight_id == flight.id, Booking.status == "confirmed"))
    return bookings.all()


@router.get('/detail/{booking_slug}')
async def booking_detail(db: Annotated[AsyncSession, Depends(get_db)] ,booking_slug: str):
    booking = await db.scalar(select(Booking).where(Booking.slug == booking_slug))
    if booking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Booking not found')

    return booking

@router.put('/{booking_slug}')
async def update_booking(db: Annotated[AsyncSession, Depends(get_db)], update_data: BookingUpdate, booking_slug: str, get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user.get('is_admin') or get_user.get('is_supplier'):
        booking = await db.scalar(select(Booking).where(Booking.slug == booking_slug))
        if booking is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Booking not found')

        flight = await db.scalar(select(Flight).where(Flight.id == booking.flight_id))
        if flight is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Flight not found')

        # Обновляем количество мест, если передано
        if update_data.seats is not None:
            seats_diff = update_data.seats - booking.seats
            if flight.available_seats < seats_diff:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not enough seats available')

            flight.available_seats -= seats_diff
            booking.seats = update_data.seats

        # Обновляем статус, если передан
        if update_data.status is not None:
            if booking.status != update_data.status:
                # Если отменяем — возвращаем места
                if update_data.status == "canceled" and booking.status != "canceled":
                    flight.available_seats += booking.seats
                # Если меняем обратно на confirmed — проверяем доступность мест
                if update_data.status == "confirmed" and booking.status == "canceled":
                    if flight.available_seats < booking.seats:
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Not enough seats available')
                    flight.available_seats -= booking.seats
                booking.status = update_data.status

        db.add_all([booking, flight])
        await db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Booking update is successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You have not enough permission for this action'
        )


@router.delete('/{booking_slug}')
async def delete_booking(db: Annotated[AsyncSession, Depends(get_db)], booking_id: int, get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user.get('is_admin') or get_user.get('is_supplier'):
        booking = await db.get(Booking, booking_id)
        if booking is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Booking not found')
        flight = await db.get(Flight, booking.flight_id)
        flight.available_seats += booking.seats
        await db.delete(booking)
        await db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Booking delete is successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You have not enough permission for this action'
        )