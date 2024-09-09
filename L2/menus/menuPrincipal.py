from sys import exit
from menus import menuCliente, menuProdutos, menuVendedor, menuVendas

class MenuPrincipal:
    def exibir(self):
        while True:
            print('1 - Menu Cliente')
            print('2 - Menu Produtos')
            print('3 - Menu Vendedor')
            print('4 - Menu Vendas')
            print('0 - Sair')
            opcao = input('Digite a opção desejada: ')
            match opcao:
                case '1':
                    menuCliente.MenuCliente().exibir()
                case '2':
                    menuProdutos.MenuProdutos().exibir()
                case '3':
                    menuVendedor.MenuVendedor().exibir()
                case '4':
                    menuVendas.MenuVendas().exibir()
                case '0':
                    exit()
                case _:
                    print('Opção inválida')

MenuPrincipal().exibir()