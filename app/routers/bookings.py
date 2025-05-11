from fastapi import APIRouter

router = APIRouter(prefix='/bookings', tags=['bookings'])

@router.get('/')
async def all_bookings():
    pass

@router.post('/')
async def create_booking():
    pass

@router.get('/{flight_slug}')
async def booking_by_flight(flight_slug: str):
    pass

@router.get('/detail/{booking_slug}')
async def booking_detail(booking_slug: str):
    pass

@router.put('/{booking_slug}')
async def update_booking(booking_slug: str):
    pass

@router.delete('/')
async def delete_booking(booking_id: int):
    pass