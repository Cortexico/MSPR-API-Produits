import os
import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.testclient import TestClient
from app.main import app
from app import database

@pytest.fixture(scope="function")
def mongo_client():
    """Setup MongoDB test client."""
    client = AsyncIOMotorClient("mongodb://admin:adminpassword@localhost:27017")
    db = client[os.getenv("MONGO_DB", "products_db")]

    # Save original references
    orig_client = database.client
    orig_database = database.database
    orig_collection = database.product_collection

    # Replace with test client
    database.client = client
    database.database = db
    database.product_collection = db.get_collection("products")

    yield database.product_collection

    # Restore original references and close client
    database.client = orig_client
    database.database = orig_database
    database.product_collection = orig_collection
    client.close()

@pytest.fixture(scope="function")
def test_client():
    """Create test client for FastAPI."""
    with TestClient(app) as client:
        yield client
