from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    duration = Column(Integer, nullable=False)  # minutes
    price = Column(Integer, nullable=False)     # IRR (Toman)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

class Barber(Base):
    __tablename__ = "barbers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    skills = Column(Text, nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    working_hours = relationship("WorkingHour", back_populates="barber", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="barber")

class WorkingHour(Base):
    __tablename__ = "working_hours"
    id = Column(Integer, primary_key=True, index=True)
    barber_id = Column(Integer, ForeignKey("barbers.id"), nullable=False, index=True)
    day_of_week = Column(Integer, nullable=False)  # Monday=0 ... Sunday=6 (طبق datetime.weekday())
    start_hour = Column(Integer, nullable=False)
    start_minute = Column(Integer, nullable=False)
    end_hour = Column(Integer, nullable=False)
    end_minute = Column(Integer, nullable=False)

    barber = relationship("Barber", back_populates="working_hours")

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(200), nullable=False)
    customer_phone = Column(String(30), nullable=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False, index=True)
    barber_id = Column(Integer, ForeignKey("barbers.id"), nullable=False, index=True)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    status = Column(String(50), default="confirmed")
    created_at = Column(DateTime, server_default=func.now())

    service = relationship("Service")
    barber = relationship("Barber", back_populates="bookings")

class ShopSetting(Base):
    __tablename__ = "shop_settings"
    id = Column(Integer, primary_key=True, index=True)
    shop_name = Column(String(200), default="پیرایشگاه من")
    theme_color = Column(String(20), default="#2563eb")
    timezone_str = Column(String(64), default="Asia/Tehran")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
