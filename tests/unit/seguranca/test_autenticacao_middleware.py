"""
Testes do middleware de autenticação.

Abordagem:
- Usamos um app mínimo com o `AuthenticationToken` para validar o fluxo sem dependências externas.
- Validamos distinção entre rotas HTML (redirect 303) e rotas de API (401 JSON) quando não há cookie.
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.autenticacao_middleware import AuthenticationToken


def test_middleware_bypassa_rotas_publicas_sem_cookie():
    # Arrange
    app = FastAPI()
    app.add_middleware(AuthenticationToken)

    @app.get("/login")
    async def login_publico():
        return {"ok": True}

    client = TestClient(app)

    # Act
    response = client.get("/login")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_middleware_redireciona_para_login_em_rota_html_sem_cookie():
    # Arrange
    app = FastAPI()
    app.add_middleware(AuthenticationToken)

    @app.get("/clientes")
    async def clientes_protegido():
        return {"ok": True}

    client = TestClient(app, follow_redirects=False)

    # Act
    response = client.get("/clientes")

    # Assert
    assert response.status_code == 303
    assert response.headers.get("location") == "/login"


def test_middleware_retorna_401_em_rota_api_sem_cookie():
    # Arrange
    app = FastAPI()
    app.add_middleware(AuthenticationToken)

    @app.get("/api/ping")
    async def api_ping():
        return {"pong": True}

    client = TestClient(app)

    # Act
    response = client.get("/api/ping")

    # Assert
    assert response.status_code == 401
    assert response.json() == {"detail": "Não autenticado. Faça login."}


def test_middleware_permite_acesso_com_cookie_session_token():
    # Arrange
    app = FastAPI()
    app.add_middleware(AuthenticationToken)

    @app.get("/clientes")
    async def clientes_protegido():
        return {"ok": True}

    client = TestClient(app)

    # Act
    response = client.get("/clientes", cookies={"session_token": "token-valido"})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"ok": True}

