from __future__ import annotations

import secrets
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.banco_de_dados.usuario_repositorio import UsuarioRepositorio
from app.dependencias import obter_usuario_repositorio

templates = Jinja2Templates(directory="templates")

router = APIRouter()


def _render_login(
    request: Request,
    *,
    email: str = "",
    senha: str = "",
    error: Optional[str] = None,
):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "email": email,
            "senha": senha,
            "error": error,
        },
    )


@router.get("/login", response_class=HTMLResponse)
async def pagina_login(request: Request):
    # Se já existir cookie, evita mostrar a tela de login novamente.
    if request.cookies.get("session_token"):
        return RedirectResponse(url="/clientes", status_code=303)

    return _render_login(request)


@router.post("/login", response_class=HTMLResponse)
async def realizar_login(
    usuario_repositorio: Annotated[
        UsuarioRepositorio, Depends(obter_usuario_repositorio)
    ],
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
):
    email = (email or "").strip()
    if not email or not senha:
        return _render_login(
            request,
            email=email,
            senha="",
            error="Email e senha são obrigatórios.",
        )

    usuario = await usuario_repositorio.buscar_usuario_por_email_senha(email, senha)
    if not usuario:
        return _render_login(
            request,
            email=email,
            senha="",
            error="Credenciais inválidas.",
        )

    token = secrets.token_urlsafe(32)
    response = RedirectResponse(url="/clientes", status_code=303)
    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        samesite="lax",
    )
    return response


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("session_token")
    return response
