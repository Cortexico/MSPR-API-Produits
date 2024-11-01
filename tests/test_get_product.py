import pytest

def test_get_product(test_client, mongo_client):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 29.99,
        "stock": 100
    }
    create_response = test_client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]
    
    response = test_client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert data["price"] == product_data["price"]
    assert data["stock"] == product_data["stock"]
