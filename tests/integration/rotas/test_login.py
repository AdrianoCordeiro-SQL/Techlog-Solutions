"""
Testes de integração (leve) da rota `/login`.

Abordagem:
- Enviamos `data=` (form) como faria um browser.
- Isolamos a consulta ao usuário via mock de `UsuarioRepositorio` para não depender de banco.
"""

from fastapi.testclient import TestClient

from app.modelos.usuario import Usuario


def test_login_falha_quando_campos_obrigatorios_estao_vazios(client: TestClient):
    # Arrange
    # Observação: `Form(...)` pode resultar em 422 quando o campo vem vazio.
    # Para exercitar a validação da própria rota (strip + obrigatórios), usamos whitespace.
    payload = {"email": "   ", "senha": "123456"}

    # Act
    response = client.post("/login", data=payload)

    # Assert
    assert response.status_code == 200
    assert "Email e senha são obrigatórios." in response.text


def test_login_falha_quando_credenciais_invalidas(client: TestClient, mock_usuario_repo):
    # Arrange
    mock_usuario_repo.buscar_usuario_por_email_senha.return_value = None
    payload = {"email": "ana@example.com", "senha": "123456"}

    # Act
    response = client.post("/login", data=payload)

    # Assert
    assert response.status_code == 200
    assert "Credenciais inválidas." in response.text


def test_login_sucesso_define_cookie_e_redireciona(client: TestClient, mock_usuario_repo):
    # Arrange
    mock_usuario_repo.buscar_usuario_por_email_senha.return_value = Usuario(
        id=1, nome="Ana", email="ana@example.com", senha="123456"
    )
    payload = {"email": "ana@example.com", "senha": "123456"}

    # Act
    response = client.post("/login", data=payload, follow_redirects=False)

    # Assert
    assert response.status_code == 303
    assert response.headers.get("location") == "/clientes"

    set_cookie = response.headers.get("set-cookie") or ""
    assert "session_token=" in set_cookie
    assert "httponly" in set_cookie.lower()

