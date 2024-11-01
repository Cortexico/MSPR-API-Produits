from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from app.schemas import ProductCreate, ProductUpdate, ProductResponse
from app.database import product_collection
from app.models import product_helper
from pydantic import ValidationError

router = APIRouter(
    prefix="/products",
    tags=["products"]
)


# Dépendance pour obtenir la collection (si nécessaire)
def get_product_collection():
    return product_collection


# GET /products
@router.get("/", response_model=List[ProductResponse])
async def get_products():
    products = []
    async for product in product_collection.find():
        products.append(product_helper(product))
    return products


# GET /products/{id}
@router.get("/{id}", response_model=ProductResponse)
async def get_product(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID de produit invalide")
    product = await product_collection.find_one({"_id": ObjectId(id)})
    if product:
        return product_helper(product)
    raise HTTPException(status_code=404, detail="Produit non trouvé")


# POST /products
@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_product(product: ProductCreate):
    new_product = product.dict()
    result = await product_collection.insert_one(new_product)
    created_product = await product_collection.find_one(
        {"_id": result.inserted_id}
    )
    return product_helper(created_product)


# PUT /products/{id}
@router.put("/{id}", response_model=ProductResponse)
async def update_product(id: str, product: ProductUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID de produit invalide")
    # Extraire uniquement les champs fournis pour la mise à jour
    try:
        update_data = product.dict(exclude_unset=True)
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=f"Erreur de validation des champs: {e.errors()}"
        )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Aucun champ valide fourni pour la mise à jour"
        )
    result = await product_collection.update_one(
        {"_id": ObjectId(id)}, {"$set": update_data}
    )

    if result.modified_count == 1:
        updated_product = await product_collection.find_one(
            {"_id": ObjectId(id)}
        )
        if updated_product:
            return product_helper(updated_product)
    existing_product = await product_collection.find_one({"_id": ObjectId(id)})
    if existing_product:
        return product_helper(existing_product)

    raise HTTPException(status_code=404, detail="Produit non trouvé")


# DELETE /products/{id}
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID de produit invalide")
    result = await product_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return
    raise HTTPException(status_code=404, detail="Produit non trouvé")
