from fastapi import FastAPI
from app.routers import flight, bookings, auth

app = FastAPI(title="Flight Booking API")

@app.get("/")
async def welcome() -> dict:
    return {"message": "My booking of flights app"}

app.include_router(flight.router)
app.include_router(bookings.router)
app.include_router(auth.router)
