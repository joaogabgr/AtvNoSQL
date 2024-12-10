from connectMongo import get_database
from .produtosController import ProdutoController
import bcrypt

class ClienteController:
    def __init__(self):
        self.db = get_database()
        self.clientes = self.db["clientes"]
        self.produto_controller = ProdutoController()

    def listar_clientes(self):
        return list(self.clientes.find())

    def buscar_cliente(self, cpf):
        return self.clientes.find_one({"cpf": cpf})

    def buscar_cliente_id(self, id):
        return self.clientes.find_one({"_id": id})

    def inserir_cliente(self):
        nome = input("Nome: ")
        idade = int(input("Idade: "))
        cpf = input("CPF: ")
        if self.verificar_cpf(cpf):
            return None

        email = input("Email: ")
        if self.verificar_email(email):
            return None
        
        senha = input("Senha: ")
        senha_crip = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        endereco = {
            "rua": input("Rua: "),
            "numero": input("Número: "),
            "bairro": input("Bairro: "),
            "cidade": input("Cidade: "),
            "estado": input("Estado: ")
        }

        cliente = {
            "nome": nome,
            "idade": idade,
            "cpf": cpf,
            "email": email,
            "senha": senha_crip,
            "endereco": endereco,
            "favoritos": [],
            "compras": []
        }
        return self.clientes.insert_one(cliente)

    def atualizar_cliente(self):
        cliente = self.selecionar_cliente()
        if not cliente:
            return 'Cliente não encontrado.'

        cliente.update({
            "nome": input("Nome: "),
            "idade": int(input("Idade: ")),
            "endereco": {
                "rua": input("Rua: "),
                "numero": input("Número: "),
                "bairro": input("Bairro: "),
                "cidade": input("Cidade: "),
                "estado": input("Estado: ")
            }
        })
        return self.clientes.replace_one({"cpf": cliente["cpf"]}, cliente)

    def deletar_cliente(self, cpf):
        return self.clientes.delete_one({"cpf": cpf})

    def selecionar_cliente(self):
        clientes = self.listar_clientes()
        if not clientes:
            print("Nenhum cliente encontrado.")
            return None

        print("\n--- Lista de Clientes ---")
        for index, cliente in enumerate(clientes):
            print(f"{index}. {cliente['nome']} - CPF: {cliente['cpf']}")

        while True:
            try:
                indice = int(input("Selecione o índice do cliente: "))
                if 0 <= indice < len(clientes):
                    return clientes[indice]
                else:
                    print("Índice inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Por favor, insira um número.")

    def verificar_email(self, email):
        return self.clientes.find_one({"email": email})

    def verificar_cpf(self, cpf):
        return self.clientes.find_one({"cpf": cpf})

    def listar_favoritos(self):
        cliente = self.selecionar_cliente()
        if not cliente:
            return "Cliente não encontrado."
        favoritos = cliente.get("favoritos", [])
        if not favoritos:
            return "Nenhum produto nos favoritos."

        print("\n--- Produtos Favoritos ---")
        for produto_id in favoritos:
            produto = self.produto_controller.produtos.find_one({"_id": produto_id})
            if produto:
                print(f"ID: {produto['_id']}, Nome: {produto['nome']}, Preço: {produto['valor']}")
            else:
                print(f"Produto com ID {produto_id} não encontrado.")
        return "Listagem de favoritos concluída."

    def adicionar_favorito(self):
        cliente = self.selecionar_cliente()
        if not cliente:
            return 'Cliente não encontrado.'

        produto = self.produto_controller.selecionar_produto()
        if not produto:
            return 'Produto não encontrado.'

        if produto["_id"] not in cliente["favoritos"]:
            cliente["favoritos"].append(produto["_id"])
            self.clientes.update_one({"cpf": cliente["cpf"]}, {"$set": {"favoritos": cliente["favoritos"]}})
            return 'Produto adicionado aos favoritos.'
        return 'Produto já está nos favoritos.'

    def remover_favorito(self):
        cliente = self.selecionar_cliente()
        if not cliente:
            return 'Cliente não encontrado.'

        produto = self.produto_controller.selecionar_produto()
        if not produto:
            return 'Produto não encontrado.'

        if produto["_id"] in cliente["favoritos"]:
            cliente["favoritos"].remove(produto["_id"])
            self.clientes.update_one({"cpf": cliente["cpf"]}, {"$set": {"favoritos": cliente["favoritos"]}})
            return 'Produto removido dos favoritos.'
        return 'Produto não está nos favoritos.'

    def avaliar_produto(self):
        cliente = self.selecionar_cliente()
        if not cliente:
            return 'Cliente não encontrado.'

        produto = self.produto_controller.selecionar_produto()
        if not produto:
            return 'Produto não encontrado.'

        avaliacao = input("Avaliação: ")
        avaliacao_data = {
            "cliente_id": cliente["_id"],
            "avaliacao": avaliacao
        }
        produto["avaliacao"].append(avaliacao_data)
        self.produto_controller.produtos.update_one({"_id": produto["_id"]}, {"$set": {"avaliacao": produto["avaliacao"]}})
        return 'Avaliação adicionada ao produto.'

    def listar_compras(self):
        cliente = self.selecionar_cliente()
        if not cliente:
            return "Cliente não encontrado."
        compras = cliente.get("compras", [])
        if not compras:
            return "Nenhuma compra registrada para este cliente."
        return compras

    def adicionar_compra(self):
        cliente = self.selecionar_cliente()
        if not cliente:
            return "Cliente não encontrado."

        produto = self.produto_controller.selecionar_produto()
        if not produto:
            return 'Produto não encontrado.'

        quantidade = int(input("Quantidade: "))
        compra = {
            "produto_id": produto["_id"],
            "produto_nome": produto["nome"],
            "quantidade": quantidade,
            "valor_total": produto["valor"] * quantidade
        }

        cliente["compras"].append(compra)
        self.clientes.update_one({"cpf": cliente["cpf"]}, {"$set": {"compras": cliente["compras"]}})

        vendedor_id = produto.get("vendedor_id")
        if vendedor_id:
            vendedor = self.db["vendedores"].find_one({"_id": vendedor_id})
            if vendedor:
                vendas = vendedor.get("vendas", [])
                vendas.append(compra)
                self.db["vendedores"].update_one({"_id": vendedor_id}, {"$set": {"vendas": vendas}})

        return "Compra adicionada com sucesso."
