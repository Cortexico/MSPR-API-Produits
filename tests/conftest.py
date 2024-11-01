import os
import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.testclient import TestClient
from app.main import app
from app import database

@pytest.fixture(scope="function")
async def mongo_client():
    """Create a MongoDB client for each test to prevent connection issues."""
    client = AsyncIOMotorClient("mongodb://admin:adminpassword@localhost:27017")
    db = client[os.environ.get("MONGO_DB", "products_db")]
    
    # Backup original references
    orig_client = database.client
    orig_database = database.database
    orig_collection = database.product_collection
    
    # Replace with test client
    database.client = client
    database.database = db
    database.product_collection = db.get_collection("products")
    
    yield database.product_collection
    
    # Restore original references
    database.client = orig_client
    database.database = orig_database
    database.product_collection = orig_collection
    
    # Close the client connection explicitly after yield
    client.close()

@pytest.fixture(scope="function")
def test_client():
    """Create a test client using FastAPI's TestClient."""
    with TestClient(app) as client:
        yield client
