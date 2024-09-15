import sys
import os

# Adiciona o diretório anterior ao caminho de importação
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers import VendedorControllers

class MenuVendedor:
    def exibir(self):
        while True:
            print('1 - Criar Vendedor')
            print('2 - Listar todos os Vendedores')
            print('3 - Listar Vendedor')
            print('4 - Atualizar Vendedor')
            print('5 - Deletar Vendedor')
            print('0 - Voltar')
            opcao = input('Digite a opção desejada: ')
            match opcao:
                case '1':
                    vendedorController = VendedorControllers.VendedorControllers()
                    vendedorController.CriarVendedor()
                case '2':
                    vendedorController = VendedorControllers.VendedorControllers()
                    vendedores = vendedorController.ListarTodosVendedores()
                    for index, vendedor in enumerate(vendedores):
                        print(f'{index} - Nome: {vendedor['nome']} - Email: {vendedor['email']} - Idade: {vendedor['idade']}')
                case '3':
                    vendedorController = VendedorControllers.VendedorControllers()
                    email = input('Digite o email do vendedor: ')
                    print(vendedorController.ListarVendedor(email))
                case '4':
                    vendedorController = VendedorControllers.VendedorControllers()
                    vendedorController.AtualizarVendedor()
                case '5':
                    vendedorController = VendedorControllers.VendedorControllers()
                    vendedorController.DeletarVendedor()
                case '0':
                    break
                case _:
                    print('Opção inválida')