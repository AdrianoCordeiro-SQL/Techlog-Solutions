from pydantic import BaseModel


class Usuario(BaseModel):
    id: int
    nome: str
    email: str
    senha: str


class UsuarioCriarAtualizar(BaseModel):
    nome: str
    email: str
    senha: str | None = None
