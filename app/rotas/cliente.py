from fastapi import APIRouter
from app.modelos.cliente import Cliente


router = APIRouter(
    prefix="/clientes"
)

CLIENTE_LIST = [
    Cliente(id_=1, nome="Raphael", email="raphael@rossi.com", telefone="123456789"),
    Cliente(id_=2, nome="João", email="joao@rossi.com", telefone="123456789"),
]

@router.get("/", response_model=list[Cliente])
async def listar_clientes():
    return CLIENTE_LIST


@router.get("/{cliente_id}", response_model=Cliente | None)
async def buscar_cliente(cliente_id: int):
    for cliente in CLIENTE_LIST:
        if cliente.id_ == cliente_id:
            return cliente
    return None
