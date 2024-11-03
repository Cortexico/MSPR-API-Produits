import os
import json
import aio_pika
import asyncio
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")

connection = None
channel = None


async def connect_to_rabbitmq(retries=5, delay=2):
    global connection, channel
    for attempt in range(retries):
        try:
            connection = await aio_pika.connect_robust(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                login=RABBITMQ_USER,
                password=RABBITMQ_PASSWORD
            )
            channel = await connection.channel()
            await channel.declare_exchange(
                'product_exchange',
                aio_pika.ExchangeType.FANOUT
            )
            print("Connexion à RabbitMQ établie avec succès.")
            break
        except Exception as e:
            print(f"Erreur de connexion à RabbitMQ: {e}")
            if attempt < retries - 1:
                print(f"Nouvelle tentative dans {delay} secondes...")
                await asyncio.sleep(delay)
            else:
                raise RuntimeError(
                    "Impossible de se connecter à RabbitMQ après plusieurs "
                    "tentatives."
                )



async def send_message_to_rabbitmq(message):
    await connect_to_rabbitmq()
    exchange = await channel.get_exchange('product_exchange')
    message_body = json.dumps(message)
    await exchange.publish(
        aio_pika.Message(body=message_body.encode()),
        routing_key=""
    )
