import os
import pytest
import asyncio
from mongomock_motor import AsyncMongoMockClient
from fastapi.testclient import TestClient
from app.main import app
from app import database

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    # Au lieu de fermer la boucle, on la nettoie
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.run_until_complete(loop.shutdown_default_executor())
    
@pytest.fixture(scope="function")
async def mock_mongo():
    """Create a mock MongoDB client and replace the real one."""
    # Création du client mock avec les credentials
    client = AsyncMongoMockClient()
    db = client[os.environ.get("MONGO_DB", "products_db")]
    
    # Sauvegarder les références originales
    orig_client = database.client
    orig_database = database.database
    orig_collection = database.product_collection
    
    # Remplacer par les mocks
    database.client = client
    database.database = db
    database.product_collection = db.get_collection("products")
    
    await database.client.start_session()  # Démarrer une session
    
    yield database.product_collection
    
    # Nettoyage
    await database.client.close()
    
    # Restaurer les références originales
    database.client = orig_client
    database.database = orig_database
    database.product_collection = orig_collection

@pytest.fixture
def test_client():
    """Create a test client."""
    with TestClient(app) as client:
        yield client