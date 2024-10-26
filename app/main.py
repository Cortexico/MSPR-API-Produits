import os
from fastapi import FastAPI
from dotenv import load_dotenv
from app.routers import products

# Charger les variables d'environnement
load_dotenv()

app = FastAPI()

# Inclure le routeur pour les produits
app.include_router(products.router)
