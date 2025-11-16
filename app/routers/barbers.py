from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/barbers", tags=["barbers"])

@router.get("/", response_model=list[schemas.BarberOut])
def list_barbers(db: Session = Depends(get_db)):
    return db.query(models.Barber).order_by(models.Barber.id.desc()).all()

@router.post("/", response_model=schemas.BarberOut)
def create_barber(payload: schemas.BarberCreate, db: Session = Depends(get_db)):
    obj = models.Barber(**payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.patch("/{barber_id}", response_model=schemas.BarberOut)
def update_barber(barber_id: int, payload: schemas.BarberUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.Barber, barber_id)
    if not obj: raise HTTPException(404, "Barber not found")
    for k,v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.delete("/{barber_id}")
def delete_barber(barber_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Barber, barber_id)
    if not obj: raise HTTPException(404, "Barber not found")
    db.delete(obj); db.commit()
    return {"ok": True}
