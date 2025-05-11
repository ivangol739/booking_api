from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class BookingStatus(str, Enum):
    confirmed = "confirmed"
    canceled = "canceled"

class BookingBase(BaseModel):
    flight_id: int
    seats: int

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    status: BookingStatus | None = None
    seats: int | None = None

class BookingResponse(BookingBase):
    id: int
    user_id: int
    booking_date: datetime
    status: BookingStatus

    class Config:
        orm_mode = True