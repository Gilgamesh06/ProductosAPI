from config.db import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from utils.enums import Estado


class Auditoria(Base):
    __abstract__ = True
    estado = Column(SqlEnum(Estado), default=Estado.ACTIVO, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    fecha_actualizacion = Column(DateTime, onupdate=datetime.now)
    fecha_borrado = Column(DateTime)


class Producto(Auditoria):
    __tablename__ = "producto"

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    precio = Column(Integer, nullable=False)
    cantidad = Column(Integer, nullable=False)
    fecha_vencimiento = Column(DateTime, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categoria.id"))
    categoria = relationship("Categoria", back_populates="productos")

    @property
    def categoria_nombre(self):
        return self.categoria.nombre if self.categoria else None


class Categoria(Auditoria):
    __tablename__ = "categoria"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False, unique=True)
    productos = relationship("Producto", back_populates="categoria")
