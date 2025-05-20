from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship, DeclarativeBase
import enum
from datetime import datetime
from app.backend.db import Base


class BookingStatus(str, enum.Enum):
    confirmed = "confirmed"
    canceled = "canceled"

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    flight_id = Column(Integer, ForeignKey("flights.id"), nullable=False)
    booking_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(BookingStatus), default=BookingStatus.confirmed)
    seats = Column(Integer, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)

    user = relationship("User", back_populates="bookings")
    flight = relationship("Flight", back_populates="bookings")

