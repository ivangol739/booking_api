from fastapi import FastAPI
from app.routers import flight, bookings

app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return {"message": "My booking of flights app"}

app.include_router(flight.router)
app.include_router(bookings.router)
