import connectMongo
from controllers import ProdutosController, ClienteControllers, VendedorControllers
import datetime

selectDatabase = connectMongo.client['MercadoLivre']
Vendedorcollection = selectDatabase['vendedor']
ProdutoCollection = selectDatabase['produto']
ClienteCollection = selectDatabase['cliente']

class VendasControllers:
    def CriarVenda(self):
        clientes = list(ClienteControllers.ClienteControllers().listarTodosClientes())
        for index, cliente in enumerate(clientes):
            print(f'{index} - Nome: {cliente["nome"]} - Email: {cliente["email"]} - Idade: {cliente["idade"]}')
        
        index = int(input('Digite o índice do cliente que deseja comprar: '))
        if index >= len(clientes):
            print('Cliente não encontrado')
            return
        emailCliente = clientes[index]['email']

        produtos = list(ProdutosController.ProdutosController().listarTodosProdutos())
        for index, produto in enumerate(produtos):
            print(f'{index} - Nome: {produto["nome"]} - Preço: {produto["preco"]} - Estoque: {produto["estoque"]}')
        
        index = int(input('Digite o índice do produto que deseja comprar: '))
        produto = produtos[index]
        nomeProduto = produto['nome']
        
        quantidade = int(input('Digite a quantidade: '))
        if int(produto['estoque']) - quantidade < 0:
            print('Estoque insuficiente')
            return

        valorTotal = quantidade * float(produto['preco'])
        idVenda = Vendedorcollection.count_documents({}) + 1

        ProdutoCollection.update_one({'nome': nomeProduto}, {'$set': {'estoque': int(produto['estoque']) - quantidade}})
        
        vendas = {
            'idVenda': idVenda,
            'dataVenda': datetime.datetime.now(),
            'valorVenda': valorTotal,
            'produtosVendidos': {
                'idProduto': produto['_id'],
                'nomeProduto': produto['nome'],
                'valorProduto': produto['preco']
            }
        }

        VendedorControllers.VendedorControllers().adicionarVenda(produto['vendedor']['emailVendedor'], vendas)
        
        compras = {
            'idCompra': idVenda,
            'dataCompra': datetime.datetime.now(),
            'valorCompra': valorTotal,
            'produtos': {
                'idProduto': produto['_id'],
                'nomeProduto': produto['nome'],
                'valorProduto': produto['preco']
            }
        }

        ClienteControllers.ClienteControllers().adicionarCompra(emailCliente, compras)
