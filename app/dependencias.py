from typing import Annotated

from fastapi import Depends

from app.banco_de_dados.cliente_repositorio import ClienteRepositorio
from app.banco_de_dados.local import BancoDeDadosLocal
from app.banco_de_dados.usuario_repositorio import UsuarioRepositorio

banco_de_dados = BancoDeDadosLocal()


def obter_banco_de_dados() -> BancoDeDadosLocal:
    return banco_de_dados


def obter_cliente_repositorio(
    banco_de_dados_local: Annotated[BancoDeDadosLocal, Depends(obter_banco_de_dados)],
) -> ClienteRepositorio:
    return ClienteRepositorio(banco_de_dados_local)


def obter_usuario_repositorio(
    banco_de_dados_local: Annotated[BancoDeDadosLocal, Depends(obter_banco_de_dados)],
) -> UsuarioRepositorio:
    return UsuarioRepositorio(banco_de_dados_local)
