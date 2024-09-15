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
    
    def ListarVendedor(self, email):
        vendedor = collection.find_one({'email': email})
        if vendedor is None:
            print('Vendedor não encontrado')
            return
        return f'Nome: {vendedor['nome']} - Email: {vendedor['email']} - Idade: {vendedor['idade']}'
    
    def AtualizarVendedor(self):
        vendedores = list(self.ListarTodosVendedores())
        for index, vendedor in enumerate(vendedores):
            print(f'{index} - Nome: {vendedor["nome"]} - Email: {vendedor["email"]} - Idade: {vendedor["idade"]}')
        
        index = int(input('Digite o índice do vendedor que deseja atualizar: '))
        if index >= len(vendedores):
            print('Vendedor não encontrado')
            return
        vendedor = vendedores[index]
        email = vendedor['email']
        nome = vendedor['nome']

        novoNome = input('Digite o novo nome do vendedor: ')

        if nome == novoNome:
            print()
        elif collection.find_one({'nome': nome}) is not None:
            print('Vendedor já cadastrado')
            return

        idade = input('Digite a nova idade do vendedor: ')
        novoEmail = input('Digite o novo email do vendedor: ')
        if novoEmail == email:
            print
        elif collection.find_one({'email': novoEmail}) is not None:
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
        collection.update_one({'email': email}, {'$set': {'nome': novoNome, 'idade': idade, 'email': novoEmail, 'endereco': endereco}})

    def DeletarVendedor(self):
        vendedores = list(self.ListarTodosVendedores())
        for index, vendedor in enumerate(vendedores):
            print(f'{index} - Nome: {vendedor["nome"]} - Email: {vendedor["email"]} - Idade: {vendedor["idade"]}')
        
        index = int(input('Digite o índice do vendedor que deseja deletar: '))
        if index >= len(vendedores):
            print('Vendedor não encontrado')
            return
        email = vendedores[index]['email']
        ProdutoCollection.delete_many({'vendedor.emailVendedor': email})
        collection.delete_one({'email': email})

    def adicionarVenda(self, email, venda):
        collection.update_one({'email': email}, {'$push': {'vendas': venda}})
        return