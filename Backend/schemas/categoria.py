from pydantic import BaseModel

class RegisterCategoria(BaseModel):
    nombre: str


class UpdateCategoria(BaseModel):
    nombre: str


class GetCategoria(BaseModel):
    id: int
    nombre: str

class GetCategoriaDelete(BaseModel):
    id: int
    nombre: str
    estado: str