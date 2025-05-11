from fastapi import APIRouter

router = APIRouter(prefix='/flights', tags=['flight'])

@router.get('/')
async def get_all_flights():
    pass

@router.post('/')
async def create_flight():
    pass

@router.put('/')
async def update_flight():
    pass

@router.delete('/')
async def delete_flight():
    pass