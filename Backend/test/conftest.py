import sys
import os
from pathlib import Path
import pytest
from testcontainers.postgres import PostgresContainer
from fastapi.testclient import TestClient

# Ensure project root (Backend/) is on sys.path so imports work
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))




@pytest.fixture(scope="session")
def postgres_container():
    """
    Fixture to provide a PostgreSQL container for testing.
    """

    # Parameters for the PostgreSQL container
    POSTGRES_USER = "test_user"
    POSTGRES_PASSWORD = "test_password"
    POSTGRES_DB = "test_db"

    # Initialize and start the PostgreSQL container
    container = PostgresContainer("postgres:14") \
        .with_env("POSTGRES_USER", POSTGRES_USER) \
        .with_env("POSTGRES_PASSWORD", POSTGRES_PASSWORD) \
        .with_env("POSTGRES_DB", POSTGRES_DB)

    container.start()

    # Expose the container connection URL via env so app's DB engine can use it
    try:
        conn_url = container.get_connection_url()
    except Exception:
        # fallback to get_container_host_ip / mapped port
        conn_url = container.get_connection_url()

    os.environ["DATABASE_URL"] = conn_url

    yield container

    # Teardown
    container.stop()


@pytest.fixture
def client(postgres_container):

    # Import app after the postgres container is started and DATABASE_URL is set
    from app import app

    return TestClient(app)


@pytest.fixture
def categoria_data_list():
    return [
        {
            "nombre": "Pantalones",
        },
        {
            "nombre": "Camisas",
        },
        {
            "nombre": "Zapatos",
        },  
        {
            "nombre": "Accesorios",
        },
        {
            "nombre": "Ropa Deportiva",
        }
    ]

@pytest.fixture
def producto_data_list():
    return [
        {
            "nombre": "Pantalon Jeans",
            "precio": 50,
            "cantidad": 100,
            "fecha_vencimiento": "2025-12-31T00:00:00",
            "categoria_id": 1
        },
        {
            "nombre": "Camisa Casual",
            "precio": 30,
            "cantidad": 150,
            "fecha_vencimiento": "2025-11-30T00:00:00",
            "categoria_id": 2
        },
        {
            "nombre": "Zapatos Deportivos",
            "precio": 80,
            "cantidad": 200,
            "fecha_vencimiento": "2026-01-15T00:00:00",
            "categoria_id": 3
        },
        {
            "nombre": "Gorra de Béisbol",
            "precio": 20,
            "cantidad": 250,
            "fecha_vencimiento": "2025-10-10T00:00:00",
            "categoria_id": 4
        },
        {
            "nombre": "Camiseta Deportiva",
            "precio": 40,
            "cantidad": 300,
            "fecha_vencimiento": "2026-02-20T00:00:00",
            "categoria_id": 5
        }
    ]

