"""
Testes de integração (leve) da rota `/registro`.

Abordagem:
- Enviamos `data=` (form) para simular o comportamento real do browser.
- Isolamos persistência usando override de dependência para um mock de `UsuarioRepositorio`.
"""

from fastapi.testclient import TestClient


def test_registro_falha_quando_campos_obrigatorios_estao_vazios(client: TestClient):
    # Arrange
    # Observação: para exercitar `strip()` e a validação da rota, usamos whitespace.
    payload = {"nome": "   ", "email": "   ", "senha": "123456", "confirma_senha": "123456"}

    # Act
    response = client.post("/registro", data=payload)

    # Assert
    assert response.status_code == 200
    assert "Nome, email e senha são obrigatórios." in response.text


def test_registro_falha_quando_senha_tem_menos_de_6(client: TestClient):
    # Arrange
    payload = {
        "nome": "Ana",
        "email": "ana@example.com",
        "senha": "12345",
        "confirma_senha": "12345",
    }

    # Act
    response = client.post("/registro", data=payload)

    # Assert
    assert response.status_code == 200
    assert "A senha deve ter pelo menos 6 caracteres." in response.text


def test_registro_falha_quando_senhas_nao_conferem(client: TestClient):
    # Arrange
    payload = {
        "nome": "Ana",
        "email": "ana@example.com",
        "senha": "123456",
        "confirma_senha": "654321",
    }

    # Act
    response = client.post("/registro", data=payload)

    # Assert
    assert response.status_code == 200
    assert "As senhas não conferem." in response.text


def test_registro_falha_quando_email_ja_existe(client: TestClient, mock_usuario_repo):
    # Arrange
    mock_usuario_repo.buscar_usuario_por_email.return_value = {
        "id": 1,
        "nome": "Fulano",
        "email": "ana@example.com",
        "senha": "123456",
    }
    payload = {
        "nome": "Ana",
        "email": "ana@example.com",
        "senha": "123456",
        "confirma_senha": "123456",
    }

    # Act
    response = client.post("/registro", data=payload)

    # Assert
    assert response.status_code == 200
    assert "Já existe uma conta com esse email." in response.text
    mock_usuario_repo.criar_usuario.assert_not_called()


def test_registro_sucesso_redireciona_para_login(client: TestClient, mock_usuario_repo):
    # Arrange
    mock_usuario_repo.buscar_usuario_por_email.return_value = None
    payload = {
        "nome": "Ana",
        "email": "ana@example.com",
        "senha": "123456",
        "confirma_senha": "123456",
    }

    # Act
    response = client.post("/registro", data=payload, follow_redirects=False)

    # Assert
    assert response.status_code == 303
    assert response.headers.get("location") == "/login"
    mock_usuario_repo.criar_usuario.assert_called_once()

