from connectMongo import get_database
from .vendedorController import VendedorController

class ProdutoController:
    def __init__(self):
        self.db = get_database()
        self.produtos = self.db["produtos"]
        self.vendedor_controller = VendedorController()

    def listar_produtos(self):
        produtos = list(self.produtos.find())
        return produtos

    def buscar_produto(self):
        produto = self.selecionar_produto()
        if not produto:
            return None
    
        produto = self.produtos.find_one({"_id": produto["_id"]})
        return produto if produto else None
    
    def buscar_produto_id(self, id):
        produto = self.produtos.find_one({"_id": id})
        return produto if produto else None

    def inserir_produto(self):
        nome = input("Nome: ")
        descricao = input("Descrição: ")
        valor = float(input("Valor: "))
        quantidade = int(input("Quantidade: "))
        
        vendedor = self.vendedor_controller.selecionar_vendedor()
        if not vendedor:
            return None

        produto = {
            "nome": nome,
            "descricao": descricao,
            "valor": valor,
            "quantidade": quantidade,
            "vendedor_id": vendedor["_id"],
            "avaliacao": []
        }
        result = self.produtos.insert_one(produto)
        
        vendedor["produtos"].append(result.inserted_id)
        self.vendedor_controller.vendedores.update_one({"_id": vendedor["_id"]}, {"$set": {"produtos": vendedor["produtos"]}})
        
        return result

    def atualizar_produto(self):
        produto = self.selecionar_produto()
        if produto is None:
            return 'Produto não encontrado.'

        nome = input("Nome: ")
        descricao = input("Descrição: ")
        valor = float(input("Valor: "))
        quantidade = int(input("Quantidade: "))

        produto_atualizado = {
            "nome": nome,
            "descricao": descricao,
            "valor": valor,
            "quantidade": quantidade,
            "vendedor_id": produto["vendedor_id"],
            "avaliacao": produto.get("avaliacao", [])
        }
        return self.produtos.replace_one({"_id": produto["_id"]}, produto_atualizado)

    def deletar_produto(self):
        produto = self.selecionar_produto()
        if produto is None:
            return 'Produto não encontrado.'

        vendedor = self.vendedor_controller.vendedores.find_one({"_id": produto["vendedor_id"]})
        if vendedor:
            vendedor["produtos"].remove(produto["_id"])
            self.vendedor_controller.vendedores.update_one({"_id": vendedor["_id"]}, {"$set": {"produtos": vendedor["produtos"]}})
        
        return self.produtos.delete_one({"_id": produto["_id"]})
    
    def selecionar_produto(self):
        produtos = self.listar_produtos()
        if not produtos:
            print("Nenhum produto encontrado.")
            return None

        print("\n--- Lista de Produtos ---")
        for index, produto in enumerate(produtos):
            print(f"{index}. {produto['nome']} - ID: {produto['_id']}")

        while True:
            try:
                indice = int(input("Selecione o índice do produto: "))
                if 0 <= indice < len(produtos):
                    return produtos[indice]
                else:
                    print("Índice inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Por favor, insira um número.")