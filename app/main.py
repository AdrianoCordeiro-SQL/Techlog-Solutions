from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

from app.autenticacao_middleware import AuthenticationToken
from app.rotas import cliente, login, registro

templates = Jinja2Templates(directory="templates")

app = FastAPI(
    title="Techlog Solutions API",
    description="CRM for Techlog Solutions",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(AuthenticationToken)
app.include_router(cliente.router)
app.include_router(cliente.front_router)
app.include_router(login.router)
app.include_router(registro.router)


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
