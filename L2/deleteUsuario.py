import connectMongo
import listarTodosUsuarios

def deleteUsuario():
    selectDatabase = connectMongo.client['MercadoLivre']
    collection = selectDatabase['usuario']
    listarTodosUsuarios.listarTodosUsuarios()
    print('Digite o email do usuario que deseja deletar')
    email = input()
    collection.delete_one({'email': email})
    print('Usuario deletado com sucesso')