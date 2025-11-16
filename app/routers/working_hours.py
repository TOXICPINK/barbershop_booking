from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/barbers", tags=["working-hours"])

@router.put("/{barber_id}/hours")
def set_hours(barber_id: int, payload: schemas.WHUpdate, db: Session = Depends(get_db)):
    barber = db.get(models.Barber, barber_id)
    if not barber: raise HTTPException(404, "Barber not found")
    db.query(models.WorkingHour).filter(models.WorkingHour.barber_id == barber_id).delete()
    for b in payload.blocks:
        db.add(models.WorkingHour(
            barber_id=barber_id,
            day_of_week=b.day_of_week,
            start_hour=b.start_hour,
            start_minute=b.start_minute,
            end_hour=b.end_hour,
            end_minute=b.end_minute
        ))
    db.commit()
    return {"ok": True}
