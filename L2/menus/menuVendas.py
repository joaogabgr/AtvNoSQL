import sys
import os

# Adiciona o diretório anterior ao caminho de importação
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers import VendasControllers

class MenuVendas:
    def exibir(self):
        while True:
            print('1 - Criar Venda')
            print('0 - Voltar')
            opcao = input('Digite a opção desejada: ')
            match opcao:
                case '1':
                    vendaController = VendasControllers.VendasControllers()
                    vendaController.CriarVenda()
                case '0':
                    break
                case _:
                    print('Opção inválida')