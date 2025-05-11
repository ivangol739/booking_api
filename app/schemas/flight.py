from pydantic import BaseModel
from datetime import datetime


class FlightBase(BaseModel):
    flight_number: str
    departure_city: str
    arrival_city: str
    departure_time: datetime
    arrival_time: datetime
    price: float
    available_seats: int

class FlightCreate(FlightBase):
    pass

class FlightUpdate(BaseModel):
    price: float | None = None
    available_seats: int | None = None

class FlightResponse(FlightBase):
    id: int

    class Config:
        orm_mode = True