"""
Testes unitários dos modelos de usuário.

Abordagem:
- Aqui validamos o que o código realmente garante hoje via Pydantic: presença de campos obrigatórios e tipos.
- Regras de senha (tamanho mínimo, confirmação) são tratadas nas rotas (`/registro`) e são testadas lá.
"""

from pydantic import ValidationError

from app.modelos.usuario import Usuario, UsuarioCriarAtualizar


def test_usuario_cria_quando_todos_campos_presentes():
    # Arrange
    payload = {"id": 1, "nome": "Ana", "email": "ana@example.com", "senha": "123456"}

    # Act
    usuario = Usuario(**payload)

    # Assert
    assert usuario.id == 1
    assert usuario.nome == "Ana"
    assert usuario.email == "ana@example.com"
    assert usuario.senha == "123456"


def test_usuario_falha_quando_falta_campo_obrigatorio():
    # Arrange
    payload = {"id": 1, "nome": "Ana", "email": "ana@example.com"}  # sem senha

    # Act / Assert
    try:
        Usuario(**payload)
        assert False, "Esperava ValidationError quando falta campo obrigatório."
    except ValidationError as exc:
        assert "senha" in str(exc)


def test_usuario_criar_atualizar_permite_senha_none():
    # Arrange
    payload = {"nome": "Ana", "email": "ana@example.com", "senha": None}

    # Act
    usuario = UsuarioCriarAtualizar(**payload)

    # Assert
    assert usuario.nome == "Ana"
    assert usuario.email == "ana@example.com"
    assert usuario.senha is None


def test_usuario_criar_atualizar_falha_quando_falta_nome_ou_email():
    # Arrange
    payload_sem_nome = {"email": "ana@example.com", "senha": "123456"}
    payload_sem_email = {"nome": "Ana", "senha": "123456"}

    # Act / Assert
    for payload in (payload_sem_nome, payload_sem_email):
        try:
            UsuarioCriarAtualizar(**payload)
            assert False, "Esperava ValidationError por campo obrigatório ausente."
        except ValidationError as exc:
            assert "field required" in str(exc) or "Field required" in str(exc)

