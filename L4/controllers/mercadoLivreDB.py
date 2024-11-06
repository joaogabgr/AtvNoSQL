from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import uuid

class MercadoLivreDB:
    def __init__(self, token, api_endpoint):
        auth_provider = PlainTextAuthProvider(username='token', password=token)
        cluster = Cluster(cloud={'secure_connect_bundle': api_endpoint}, auth_provider=auth_provider)
        self.sessao = cluster.connect()
        self.sessao.set_keyspace('default_keyspace')

    def inserir_usuario(self, nome, idade, endereco):
        id_usuario = uuid.uuid4()
        cql_query = f"INSERT INTO usuarios (id, nome, idade, endereco) VALUES ({id_usuario}, '{nome}', {idade}, '{endereco}')"
        self.sessao.execute(cql_query)

    def inserir_vendedor(self, nome, idade, endereco):
        id_vendedor = uuid.uuid4()
        cql_query = f"INSERT INTO vendedores (id, nome, idade, endereco) VALUES ({id_vendedor}, '{nome}', {idade}, '{endereco}')"
        self.sessao.execute(cql_query)
        print(f"Vendedor {nome} inserido com sucesso com ID {id_vendedor}.")

    def inserir_produto(self, nome, valor, id_vendedor):
        if isinstance(id_vendedor, str):
            id_vendedor = uuid.UUID(id_vendedor)
        
        id_produto = uuid.uuid4()
        cql_query = f"""
            INSERT INTO produtos (id, nome, valor, vendedor_id)
            VALUES ({id_produto}, '{nome}', {valor}, {id_vendedor});
        """
        self.sessao.execute(cql_query)
        print(f"Produto {nome} inserido com sucesso com ID {id_produto}.")

    def inserir_compra(self, id_usuario, id_produto, quantidade, valor):
        if isinstance(id_usuario, str):
            id_usuario = uuid.UUID(id_usuario)
        
        id_compra = uuid.uuid4()
        cql_query = f"""
            INSERT INTO compras (id, idUsuario, idProduto, quantidade, valor)
            VALUES ({id_compra}, {id_usuario}, {id_produto}, {quantidade}, {valor});
        """
        self.sessao.execute(cql_query)
        print(f"Compra registrada com sucesso com ID {id_compra}.")

    def atualizar_usuario(self, id_usuario, novo_nome=None, nova_idade=None, novo_endereco=None):
        campos_set = []

        if novo_nome:
            campos_set.append(f"nome = '{novo_nome}'")
        if nova_idade is not None:
            campos_set.append(f"idade = {nova_idade}")
        if novo_endereco:
            campos_set.append(f"endereco = '{novo_endereco}'")

        if not campos_set:
            print("Nenhuma informação para atualizar.")
            return

        campos_set_str = ", ".join(campos_set)
        cql_query = f"UPDATE usuarios SET {campos_set_str} WHERE id = {id_usuario};"
        self.sessao.execute(cql_query)
        print(f"Usuário com ID {id_usuario} atualizado com sucesso.")

    def obter_todos_usuarios(self):
        cql_query = "SELECT id, nome FROM usuarios;"
        resultado = self.sessao.execute(cql_query)
        return [(linha.id, linha.nome) for linha in resultado]

    def obter_todos_vendedores(self):
        cql_query = "SELECT id, nome FROM vendedores;"
        resultado = self.sessao.execute(cql_query)
        return [(linha.id, linha.nome) for linha in resultado]

    def obter_todos_produtos(self):
        cql_query = "SELECT id, nome FROM produtos;"
        resultado = self.sessao.execute(cql_query)
        return [(linha.id, linha.nome) for linha in resultado]

    def obter_todas_compras(self):
        cql_query = "SELECT id, idusuario, idproduto FROM compras"
        resultado = self.sessao.execute(cql_query)
        return [(linha.id, linha.idusuario, linha.idproduto) for linha in resultado]

    def obter_nome_usuario(self, id_usuario):
        cql_query = "SELECT nome FROM usuarios WHERE id = %s"
        linha = self.sessao.execute(cql_query, (id_usuario,)).one()
        return linha.nome if linha else "Desconhecido"

    def obter_nome_produto(self, id_produto):
        cql_query = "SELECT nome FROM produtos WHERE id = %s"
        linha = self.sessao.execute(cql_query, (id_produto,)).one()
        return linha.nome if linha else "Desconhecido"

    def obter_produto_por_id(self, id_produto):
        cql_query = f"SELECT id, nome, valor FROM produtos WHERE id = {id_produto};"
        resultado = self.sessao.execute(cql_query)
        for linha in resultado:
            return {'id': linha.id, 'nome': linha.nome, 'valor': linha.valor}
        return None

    def deletar_compra(self, id_compra):
        cql_query = f"DELETE FROM compras WHERE id = {id_compra};"
        self.sessao.execute(cql_query)
        print(f"Compra com ID {id_compra} deletada com sucesso.")

    def buscar_produto(self, id_produto):
        produto = self.obter_produto_por_id(id_produto)
        if produto:
            print(f"Produto encontrado: {produto}")
        else:
            print(f"Produto com ID {id_produto} não encontrado.")
