from fastapi import FastAPI
from config.db import Base, engine
from models import models  # Import models to register them with Base
from routes import categoria, producto

app = FastAPI()

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app.include_router(categoria.router, prefix="/categoria", tags=["categoria"])
app.include_router(producto.router, prefix="/producto", tags=["producto"])
