from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .database import SessionLocal, User


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/view-all-users", response_class=HTMLResponse)
async def view_all_users(request: Request):

    db = SessionLocal()

    try:
        users = (
            db.query(User)
            .order_by(User.id.desc())
            .all()
        )

        return templates.TemplateResponse(
            request=request,
            name="all_users.html",
            context={
                "users": users
            }
        )

    finally:
        db.close()