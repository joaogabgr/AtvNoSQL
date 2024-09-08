import connectMongo
from models import Produtos

selectDatabase = connectMongo.client['MercadoLivre']
collection = selectDatabase['produto']
vendedorCollection = selectDatabase['vendedor']

class ProdutosController:
    def criarProduto(self):
        nome = input('Digite o nome do produto: ')
        if collection.find_one({'nome': nome}) is not None:
            print('Produto já cadastrado')
            return
        preco = input('Digite o preço do produto: ')
        estoque = input('Digite o estoque do produto: ')

        vendedor = input('Digite o email do vendedor: ')
        vendedor = vendedorCollection.find_one({'email': vendedor})
        if vendedor == None:
            print('Vendedor não encontrado')
            return
        else:
            vendedorInfos = {
                'IdVendedor': vendedor['_id'],
                'emailVendedor': vendedor['email'],
                'NomeVendedor': vendedor['nome']
            }
        
        produto = Produtos.Produtos(nome, preco, estoque, vendedorInfos)
        vendedorCollection.update_one({'email': vendedor['email']}, {'$push': {'produtos': produto.__dict__}})
        collection.insert_one(produto.__dict__)

    def listarTodosProdutos(self):
        return collection.find()
    
    def listarProduto(self, nome):
        if collection.find_one({'nome': nome}) is None:
            print('Produto não encontrado')
            return
        return collection.find_one({'nome': nome})
    
    def atualizarProduto(self):
        nome = input('Digite o nome do produto: ')
        produto = collection.find_one({'nome': nome})
        if produto is None:
            print('Produto não encontrado')
            return
        novoNome = input('Digite o novo nome do produto: ')
        if collection.find_one({'nome': novoNome}) is not None:
            print('Produto já cadastrado')
            return
        novoPreco = input('Digite o novo preço do produto: ')
        novoEstoque = input('Digite o novo estoque do produto: ')

        vendedor = produto['vendedor']
        vendedorCollection.update_one(
            {'_id': vendedor['_id'], 'produtos.nome': nome},
            {'$set': {
            'produtos.$.nome': novoNome,
            'produtos.$.preco': novoPreco,
            'produtos.$.estoque': novoEstoque
            }}
        )
        collection.update_one({'nome': nome}, {'$set': {'nome': novoNome, 'preco': novoPreco, 'estoque': novoEstoque}})

    def deletarProduto(self):
        nome = input('Digite o nome do produto: ')
        if collection.find_one({'nome': nome}) is None:
            print('Produto não encontrado')
            return
        collection.delete_one({'nome': nome})