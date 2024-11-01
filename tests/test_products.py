import pytest
import asyncio

@pytest.mark.asyncio
async def test_create_product(test_client, mongo_client):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 29.99,
        "stock": 100
    }
    response = await asyncio.to_thread(test_client.post, "/products/", json=product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert data["price"] == product_data["price"]
    assert data["stock"] == product_data["stock"]

@pytest.mark.asyncio
async def test_get_products(test_client, mongo_client):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 29.99,
        "stock": 100
    }
    await asyncio.to_thread(test_client.post, "/products/", json=product_data)
    
    response = await asyncio.to_thread(test_client.get, "/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == product_data["name"]

@pytest.mark.asyncio
async def test_get_product(test_client, mongo_client):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 29.99,
        "stock": 100
    }
    create_response = await asyncio.to_thread(test_client.post, "/products/", json=product_data)
    product_id = create_response.json()["id"]
    
    response = await asyncio.to_thread(test_client.get, f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == product_data["name"]

@pytest.mark.asyncio
async def test_update_product(test_client, mongo_client):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 29.99,
        "stock": 100
    }
    create_response = await asyncio.to_thread(test_client.post, "/products/", json=product_data)
    product_id = create_response.json()["id"]
    
    update_data = {
        "name": "Updated Product",
        "price": 39.99
    }
    response = await asyncio.to_thread(test_client.put, f"/products/{product_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["price"] == update_data["price"]

@pytest.mark.asyncio
async def test_delete_product(test_client, mongo_client):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 29.99,
        "stock": 100
    }
    create_response = await asyncio.to_thread(test_client.post, "/products/", json=product_data)
    product_id = create_response.json()["id"]
    
    response = await asyncio.to_thread(test_client.delete, f"/products/{product_id}")
    assert response.status_code == 204
    
    get_response = await asyncio.to_thread(test_client.get, f"/products/{product_id}")
    assert get_response.status_code == 404
