# menu.py
from controllers.mercadoLivreDB import MercadoLivreDB

def show_menu(db):
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
            while True:
                try:
                    age = int(input("Digite a idade do usuário: "))
                    break
                except ValueError:
                    print("Erro: A idade deve ser um número inteiro válido. Tente novamente.")
            address = input("Digite o endereço do usuário: ")
            db.insert_user(name, age, address)

        elif choice == '2':
            name = input("Digite o nome do vendedor: ")
            while True:
                try:
                    age = int(input("Digite a idade do vendedor: "))
                    break
                except ValueError:
                    print("Erro: A idade deve ser um número inteiro válido. Tente novamente.")
            address = input("Digite o endereço do vendedor: ")
            db.insert_seller(name, age, address)

        elif choice == '3':
            name = input("Digite o nome do produto: ")
            while True:
                try:
                    price = float(input("Digite o preço do produto: "))
                    break
                except ValueError:
                    print("Erro: O preço deve ser um número válido. Tente novamente.")
            seller_id = select_from_list(db.get_all_sellers(), "vendedor")
            db.insert_product(name, price, seller_id)

        elif choice == '4':
            user_id = select_from_list(db.get_all_users(), "usuário")
            product_id = select_from_list(db.get_all_products(), "produto")
            while True:
                try:
                    quantity = int(input("Digite a quantidade: "))
                    break
                except ValueError:
                    print("Erro: A quantidade deve ser um número inteiro válido. Tente novamente.")
            product = db.get_product_by_id(product_id)
            if product:
                price = product['valor']
                value = price * quantity
                db.insert_purchase(user_id, product_id, quantity, value)
            else:
                print(f"Produto com ID {product_id} não encontrado.")

        elif choice == '5':
            user_id = select_from_list(db.get_all_users(), "usuário")
            new_name = input("Digite o novo nome (deixe vazio para não alterar): ")
            new_age = input("Digite a nova idade (deixe vazio para não alterar): ")
            if new_age:
                while True:
                    try:
                        new_age = int(new_age)
                        break
                    except ValueError:
                        print("Erro: A idade deve ser um número inteiro válido. Tente novamente.")
                        new_age = input("Digite a nova idade (deixe vazio para não alterar): ")
            new_address = input("Digite o novo endereço (deixe vazio para não alterar): ")
            db.update_user(user_id, new_name if new_name else None, new_age if new_age else None, new_address if new_address else None)

        elif choice == '6':
            product_id = select_from_list(db.get_all_products(), "produto")
            db.search_product(product_id)

        elif choice == '7':
            purchases = db.get_all_purchases()
            purchase_id = select_from_list_delete(purchases, "compra", db)
            db.delete_purchase(purchase_id)

        elif choice == '8':
            print("Saindo...")
            break

        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")


# Função para exibir uma lista e selecionar o índice
def select_from_list(items, list_name):
    # Exibe a lista de itens com um número correspondente
    for idx, item in enumerate(items):
        # Acessando pelos índices das tuplas
        print(f"{idx + 1}. {item[1] if len(item) > 1 else str(item[0])}")  # item[1] é o nome
    
    # Lê a seleção do usuário
    selected_idx = int(input(f"Escolha um {list_name}: ")) - 1
    return items[selected_idx][0]  # Retorna o ID (primeiro elemento da tupla)

def select_from_list_delete(items, list_name, db):
    for idx, item in enumerate(items):
        user_name = db.get_user_name(item[1])
        product_name = db.get_product_name(item[2])
        print(f"{idx + 1}. Usuário: {user_name}, Produto: {product_name}")
    selected_idx = int(input(f"Escolha uma {list_name}: ")) - 1
    return items[selected_idx][0]