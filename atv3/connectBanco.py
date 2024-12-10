from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import redis

MONGO_URI = "mongodb+srv://anaMongo:peter@mercadolivre.lqxr38k.mongodb.net/?retryWrites=true&w=majority&appName=mercadoLivre"
DATABASE_NAME = "MercadoLivre"
REDIS_HOST = 'redis-16270.c98.us-east-1-4.ec2.redns.redis-cloud.com'
REDIS_PORT = 16270
REDIS_PASSWORD = 'kSdDVaIX1GZWigrXDMNDDOIBaONkjusi'

mongo_client = None
mongo_db = None
redis_client = None

def get_mongo_database():
    global mongo_client, mongo_db
    if mongo_client is None:
        try:
            mongo_client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
            mongo_db = mongo_client[DATABASE_NAME]
            mongo_client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(f"Erro ao conectar ao MongoDB: {e}")
            raise
    return mongo_db

def get_redis_client():
    global redis_client
    if redis_client is None:
        try:
            redis_client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                password=REDIS_PASSWORD,
            )
            redis_client.ping()
            print("Successfully connected to Redis!")
        except Exception as e:
            print(f"Erro ao conectar ao Redis: {e}")
            raise
    return redis_client