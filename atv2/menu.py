from controllers.clienteController import ClienteController
from controllers.vendedorController import VendedorController
from controllers.produtosController import ProdutoController

def exibir_menu_principal():
    print("\n--- MENU PRINCIPAL ---")
    print("1. Gerenciar Clientes")
    print("2. Gerenciar Vendedores")
    print("3. Gerenciar Produtos")
    print("4. Gerenciar Compras")
    print("5. Gerenciar Favoritos")
    print("0. Sair")

def exibir_menu_cliente():
    print("\n--- MENU CLIENTE ---")
    print("1. Listar clientes")
    print("2. Buscar cliente")
    print("3. Inserir cliente")
    print("4. Atualizar cliente")
    print("5. Deletar cliente")
    print("6. Avaliar produto")
    print("0. Voltar ao menu principal")

def exibir_menu_compra():
    print("\n--- MENU COMPRA ---")
    print("1. Listar compras do cliente")
    print("2. Adicionar compra ao cliente")
    print("0. Voltar ao menu principal")

def exibir_menu_vendedor():
    print("\n--- MENU VENDEDOR ---")
    print("1. Listar vendedores")
    print("2. Buscar vendedor")
    print("3. Inserir vendedor")
    print("4. Atualizar vendedor")
    print("5. Deletar vendedor")
    print("0. Voltar ao menu principal")

def exibir_menu_produto():
    print("\n--- MENU PRODUTO ---")
    print("1. Listar produtos")
    print("2. Buscar produto")
    print("3. Inserir produto")
    print("4. Atualizar produto")
    print("5. Deletar produto")
    print("0. Voltar ao menu principal")

def exibir_menu_favorito():
    print("\n--- MENU FAVORITO ---")
    print("1. Listar produtos favoritos do cliente")
    print("2. Adicionar produto aos favoritos")
    print("3. Remover produto dos favoritos")
    print("0. Voltar ao menu principal")

def executar_opcao_cliente(opcao, controller):
    if opcao == "1":
        listar_clientes(controller)
    elif opcao == "2":
        buscar_cliente(controller)
    elif opcao == "3":
        inserir_cliente(controller)
    elif opcao == "4":
        atualizar_cliente(controller)
    elif opcao == "5":
        deletar_cliente(controller)
    elif opcao == "6":
        avaliar_produto(controller)
    elif opcao == "0":
        return False
    else:
        print("Opção inválida. Tente novamente.")
    return True

def listar_clientes(controller):
    clientes = controller.listar_clientes()
    print("\n--- Lista de Clientes ---")
    for cliente in clientes:
        print(f"Nome: {cliente['nome']} | CPF: {cliente['cpf']} | Email: {cliente['email']}")

def buscar_cliente(controller):
    cliente = controller.selecionar_cliente()
    cliente = controller.buscar_cliente(cliente["cpf"]) if cliente else None
    if cliente:
        print("\n--- Dados do Cliente ---")
        print(f"ID: {cliente['_id']}")
        print(f"Nome: {cliente['nome']}")
        print(f"Idade: {cliente['idade']}")
        print(f"CPF: {cliente['cpf']}")
        print(f"Email: {cliente['email']}")
        print("Endereço:")
        print(f"  Rua: {cliente['endereco']['rua']}, {cliente['endereco']['numero']}")
        print(f"  Bairro: {cliente['endereco']['bairro']}")
        print(f"  Cidade: {cliente['endereco']['cidade']} - Estado: {cliente['endereco']['estado']}")
        print("\n--- Compras do Cliente ---")
        produto_controller = ProdutoController()
        for compra in cliente['compras']:
            produto = produto_controller.buscar_produto_id(compra['produto_id'])
            print(f"Produto: {produto['nome']} | Quantidade: {compra['quantidade']} | Valor Total: {compra['valor_total']}")
    else:
        print("Cliente não encontrado.")

def inserir_cliente(controller):
    resultado = controller.inserir_cliente()
    print("Cliente inserido com sucesso!" if resultado else "Erro ao inserir cliente.")

def atualizar_cliente(controller):
    resultado = controller.atualizar_cliente()
    print("Cliente atualizado com sucesso!" if resultado.modified_count > 0 else "Erro ao atualizar cliente.")

def deletar_cliente(controller):
    resultado = controller.deletar_cliente()
    print("Cliente deletado com sucesso!" if resultado.deleted_count > 0 else "Cliente não encontrado.")

def avaliar_produto(controller):
    resultado = controller.avaliar_produto()
    print(resultado)

def executar_opcao_compra(opcao, controller):
    if opcao == "1":
        listar_compras(controller)
    elif opcao == "2":
        adicionar_compra(controller)
    elif opcao == "0":
        return False
    else:
        print("Opção inválida. Tente novamente.")
    return True

def listar_compras(controller):
    compras = controller.listar_compras()
    print("\n--- Compras do Cliente ---")
    for compra in compras:
        print(f"Produto ID: {compra['produto_nome']} | Quantidade: {compra['quantidade']} | Valor Total: {compra['valor_total']}")

def adicionar_compra(controller):
    resultado = controller.adicionar_compra()
    print(resultado)

def executar_opcao_vendedor(opcao, controller):
    if opcao == "1":
        listar_vendedores(controller)
    elif opcao == "2":
        buscar_vendedor(controller)
    elif opcao == "3":
        inserir_vendedor(controller)
    elif opcao == "4":
        atualizar_vendedor(controller)
    elif opcao == "5":
        deletar_vendedor(controller)
    elif opcao == "0":
        return False
    else:
        print("Opção inválida. Tente novamente.")
    return True

def listar_vendedores(controller):
    vendedores = controller.listar_vendedores()
    print("\n--- Lista de Vendedores ---")
    for vendedor in vendedores:
        print(f"Nome: {vendedor['nome']} | CPF: {vendedor['cpf']} | Email: {vendedor['email']}")

def buscar_vendedor(controller):
    vendedor = controller.selecionar_vendedor()
    vendedor = controller.buscar_vendedor(vendedor["cpf"]) if vendedor else None
    if vendedor:
        print("\n--- Dados do Vendedor ---")
        print(f"ID: {vendedor['_id']}")
        print(f"Nome: {vendedor['nome']}")
        print(f"Idade: {vendedor['idade']}")
        print(f"CPF: {vendedor['cpf']}")
        print(f"Email: {vendedor['email']}")
        print("Endereço:")
        print(f"  Rua: {vendedor['endereco']['rua']}, {vendedor['endereco']['numero']}")
        print(f"  Bairro: {vendedor['endereco']['bairro']}")
        print(f"  Cidade: {vendedor['endereco']['cidade']} - Estado: {vendedor['endereco']['estado']}")
        print(f"Vendas: {vendedor['vendas']}")
        print(f"Produtos: {vendedor['produtos']}")
    else:
        print("Vendedor não selecionado.")

def inserir_vendedor(controller):
    resultado = controller.inserir_vendedor()
    print("Vendedor inserido com sucesso!" if resultado else "Erro ao inserir vendedor.")

def atualizar_vendedor(controller):
    vendedor = controller.selecionar_vendedor()
    if vendedor:
        resultado = controller.atualizar_vendedor(vendedor["cpf"])
        print("Vendedor atualizado com sucesso!" if resultado.modified_count > 0 else "Erro ao atualizar vendedor.")
    else:
        print("Vendedor não selecionado.")

def deletar_vendedor(controller):
    vendedor = controller.selecionar_vendedor()
    if vendedor:
        resultado = controller.deletar_vendedor(vendedor["cpf"])
        print("Vendedor deletado com sucesso!" if resultado.deleted_count > 0 else "Vendedor não encontrado.")
    else:
        print("Vendedor não selecionado.")

def executar_opcao_produto(opcao, controller):
    if opcao == "1":
        listar_produtos(controller)
    elif opcao == "2":
        buscar_produto(controller)
    elif opcao == "3":
        inserir_produto(controller)
    elif opcao == "4":
        atualizar_produto(controller)
    elif opcao == "5":
        deletar_produto(controller)
    elif opcao == "0":
        return False
    else:
        print("Opção inválida. Tente novamente.")
    return True

def listar_produtos(controller):
    produtos = controller.listar_produtos()
    print("\n--- Lista de Produtos ---")
    for produto in produtos:
        print(f"Nome: {produto['nome']} | Valor: {produto['valor']} | Quantidade: {produto['quantidade']}")

def buscar_produto(controller):
    produto = controller.buscar_produto()
    if produto:
        print("\n--- Dados do Produto ---")
        print(f"Nome: {produto['nome']}")
        print(f"Descrição: {produto['descricao']}")
        print(f"Valor: {produto['valor']}")
        print(f"Quantidade: {produto['quantidade']}")
        print(f"Vendedor ID: {produto['vendedor_id']}")
        print("\n--- Avaliações do Produto ---")
        cliente_controller = ClienteController()
        for avaliacao in produto['avaliacao']:
            cliente = cliente_controller.buscar_cliente_id(avaliacao['cliente_id'])
            print(f"Cliente: {cliente['nome']} | Nota: {avaliacao['avaliacao']}")
    else:
        print("Produto não encontrado.")

def inserir_produto(controller):
    resultado = controller.inserir_produto()
    print("Produto inserido com sucesso!" if resultado else "Erro ao inserir produto.")

def atualizar_produto(controller):
    resultado = controller.atualizar_produto()
    print("Produto atualizado com sucesso!" if resultado.modified_count > 0 else "Erro ao atualizar produto.")

def deletar_produto(controller):
    resultado = controller.deletar_produto()
    print("Produto deletado com sucesso!" if resultado.deleted_count > 0 else "Produto não encontrado.")

def executar_opcao_favorito(opcao, controller):
    if opcao == "1":
        listar_favoritos(controller)
    elif opcao == "2":
        adicionar_favorito(controller)
    elif opcao == "3":
        remover_favorito(controller)
    elif opcao == "0":
        return False
    else:
        print("Opção inválida. Tente novamente.")
    return True

def listar_favoritos(controller):
    favoritos = controller.listar_favoritos()
    print("\n--- Produtos Favoritos ---")
    print(favoritos)

def adicionar_favorito(controller):
    resultado = controller.adicionar_favorito()
    print(resultado)

def remover_favorito(controller):
    resultado = controller.remover_favorito()
    print(resultado)

def main():
    cliente_controller = ClienteController()
    vendedor_controller = VendedorController()
    produto_controller = ProdutoController()

    while True:
        exibir_menu_principal()
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            while True:
                exibir_menu_cliente()
                opcao_cliente = input("Escolha uma opção: ")
                if not executar_opcao_cliente(opcao_cliente, cliente_controller):
                    break
        elif opcao == "2":
            while True:
                exibir_menu_vendedor()
                opcao_vendedor = input("Escolha uma opção: ")
                if not executar_opcao_vendedor(opcao_vendedor, vendedor_controller):
                    break
        elif opcao == "3":
            while True:
                exibir_menu_produto()
                opcao_produto = input("Escolha uma opção: ")
                if not executar_opcao_produto(opcao_produto, produto_controller):
                    break
        elif opcao == "4":
            while True:
                exibir_menu_compra()
                opcao_compra = input("Escolha uma opção: ")
                if not executar_opcao_compra(opcao_compra, cliente_controller):
                    break
        elif opcao == "5":
            while True:
                exibir_menu_favorito()
                opcao_favorito = input("Escolha uma opção: ")
                if not executar_opcao_favorito(opcao_favorito, cliente_controller):
                    break
        elif opcao == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()