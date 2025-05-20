from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from sqlalchemy import insert
from slugify import slugify

from app.backend.db_depends import get_db
from app.schemas.flight import FlightBase, FlightCreate, FlightUpdate, FlightResponse
from app.models.bookings import Booking
from app.models.flight import Flight

router = APIRouter(prefix='/flights', tags=['flights'])

@router.get('/')
async def get_all_flights():
    pass

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_flight(db: Annotated[AsyncSession, Depends(get_db)], flight_data: FlightCreate):
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

@router.put('/')
async def update_flight():
    pass

@router.delete('/')
async def delete_flight():
    pass