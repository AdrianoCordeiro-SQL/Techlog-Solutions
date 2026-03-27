"""
Testes unitários do `UsuarioRepositorio` (sem banco real).

Abordagem:
- Mockamos `BancoDeDadosLocal.conectar()` como context manager que fornece `conexao` e `cursor`.
- Assim validamos SQL/parametrização e mapeamento de retorno para modelos, sem depender de SQLite.
"""

from __future__ import annotations

from contextlib import contextmanager
from unittest.mock import MagicMock

import pytest

from app.banco_de_dados.usuario_repositorio import UsuarioRepositorio
from app.modelos.usuario import UsuarioCriarAtualizar


def _make_bd_with_cursor(cursor: MagicMock) -> MagicMock:
    conexao = MagicMock()
    conexao.cursor.return_value = cursor

    @contextmanager
    def conectar():
        yield conexao

    bd = MagicMock()
    bd.conectar = conectar
    return bd


@pytest.mark.asyncio
async def test_buscar_usuario_por_email_retorna_none_quando_nao_encontra():
    # Arrange
    cursor = MagicMock()
    cursor.fetchone.return_value = None
    bd = _make_bd_with_cursor(cursor)
    repo = UsuarioRepositorio(bd)

    # Act
    result = await repo.buscar_usuario_por_email("ana@example.com")

    # Assert
    assert result is None
    cursor.execute.assert_called_once_with(
        "SELECT id, nome, email, senha FROM usuarios WHERE email = ?",
        ("ana@example.com",),
    )


@pytest.mark.asyncio
async def test_buscar_usuario_por_email_mapeia_para_modelo():
    # Arrange
    cursor = MagicMock()
    cursor.fetchone.return_value = (1, "Ana", "ana@example.com", "123456")
    bd = _make_bd_with_cursor(cursor)
    repo = UsuarioRepositorio(bd)

    # Act
    result = await repo.buscar_usuario_por_email("ana@example.com")

    # Assert
    assert result is not None
    assert result.id == 1
    assert result.nome == "Ana"
    assert result.email == "ana@example.com"
    assert result.senha == "123456"


@pytest.mark.asyncio
async def test_buscar_usuario_por_email_senha_retorna_none_quando_nao_encontra():
    # Arrange
    cursor = MagicMock()
    cursor.fetchone.return_value = None
    bd = _make_bd_with_cursor(cursor)
    repo = UsuarioRepositorio(bd)

    # Act
    result = await repo.buscar_usuario_por_email_senha("ana@example.com", "123456")

    # Assert
    assert result is None
    cursor.execute.assert_called_once_with(
        "SELECT id, nome, email FROM usuarios WHERE email = ? AND senha = ?",
        ("ana@example.com", "123456"),
    )


@pytest.mark.asyncio
async def test_buscar_usuario_por_email_senha_mapeia_para_modelo():
    # Arrange
    cursor = MagicMock()
    cursor.fetchone.return_value = (1, "Ana", "ana@example.com")
    bd = _make_bd_with_cursor(cursor)
    repo = UsuarioRepositorio(bd)

    # Act
    result = await repo.buscar_usuario_por_email_senha("ana@example.com", "123456")

    # Assert
    assert result is not None
    assert result.id == 1
    assert result.nome == "Ana"
    assert result.email == "ana@example.com"
    assert result.senha == "123456"


@pytest.mark.asyncio
async def test_criar_usuario_falha_quando_senha_ausente():
    # Arrange
    cursor = MagicMock()
    bd = _make_bd_with_cursor(cursor)
    repo = UsuarioRepositorio(bd)
    usuario = UsuarioCriarAtualizar(nome="Ana", email="ana@example.com", senha=None)

    # Act / Assert
    with pytest.raises(ValueError, match="Senha é obrigatória"):
        await repo.criar_usuario(usuario)


@pytest.mark.asyncio
async def test_criar_usuario_executa_insert_e_retorna_modelo():
    # Arrange
    cursor = MagicMock()
    cursor.lastrowid = 123
    bd = _make_bd_with_cursor(cursor)
    repo = UsuarioRepositorio(bd)
    usuario = UsuarioCriarAtualizar(nome="Ana", email="ana@example.com", senha="123456")

    # Act
    result = await repo.criar_usuario(usuario)

    # Assert
    cursor.execute.assert_called_once_with(
        "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
        ("Ana", "ana@example.com", "123456"),
    )
    assert result.id == 123
    assert result.nome == "Ana"
    assert result.email == "ana@example.com"
    assert result.senha == "123456"


@pytest.mark.asyncio
async def test_criar_usuario_falha_quando_lastrowid_none():
    # Arrange
    cursor = MagicMock()
    cursor.lastrowid = None
    bd = _make_bd_with_cursor(cursor)
    repo = UsuarioRepositorio(bd)
    usuario = UsuarioCriarAtualizar(nome="Ana", email="ana@example.com", senha="123456")

    # Act / Assert
    with pytest.raises(RuntimeError, match="ID nao retornado"):
        await repo.criar_usuario(usuario)

