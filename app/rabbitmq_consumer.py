# import os
# import json
# import aio_pika
# from app.database import product_collection
# from app.models import product_helper
# from dotenv import load_dotenv

# load_dotenv()

# RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
# RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT", "5672"))
# RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
# RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")

# async def process_message(message: aio_pika.IncomingMessage):
#     async with message.process():
#         data = json.loads(message.body)
#         action = data.get('action')
#         product_data = data.get('data')

#         if action == 'create':
#             await product_collection.insert_one(product_data)
#         elif action == 'update':
#             product_id = product_data.get('_id')
#             if product_id:
#                 await product_collection.update_one(
#                     {'_id': product_id},
#                     {'$set': product_data}
#                 )
#         elif action == 'delete':
#             product_id = product_data.get('id')
#             if product_id:
#                 await product_collection.delete_one({'_id': product_id})

# async def start_consumer():
#     connection = await aio_pika.connect_robust(
#         host=RABBITMQ_HOST,
#         port=RABBITMQ_PORT,
#         login=RABBITMQ_USER,
#         password=RABBITMQ_PASSWORD
#     )
#     channel = await connection.channel()
#     exchange = await channel.declare_exchange('product_updates', aio_pika.ExchangeType.FANOUT)
#     queue = await channel.declare_queue('', exclusive=True)
#     await queue.bind(exchange)

#     await queue.consume(process_message)