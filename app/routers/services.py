from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/services", tags=["services"])

@router.get("/", response_model=list[schemas.ServiceOut])
def list_services(db: Session = Depends(get_db)):
    return db.query(models.Service).order_by(models.Service.id.desc()).all()

@router.post("/", response_model=schemas.ServiceOut)
def create_service(payload: schemas.ServiceCreate, db: Session = Depends(get_db)):
    obj = models.Service(**payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.patch("/{service_id}", response_model=schemas.ServiceOut)
def update_service(service_id: int, payload: schemas.ServiceUpdate, db: Session = Depends(get_db)):
    obj = db.get(models.Service, service_id)
    if not obj: raise HTTPException(404, "Service not found")
    for k,v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.delete("/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    obj = db.get(models.Service, service_id)
    if not obj: raise HTTPException(404, "Service not found")
    db.delete(obj); db.commit()
    return {"ok": True}
