import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session 
from config.db import SessionLocal, engine, get_db
from models.models import Categoria
from schemas.categoria import GetCategoria, RegisterCategoria, UpdateCategoria
from datetime import datetime
from utils.enums import Estado
from utils.pagination import Page  

router = APIRouter()

@router.post("/register", response_model=GetCategoria)
async def register_categoria(categoria: RegisterCategoria, db: Session = Depends(get_db)):
    try:
        categoria = Categoria(**categoria.dict())
        db.add(categoria)
        db.commit()
        return categoria
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/update/{id}", response_model=GetCategoria)
async def update_categoria(id: int, categoria: UpdateCategoria, db: Session = Depends(get_db)):
    try:
        categoria_db = db.query(Categoria).filter(Categoria.id == id).first()
        if not categoria_db:
            raise HTTPException(status_code=404, detail="Categoria no encontrada")
        
        if categoria_db.estado == Estado.INACTIVO:
            raise HTTPException(status_code=400, detail="No se puede actualizar una categoria INACTIVA")

        categoria_db.nombre = categoria.nombre
        categoria_db.fecha_actualizacion = datetime.now()
        db.add(categoria_db)
        db.commit()
        db.refresh(categoria_db)
        return categoria_db
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/activate/{id}", response_model=GetCategoria)
async def activate_categoria(id: int, db: Session = Depends(get_db)):
    try:
        categoria = db.query(Categoria).filter(Categoria.id == id).first()
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria no encontrada")
        
        if categoria.estado == Estado.ACTIVO:
            raise HTTPException(status_code=400, detail="La categoria ya está ACTIVA")
            
        categoria.estado = Estado.ACTIVO
        categoria.fecha_actualizacion = datetime.now()
        db.add(categoria)
        db.commit()
        db.refresh(categoria)
        return categoria
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get/{id}", response_model=GetCategoria)
async def get_categoria(id: int, db: Session = Depends(get_db)):
    try:
        categoria = db.query(Categoria).filter(Categoria.id == id).first()
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria no encontrada")
        if categoria.estado == Estado.INACTIVO:
            raise HTTPException(status_code=400, detail="La Categoria está INACTIVO")
        return categoria
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get", response_model=Page[GetCategoria])
async def get_categorias(page: int = 1, size: int = 10, db: Session = Depends(get_db)):
    try:
        offset = (page - 1) * size
        query = db.query(Categoria).filter(Categoria.estado == Estado.ACTIVO)
        total_elements = query.count()
        categorias = query.offset(offset).limit(size).all()
        total_pages = (total_elements + size - 1) // size
        return Page(
            content=categorias,
            total_elements=total_elements,
            total_pages=total_pages,
            page=page,
            size=size
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{id}", response_model=GetCategoria)
async def delete_categoria(id: int, db: Session = Depends(get_db)):
    try:
        categoria = db.query(Categoria).filter(Categoria.id == id).first()
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria no encontrada")
        categoria.estado = Estado.INACTIVO
        categoria.fecha_borrado = datetime.now()
        db.add(categoria)
        db.commit()
        return categoria
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

