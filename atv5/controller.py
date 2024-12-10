from connectNeo4j import connect_neo4j, close_neo4j
import uuid
from datetime import datetime

class Neo4jController:
    def __init__(self):
        self.driver = connect_neo4j()

    def insert_usuario(self):
        nome = input("Digite o nome: ")
        email = input("Digite o email: ")
        senha = input("Digite a senha: ")
        rua = input("Digite a rua: ")
        numero = input("Digite o numero: ")
        bairro = input("Digite o bairro: ")
        cidade = input("Digite a cidade: ")
        estado = input("Digite o estado: ")
        cep = input("Digite o cep: ")
        query = """
        CREATE (u:Usuario {
            id: $id, nome: $nome, email: $email, senha: $senha, 
            rua: $rua, numero: $numero, bairro: $bairro, 
            cidade: $cidade, estado: $estado, cep: $cep
        })
        """
        with self.driver.session() as session:
            session.run(query, id=str(uuid.uuid4()), nome=nome, email=email, senha=senha, 
                        rua=rua, numero=numero, bairro=bairro, cidade=cidade, estado=estado, cep=cep)

    def insert_vendedor(self):
        name = input("Digite o nome: ")
        email = input("Digite o email: ")
        senha = input("Digite a senha: ")
        rua = input("Digite a rua: ")
        numero = input("Digite o numero: ")
        bairro = input("Digite o bairro: ")
        cidade = input("Digite a cidade: ")
        estado = input("Digite o estado: ")
        cep = input("Digite o cep: ")
        query = """
        CREATE (v:Vendedor {
            id: $id, name: $name, email: $email, senha: $senha, 
            rua: $rua, numero: $numero, bairro: $bairro, 
            cidade: $cidade, estado: $estado, cep: $cep
        })
        """
        with self.driver.session() as session:
            session.run(query, id=str(uuid.uuid4()), name=name, email=email, senha=senha, 
                        rua=rua, numero=numero, bairro=bairro, cidade=cidade, estado=estado, cep=cep)

    def insert_produto(self):
        name = input("Digite o nome do produto: ")
        price = float(input("Digite o preço: "))
        seller_id = self.select_vendedor()
        query = """
        MATCH (v:Vendedor {id: $seller_id})
        CREATE (p:Produto {
            id: $id, name: $name, price: $price
        })-[:VENDIDO_POR]->(v)
        """
        with self.driver.session() as session:
            session.run(query, id=str(uuid.uuid4()), name=name, price=price, seller_id=seller_id)

    def insert_compra(self):
        user_id = self.select_usuario()
        product_id = self.select_produto()
        date = datetime.now().strftime("%Y-%m-%d")
        query = """
        MATCH (u:Usuario {id: $user_id}), (p:Produto {id: $product_id})
        CREATE (c:Compra {
            id: $id, date: $date
        })-[:COMPRADO_POR]->(u)-[:COMPROU]->(p)
        """
        with self.driver.session() as session:
            session.run(query, id=str(uuid.uuid4()), user_id=user_id, product_id=product_id, date=date)

    def search_usuario(self):
        query = "MATCH (u:Usuario) RETURN u.id AS id, u.nome AS nome"
        with self.driver.session() as session:
            result = session.run(query)
            usuarios = result.data()
            if usuarios:
                print("Usuários disponíveis:")
                for i, usuario in enumerate(usuarios):
                    print(f"{i}: Nome: {usuario['nome']} (ID: {usuario['id']})")
                index = int(input("Selecione o índice do usuário: "))
                if 0 <= index < len(usuarios):
                    selected_usuario = usuarios[index]
                    query = "MATCH (u:Usuario {id: $id}) RETURN u"
                    result = session.run(query, id=selected_usuario['id'])
                    usuario_info = result.single()
                    if usuario_info:
                        usuario = usuario_info['u']
                        print(f"Usuário selecionado:\nID: {usuario['id']}\nNome: {usuario['nome']}\nEmail: {usuario['email']}\nRua: {usuario['rua']}\nNúmero: {usuario['numero']}\nBairro: {usuario['bairro']}\nCidade: {usuario['cidade']}\nEstado: {usuario['estado']}\nCEP: {usuario['cep']}")
                        return usuario
                    else:
                        print("Usuário não encontrado.")
                        return None
                else:
                    print("Índice inválido.")
                    return None
            else:
                print("Nenhum usuário disponível.")
                return None

    def search_vendedor(self):
        query = "MATCH (v:Vendedor) RETURN v.id AS id, v.name AS name"
        with self.driver.session() as session:
            result = session.run(query)
            vendedores = result.data()
            if vendedores:
                print("Vendedores disponíveis:")
                for i, vendedor in enumerate(vendedores):
                    print(f"{i}: Nome: {vendedor['name']} (ID: {vendedor['id']})")
                index = int(input("Selecione o índice do vendedor: "))
                if 0 <= index < len(vendedores):
                    selected_vendedor = vendedores[index]
                    query = "MATCH (v:Vendedor {id: $id}) RETURN v"
                    result = session.run(query, id=selected_vendedor['id'])
                    vendedor_info = result.single()
                    if vendedor_info:
                        vendedor = vendedor_info['v']
                        print(f"Vendedor selecionado:\nID: {vendedor['id']}\nNome: {vendedor['name']}\nEmail: {vendedor['email']}\nRua: {vendedor['rua']}\nNúmero: {vendedor['numero']}\nBairro: {vendedor['bairro']}\nCidade: {vendedor['cidade']}\nEstado: {vendedor['estado']}\nCEP: {vendedor['cep']}")
                        return vendedor
                    else:
                        print("Vendedor não encontrado.")
                        return None
                else:
                    print("Índice inválido.")
                    return None
            else:
                print("Nenhum vendedor disponível.")
                return None

    def search_produto(self):
        query = "MATCH (p:Produto) RETURN p.id AS id, p.name AS name"
        with self.driver.session() as session:
            result = session.run(query)
            produtos = result.data()
            if produtos:
                print("Produtos disponíveis:")
                for i, produto in enumerate(produtos):
                    print(f"{i}: Nome: {produto['name']} (ID: {produto['id']})")
                index = int(input("Selecione o índice do produto: "))
                if 0 <= index < len(produtos):
                    selected_produto = produtos[index]
                    query = "MATCH (p:Produto {id: $id}) RETURN p"
                    result = session.run(query, id=selected_produto['id'])
                    produto_info = result.single()
                    if produto_info:
                        produto = produto_info['p']
                        print(f"Produto selecionado:\nID: {produto['id']}\nNome: {produto['name']}\nPreço: {produto['price']}")
                        return produto
                    else:
                        print("Produto não encontrado.")
                        return None
                else:
                    print("Índice inválido.")
                    return None
            else:
                print("Nenhum produto disponível.")
                return None

    def search_compra(self):
        query = """
        MATCH (c:Compra)-[:COMPRADO_POR]->(u:Usuario)-[:COMPROU]->(p:Produto)
        RETURN c.id AS id, c.date AS date, u.nome AS usuario_nome, p.name AS produto_nome
        """
        with self.driver.session() as session:
            result = session.run(query)
            compras = result.data()
            if compras:
                print("Compras disponíveis:")
                for i, compra in enumerate(compras):
                    print(f"{i}: Data: {compra['date']} (ID: {compra['id']})")
                index = int(input("Selecione o índice da compra: "))
                if 0 <= index < len(compras):
                    selected_compra = compras[index]
                    query = """
                    MATCH (c:Compra {id: $id})-[:COMPRADO_POR]->(u:Usuario)-[:COMPROU]->(p:Produto)
                    RETURN c.id AS id, c.date AS date, u.nome AS usuario_nome, p.name AS produto_nome
                    """
                    result = session.run(query, id=selected_compra['id'])
                    compra_info = result.single()
                    if compra_info:
                        compra = compra_info
                        print(f"Compra selecionada:\nID: {compra['id']}\nData: {compra['date']}\nComprador: {compra['usuario_nome']}\nProduto: {compra['produto_nome']}")
                        return compra
                    else:
                        print("Compra não encontrada.")
                        return None
                else:
                    print("Índice inválido.")
                    return None
            else:
                print("Nenhuma compra disponível.")
                return None

    def select_usuario(self):
        query = "MATCH (u:Usuario) RETURN u.id AS id, u.nome AS nome"
        with self.driver.session() as session:
            result = session.run(query)
            usuarios = result.data()
            for i, usuario in enumerate(usuarios):
                print(f"{i}: {usuario['nome']} (ID: {usuario['id']})")
            index = int(input("Selecione o índice do usuário: "))
            return usuarios[index]['id']

    def select_vendedor(self):
        query = "MATCH (v:Vendedor) RETURN v.id AS id, v.name AS name"
        with self.driver.session() as session:
            result = session.run(query)
            vendedores = result.data()
            for i, vendedor in enumerate(vendedores):
                print(f"{i}: {vendedor['name']} (ID: {vendedor['id']})")
            index = int(input("Selecione o índice do vendedor: "))
            return vendedores[index]['id']

    def select_produto(self):
        query = "MATCH (p:Produto) RETURN p.id AS id, p.name AS name"
        with self.driver.session() as session:
            result = session.run(query)
            produtos = result.data()
            for i, produto in enumerate(produtos):
                print(f"{i}: {produto['name']} (ID: {produto['id']})")
            index = int(input("Selecione o índice do produto: "))
            return produtos[index]['id']

    def select_compra(self):
        query = "MATCH (c:Compra) RETURN c.id AS id, c.date AS date"
        with self.driver.session() as session:
            result = session.run(query)
            compras = result.data()
            for i, compra in enumerate(compras):
                print(f"{i}: Compra ID: {compra['id']}, Data: {compra['date']}")
            index = int(input("Selecione o índice da compra: "))
            return compras[index]['id']

    def close(self):
        close_neo4j(self.driver)