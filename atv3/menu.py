from clienteController import ClienteController

def menu():
    controller = ClienteController()
    user_id = None

    while True:
        print("\n=== MENU ===")
        print("1. Autenticar Usuário")
        print("2. Listar Produtos")
        print("3. Adicionar Favorito")
        print("4. Remover Favorito")
        print("5. Adicionar Compra")
        print("6. Adicionar Avaliação")
        print("7. Remover Avaliação")
        print("8. Logout")
        print("9. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            email = input("Email: ")
            senha = input("Senha: ")
            autenticado, resultado = controller.autenticar_usuario(email, senha)
            if autenticado:
                user_id = resultado
                print("Usuário autenticado com sucesso.")
            else:
                print(f"Falha na autenticação: {resultado}")

        elif opcao == "2":
            if user_id and controller.verificar_autenticacao(user_id):
                produtos = controller.listar_produtos(user_id)
                if produtos:
                    print("\n=== Lista de Produtos ===")
                    for produto in produtos:
                        print("\n--- Dados do Produto ---")
                        print(f"Nome: {produto['nome']}")
                        print(f"Descrição: {produto['descricao']}")
                        print(f"Valor: {produto['valor']}")
                        print(f"Quantidade: {produto['quantidade']}")
                        print(f"Vendedor ID: {produto['vendedor_id']}")
                        print("\n--- Avaliações do Produto ---")
                        for avaliacao in produto['avaliacao']:
                            cliente = controller.buscar_cliente_id(avaliacao['cliente_id'])
                            print(f"Cliente: {cliente['nome']} | Nota: {avaliacao['avaliacao']}")
                else:
                    print("Nenhum produto disponível.")
            else:
                print("Usuário não autenticado. Faça login para continuar.")

        elif opcao == "3":
            if user_id and controller.verificar_autenticacao(user_id):
                resultado = controller.adicionar_favorito(user_id)
                print(resultado)
            else:
                print("Usuário não autenticado. Faça login para continuar.")

        elif opcao == "4":
            if user_id and controller.verificar_autenticacao(user_id):
                resultado = controller.remover_favorito(user_id)
                print(resultado)
            else:
                print("Usuário não autenticado. Faça login para continuar.")

        elif opcao == "5":
            if user_id and controller.verificar_autenticacao(user_id):
                resultado = controller.adicionar_compra(user_id)
                print(resultado)
            else:
                print("Usuário não autenticado. Faça login para continuar.")

        elif opcao == "6":
            if user_id and controller.verificar_autenticacao(user_id):
                resultado = controller.adicionar_avaliacao(user_id)
                print(resultado)
            else:
                print("Usuário não autenticado. Faça login para continuar.")

        elif opcao == "7":
            if user_id and controller.verificar_autenticacao(user_id):
                resultado = controller.remover_avaliacao(user_id)
                print(resultado)

        elif opcao == "8":
            if user_id:
                resultado = controller.logout_usuario(user_id)
                user_id = None
                print(resultado)
            else:
                print("Nenhum usuário está autenticado.")

        elif opcao == "9":
            print("Encerrando o programa. Até logo!")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
