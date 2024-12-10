from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# Credenciais do Astra DB
TOKEN = "AstraCS:ZTDirJKWZTtrYlsgZBkqTAUi:4b1199744185b39180f27d0c85d8b73a4279fe4f4b0e7d5c1411c9310bcb74fa"
ASTRA_DB_ID = "e7f01c54-d8e0-494e-b557-705a9959f49b"
ASTRA_DB_REGION = "us-east-2"
SECURE_CONNECT_BUNDLE = "./secure-connect-cassandra.zip"

def connect_cassandra():
    auth_provider = PlainTextAuthProvider(username='token', password=TOKEN)
    cluster = Cluster(cloud={'secure_connect_bundle': SECURE_CONNECT_BUNDLE}, auth_provider=auth_provider)
    session = cluster.connect()
    session.set_keyspace('default_keyspace')  # Substitua pelo seu keyspace, se necessário
    return session

def create_tables(session):
    queries = [
        """
        CREATE TABLE IF NOT EXISTS usuario (
            id UUID PRIMARY KEY,
            nome TEXT,
            email TEXT,
            senha TEXT,
            rua TEXT,
            numero TEXT,
            bairro TEXT,
            cidade TEXT,
            estado TEXT,
            cep TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS vendedor (
            id UUID PRIMARY KEY,
            name TEXT,
            email TEXT,
            senha TEXT,
            rua TEXT,
            numero TEXT,
            bairro TEXT,
            cidade TEXT,
            estado TEXT,
            cep TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS produto (
            id UUID PRIMARY KEY,
            name TEXT,
            price FLOAT,
            seller_id UUID
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS compra (
            purchase_id UUID PRIMARY KEY,
            user_id UUID,
            product_id UUID,
            date TEXT
        )
        """
    ]

    for i, query in enumerate(queries, 1):
        try:
            session.execute(query)
            print(f"Tabela {i} criada com sucesso.")
        except Exception as e:
            print(f"Erro ao criar a tabela {i}: {e}")

if __name__ == "__main__":
    session = connect_cassandra()
    create_tables(session)
