import os
import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from mongomock_motor import AsyncMongoMockClient
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_database

# Configuration pour les tests
TEST_MONGO_URL = "mongodb://testdb:27017"
os.environ["MONGO_HOST"] = "testdb"
os.environ["MONGO_PORT"] = "27017"
os.environ["MONGO_DB"] = "test_products_db"
os.environ["MONGO_USER"] = "test_user"
os.environ["MONGO_PASSWORD"] = "test_password"

@pytest.fixture
def mock_mongodb():
    client = AsyncMongoMockClient()
    db = client[os.environ["MONGO_DB"]]
    return db

@pytest.fixture
def override_get_database(mock_mongodb):
    async def _get_database():
        return mock_mongodb
    return _get_database

@pytest.fixture
def test_app(override_get_database):
    app.dependency_overrides[get_database] = override_get_database
    return app

@pytest.fixture
def test_client(test_app):
    return TestClient(test_app)

# Fixture pour nettoyer la base de données après chaque test
@pytest.fixture(autouse=True)
async def cleanup_database(mock_mongodb):
    yield
    collections = await mock_mongodb.list_collection_names()
    for collection in collections:
        await mock_mongodb[collection].delete_many({})