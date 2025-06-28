from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from sqlalchemy import insert

from app.backend.db_depends import get_db
from app.schemas.flight import FlightBase, FlightCreate, FlightUpdate, FlightResponse
from app.models.flight import Flight
from sqlalchemy import select

from slugify import slugify
from datetime import datetime
from app.routers.auth import get_current_user


router = APIRouter(prefix='/flights', tags=['flights'])

@router.get('/')
async def get_all_flights(db: Annotated[AsyncSession, Depends(get_db)]):
    flights = await db.scalars(select(Flight))
    return flights.all()

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_flight(db: Annotated[AsyncSession, Depends(get_db)], flight_data: FlightCreate, get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user.get('is_admin'):
        await db.execute(insert(Flight).values(
            flight_number=flight_data.flight_number,
            departure_city=flight_data.departure_city,
            arrival_city=flight_data.arrival_city,
            departure_time=flight_data.departure_time,
            arrival_time=flight_data.arrival_time,
            price=flight_data.price,
            available_seats=flight_data.available_seats,
            slug=slugify(flight_data.flight_number),
        ))
        await db.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You must be admin user for this'
        )

@router.put('/{flight_slug}')
async def update_flight(db: Annotated[AsyncSession, Depends(get_db)], flight_slug: str, flight_data: FlightUpdate, get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user.get('is_admin'):
        flight = await db.scalar(select(Flight).where(Flight.slug == flight_slug))
        if flight is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Flight not found')

        flight.price = flight_data.price
        flight.available_seats = flight_data.available_seats

        await db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Flight update is successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You must be admin user for this'
        )


@router.delete('/{flight_slug}')
async def delete_flight(db: Annotated[AsyncSession, Depends(get_db)], flight_slug: str, get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user.get('is_admin'):
        flight = await db.scalar(select(Flight).where(Flight.slug == flight_slug))
        if flight is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Flight not found')

        await db.delete(flight)
        await db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Flight delete is successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You must be admin user for this'
        )