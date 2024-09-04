import connectMongo
import listarTodosUsuarios

def listarUsuario():
    selectDatabase = connectMongo.client['MercadoLivre']
    collection = selectDatabase['usuario']
    listarTodosUsuarios.listarTodosUsuarios()
    print('Digite o email do usuário que deseja visualizar')
    email = input()
    usuario = collection.find_one({'email': email})
    print('Nome:', usuario['nome'])
    print('Email:', usuario['email'])
    print('Idade:', usuario['idade'])
    print('Endereço:')
    print('Pais:', usuario['endereco']['pais'])
    print('Estado:', usuario['endereco']['estado'])
    print('Cidade:', usuario['endereco']['cidade'])
    print('Rua:', usuario['endereco']['rua'])
    print('Numero:', usuario['endereco']['numero'])