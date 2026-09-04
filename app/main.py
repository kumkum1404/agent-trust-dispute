from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.routes import router


app = FastAPI(
    title="Agent Trust & Dispute Layer",
    description="AI Agent Payment Security System",
    version="1.0.0"
)


# Static files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# Templates
templates = Jinja2Templates(
    directory="templates"
)


# API routes
app.include_router(
    router,
    prefix="/api"
)


@app.get("/")
async def dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )