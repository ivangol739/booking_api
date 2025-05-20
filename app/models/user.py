from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.backend.db import Base
import enum

class RoleEnum(str, enum.Enum):
    user = "user"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.user)

    bookings = relationship("Booking", back_populates="user")