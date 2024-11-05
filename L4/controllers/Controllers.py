from astrapy import DataAPIClient
import uuid

class MercadoLivreDB:
    def __init__(self, token, api_endpoint):
        # Inicializa o cliente Astra DB
        self.client = DataAPIClient(token)
        self.db = self.client.get_database_by_api_endpoint(api_endpoint)

    def insert_user(self, name, email):
        user_id = str(uuid.uuid4())
        collection = self.db.get_collection('usuario')  # Obtém a coleção 'usuario'
        query = {"user_id": user_id, "name": name, "email": email}
        collection.insert_one(query)  # Insere um documento na coleção
        print(f"Usuário {name} inserido com sucesso com ID {user_id}.")

    def insert_seller(self, name, rating):
        seller_id = str(uuid.uuid4())
        collection = self.db.get_collection('vendedor')  # Obtém a coleção 'vendedor'
        query = {"seller_id": seller_id, "name": name, "rating": rating}
        collection.insert_one(query)  # Insere um documento na coleção
        print(f"Vendedor {name} inserido com sucesso com ID {seller_id}.")

    def insert_product(self, name, price):
        product_id = str(uuid.uuid4())
        collection = self.db.get_collection('produto')  # Obtém a coleção 'produto'
        query = {"product_id": product_id, "name": name, "price": price}
        collection.insert_one(query)  # Insere um documento na coleção
        print(f"Produto {name} inserido com sucesso com ID {product_id}.")

    def insert_purchase(self, user_id, product_id, quantity):
        purchase_id = str(uuid.uuid4())
        collection = self.db.get_collection('compra')  # Obtém a coleção 'compra'
        query = {"purchase_id": purchase_id, "user_id": user_id, "product_id": product_id, "quantity": quantity}
        collection.insert_one(query)  # Insere um documento na coleção
        print(f"Compra registrada com sucesso com ID {purchase_id}.")

    def update_user(self, user_id, new_name=None, new_email=None):
        collection = self.db.get_collection('usuario')  # Obtém a coleção 'usuario'
        updates = {}
        
        if new_name:
            updates["name"] = new_name
        if new_email:
            updates["email"] = new_email

        if updates:
            collection.update_one({"user_id": user_id}, {"$set": updates})
            print(f"Usuário {user_id} atualizado com sucesso.")

    def search_product(self, product_id):
        collection = self.db.get_collection('produto')  # Obtém a coleção 'produto'
        query = collection.find_one({"product_id": product_id})
        if query:
            print(f"Produto encontrado: ID: {query['product_id']}, Nome: {query['name']}, Preço: {query['price']}")
        else:
            print(f"Produto com ID {product_id} não encontrado.")

    def delete_purchase(self, purchase_id):
        collection = self.db.get_collection('compra')  # Obtém a coleção 'compra'
        result = collection.delete_one({"purchase_id": purchase_id})
        if result.deleted_count > 0:
            print(f"Compra {purchase_id} deletada com sucesso.")
        else:
            print(f"Compra com ID {purchase_id} não encontrada.")
