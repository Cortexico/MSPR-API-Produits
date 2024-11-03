import pytest

@pytest.mark.asyncio
async def test_update_product(test_client, mongo_client):
    # Données initiales pour créer le produit
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 29.99,
        "stock": 100
    }
    # Création du produit initial
    create_response = await test_client.post("/products/", json=product_data)
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    # Données de mise à jour (modification de tous les champs)
    update_data = {
        "name": "Updated Product",
        "description": "Updated Description",
        "price": 39.99,
        "stock": 150
    }
    # Mise à jour du produit
    response = await test_client.put(f"/products/{product_id}", json=update_data)
    assert response.status_code == 200  # Vérifie que la mise à jour a réussi
    data = response.json()

    # Vérifie si les champs ont bien été mis à jour
    assert data["name"] == update_data["name"]
    assert data["description"] == update_data["description"]
    assert data["price"] == update_data["price"]
    assert data["stock"] == update_data["stock"]
