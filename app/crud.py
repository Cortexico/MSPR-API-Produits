from bson import ObjectId
from app.database import product_collection
from app.models import product_helper
from app.schemas import ProductCreate, ProductUpdate

# Récupérer un produit par ID
async def get_product(id: str):
    product = await product_collection.find_one({"_id": ObjectId(id)})
    if product:
        return product_helper(product)
    return None

# Récupérer tous les produits
async def get_products():
    products = []
    async for product in product_collection.find():
        products.append(product_helper(product))
    return products

# Créer un nouveau produit
async def create_product(product_data: ProductCreate):
    product = product_data.dict()
    result = await product_collection.insert_one(product)
    new_product = await product_collection.find_one({"_id": result.inserted_id})
    return product_helper(new_product)

# Mettre à jour un produit
async def update_product(id: str, product_data: ProductUpdate):
    update_data = {k: v for k, v in product_data.dict().items() if v is not None}
    if len(update_data) >= 1:
        result = await product_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": update_data}
        )
        if result.modified_count == 1:
            updated_product = await product_collection.find_one({"_id": ObjectId(id)})
            if updated_product:
                return product_helper(updated_product)
    existing_product = await product_collection.find_one({"_id": ObjectId(id)})
    if existing_product:
        return product_helper(existing_product)
    return None

# Supprimer un produit
async def delete_product(id: str):
    result = await product_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0
