import os
import pytest
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.testclient import TestClient
from app.main import app
from app import database

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the entire session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def mongo_client():
    """Create a MongoDB client for the testing session."""
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

@pytest.fixture(scope="function")
def test_client():
    """Create a test client using FastAPI's TestClient."""
    with TestClient(app) as client:
        yield client
