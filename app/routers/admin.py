from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/admin", tags=["admin"])

def _require_admin(request: Request):
    if not request.session.get("is_admin"):
        from fastapi import HTTPException
        raise HTTPException(401, "نیاز به ورود ادمین")
    return True

@router.get("/ui", response_class=HTMLResponse)
def admin_ui(request: Request, ok=Depends(_require_admin)):
    return request.app.state.templates.TemplateResponse("admin/ui.html", {"request": request})

@router.get("/settings", response_class=HTMLResponse)
def admin_settings(request: Request, ok=Depends(_require_admin)):
    return request.app.state.templates.TemplateResponse("admin/ui.html", {"request": request, "section": "settings"})
