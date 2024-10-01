from pymongo import MongoClient
from pymongo.errors import PyMongoError  # Importar a classe mais genérica

# URI de conexão com o MongoDB
uri = "mongodb+srv://joaoggbs62:gZ8PatNu0bI3lHOb@cluster0.wqjd7lm.mongodb.net/?retryWrites=true&w=majority"

def connect_mongo():
    """Conecta ao MongoDB e retorna o cliente."""
    client = MongoClient(uri)
    try:
        client.admin.command('ping')  # Testa a conexão
        print("Conectado ao MongoDB com sucesso!")
        return client
    except PyMongoError as e:  # Captura qualquer erro do PyMongo
        print("Erro ao conectar ao MongoDB:", e)
        raise e
