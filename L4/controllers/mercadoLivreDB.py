from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import uuid

class MercadoLivreDB:
    def __init__(self, token, api_endpoint):
        # Configuração para conectar ao Astra DB com o cassandra-driver
        auth_provider = PlainTextAuthProvider(username='token', password=token)
        cluster = Cluster(cloud={'secure_connect_bundle': api_endpoint}, auth_provider=auth_provider)
        self.session = cluster.connect()  # Cria a sessão com o banco de dados
        
        # Definindo o keyspace
        self.session.set_keyspace('default_keyspace')

    def insert_user(self, name, age, address):
        user_id = uuid.uuid4()
        cql_query = f"INSERT INTO usuarios (id, nome, idade, endereco) VALUES ({user_id}, '{name}', {age}, '{address}')"
        self.session.execute(cql_query)

    def insert_seller(self, name, age, address):
        seller_id = uuid.uuid4()  # Aqui está a correção
        cql_query = f"INSERT INTO vendedores (id, nome, idade, endereco) VALUES ({seller_id}, '{name}', {age}, '{address}')"
        self.session.execute(cql_query)
        print(f"Vendedor {name} inserido com sucesso com ID {seller_id}.")

    def insert_product(self, name, price, seller_id):
        # Garantir que o seller_id seja um UUID
        if isinstance(seller_id, str):  # Se o seller_id for passado como string
            seller_id = uuid.UUID(seller_id)  # Converte para UUID

        product_id = uuid.uuid4()
        cql_query = f"""
            INSERT INTO produtos (id, nome, valor, vendedor_id)
            VALUES ({product_id}, '{name}', {price}, {seller_id});
        """
        self.session.execute(cql_query)
        print(f"Produto {name} inserido com sucesso com ID {product_id}.")

    def insert_purchase(self, user_id, product_id, quantity, value):
        # Garantir que o user_id seja um UUID
        if isinstance(user_id, str):  # Se o user_id for passado como string
            user_id = uuid.UUID(user_id)  # Converte para UUID

        purchase_id = uuid.uuid4()
        cql_query = f"""
            INSERT INTO compras (id, idUsuario, idProduto, quantidade, valor)
            VALUES ({purchase_id}, {user_id}, {product_id}, {quantity}, {value});
        """
        self.session.execute(cql_query)
        print(f"Compra registrada com sucesso com ID {purchase_id}.")

    def update_user(self, user_id, new_name=None, new_age=None, new_address=None):
        set_clause = []

        if new_name:
            set_clause.append(f"nome = '{new_name}'")
        if new_age is not None:
            set_clause.append(f"idade = {new_age}")
        if new_address:
            set_clause.append(f"endereco = '{new_address}'")

        if not set_clause:
            print("Nenhuma informação para atualizar.")
            return

        set_clause_str = ", ".join(set_clause)
        cql_query = f"UPDATE usuarios SET {set_clause_str} WHERE id = {user_id};"
        self.session.execute(cql_query)
        print(f"Usuário com ID {user_id} atualizado com sucesso.")

    def get_all_users(self):
        cql_query = "SELECT id, nome FROM usuarios;"
        result = self.session.execute(cql_query)
        return [(row.id, row.nome) for row in result]

    def get_all_sellers(self):
        cql_query = "SELECT id, nome FROM vendedores;"
        result = self.session.execute(cql_query)
        return [(row.id, row.nome) for row in result]

    def get_all_products(self):
        cql_query = "SELECT id, nome FROM produtos;"
        result = self.session.execute(cql_query)
        return [(row.id, row.nome) for row in result]

    def get_all_purchases(self):
        cql_query = "SELECT id, idusuario, idproduto FROM compras"
        result = self.session.execute(cql_query)
        return [(row.id, row.idusuario, row.idproduto) for row in result]

    def get_user_name(self, user_id):
        cql_query = "SELECT nome FROM usuarios WHERE id = %s"
        row = self.session.execute(cql_query, (user_id,)).one()
        return row.nome if row else "Unknown"

    def get_product_name(self, product_id):
        cql_query = "SELECT nome FROM produtos WHERE id = %s"
        row = self.session.execute(cql_query, (product_id,)).one()
        return row.nome if row else "Unknown"

    def get_product_by_id(self, product_id):
        cql_query = f"SELECT id, nome, valor FROM produtos WHERE id = {product_id};"
        result = self.session.execute(cql_query)
        for row in result:
            return {'id': row.id, 'nome': row.nome, 'valor': row.valor}
        return None

    def delete_purchase(self, purchase_id):
        cql_query = f"DELETE FROM compras WHERE id = {purchase_id};"
        self.session.execute(cql_query)
        print(f"Compra com ID {purchase_id} deletada com sucesso.")

    def search_product(self, product_id):
        product = self.get_product_by_id(product_id)
        if product:
            print(f"Produto encontrado: {product}")
        else:
            print(f"Produto com ID {product_id} não encontrado.")
