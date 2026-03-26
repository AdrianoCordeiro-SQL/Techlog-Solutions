from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.banco_de_dados.cliente_repositorio import ClienteRepositorio
from app.dependencias import obter_cliente_repositorio
from app.modelos.cliente import Cliente

router = APIRouter(
    prefix="/clientes"
)

CLIENTE_LIST = [
    Cliente(id_=1, nome="Raphael", email="raphael@rossi.com", telefone="123456789"),
    Cliente(id_=2, nome="João", email="joao@rossi.com", telefone="123456789"),
]

@router.get("/", response_model=list[Cliente])
async def listar_clientes(cliente_repositorio: Annotated[ClienteRepositorio, Depends(obter_cliente_repositorio)]):
    return await cliente_repositorio.listar_clientes()


@router.get("/{cliente_id}", response_model=Cliente | None)
async def buscar_cliente(
  cliente_repositorio: Annotated[ClienteRepositorio, Depends(obter_cliente_repositorio)],
    cliente_id: int):
    cliente = await cliente_repositorio.buscar_cliente(cliente_id)

    if not cliente:
      raise HTTPException(status_code=404, detail="Cliente não encontrado!")
            
    return cliente
