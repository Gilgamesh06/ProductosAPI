from pydantic import BaseModel
from datetime import datetime

class RegisterProducto(BaseModel):
    nombre: str
    precio: int
    cantidad: int
    fecha_vencimiento: datetime
    categoria_id: int


class UpdateProducto(BaseModel):
    nombre: str
    precio: int
    cantidad: int
    fecha_vencimiento: datetime
    categoria_id: int


class GetProducto(BaseModel):
    id: int
    nombre: str
    precio: int
    cantidad: int
    fecha_vencimiento: datetime
    categoria_nombre: str


    
