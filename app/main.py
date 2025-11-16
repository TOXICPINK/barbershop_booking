import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .database import engine, SessionLocal
from . import models
from .routers import services, barbers, bookings, availability, working_hours, admin, admin_auth

# ساخت جداول
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Barbershop Booking")
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "dev-session-secret"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(BASE_DIR, "templates")
static_dir = os.path.join(BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=templates_dir)
app.state.templates = templates

app.state.admin_user = os.getenv("ADMIN_USER", "admin")
app.state.admin_pass = os.getenv("ADMIN_PASS", "admin123")

app.include_router(services.router)
app.include_router(barbers.router)
app.include_router(bookings.router)
app.include_router(availability.router)
app.include_router(working_hours.router)
app.include_router(admin_auth.router)
app.include_router(admin.router)

@app.on_event("startup")
def seed_data():
    db = SessionLocal()
    try:
        if not db.query(models.Service).first():
            db.add(models.Service(title="اصلاح مردانه", duration=30, price=150000))
        if not db.query(models.Barber).first():
            b = models.Barber(name="استاد رضا", skills="اصلاح، خط ریش")
            db.add(b)
            db.flush()
            # ساعات کاری: دوشنبه تا جمعه 10:00-18:00 (weekday: Mon=0 ...)
            for wd in [0,1,2,3,4]:
                db.add(models.WorkingHour(
                    barber_id=b.id, day_of_week=wd,
                    start_hour=10, start_minute=0,
                    end_hour=18, end_minute=0
                ))
        db.commit()
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/book", response_class=HTMLResponse)
def page_book(request: Request):
    return templates.TemplateResponse("book.html", {"request": request})
