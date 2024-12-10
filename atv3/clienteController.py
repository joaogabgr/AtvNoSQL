import bcrypt
from bson import ObjectId
from connectBanco import get_mongo_database, get_redis_client

EXPIRACAO_SESSAO = 3600

class ClienteController:
    def __init__(self):
        self.db = get_mongo_database()
        self.clientes = self.db["clientes"]
        self.redis_client = get_redis_client()

    def autenticar_usuario(self, email, senha):
        usuario = self.clientes.find_one({"email": email})
        if not usuario:
            return False, "Usuário não encontrado."

        if not bcrypt.checkpw(senha.encode("utf-8"), usuario["senha"]):
            return False, "Senha incorreta."

        session_key = f"session:{usuario['_id']}"
        self.redis_client.set(session_key, email, ex=EXPIRACAO_SESSAO)
        return True, usuario["_id"]

    def logout_usuario(self, user_id):
        session_key = f"session:{user_id}"
        self.redis_client.delete(session_key)
        return "Usuário deslogado com sucesso."

    def verificar_autenticacao(self, user_id):
        session_key = f"session:{user_id}"
        if self.redis_client.get(session_key):
            return True
        return False

    def listar_produtos(self, user_id):
        if not self.verificar_autenticacao(user_id):
            return "Usuário não autenticado. Faça login para continuar."
        
        produtos = list(self.db["produtos"].find())
        for index, produto in enumerate(produtos):
            print(f"{index}. {produto['nome']} - Preço: {produto['valor']}")
        return produtos

    def selecionar_produto(self, user_id):
        produtos = self.listar_produtos(user_id)
        if not produtos:
            return None

        while True:
            try:
                indice = int(input("Selecione o índice do produto: "))
                if 0 <= indice < len(produtos):
                    return produtos[indice]
                else:
                    print("Índice inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Por favor, insira um número.")

    def adicionar_favorito(self, user_id):
        if not self.verificar_autenticacao(user_id):
            return "Usuário não autenticado. Faça login para continuar."

        usuario = self.clientes.find_one({"_id": ObjectId(user_id)})
        if not usuario:
            return "Erro ao acessar dados do usuário."

        produto = self.selecionar_produto(user_id)
        if not produto:
            return 'Produto não encontrado.'

        if produto["_id"] not in usuario.get("favoritos", []):
            usuario.setdefault("favoritos", []).append(produto["_id"])
            self.clientes.update_one({"_id": ObjectId(user_id)}, {"$set": {"favoritos": usuario["favoritos"]}})
            return "Produto adicionado aos favoritos."
        return "Produto já está nos favoritos."

    def remover_favorito(self, user_id):
        if not self.verificar_autenticacao(user_id):
            return "Usuário não autenticado. Faça login para continuar."

        usuario = self.clientes.find_one({"_id": ObjectId(user_id)})
        if not usuario:
            return "Erro ao acessar dados do usuário."

        produto = self.selecionar_produto(user_id)
        if not produto:
            return 'Produto não encontrado.'

        if produto["_id"] in usuario.get("favoritos", []):
            usuario["favoritos"].remove(produto["_id"])
            self.clientes.update_one({"_id": ObjectId(user_id)}, {"$set": {"favoritos": usuario["favoritos"]}})
            return "Produto removido dos favoritos."
        return "Produto não está nos favoritos."

    def adicionar_compra(self, user_id):
        if not self.verificar_autenticacao(user_id):
            return "Usuário não autenticado. Faça login para continuar."

        usuario = self.clientes.find_one({"_id": ObjectId(user_id)})
        if not usuario:
            return "Erro ao acessar dados do usuário."

        produto = self.selecionar_produto(user_id)
        if not produto:
            return 'Produto não encontrado.'

        quantidade = int(input("Quantidade: "))
        compra = {
            "produto_id": produto["_id"],
            "produto_nome": produto["nome"],
            "quantidade": quantidade,
            "valor_total": produto["valor"] * quantidade,
        }

        usuario.setdefault("compras", []).append(compra)
        self.clientes.update_one({"_id": ObjectId(user_id)}, {"$set": {"compras": usuario["compras"]}})

        vendedor_id = produto.get("vendedor_id")
        if vendedor_id:
            vendedor = self.db["vendedores"].find_one({"_id": ObjectId(vendedor_id)})
            if vendedor:
                vendas = vendedor.setdefault("vendas", [])
                vendas.append(compra)
                self.db["vendedores"].update_one({"_id": ObjectId(vendedor_id)}, {"$set": {"vendas": vendas}})

        return "Compra adicionada com sucesso."
    
    def buscar_cliente_id(self, cliente_id):
        return self.clientes.find_one({"_id": ObjectId(cliente_id)})
    
    def adicionar_avaliacao(self, user_id):
        if not self.verificar_autenticacao(user_id):
            return "Usuário não autenticado. Faça login para continuar."

        usuario = self.clientes.find_one({"_id": ObjectId(user_id)})
        if not usuario:
            return "Erro ao acessar dados do usuário."

        produto = self.selecionar_produto(user_id)
        if not produto:
            return 'Produto não encontrado.'

        avaliacao = input("Avaliação: ")
        avaliacao_data = {
            "cliente_id": usuario["_id"],
            "avaliacao": avaliacao
        }
        produto.setdefault("avaliacao", []).append(avaliacao_data)
        self.db["produtos"].update_one({"_id": produto["_id"]}, {"$set": {"avaliacao": produto["avaliacao"]}})
        return 'Avaliação adicionada ao produto.'

    def remover_avaliacao(self, user_id):
        if not self.verificar_autenticacao(user_id):
            return "Usuário não autenticado. Faça login para continuar."

        usuario = self.clientes.find_one({"_id": ObjectId(user_id)})
        if not usuario:
            return "Erro ao acessar dados do usuário."

        produto = self.selecionar_produto(user_id)
        if not produto:
            return 'Produto não encontrado.'

        avaliacao_encontrada = None
        for avaliacao in produto.get("avaliacao", []):
            if avaliacao["cliente_id"] == usuario["_id"]:
                avaliacao_encontrada = avaliacao
                break

        if avaliacao_encontrada:
            produto["avaliacao"].remove(avaliacao_encontrada)
            self.db["produtos"].update_one({"_id": produto["_id"]}, {"$set": {"avaliacao": produto["avaliacao"]}})
            return 'Avaliação removida do produto.'
        return 'Avaliação não encontrada.'