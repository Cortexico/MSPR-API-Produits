import os
import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi.testclient import TestClient
from app.main import app
from app import database

@pytest.fixture(scope="function")
async def mongo_client():
    """Create a real MongoDB client for testing."""
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

    # Cleanup
    await client.close()

    # Restore original references
    database.client = orig_client
    database.database = orig_database
    database.product_collection = orig_collection

@pytest.fixture
def test_client():
    """Create a test client that runs synchronously in a separate thread."""
    with TestClient(app) as client:
        yield client
