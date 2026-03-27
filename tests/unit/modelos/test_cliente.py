"""
Testes unitários dos modelos de cliente.

Abordagem:
- Garantimos que os campos obrigatórios existem e que o modelo aceita payload válido.
- Validações de formato (ex.: e-mail) não existem no modelo atual, então não são forçadas aqui.
"""

from pydantic import ValidationError

from app.modelos.cliente import Cliente, ClienteCriarAtualizar


def test_cliente_cria_quando_todos_campos_presentes():
    # Arrange
    payload = {
        "id_": 10,
        "nome": "Cliente X",
        "email": "cliente@example.com",
        "telefone": "11999999999",
    }

    # Act
    cliente = Cliente(**payload)

    # Assert
    assert cliente.id_ == 10
    assert cliente.nome == "Cliente X"
    assert cliente.email == "cliente@example.com"
    assert cliente.telefone == "11999999999"


def test_cliente_falha_quando_falta_campo_obrigatorio():
    # Arrange
    payload = {"id_": 10, "nome": "Cliente X", "email": "cliente@example.com"}  # sem telefone

    # Act / Assert
    try:
        Cliente(**payload)
        assert False, "Esperava ValidationError quando falta campo obrigatório."
    except ValidationError as exc:
        assert "telefone" in str(exc)


def test_cliente_criar_atualizar_falha_quando_falta_campo_obrigatorio():
    # Arrange
    payload = {"nome": "Cliente X", "email": "cliente@example.com"}  # sem telefone

    # Act / Assert
    try:
        ClienteCriarAtualizar(**payload)
        assert False, "Esperava ValidationError quando falta campo obrigatório."
    except ValidationError as exc:
        assert "telefone" in str(exc)

