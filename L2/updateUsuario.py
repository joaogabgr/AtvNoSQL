import connectMongo
import listarTodosUsuarios
import verifyEmail

def updateUsuario():
    selectDatabase = connectMongo.client['MercadoLivre']
    collection = selectDatabase['usuario']
    listarTodosUsuarios.listarTodosUsuarios()
    print('Digite o email do usuario que deseja atualizar')
    email = input()

    print('Digite o novo nome')
    nome = input()
    print('Digite a nova senha')
    senha = input()
    print('Digite a nova idade')
    idade = int(input())
    print('Deseja adicionar um endereco? (s/n)')
    opcao = input()
    if (opcao == 's'):
        print('Digite o nome da rua')
        rua = input()
        print('Digite o numero da casa')
        numero = int(input())
        print('Digite o complemento')
        complemento = input()
        print('Digite o bairro')
        bairro = input()
        print('Digite a cidade')
        cidade = input()
        print('Digite o estado')
        estado = input()
        print('Digite o pais')
        pais = input()
        endereco = {
            'rua': rua,
            'numero': numero,
            'complemento': complemento,
            'bairro': bairro,
            'cidade': cidade,
            'estado': estado,
            'pais': pais
        }
    else:
        endereco = {}
    
    new_user = {
        'nome': nome,
        'senha': senha,
        'idade': idade,
        'endereco': endereco
    }

    collection.update_one({'email': email}, {'$set': new_user})
    print('Usuario atualizado com sucesso')