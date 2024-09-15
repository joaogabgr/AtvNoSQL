import connectMongo
from controllers import VendedorControllers, ClienteControllers
from models import Produtos

selectDatabase = connectMongo.client['MercadoLivre']
collection = selectDatabase['produto']
vendedorCollection = selectDatabase['vendedor']
clienteCollection = selectDatabase['cliente']

class ProdutosController:
    def criarProduto(self):
        nome = input('Digite o nome do produto: ')
        preco = input('Digite o preço do produto: ')
        estoque = input('Digite o estoque do produto: ')
        vendedores = list(VendedorControllers.VendedorControllers().ListarTodosVendedores())
        for index, vendedor in enumerate(vendedores):
            print(f'{index} - Nome: {vendedor["nome"]} - Email: {vendedor["email"]} - Idade: {vendedor["idade"]}')
        index = int(input('Digite o índice do vendedor: '))
        if index >= len(vendedores):
            print('Vendedor não encontrado')
            return
        emailVendedor = vendedores[index]['email']
        infosVendedor = {
            'idVendedor': vendedores[index]['_id'],
            'nomeVendedor': vendedores[index]['nome'],
            'emailVendedor': emailVendedor
        }
        produto = Produtos.Produtos(nome, preco, estoque, infosVendedor)
        collection.insert_one(produto.__dict__)
        vendedorCollection.update_one(
            {'_id': infosVendedor['idVendedor']},
            {'$push': {'produtos': {'nome': nome, 'preco': preco, 'estoque': estoque}}}
        )

    def listarTodosProdutos(self):
        return collection.find()
    
    def atualizarProduto(self):
        produtos = list(self.listarTodosProdutos())
        
        for index, produto in enumerate(produtos):
            print(f'{index} - Nome: {produto["nome"]} - Preço: {produto["preco"]} - Estoque: {produto["estoque"]}')
        
        index = int(input('Digite o índice do produto que deseja atualizar: '))
        if index >= len(produtos):
            print('Produto não encontrado')
            return
        nome = produtos[index]['nome']
        idProduto = produtos[index]['_id']
        novoNome = input('Digite o novo nome do produto: ')
        preco = input('Digite o novo preço do produto: ')
        estoque = input('Digite o novo estoque do produto: ')

        collection.update_one(
            {'nome': nome}, 
            {'$set': {'nome': novoNome, 'preco': preco, 'estoque': estoque}}
        )

        vendedorCollection.update_one(
            {'email': produtos[index]['vendedor']['emailVendedor']},
            {'$set': {'produtos.$[element].nome': novoNome,'produtos.$[element].preco': preco, 'produtos.$[element].estoque': estoque}},
            array_filters=[{'element.nome': nome}]
        )
        ClienteControllers.ClienteControllers().atualizarFavorito(idProduto, novoNome, preco)

        print(f'Produto {nome} atualizado com sucesso!')



    def deletarProduto(self):
        produtos = list(self.listarTodosProdutos())
        
        # Exibe a lista de produtos
        for index, produto in enumerate(produtos):
            print(f'{index} - Nome: {produto["nome"]} - Preço: {produto["preco"]} - Estoque: {produto["estoque"]}')
        
        # Solicita o índice do produto a ser deletado
        index = int(input('Digite o índice do produto que deseja deletar: '))
        if index >= len(produtos):
            print('Produto não encontrado')
            return

        # Coleta os dados do produto a ser deletado
        nome = produtos[index]['nome']
        idProduto = produtos[index]['_id']

        # Remove o produto da coleção principal
        collection.delete_one({'nome': nome})

        vendedorCollection.update_one(
            {'_id': produtos[index]['vendedor']['idVendedor']},
            {'$pull': {'produtos': {'nome': nome}}}  # Remove o produto baseado no nome
        )

        clienteCollection.update_many(
            {'favoritos.idProduto': idProduto},
            {'$pull': {'favoritos': {'idProduto': idProduto}}}  # Remove o favorito com o idProduto correspondente
        )

        print(f'Produto {nome} deletado com sucesso!')
