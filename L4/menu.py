from controllers.mercadoLivreDB import MercadoLivreDB

def exibir_menu(db):
    while True:
        print("\nMenu:")
        print("1. Adicionar Usuário")
        print("2. Adicionar Vendedor")
        print("3. Adicionar Produto")
        print("4. Adicionar Compra")
        print("5. Atualizar Usuário")
        print("6. Pesquisar Produto")
        print("7. Deletar Compra")
        print("8. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Digite o nome do usuário: ")
            while True:
                try:
                    idade = int(input("Digite a idade do usuário: "))
                    break
                except ValueError:
                    print("Erro: A idade deve ser um número inteiro válido. Tente novamente.")
            endereco = input("Digite o endereço do usuário: ")
            db.inserir_usuario(nome, idade, endereco)

        elif opcao == '2':
            nome = input("Digite o nome do vendedor: ")
            while True:
                try:
                    idade = int(input("Digite a idade do vendedor: "))
                    break
                except ValueError:
                    print("Erro: A idade deve ser um número inteiro válido. Tente novamente.")
            endereco = input("Digite o endereço do vendedor: ")
            db.inserir_vendedor(nome, idade, endereco)

        elif opcao == '3':
            nome = input("Digite o nome do produto: ")
            while True:
                try:
                    valor = float(input("Digite o preço do produto: "))
                    break
                except ValueError:
                    print("Erro: O preço deve ser um número válido. Tente novamente.")
            id_vendedor = selecionar_da_lista(db.obter_todos_vendedores(), "vendedor")
            db.inserir_produto(nome, valor, id_vendedor)

        elif opcao == '4':
            id_usuario = selecionar_da_lista(db.obter_todos_usuarios(), "usuário")
            id_produto = selecionar_da_lista(db.obter_todos_produtos(), "produto")
            while True:
                try:
                    quantidade = int(input("Digite a quantidade: "))
                    break
                except ValueError:
                    print("Erro: A quantidade deve ser um número inteiro válido. Tente novamente.")
            produto = db.obter_produto_por_id(id_produto)
            if produto:
                valor = produto['valor'] * quantidade
                db.inserir_compra(id_usuario, id_produto, quantidade, valor)
            else:
                print(f"Produto com ID {id_produto} não encontrado.")

        elif opcao == '5':
            id_usuario = selecionar_da_lista(db.obter_todos_usuarios(), "usuário")
            novo_nome = input("Digite o novo nome (deixe vazio para não alterar): ")
            nova_idade = input("Digite a nova idade (deixe vazio para não alterar): ")
            if nova_idade:
                while True:
                    try:
                        nova_idade = int(nova_idade)
                        break
                    except ValueError:
                        print("Erro: A idade deve ser um número inteiro válido. Tente novamente.")
                        nova_idade = input("Digite a nova idade (deixe vazio para não alterar): ")
            novo_endereco = input("Digite o novo endereço (deixe vazio para não alterar): ")
            db.atualizar_usuario(id_usuario, novo_nome if novo_nome else None, nova_idade if nova_idade else None, novo_endereco if novo_endereco else None)

        elif opcao == '6':
            id_produto = selecionar_da_lista(db.obter_todos_produtos(), "produto")
            db.buscar_produto(id_produto)

        elif opcao == '7':
            compras = db.obter_todas_compras()
            id_compra = selecionar_da_lista_exclusao(compras, "compra", db)
            db.deletar_compra(id_compra)

        elif opcao == '8':
            print("Saindo...")
            break

        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

def selecionar_da_lista(itens, nome_lista):
    for idx, item in enumerate(itens):
        print(f"{idx + 1}. {item[1] if len(item) > 1 else str(item[0])}")
    indice_selecionado = int(input(f"Escolha um {nome_lista}: ")) - 1
    return itens[indice_selecionado][0]

def selecionar_da_lista_exclusao(itens, nome_lista, db):
    for idx, item in enumerate(itens):
        nome_usuario = db.obter_nome_usuario(item[1])
        nome_produto = db.obter_nome_produto(item[2])
        print(f"{idx + 1}. Usuário: {nome_usuario}, Produto: {nome_produto}")
    indice_selecionado = int(input(f"Escolha uma {nome_lista}: ")) - 1
    return itens[indice_selecionado][0]
