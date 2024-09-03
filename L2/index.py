import connectMongo
import listarTodosUsuarios
import criarUsuario

connectMongo.client.admin

while True:
    print('1. Criar novo usuario')
    print('2. Delete usuario')
    print('3. Editar usuario')
    print('4. Listar todos os usuarios')
    print('5. Listar um usuario')
    print('6. Sair')
    opcao = int(input('Digite a opcao desejada: '))
    if (opcao == 4):
        listarTodosUsuarios.listarTodosUsuarios()
    elif (opcao == 1):
        criarUsuario.criarUsuario()
    elif (opcao == 6):
        print('Saindo...')
        break
    else:
        print('Opcao invalida')
        continue
