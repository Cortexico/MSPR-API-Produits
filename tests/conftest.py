import os
import pytest
from mongomock_motor import AsyncMongoMockClient
from fastapi.testclient import TestClient
from app.main import app
from app import database

# Configuration pour les tests
os.environ["MONGO_USER"] = "test_user"
os.environ["MONGO_PASSWORD"] = "test_password"
os.environ["MONGO_HOST"] = "testdb"
os.environ["MONGO_PORT"] = "27017"
os.environ["MONGO_DB"] = "test_products_db"

@pytest.fixture
async def mock_mongo():
    client = AsyncMongoMockClient()
    database.client = client
    database.database = client[os.environ["MONGO_DB"]]
    database.product_collection = database.database.get_collection("products")
    yield database.product_collection
    # Nettoyage après les tests
    await database.product_collection.delete_many({})

@pytest.fixture
def test_client(mock_mongo):
    return TestClient(app)