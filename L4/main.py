from controllers.Controllers import MercadoLivreDB

def main():
    TOKEN = "AstraCS:fyIJCEQXkwEjObmeqeqZaInm:44c960d3bd9b3a87cd3e2b605739fff3ceeb14acb23af63f5fc9fbca031cff15"
    API_ENDPOINT = "https://9f3876e3-09f2-44c9-98ea-3eea980fdf24-us-east-2.apps.astra.datastax.com"
    
    db = MercadoLivreDB(TOKEN, API_ENDPOINT)

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

        choice = input("Escolha uma opção: ")

        if choice == '1':
            name = input("Digite o nome do usuário: ")
            email = input("Digite o email do usuário: ")
            db.insert_user(name, email)

        elif choice == '2':
            name = input("Digite o nome do vendedor: ")
            rating = float(input("Digite a classificação do vendedor: "))
            db.insert_seller(name, rating)

        elif choice == '3':
            name = input("Digite o nome do produto: ")
            price = float(input("Digite o preço do produto: "))
            db.insert_product(name, price)

        elif choice == '4':
            user_id = input("Digite o ID do usuário: ")
            product_id = input("Digite o ID do produto: ")
            quantity = int(input("Digite a quantidade: "))
            db.insert_purchase(user_id, product_id, quantity)

        elif choice == '5':
            user_id = input("Digite o ID do usuário a ser atualizado: ")
            new_name = input("Digite o novo nome (deixe vazio para não alterar): ")
            new_email = input("Digite o novo email (deixe vazio para não alterar): ")
            db.update_user(user_id, new_name if new_name else None, new_email if new_email else None)

        elif choice == '6':
            product_id = input("Digite o ID do produto a ser pesquisado: ")
            db.search_product(product_id)

        elif choice == '7':
            purchase_id = input("Digite o ID da compra a ser deletada: ")
            db.delete_purchase(purchase_id)

        elif choice == '8':
            print("Saindo...")
            break

        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    main()
