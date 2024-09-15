import connectMongo
from models import Cliente
from controllers import ProdutosController

selectDatabase = connectMongo.client['MercadoLivre']
collection = selectDatabase['usuario']

class ClienteControllers:
    def criarCliente(self):
        nome = input('Digite o nome do cliente: ')
        idade = input('Digite a idade do cliente: ')
        email = input('Digite o email do cliente: ')
        if collection.find_one({'email': email}) is not None:
            print('Email já cadastrado')
            return
        pais = input('Digite o país do cliente: ')
        estado = input('Digite o estado do cliente: ')
        cidade = input('Digite a cidade do cliente: ')
        bairro = input('Digite o bairro do cliente: ')
        rua = input('Digite a rua do cliente: ')
        numero = input('Digite o número do cliente: ')
        complemento = input('Digite o complemento do cliente: ')
        endereco = {
            'pais': pais,
            'estado': estado,
            'cidade': cidade,
            'bairro': bairro,
            'rua': rua,
            'numero': numero,
            'complemento': complemento
        }

        cliente = Cliente.Cliente(nome, email, idade)
        cliente.Endereco = endereco
        collection.insert_one(cliente.__dict__)

    def listarTodosClientes(self):
        return collection.find()
    
    def listarCliente(self, email):
        cliente = collection.find_one({'email': email})
        if cliente is None:
            print('Cliente não encontrado')
            return
        return f'Nome: {cliente['nome']} - Email: {cliente['email']} - Idade: {cliente['idade']}'
    
    def atualizarCliente(self):
        clientes = list(self.listarTodosClientes())
        for index, cliente in enumerate(clientes):
            print(f'{index} - Nome: {cliente["nome"]} - Email: {cliente["email"]} - Idade: {cliente["idade"]}')
        
        index = int(input('Digite o índice do cliente que deseja deletar: '))
        if index >= len(clientes):
            print('Cliente não encontrado')
            return
        email = clientes[index]['email']
        nome = input('Digite o novo nome do cliente: ')
        idade = input('Digite a nova idade do cliente: ')
        novoEmail = input('Digite o novo email do cliente: ')
        if novoEmail == email:
            print()
        elif collection.find_one({'email': novoEmail}) is not None:
            print('Email já cadastrado')
            return
        pais = input('Digite o novo país do cliente: ')
        estado = input('Digite o novo estado do cliente: ')
        cidade = input('Digite a nova cidade do cliente: ')
        bairro = input('Digite o novo bairro do cliente: ')
        rua = input('Digite a nova rua do cliente: ')
        numero = input('Digite o novo número do cliente: ')
        complemento = input('Digite o novo complemento do cliente: ')
        endereco = {
            'pais': pais,
            'estado': estado,
            'cidade': cidade,
            'bairro': bairro,
            'rua': rua,
            'numero': numero,
            'complemento': complemento
        }
        Cliente = {'nome': nome, 'idade': idade, 'email': novoEmail}
        Cliente['Endereco'] = endereco
        collection.update_one({'email': email}, {'$set': Cliente})

    def deletarCliente(self):
        clientes = list(self.listarTodosClientes())
        for index, cliente in enumerate(clientes):
            print(f'{index} - Nome: {cliente["nome"]} - Email: {cliente["email"]} - Idade: {cliente["idade"]}')
        
        index = int(input('Digite o índice do cliente que deseja deletar: '))
        if index >= len(clientes):
            print('Cliente não encontrado')
            return
        email = clientes[index]['email']
        if collection.find_one({'email': email}) is None:
            print('Cliente não encontrado')
            return
        collection.delete_one({'email': email})

    def adicionarFavorito(self):
        clientes = list(self.listarTodosClientes())
        for index, cliente in enumerate(clientes):
            print(f'{index} - Nome: {cliente["nome"]} - Email: {cliente["email"]} - Idade: {cliente["idade"]}')
        
        index = int(input('Digite o índice do cliente que deseja adicionar o favorito: '))
        if index >= len(clientes):
            print('Cliente não encontrado')
            return
        email = clientes[index]['email']
        produtos = list(ProdutosController.ProdutosController().listarTodosProdutos())
        for index, produto in enumerate(produtos):
            print(f'{index} - Nome: {produto["nome"]} - Preço: {produto["preco"]} - Estoque: {produto["estoque"]}')
        
        index = int(input('Digite o índice do produto que deseja adicionar aos favoritos: '))
        if index >= len(produtos):
            print('Produto não encontrado')
            return
        produto = produtos[index]
        favorito = {
            'idProduto': produto['_id'],
            'nomeProduto': produto['nome'],
            'valorProduto': produto['preco']
        }
        collection.update_one({'email': email}, {'$push': {'favoritos': favorito}})
    

    def atualizarFavorito(self, idProduto, novoNome, preco):
        collection.update_many(
            {'favoritos.idProduto': idProduto},  # Filtro para encontrar o produto pelo idProduto
            {'$set': {
                'favoritos.$[element].nomeProduto': novoNome,
                'favoritos.$[element].valorProduto': preco
            }},
            array_filters=[{'element.idProduto': idProduto}]  # Usar idProduto como filtro
        )

    def adicionarCompra(self, email, compra):
        collection.update_one({'email': email}, {'$push': {'compras': compra}})
        return 

