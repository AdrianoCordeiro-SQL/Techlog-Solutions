from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.banco_de_dados.cliente_repositorio import ClienteRepositorio
from app.dependencias import obter_cliente_repositorio
from app.modelos.cliente import Cliente, ClienteCriarAtualizar

router = APIRouter(prefix="/clientes")

@router.get("/", response_model=list[Cliente])
async def listar_clientes(
    cliente_repositorio: Annotated[ClienteRepositorio, Depends(obter_cliente_repositorio)],
):
    return await cliente_repositorio.listar_clientes()


@router.get("/{cliente_id}", response_model=Cliente | None)
async def buscar_cliente(
    cliente_repositorio: Annotated[
        ClienteRepositorio, Depends(obter_cliente_repositorio)
    ],
    cliente_id: int,
):
    cliente = await cliente_repositorio.buscar_cliente(cliente_id)

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado!")

    return cliente


@router.post("/", response_model=Cliente, status_code=201)
async def criar_cliente(
    cliente: ClienteCriarAtualizar,
    cliente_repositorio: Annotated[
        ClienteRepositorio, Depends(obter_cliente_repositorio)
    ],
):
    return await cliente_repositorio.criar_cliente(cliente)


@router.put("/{cliente_id}", response_model=Cliente)
async def atualizar_cliente(
    cliente_id: int,
    cliente: ClienteCriarAtualizar,
    cliente_repositorio: Annotated[
        ClienteRepositorio, Depends(obter_cliente_repositorio)
    ],
):
    cliente_atualizado = await cliente_repositorio.atualizar_cliente(cliente_id, cliente)
    if not cliente_atualizado:
        raise HTTPException(status_code=404, detail="Cliente não encontrado!")
    return cliente_atualizado


@router.delete("/{cliente_id}", status_code=204)
async def deletar_cliente(
    cliente_id: int,
    cliente_repositorio: Annotated[
        ClienteRepositorio, Depends(obter_cliente_repositorio)
    ],
):
    cliente_deletado = await cliente_repositorio.deletar_cliente(cliente_id)
    if not cliente_deletado:
        raise HTTPException(status_code=404, detail="Cliente não encontrado!")
