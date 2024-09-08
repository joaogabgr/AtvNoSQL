import connectMongo
from models import Vendedor

selectDatabase = connectMongo.client['MercadoLivre']
collection = selectDatabase['vendedor']
ProdutoCollection = selectDatabase['produto']

class VendedorControllers:
    def CriarVendedor(self):
        nome = input('Digite o nome do vendedor: ')
        idade = input('Digite a idade do vendedor: ')
        email = input('Digite o email do vendedor: ')
        if collection.find_one({'email': email}) is not None:
            print('Email já cadastrado')
            return
        
        pais = input('Digite o país do vendedor: ')
        estado = input('Digite o estado do vendedor: ')
        cidade = input('Digite a cidade do vendedor: ')
        bairro = input('Digite o bairro do vendedor: ')
        rua = input('Digite a rua do vendedor: ')
        numero = input('Digite o número do vendedor: ')
        complemento = input('Digite o complemento do vendedor: ')
        endereco = {
            'pais': pais,
            'estado': estado,
            'cidade': cidade,
            'bairro': bairro,
            'rua': rua,
            'numero': numero,
            'complemento': complemento
        }

        vendedor = Vendedor.Vendedor(nome, idade, email)
        vendedor.Endereco = endereco
        
        collection.insert_one(vendedor.__dict__)
        return vendedor
    
    def ListarTodosVendedores(self):
        return collection.find()
    
    def ListarVendedor(self):
        email = input('Digite o email do vendedor: ')
        if collection.find_one({'email': email}) is None:
            print('Vendedor não encontrado')
            return
        return collection.find_one({'email': email})
    
    def AtualizarVendedor(self):
        email = input('Digite o email do vendedor: ')
        if collection.find_one({'email': email}) is None:
            print('Vendedor não encontrado')
            return
        
        nome = input('Digite o novo nome do vendedor: ')
        idade = input('Digite a nova idade do vendedor: ')
        novoEmail = input('Digite o novo email do vendedor: ')
        if collection.find_one({'email': novoEmail}) is not None:
            print('Email já cadastrado')
            return
        
        pais = input('Digite o novo país do vendedor: ')
        estado = input('Digite o novo estado do vendedor: ')
        cidade = input('Digite a nova cidade do vendedor: ')
        bairro = input('Digite o novo bairro do vendedor: ')
        rua = input('Digite a nova rua do vendedor: ')
        numero = input('Digite o novo número do vendedor: ')
        complemento = input('Digite o novo complemento do vendedor: ')
        endereco = {
            'pais': pais,
            'estado': estado,
            'cidade': cidade,
            'bairro': bairro,
            'rua': rua,
            'numero': numero,
            'complemento': complemento
        }

        ProdutoCollection.update_many({'vendedor.emailVendedor': email}, {'$set': {'vendedor.emailVendedor': novoEmail}})
        collection.update_one({'email': email}, {'$set': {'nome': nome, 'idade': idade, 'email': novoEmail, 'endereco': endereco}})

    def DeletarVendedor(self):
        email = input('Digite o email do vendedor: ')
        if collection.find_one({'email': email}) is None:
            print('Vendedor não encontrado')
            return
        
        collection.delete_one({'email': email})

    def adicionarVenda(self, email, venda):
        collection.update_one({'email': email}, {'$push': {'vendas': venda}})
        return