from __future__ import annotations

from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.banco_de_dados.usuario_repositorio import UsuarioRepositorio
from app.dependencias import obter_usuario_repositorio
from app.modelos.usuario import UsuarioCriarAtualizar

templates = Jinja2Templates(directory="templates")

router = APIRouter()


def _render_registro(
    request: Request,
    *,
    nome: str = "",
    email: str = "",
    error: Optional[str] = None,
):
    return templates.TemplateResponse(
        request=request,
        name="registro.html",
        context={
            "nome": nome,
            "email": email,
            "error": error,
        },
    )


@router.get("/registro", response_class=HTMLResponse)
async def pagina_registro(request: Request):
    # Se já estiver logado, não precisa registrar novamente.
    if request.cookies.get("session_token"):
        return RedirectResponse(url="/clientes", status_code=303)

    return _render_registro(request)


@router.post("/registro", response_class=HTMLResponse)
async def realizar_registro(
    usuario_repositorio: Annotated[
        UsuarioRepositorio, Depends(obter_usuario_repositorio)
    ],
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    confirma_senha: str = Form(...),
):
    nome = (nome or "").strip()
    email = (email or "").strip()

    if not nome or not email or not senha or not confirma_senha:
        return _render_registro(
            request,
            nome=nome,
            email=email,
            error="Nome, email e senha são obrigatórios.",
        )

    if len(senha) < 6:
        return _render_registro(
            request,
            nome=nome,
            email=email,
            error="A senha deve ter pelo menos 6 caracteres.",
        )

    if senha != confirma_senha:
        return _render_registro(
            request,
            nome=nome,
            email=email,
            error="As senhas não conferem.",
        )

    usuario_existente = await usuario_repositorio.buscar_usuario_por_email(email)
    if usuario_existente:
        return _render_registro(
            request,
            nome=nome,
            email=email,
            error="Já existe uma conta com esse email.",
        )

    await usuario_repositorio.criar_usuario(
        UsuarioCriarAtualizar(nome=nome, email=email, senha=senha)
    )
    return RedirectResponse(url="/login", status_code=303)
