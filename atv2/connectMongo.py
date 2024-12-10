from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

MONGO_URI = "mongodb+srv://anaMongo:peter@mercadolivre.lqxr38k.mongodb.net/?retryWrites=true&w=majority&appName=mercadoLivre"
DATABASE_NAME = "MercadoLivre"

client = None
db = None

def get_database():
    global client, db
    if client is None:
        try:
            client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
            db = client[DATABASE_NAME]
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(f"Erro ao conectar ao MongoDB: {e}")
            raise
    return db
