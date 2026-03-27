from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.banco_de_dados.cliente_repositorio import ClienteRepositorio
from app.dependencias import obter_cliente_repositorio
from app.modelos.cliente import Cliente, ClienteCriarAtualizar

templates = Jinja2Templates(directory="templates")

api_router = APIRouter(prefix="/api/clientes")
front_router = APIRouter(prefix="/clientes")

router = APIRouter()


@api_router.get("/", response_model=list[Cliente])
async def listar_clientes(
    cliente_repositorio: Annotated[
        ClienteRepositorio, Depends(obter_cliente_repositorio)
    ],
):
    return await cliente_repositorio.listar_clientes()


@api_router.get("/{cliente_id}", response_model=Cliente | None)
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


@api_router.post("/", response_model=Cliente, status_code=201)
async def criar_cliente(
    cliente: ClienteCriarAtualizar,
    cliente_repositorio: Annotated[
        ClienteRepositorio, Depends(obter_cliente_repositorio)
    ],
):
    return await cliente_repositorio.criar_cliente(cliente)


@api_router.put("/{cliente_id}", response_model=Cliente)
async def atualizar_cliente(
    cliente_id: int,
    cliente: ClienteCriarAtualizar,
    cliente_repositorio: Annotated[
        ClienteRepositorio, Depends(obter_cliente_repositorio)
    ],
):
    cliente_atualizado = await cliente_repositorio.atualizar_cliente(
        cliente_id, cliente
    )
    if not cliente_atualizado:
        raise HTTPException(status_code=404, detail="Cliente não encontrado!")
    return cliente_atualizado


@api_router.delete("/{cliente_id}", status_code=204)
async def deletar_cliente(
    cliente_id: int,
    cliente_repositorio: Annotated[
        ClienteRepositorio, Depends(obter_cliente_repositorio)
    ],
):
    cliente_deletado = await cliente_repositorio.deletar_cliente(cliente_id)
    if not cliente_deletado:
        raise HTTPException(status_code=404, detail="Cliente não encontrado!")


@front_router.get("/", response_class=HTMLResponse)
async def pagina_listar_clientes(
    request: Request,
    cliente_repositorio: Annotated[
        ClienteRepositorio, Depends(obter_cliente_repositorio)
    ],
):
    clientes = await cliente_repositorio.listar_clientes()
    return templates.TemplateResponse(
        request=request,
        name="clientes.html",
        context={"clientes": clientes, "titulo": "Lista de Clientes"},
    )


router.include_router(api_router)
router.include_router(front_router)


@front_router.get("/novo", response_class=HTMLResponse)
async def pagina_criar_cliente(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="clientes-form.html",
        context={},  # Formulário de criação não precisa de dados adicionais.
    )


@front_router.get("/{cliente_id}", response_class=HTMLResponse)
async def pagina_editar_cliente(
    request: Request,
    cliente_id: int,
    cliente_repositorio: Annotated[
        ClienteRepositorio, Depends(obter_cliente_repositorio)
    ],
):
    cliente = await cliente_repositorio.buscar_cliente(cliente_id)
    return templates.TemplateResponse(
        request=request,
        name="clientes-form.html",
        context={
            "cliente": cliente,
        },
    )
