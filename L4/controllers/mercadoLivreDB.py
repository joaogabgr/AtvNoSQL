# mercado_livre_db.py
from astrapy import DataAPIClient
import uuid

class MercadoLivreDB:
    def __init__(self, token, api_endpoint):
        # Inicializa o cliente Astra DB
        self.client = DataAPIClient(token)
        self.db = self.client.get_database_by_api_endpoint(api_endpoint)

    def insert_user(self, name, age, address):
        user_id = str(uuid.uuid4())
        collection = self.db.get_collection('usuarios')  # Tabela 'usuarios'
        query = {"id": user_id, "nome": name, "idade": age, "endereco": address}
        collection.insert_one(query)
        print(f"Usuário {name} inserido com sucesso com ID {user_id}.")

    def insert_seller(self, name, age, address):
        seller_id = str(uuid.uuid4())
        collection = self.db.get_collection('vendedores')  # Tabela 'vendedores'
        query = {"id": seller_id, "nome": name, "idade": age, "endereco": address}
        collection.insert_one(query)
        print(f"Vendedor {name} inserido com sucesso com ID {seller_id}.")

    def insert_product(self, name, price, seller_id):
        product_id = str(uuid.uuid4())
        collection = self.db.get_collection('produtos')  # Tabela 'produtos'
        query = {
            "id": product_id,
            "nome": name,
            "valor": price,
            "vendedor_id": seller_id
        }
        collection.insert_one(query)
        print(f"Produto {name} inserido com sucesso com ID {product_id}.")

    def insert_purchase(self, user_id, product_id, quantity, value):
        purchase_id = str(uuid.uuid4())
        collection = self.db.get_collection('compras')  # Tabela 'compras'
        query = {
            "id": purchase_id,
            "idUsuario": user_id,
            "idProduto": product_id,
            "quantidade": quantity,
            "valor": value
        }
        collection.insert_one(query)
        print(f"Compra registrada com sucesso com ID {purchase_id}.")

    def update_user(self, user_id, new_name=None, new_age=None, new_address=None):
        collection = self.db.get_collection('usuarios')  # Tabela 'usuarios'
        updates = {}
        
        if new_name:
            updates["nome"] = new_name
        if new_age:
            updates["idade"] = new_age
        if new_address:
            updates["endereco"] = new_address

        if updates:
            collection.update_one({"id": user_id}, {"$set": updates})
            print(f"Usuário {user_id} atualizado com sucesso.")

    def search_product(self, product_id):
        collection = self.db.get_collection('produtos')  # Tabela 'produtos'
        query = collection.find_one({"id": product_id})
        if query:
            print(f"Produto encontrado: ID: {query['id']}, Nome: {query['nome']}, Preço: {query['valor']}")
        else:
            print(f"Produto com ID {product_id} não encontrado.")

    def delete_purchase(self, purchase_id):
        collection = self.db.get_collection('compras')  # Tabela 'compras'
        result = collection.delete_one({"id": purchase_id})
        if result.deleted_count > 0:
            print(f"Compra {purchase_id} deletada com sucesso.")
        else:
            print(f"Compra com ID {purchase_id} não encontrada.")

    def get_product_by_id(self, product_id):
        collection = self.db.get_collection('produtos')  # Tabela 'produtos'
        query = collection.find_one({"id": product_id})
        return query  # Retorna o documento do produto ou None se não encontrado

    def get_all_users(self):
        collection = self.db.get_collection('usuarios')  # Tabela 'usuarios'
        return list(collection.find())  # Retorna todos os usuários

    def get_all_sellers(self):
        collection = self.db.get_collection('vendedores')  # Tabela 'vendedores'
        return list(collection.find())  # Retorna todos os vendedores

    def get_all_products(self):
        collection = self.db.get_collection('produtos')  # Tabela 'produtos'
        return list(collection.find())  # Retorna todos os produtos

    def get_all_purchases(self):
        collection = self.db.get_collection('compras')  # Tabela 'compras'
        return list(collection.find())  # Retorna todas as compras