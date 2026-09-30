from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from .routes import router
from .admin import router as admin_router


app = FastAPI(
    title="FitBuddy - AI Fitness Plan Generator"
)

templates = Jinja2Templates(directory="templates")

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

app.include_router(router)
app.include_router(admin_router)


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )