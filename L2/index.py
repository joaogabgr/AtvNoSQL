import connectMongo
import listarTodosUsuarios
import criarUsuario
import deleteUsuario
import updateUsuario
import listarUsuario

connectMongo.client.admin

while True:
    print('1. Criar novo usuario')
    print('2. Delete usuario')
    print('3. Editar usuario')
    print('4. Listar todos os usuarios')
    print('5. Listar um usuario')
    print('6. Sair')
    opcao = int(input('Digite a opcao desejada: '))
    match opcao:
        case 1:
            criarUsuario.criarUsuario()
        case 2:
            deleteUsuario.deleteUsuario()
        case 3:
            updateUsuario.updateUsuario()
        case 4:
            listarTodosUsuarios.listarTodosUsuarios()
        case 5:
            listarUsuario.listarUsuario()
        case 6:
            break
