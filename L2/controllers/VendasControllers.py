import connectMongo
from controllers import ProdutosController, ClienteControllers, VendedorControllers
import datetime

selectDatabase = connectMongo.client['MercadoLivre']
Vendedorcollection = selectDatabase['vendedor']
ProdutoCollection = selectDatabase['produto']
ClienteCollection = selectDatabase['cliente']

class VendasControllers:
    def CriarVenda(self):
        for clientes in ClienteControllers.ClienteControllers().listarTodosClientes():
            print(f"Nome: {clientes['nome']} - Email: {clientes['email']}")
        emailCliente = input('Digite o email do cliente: ')
        
        if ClienteControllers.ClienteControllers().listarCliente(emailCliente) == None:
            return
        
        for produtos in ProdutosController.ProdutosController().listarTodosProdutos():
            print(f"Nome: {produtos['nome']} - Valor: {produtos['preco']} - Estoque: {produtos['estoque']}")

        nomeProduto = input('Digite o nome do produto: ')
        produto = ProdutosController.ProdutosController().listarProduto(nomeProduto)
        if produto == None:
            return
        
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
