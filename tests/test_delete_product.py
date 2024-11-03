import pytest

@pytest.mark.asyncio
async def test_delete_product(test_client, mongo_client):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 29.99,
        "stock": 100
    }
    create_response = await test_client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]
    
    response = await test_client.delete(f"/products/{product_id}")
    assert response.status_code == 204
    
    get_response = await test_client.get(f"/products/{product_id}")
    assert get_response.status_code == 404
