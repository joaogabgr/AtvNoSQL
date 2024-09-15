import sys
import os

# Adiciona o diretório anterior ao caminho de importação
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers import ProdutosController

class MenuProdutos:
    def exibir(self):
        while True:
            print('1 - Criar Produto')
            print('2 - Listar todos os Produtos')
            print('3 - Atualizar Produto')
            print('4 - Deletar Produto')
            print('0 - Voltar')
            opcao = input('Digite a opção desejada: ')
            match opcao:
                case '1':
                    produtoController = ProdutosController.ProdutosController()
                    produtoController.criarProduto()
                case '2':
                    produtoController = ProdutosController.ProdutosController()
                    produtos = produtoController.listarTodosProdutos()
                    for index, produto in enumerate(produtos):
                        print(f'{index} - Nome: {produto['nome']} - Preço: {produto['preco']} - Estoque: {produto['estoque']}')
                case '3':
                    produtoController = ProdutosController.ProdutosController()
                    produtoController.atualizarProduto()
                case '4':
                    produtoController = ProdutosController.ProdutosController()
                    produtoController.deletarProduto()
                case '0':
                    break
                case _:
                    print('Opção inválida')