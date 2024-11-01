import pytest

def test_update_product(test_client, mongo_client):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 29.99,
        "stock": 100
    }
    create_response = test_client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]
    
    update_data = {
        "name": "Updated Product",
        "price": 39.99
    }
    response = test_client.put(f"/products/{product_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["price"] == update_data["price"]
