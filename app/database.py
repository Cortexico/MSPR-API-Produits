import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB = os.getenv("MONGO_DB")

# Construire la chaîne de connexion
MONGO_DETAILS = (
    f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
)

# Créer le client MongoDB asynchrone
client = AsyncIOMotorClient(MONGO_DETAILS)

# Accéder à la base de données
database = client[MONGO_DB]

# Collection des produits
product_collection = database.get_collection("products")
