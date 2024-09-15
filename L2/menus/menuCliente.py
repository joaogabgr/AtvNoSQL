import sys
import os

# Adiciona o diretório anterior ao caminho de importação
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Agora você pode importar o arquivo da pasta anterior
from controllers import ClienteControllers

class MenuCliente:
    def exibir(self):
        while True:
            print('1 - Criar Cliente')
            print('2 - Listar todos os Clientes')
            print('3 - Listar Cliente')
            print('4 - Atualizar Cliente')
            print('5 - Deletar Cliente')
            print('6 - Adicionar Favorito')
            print('0 - Sair')
            opcao = input('Digite a opção desejada: ')
            
            match opcao:
                case '1':
                    clienteController = ClienteControllers.ClienteControllers()
                    clienteController.criarCliente()
                case '2':
                    clienteController = ClienteControllers.ClienteControllers()
                    clientes = clienteController.listarTodosClientes()
                    for index, cliente in enumerate(clientes):
                        print(f'{index} - Nome: {cliente['nome']} - Email: {cliente['email']} - Idade: {cliente['idade']}')
                case '3':
                    clienteController = ClienteControllers.ClienteControllers()
                    email = input('Digite o email do cliente: ')
                    print(clienteController.listarCliente(email))
                case '4':
                    clienteController = ClienteControllers.ClienteControllers()
                    clienteController.atualizarCliente()
                case '5':
                    clienteController = ClienteControllers.ClienteControllers()
                    clienteController.deletarCliente()
                case '6':
                    clienteController = ClienteControllers.ClienteControllers()
                    clienteController.adicionarFavorito()
                case '0':
                    break
                case _:
                    print('Opção inválida')
