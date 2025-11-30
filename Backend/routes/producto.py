import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 
from config.db import SessionLocal, engine, get_db
from models.models import Producto
from schemas.producto import GetProducto, RegisterProducto, UpdateProducto  

from datetime import datetime
from utils.enums import Estado
from utils.pagination import Page

router = APIRouter()

@router.post("/register", response_model=GetProducto)
async def register_producto(producto: RegisterProducto, db: Session = Depends(get_db)):
    try:
        producto = Producto(**producto.dict())
        db.add(producto)
        db.commit()
        return producto
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update/{id}", response_model=GetProducto)
async def update_producto(id: int, producto: UpdateProducto, db: Session = Depends(get_db)):
    try:
        producto_db = db.query(Producto).filter(Producto.id == id).first()
        if not producto_db:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        if producto_db.estado == Estado.INACTIVO:
            raise HTTPException(status_code=400, detail="No se puede actualizar un producto INACTIVO")

        producto_db.nombre = producto.nombre
        producto_db.precio = producto.precio
        producto_db.cantidad = producto.cantidad
        producto_db.fecha_vencimiento = producto.fecha_vencimiento
        producto_db.categoria_id = producto.categoria_id
        producto_db.fecha_actualizacion = datetime.now()
        
        db.add(producto_db)
        db.commit()
        db.refresh(producto_db)
        return producto_db
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/activate/{id}", response_model=GetProducto)
async def activate_producto(id: int, db: Session = Depends(get_db)):
    try:
        producto = db.query(Producto).filter(Producto.id == id).first()
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        if producto.estado == Estado.ACTIVO:
            raise HTTPException(status_code=400, detail="El producto ya está ACTIVO")
            
        producto.estado = Estado.ACTIVO
        producto.fecha_actualizacion = datetime.now()
        db.add(producto)
        db.commit()
        db.refresh(producto)
        return producto
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get/{id}", response_model=GetProducto)
async def get_producto(id: int, db: Session = Depends(get_db)):
    try:
        producto = db.query(Producto).filter(Producto.id == id).first()
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        if producto.estado == Estado.INACTIVO:
             raise HTTPException(status_code=400, detail="El producto está INACTIVO")

        return producto
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))     

@router.get("/get", response_model=Page[GetProducto])   
async def get_productos(page: int = 1, size: int = 10, db: Session = Depends(get_db)):
    try:
        offset = (page - 1) * size
        query = db.query(Producto).filter(Producto.estado == Estado.ACTIVO)
        total_elements = query.count()
        productos = query.offset(offset).limit(size).all()
        total_pages = (total_elements + size - 1) // size
        return Page(
            content=productos,
            total_elements=total_elements,
            total_pages=total_pages,
            page=page,
            size=size
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/{id}", response_model=GetProducto)
async def delete_producto(id: int, db: Session = Depends(get_db)):
    try:
        producto = db.query(Producto).filter(Producto.id == id).first()
        if not producto:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        producto.estado = Estado.INACTIVO
        producto.fecha_borrado = datetime.now()
        db.add(producto)
        db.commit()
        return producto
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))     