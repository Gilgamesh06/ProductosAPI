from pydantic import BaseModel

class RegisterCategoria(BaseModel):
    nombre: str


class UpdateCategoria(BaseModel):
    nombre: str


class GetCategoria(BaseModel):
    id: int
    nombre: str
