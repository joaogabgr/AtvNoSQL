from neo4j import GraphDatabase
import bcrypt
from datetime import datetime

URI = "neo4j+s://d127d52e.databases.neo4j.io"
AUTH = ("neo4j", "n6m1FlX7-R_y6xgfBscuFTVnWDrf0PAlzaS2neaytwI")
employee_threshold = 10

class Neo4jConnection:
    def __init__(self, uri, auth):
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def close(self):
        self.driver.close()

class UserManager:
    def __init__(self, connection):
        self.connection = connection

    def criar_usuario(self, email, nome, sobrenome, username, hashed_senha, cpf):
        query = """
        CREATE (u:Usuario {
            email: $email,
            nome: $nome,
            sobrenome: $sobrenome,
            username: $username,
            senha: $hashed_senha,
            cpf: $cpf
        })
        RETURN u
        """
        with self.connection.driver.session() as session:
            result = session.run(query, email=email, nome=nome, sobrenome=sobrenome,
                               username=username, hashed_senha=hashed_senha, cpf=cpf)
            return result.single()

    def listar_usuarios(self):
        query = "MATCH (u:Usuario) RETURN u"
        with self.connection.driver.session() as session:
            result = session.run(query)
            return [record["u"] for record in result]

class VendorManager:
    def __init__(self, connection):
        self.connection = connection

    def criar_vendedor(self, nome, sobrenome, cpf):
        with self.connection.driver.session() as session:
            verifica = session.run("""
                MATCH (v:Vendedor {cpf: $cpf})
                RETURN v
            """, cpf=cpf).single()
            if verifica:
                return None
            result = session.run("""
                CREATE (v:Vendedor {
                    nome: $nome,
                    sobrenome: $sobrenome,
                    cpf: $cpf
                })
                RETURN v
            """, nome=nome, sobrenome=sobrenome, cpf=cpf)
            return result.single()

    def listar_vendedores(self):
        query = "MATCH (v:Vendedor) RETURN v"
        with self.connection.driver.session() as session:
            result = session.run(query)
            return [record["v"] for record in result]

class ProductManager:
    def __init__(self, connection):
        self.connection = connection

    def criar_produto(self, nome, descricao, preco, vendedor_cpf):
        query = """
            MATCH (v:Vendedor {cpf: $vendedor_cpf})
            CREATE (p:Produto {
                nome: $nome,
                descricao: $descricao,
                preco: $preco
            })-[:VENDIDO_POR]->(v)
            RETURN p, v
        """
        with self.connection.driver.session() as session:
            return session.run(query, nome=nome, descricao=descricao, preco=preco, vendedor_cpf=vendedor_cpf).single()

    def listar_produtos(self):
        query = """
        MATCH (p:Produto)-[:VENDIDO_POR]->(v:Vendedor)
        RETURN p, v
        """
        with self.connection.driver.session() as session:
            result = session.run(query)
            return [{"produto": record["p"], "vendedor": record["v"]} for record in result]

class PurchaseManager:
    def __init__(self, connection):
        self.connection = connection

    def criar_compra(self, produto_id, usuario_id, quantidade, estado):
        data_compra = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        query = """
        MATCH (p:Produto), (u:Usuario)
        WHERE id(p) = $produto_id AND id(u) = $usuario_id
        CREATE (u)-[:COMPROU]->(c:Compra {
            quantidade: $quantidade,
            estado: $estado,
            data_compra: datetime($data_compra)
        })-[:DE]->(p)
        RETURN c
        """
        with self.connection.driver.session() as session:
            result = session.run(query, produto_id=produto_id, usuario_id=usuario_id,
                               quantidade=quantidade, estado=estado, data_compra=data_compra)
            return result.single()

    def listar_compras(self):
        query = """
        MATCH (u:Usuario)-[:COMPROU]->(c:Compra)-[:DE]->(p:Produto)
        RETURN c, u, p
        """
        with self.connection.driver.session() as session:
            result = session.run(query)
            return [{"compra": record["c"], "usuario": record["u"], "produto": record["p"]} for record in result]

class FavoriteManager:
    def __init__(self, connection):
        self.connection = connection

    def adicionar_favorito(self, usuario_id, produto_id):
        query = """
        MATCH (u:Usuario), (p:Produto)
        WHERE id(u) = $usuario_id AND id(p) = $produto_id
        CREATE (u)-[:FAVORITOU]->(f:Favorito {data_favorito: datetime()})-[:REFERENCIA]->(p)
        RETURN f
        """
        with self.connection.driver.session() as session:
            return session.run(query, usuario_id=usuario_id, produto_id=produto_id).single()

    def listar_favoritos(self, usuario_id):
        query = """
        MATCH (u:Usuario)-[:FAVORITOU]->(f:Favorito)-[:REFERENCIA]->(p:Produto)
        WHERE id(u) = $usuario_id
        RETURN p
        """
        with self.connection.driver.session() as session:
            result = session.run(query, usuario_id=usuario_id)
            return [record["p"] for record in result]

class Application:
    def __init__(self):
        self.connection = Neo4jConnection(URI, AUTH)
        self.user_manager = UserManager(self.connection)
        self.vendor_manager = VendorManager(self.connection)
        self.product_manager = ProductManager(self.connection)
        self.purchase_manager = PurchaseManager(self.connection)
        self.favorite_manager = FavoriteManager(self.connection)

    def run(self):
        try:
            while True:
                print("\nMenu Neo4j:")
                print("1. Criar Usuário")
                print("2. Listar Todos os Usuários")
                print("3. Criar Vendedor")
                print("4. Listar Todos os Vendedores")
                print("5. Criar Produto")
                print("6. Listar Todos os Produtos")
                print("7. Registrar Compra")
                print("8. Listar Todas as Compras")
                print("9. Adicionar Produto aos Favoritos")
                print("10. Listar Favoritos de um Usuário")
                print("11. Sair")
                opcao = input("Selecione uma opção: ")

                if opcao == "1":
                    self.criar_usuario()

                elif opcao == "2":
                    self.listar_usuarios()

                elif opcao == "3":
                    self.criar_vendedor()

                elif opcao == "4":
                    self.listar_vendedores()

                elif opcao == "5":
                    self.criar_produto()

                elif opcao == "6":
                    self.listar_produtos()

                elif opcao == "7":
                    self.registrar_compra()

                elif opcao == "8":
                    self.listar_compras()

                elif opcao == "9":
                    self.adicionar_favorito()

                elif opcao == "10":
                    self.listar_favoritos()

                elif opcao == "11":
                    print("Saindo do programa.")
                    break
                else:
                    print("Opção inválida. Por favor, tente novamente.")
        finally:
            self.connection.close()

    def criar_usuario(self):
        email = input("Digite o email do usuário: ")
        nome = input("Digite o nome do usuário: ")
        sobrenome = input("Digite o sobrenome do usuário: ")
        username = input("Digite o username do usuário: ")
        senha = input("Digite a senha do usuário: ")
        cpf = input("Digite o CPF do usuário: ")
        hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        try:
            result = self.user_manager.criar_usuario(email, nome, sobrenome, username, hashed_senha, cpf)
            if result:
                usuario = result["u"]
                print(f"Usuário '{usuario['nome']} {usuario['sobrenome']}' criado com sucesso.")
            else:
                print("Erro: não foi possível criar o usuário.")
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")

    def listar_usuarios(self):
        try:
            usuarios = self.user_manager.listar_usuarios()
            if usuarios:
                print("\nLista de Usuários:")
                for u in usuarios:
                    print(f"Nome: {u['nome']}, Email: {u['email']}, Username: {u['username']}")
            else:
                print("Nenhum usuário encontrado.")
        except Exception as e:
            print(f"Erro ao listar usuários: {e}")

    def criar_vendedor(self):
        nome = input("Digite o nome do vendedor: ")
        sobrenome = input("Digite o sobrenome do vendedor: ")
        cpf = input("Digite o CPF do vendedor: ")

        try:
            result = self.vendor_manager.criar_vendedor(nome, sobrenome, cpf)
            if result:
                vendedor = result["v"]
                print(f"Vendedor '{vendedor['nome']}' criado com sucesso.")
            else:
                print("Erro: CPF já cadastrado para outro vendedor.")
        except Exception as e:
            print(f"Erro ao criar vendedor: {e}")

    def listar_vendedores(self):
        try:
            vendedores = self.vendor_manager.listar_vendedores()
            if vendedores:
                print("\nLista de Vendedores:")
                for v in vendedores:
                    print(f"Nome: {v['nome']} {v['sobrenome']}, CPF: {v['cpf']}")
            else:
                print("Nenhum vendedor encontrado.")
        except Exception as e:
            print(f"Erro ao listar vendedores: {e}")

    def criar_produto(self):
        nome = input("Digite o nome do produto: ")
        descricao = input("Digite a descrição do produto: ")
        try:
            preco = float(input("Digite o preço do produto: "))
        except ValueError:
            print("Preço inválido. Por favor, insira um número.")
            return

        try:
            vendedores = self.vendor_manager.listar_vendedores()
            if not vendedores:
                print("Não há vendedores cadastrados.")
                return

            print("\nSelecione o vendedor associado ao produto:")
            for idx, vendedor in enumerate(vendedores, start=1):
                print(f"{idx}. {vendedor['nome']} {vendedor['sobrenome']} (CPF: {vendedor['cpf']})")

            escolha = input("Digite o número correspondente ao vendedor: ")
            if escolha.isdigit() and 1 <= int(escolha) <= len(vendedores):
                vendedor_cpf = vendedores[int(escolha) - 1]["cpf"]
            else:
                print("Opção inválida.")
                return

            result = self.product_manager.criar_produto(nome, descricao, preco, vendedor_cpf)
            produto = result["p"]
            vendedor = result["v"]
            print(f"Produto '{produto['nome']}' criado e vinculado ao vendedor {vendedor['nome']} {vendedor['sobrenome']}.")
        except Exception as e:
            print(f"Erro ao criar produto: {e}")

    def listar_produtos(self):
        try:
            produtos = self.product_manager.listar_produtos()
            if produtos:
                print("\nLista de Produtos:")
                for item in produtos:
                    produto = item["produto"]
                    vendedor = item["vendedor"]
                    print(f"Produto: {produto['nome']}, Descrição: {produto['descricao']}, Preço: {produto['preco']}, Vendedor: {vendedor['nome']} {vendedor['sobrenome']}")
            else:
                print("Nenhum produto encontrado.")
        except Exception as e:
            print(f"Erro ao listar produtos: {e}")

    def registrar_compra(self):
        try:
            produtos = self.product_manager.listar_produtos()
            if not produtos:
                print("Não há produtos cadastrados.")
                return

            print("\nSelecione o produto que deseja comprar:")
            for idx, item in enumerate(produtos, start=1):
                produto = item["produto"]
                vendedor = item["vendedor"]
                print(f"{idx}. Produto: {produto['nome']}, Vendedor: {vendedor['nome']} {vendedor['sobrenome']}")

            escolha_produto = input("Digite o número correspondente ao produto: ")
            if escolha_produto.isdigit() and 1 <= int(escolha_produto) <= len(produtos):
                produto_id = produtos[int(escolha_produto) - 1]["produto"].element_id
            else:
                print("Opção inválida.")
                return

            usuarios = self.user_manager.listar_usuarios()
            if not usuarios:
                print("Não há usuários cadastrados.")
                return

            print("\nSelecione o usuário que está realizando a compra:")
            for idx, usuario in enumerate(usuarios, start=1):
                print(f"{idx}. {usuario['nome']} {usuario['sobrenome']} (Email: {usuario['email']})")

            escolha_usuario = input("Digite o número correspondente ao usuário: ")
            if escolha_usuario.isdigit() and 1 <= int(escolha_usuario) <= len(usuarios):
                usuario_id = usuarios[int(escolha_usuario) - 1].id
            else:
                print("Opção inválida.")
                return

            quantidade = input("Digite a quantidade desejada: ")
            if quantidade.isdigit() and int(quantidade) > 0:
                quantidade = int(quantidade)
            else:
                print("Quantidade inválida.")
                return

            estado = input("Digite o estado da compra: ")

            result = self.purchase_manager.criar_compra(produto_id, usuario_id, quantidade, estado)
            if result:
                compra = result["c"]
                data_compra = compra["data_compra"]
                print(f"Compra registrada com sucesso em {data_compra}.")
            else:
                print("Erro ao registrar compra.")
        except Exception as e:
            print(f"Erro ao registrar compra: {e}")

    def listar_compras(self):
        try:
            compras = self.purchase_manager.listar_compras()
            if compras:
                print("\nLista de Compras:")
                for item in compras:
                    compra = item["compra"]
                    usuario = item["usuario"]
                    produto = item["produto"]
                    data_compra = compra["data_compra"]
                    print(f"Usuário: {usuario['nome']} {usuario['sobrenome']}, Produto: {produto['nome']}, Quantidade: {compra['quantidade']}, Estado: {compra['estado']}, Data: {data_compra}")
            else:
                print("Nenhuma compra encontrada.")
        except Exception as e:
            print(f"Erro ao listar compras: {e}")

    def adicionar_favorito(self):
        try:
            produtos = self.product_manager.listar_produtos()
            if not produtos:
                print("Não há produtos cadastrados.")
                return

            print("\nSelecione o produto que deseja adicionar aos favoritos:")
            for idx, item in enumerate(produtos, start=1):
                produto = item["produto"]
                vendedor = item["vendedor"]
                print(f"{idx}. Produto: {produto['nome']}, Vendedor: {vendedor['nome']} {vendedor['sobrenome']}")

            escolha_produto = input("Digite o número correspondente ao produto: ")
            if escolha_produto.isdigit() and 1 <= int(escolha_produto) <= len(produtos):
                produto_id = produtos[int(escolha_produto) - 1]["produto"].id
            else:
                print("Opção inválida.")
                return

            usuarios = self.user_manager.listar_usuarios()
            if not usuarios:
                print("Não há usuários cadastrados.")
                return

            print("\nSelecione o usuário que está adicionando o produto aos favoritos:")
            for idx, usuario in enumerate(usuarios, start=1):
                print(f"{idx}. {usuario['nome']} {usuario['sobrenome']} (Email: {usuario['email']})")

            escolha_usuario = input("Digite o número correspondente ao usuário: ")
            if escolha_usuario.isdigit() and 1 <= int(escolha_usuario) <= len(usuarios):
                usuario_id = usuarios[int(escolha_usuario) - 1].id
            else:
                print("Opção inválida.")
                return

            result = self.favorite_manager.adicionar_favorito(usuario_id, produto_id)
            if result:
                print("Produto adicionado aos favoritos com sucesso.")
            else:
                print("Erro ao adicionar favorito.")
        except Exception as e:
            print(f"Erro ao adicionar favorito: {e}")

    def listar_favoritos(self):
        try:
            usuarios = self.user_manager.listar_usuarios()
            if not usuarios:
                print("Não há usuários cadastrados.")
                return

            print("\nSelecione o usuário para ver seus favoritos:")
            for idx, usuario in enumerate(usuarios, start=1):
                print(f"{idx}. {usuario['nome']} {usuario['sobrenome']} (Email: {usuario['email']})")

            escolha_usuario = input("Digite o número correspondente ao usuário: ")
            if escolha_usuario.isdigit() and 1 <= int(escolha_usuario) <= len(usuarios):
                usuario_id = usuarios[int(escolha_usuario) - 1].id
                usuario = usuarios[int(escolha_usuario) - 1]
            else:
                print("Opção inválida.")
                return

            favoritos = self.favorite_manager.listar_favoritos(usuario_id)
            if favoritos:
                print(f"\nProdutos favoritos de {usuario['nome']} {usuario['sobrenome']}:")
                for produto in favoritos:
                    print(f"- {produto['nome']}: {produto['descricao']} (Preço: {produto['preco']})")
            else:
                print("Este usuário não possui produtos favoritos.")
        except Exception as e:
            print(f"Erro ao listar favoritos: {e}")

def main():
    app = Application()
    app.run()

if __name__ == "__main__":
    main()