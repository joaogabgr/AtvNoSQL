import connectMongo
from models import Cliente

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
        if collection.find_one({'email': email}) is None:
            print('Cliente não encontrado')
            return
        return collection.find_one({'email': email})
    
    def atualizarCliente(self):
        email = input('Digite o email do cliente: ')
        if collection.find_one({'email': email}) is None:
            print('Cliente não encontrado')
            return
        nome = input('Digite o novo nome do cliente: ')
        idade = input('Digite a nova idade do cliente: ')
        novoEmail = input('Digite o novo email do cliente: ')
        if collection.find_one({'email': novoEmail}) is not None:
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
        email = input('Digite o email do cliente: ')
        if collection.find_one({'email': email}) is None:
            print('Cliente não encontrado')
            return
        collection.delete_one({'email': email})

    def adicionarCompra(self, email, compra):
        collection.update_one({'email': email}, {'$push': {'compras': compra}})
        return 

