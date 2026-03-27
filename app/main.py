from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from app.rotas import cliente

templates = Jinja2Templates(directory="templates")

app = FastAPI(
    title="Techlog Solutions API",
    description="CRM for Techlog Solutions",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(cliente.router)
app.include_router(cliente.front_router)


@app.get("/")
async def health_check():
    return {"status": "OK"}


@app.get("/front", response_class=HTMLResponse)
async def front_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"titulo": "Techlog Solutions CRM", "versao": "1.0.0"},
    )
