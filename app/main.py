from fastapi import FastAPI
from dotenv import load_dotenv
from app.routers import products
from app.rabbitmq_publisher import connect_to_rabbitmq

# Charger les variables d'environnement
load_dotenv()

app = FastAPI()

# Inclure le routeur pour les produits
app.include_router(products.router)

# démarrer l'application et initilaser la connexion rabbitmq
@app.on_event("startup")
async def startup_event():
    await connect_to_rabbitmq()
    print("Connexion à RabbitMQ établie avec succès pour le publisher.")
