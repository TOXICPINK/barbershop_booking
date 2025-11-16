from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_302_FOUND

router = APIRouter(prefix="/admin", tags=["admin-auth"])

@router.get("/login")
def login_page(request: Request):
    return request.app.state.templates.TemplateResponse("admin/login.html", {"request": request})

@router.post("/login")
def do_login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == request.app.state.admin_user and password == request.app.state.admin_pass:
        request.session["is_admin"] = True
        return RedirectResponse(url="/admin/ui", status_code=HTTP_302_FOUND)
    raise HTTPException(401, "نام کاربری یا رمز اشتباه است.")

@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/admin/login", status_code=HTTP_302_FOUND)
