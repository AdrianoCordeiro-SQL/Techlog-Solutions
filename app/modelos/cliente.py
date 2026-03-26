from pydantic import BaseModel

class Cliente(BaseModel):
  id_: int
  nome: str
  email: str
  telefone: str