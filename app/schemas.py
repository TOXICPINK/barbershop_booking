from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class ServiceBase(BaseModel):
    title: str
    duration: int
    price: int
    active: bool = True
class ServiceCreate(ServiceBase): pass
class ServiceUpdate(BaseModel):
    title: Optional[str] = None
    duration: Optional[int] = None
    price: Optional[int] = None
    active: Optional[bool] = None
class ServiceOut(ServiceBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class BarberBase(BaseModel):
    name: str
    skills: Optional[str] = None
    active: bool = True
class BarberCreate(BarberBase): pass
class BarberUpdate(BaseModel):
    name: Optional[str] = None
    skills: Optional[str] = None
    active: Optional[bool] = None
class BarberOut(BarberBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class WHBlock(BaseModel):
    day_of_week: int
    start_hour: int
    start_minute: int
    end_hour: int
    end_minute: int
class WHUpdate(BaseModel):
    blocks: List[WHBlock]

class BookingCreate(BaseModel):
    customer_name: str
    customer_phone: Optional[str] = None
    service_id: int
    barber_id: int
    start_datetime: datetime

class BookingOut(BaseModel):
    id: int
    customer_name: str
    customer_phone: Optional[str] = None
    service_id: int
    barber_id: int
    start_datetime: datetime
    end_datetime: datetime
    status: str
    model_config = ConfigDict(from_attributes=True)

class SettingUpdate(BaseModel):
    shop_name: Optional[str] = None
    theme_color: Optional[str] = None
    timezone_str: Optional[str] = None
