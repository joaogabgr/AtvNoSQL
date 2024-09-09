import connectMongo
from controllers import ProdutosController, ClienteControllers, VendedorControllers
import datetime

selectDatabase = connectMongo.client['MercadoLivre']
Vendedorcollection = selectDatabase['vendedor']
ProdutoCollection = selectDatabase['produto']
ClienteCollection = selectDatabase['cliente']

class VendasControllers:
    def CriarVenda(self):
        ClienteControllers.ClienteControllers().listarTodosClientes()
        emailCliente = input('Digite o email do cliente: ')
        
        if ClienteControllers.ClienteControllers().listarCliente(emailCliente) == None:
            return
        
        ProdutosController.ProdutosController().listarTodosProdutos()

        nomeProduto = input('Digite o nome do produto: ')
        produtoTeste = ProdutosController.ProdutosController().listarProduto(nomeProduto)
        if produtoTeste == None:
            return
        else:
            produto = ProdutoCollection.find_one({'nome': nomeProduto})
        
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
