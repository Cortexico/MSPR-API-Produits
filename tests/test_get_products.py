import pytest

@pytest.mark.asyncio
async def test_get_products(test_client, mongo_client):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 29.99,
        "stock": 100
    }
    await test_client.post("/products/", json=product_data)

    response = await test_client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == product_data["name"]
