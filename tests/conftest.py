import os
import pytest
import asyncio
from mongomock_motor import AsyncMongoMockClient
from fastapi.testclient import TestClient
from app.main import app
from app import database

# Configuration pour les tests
os.environ["MONGO_USER"] = "products"
os.environ["MONGO_PASSWORD"] = "apiProducts"
os.environ["MONGO_HOST"] = "localhost"
os.environ["MONGO_PORT"] = "27017"
os.environ["MONGO_DB"] = "products_db"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def mock_mongo():
    """Create a mock MongoDB client and replace the real one."""
    client = AsyncMongoMockClient()
    db = client[os.environ["MONGO_DB"]]
    # Sauvegarder les références originales
    orig_client = database.client
    orig_database = database.database
    orig_collection = database.product_collection
    
    # Remplacer par les mocks
    database.client = client
    database.database = db
    database.product_collection = db.get_collection("products")
    
    yield database.product_collection
    
    # Restaurer les références originales
    database.client = orig_client
    database.database = orig_database
    database.product_collection = orig_collection

@pytest.fixture
def test_client(mock_mongo):
    with TestClient(app) as client:
        yield client
