import connectMongo

def criarUsuario():

    selectDatabase = connectMongo.client['MercadoLivre']
    collection = selectDatabase['usuario']

    print('Digite o nome do usuario')
    nome = input()
    print('Digite o email do usuario')
    email = input()
    print('Digite a senha do usuario')
    senha = input()
    print('Digite a idade do usuario')
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
        'email': email,
        'senha': senha,
        'idade': idade,
        'endereco': endereco
    }

    collection.insert_one(new_user)