from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from datetime import timedelta

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.get("/", response_model=list[schemas.BookingOut])
def list_bookings(db: Session = Depends(get_db)):
    return db.query(models.Booking).order_by(models.Booking.id.desc()).all()

@router.post("/", response_model=schemas.BookingOut)
def create_booking(payload: schemas.BookingCreate, db: Session = Depends(get_db)):
    service = db.get(models.Service, payload.service_id)
    barber = db.get(models.Barber, payload.barber_id)
    if not service or not barber:
        raise HTTPException(400, "Invalid service or barber")
    start = payload.start_datetime
    end = start + timedelta(minutes=service.duration)

    exists = db.query(models.Booking).filter(
        models.Booking.barber_id == payload.barber_id,
        models.Booking.status == "confirmed",
        ~((models.Booking.end_datetime <= start) | (models.Booking.start_datetime >= end))
    ).first()
    if exists:
        raise HTTPException(409, "Slot not available")

    obj = models.Booking(
        customer_name=payload.customer_name,
        customer_phone=payload.customer_phone,
        service_id=payload.service_id,
        barber_id=payload.barber_id,
        start_datetime=start,
        end_datetime=end,
        status="confirmed"
    )
    db.add(obj); db.commit(); db.refresh(obj)
    return obj
