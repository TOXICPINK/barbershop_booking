from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from .. import models
from ..database import get_db

router = APIRouter(prefix="/availability", tags=["availability"])

def _minutes(h: int, m: int) -> int:
    return h*60 + m

@router.get("/")
def get_availability(
    barber_id: int = Query(...),
    date: str = Query(...),
    service_duration: int = Query(30),
    db: Session = Depends(get_db)
):
    barber = db.get(models.Barber, barber_id)
    if not barber: raise HTTPException(404, "Barber not found")

    try:
        d = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(400, "Invalid date format, expected YYYY-MM-DD")

    weekday = d.weekday()
    blocks = db.query(models.WorkingHour).filter(
        models.WorkingHour.barber_id == barber_id,
        models.WorkingHour.day_of_week == weekday
    ).all()

    start_day = datetime(d.year, d.month, d.day, 0, 0, 0)
    end_day = start_day + timedelta(days=1)
    bookings = db.query(models.Booking).filter(
        models.Booking.barber_id == barber_id,
        models.Booking.start_datetime >= start_day,
        models.Booking.start_datetime < end_day,
        models.Booking.status == "confirmed"
    ).all()

    busy = [(b.start_datetime, b.end_datetime) for b in bookings]
    slots = []
    for b in blocks:
        start_min = _minutes(b.start_hour, b.start_minute)
        end_min = _minutes(b.end_hour, b.end_minute)
        t = start_min
        while t + service_duration <= end_min:
            slot_start = start_day + timedelta(minutes=t)
            slot_end = start_day + timedelta(minutes=t + service_duration)
            if not any(not (slot_end <= s or slot_start >= e) for s, e in busy):
                slots.append(slot_start.strftime("%H:%M"))
            t += service_duration
    return {"date": date, "barber_id": barber_id, "slots": slots}
