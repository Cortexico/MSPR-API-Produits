import pytest
from fastapi.testclient import TestClient

def test_create_product(test_client):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 29.99,
        "quantity": 100
    }
    response = test_client.post("/products/", json=product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["description"] == product_data["description"]
    assert data["price"] == product_data["price"]
    assert data["quantity"] == product_data["quantity"]

def test_get_products(test_client):
    # Créer un produit de test
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 29.99,
        "quantity": 100
    }
    test_client.post("/products/", json=product_data)
    
    # Récupérer la liste des produits
    response = test_client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == product_data["name"]

def test_get_product(test_client):
    # Créer un produit de test
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 29.99,
        "quantity": 100
    }
    create_response = test_client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]
    
    # Récupérer le produit par son ID
    response = test_client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == product_data["name"]

def test_update_product(test_client):
    # Créer un produit de test
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 29.99,
        "quantity": 100
    }
    create_response = test_client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]
    
    # Mettre à jour le produit
    update_data = {
        "name": "Updated Product",
        "price": 39.99
    }
    response = test_client.put(f"/products/{product_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["price"] == update_data["price"]

def test_delete_product(test_client):
    # Créer un produit de test
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 29.99,
        "quantity": 100
    }
    create_response = test_client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]
    
    # Supprimer le produit
    response = test_client.delete(f"/products/{product_id}")
    assert response.status_code == 204
    
    # Vérifier que le produit a été supprimé
    get_response = test_client.get(f"/products/{product_id}")
    assert get_response.status_code == 404