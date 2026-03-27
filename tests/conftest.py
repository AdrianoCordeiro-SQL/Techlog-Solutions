"""
Fixtures compartilhadas da suíte de testes.

Escolhas principais:
- **Mocks ao invés de DB real**: o projeto instancia `BancoDeDadosLocal()` em `app/dependencias.py` no import.
  Para evitar side-effects (criar arquivo SQLite/print), desativamos `inicializar_banco()` ainda no import do pytest.
- **Override de dependências**: rotas de `/login` e `/registro` recebem `UsuarioRepositorio` via `Depends`;
  nos testes, substituímos por um mock para isolar a lógica das rotas.
"""

from __future__ import annotations

import importlib
from typing import Generator
from unittest.mock import AsyncMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.staticfiles import StaticFiles


# Evita inicialização real do SQLite no import de `app.dependencias`.
try:
    from app.banco_de_dados.local import BancoDeDadosLocal

    BancoDeDadosLocal.inicializar_banco = lambda self: None  # type: ignore[assignment]
except Exception:
    # Se o import falhar por qualquer motivo, os testes que dependem do app vão acusar.
    pass


@pytest.fixture()
def mock_usuario_repo() -> AsyncMock:
    """
    Mock do `UsuarioRepositorio` usado por rotas.

    Usamos AsyncMock porque os métodos do repositório são `async def`.
    """

    repo = AsyncMock()
    repo.buscar_usuario_por_email = AsyncMock()
    repo.buscar_usuario_por_email_senha = AsyncMock()
    repo.criar_usuario = AsyncMock()
    return repo


@pytest.fixture()
def fastapi_app(mock_usuario_repo: AsyncMock) -> FastAPI:
    """
    App FastAPI de teste com rotas reais + override de dependência.
    """

    # Import tardio para garantir que o patch de `inicializar_banco` já está ativo.
    import app.dependencias as dependencias
    import app.rotas.login as login_rotas
    import app.rotas.registro as registro_rotas

    # Alguns módulos podem já ter sido importados em outros testes; recarrega para pegar patch.
    importlib.reload(dependencias)
    importlib.reload(login_rotas)
    importlib.reload(registro_rotas)

    app = FastAPI()
    # Necessário para templates que usam `url_for('static', ...)`.
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(login_rotas.router)
    app.include_router(registro_rotas.router)

    # Rotas auxiliares para testar middleware/redirect sem depender de outras partes.
    @app.get("/clientes")
    async def clientes_protegido():
        return {"ok": True}

    @app.get("/api/ping")
    async def api_ping():
        return {"pong": True}

    app.dependency_overrides[dependencias.obter_usuario_repositorio] = lambda: mock_usuario_repo
    return app


@pytest.fixture()
def client(fastapi_app: FastAPI) -> Generator[TestClient, None, None]:
    """
    Cliente de testes para chamadas HTTP (integração leve).
    """

    with TestClient(fastapi_app) as c:
        yield c

