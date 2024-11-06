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
            
            # Tratamento de erro para idade do usuário
            while True:
                try:
                    age = int(input("Digite a idade do usuário: "))
                    break  # Se a conversão for bem-sucedida, sai do loop
                except ValueError:
                    print("Erro: A idade deve ser um número inteiro válido. Tente novamente.")

            address = input("Digite o endereço do usuário: ")
            db.insert_user(name, age, address)

        elif choice == '2':
            name = input("Digite o nome do vendedor: ")
            
            # Tratamento de erro para idade do vendedor
            while True:
                try:
                    age = int(input("Digite a idade do vendedor: "))
                    break  # Se a conversão for bem-sucedida, sai do loop
                except ValueError:
                    print("Erro: A idade deve ser um número inteiro válido. Tente novamente.")

            address = input("Digite o endereço do vendedor: ")
            db.insert_seller(name, age, address)

        elif choice == '3':
            name = input("Digite o nome do produto: ")
            
            # Tratamento de erro para preço do produto
            while True:
                try:
                    price = float(input("Digite o preço do produto: "))
                    break  # Se a conversão for bem-sucedida, sai do loop
                except ValueError:
                    print("Erro: O preço deve ser um número válido. Tente novamente.")
            
            seller_id = select_from_list(db.get_all_sellers(), "vendedor")
            db.insert_product(name, price, seller_id)

        elif choice == '4':
            user_id = select_from_list(db.get_all_users(), "usuário")
            product_id = select_from_list(db.get_all_products(), "produto")

            # Tratamento de erro para quantidade
            while True:
                try:
                    quantity = int(input("Digite a quantidade: "))
                    break  # Se a conversão for bem-sucedida, sai do loop
                except ValueError:
                    print("Erro: A quantidade deve ser um número inteiro válido. Tente novamente.")

            # Buscar o preço do produto automaticamente
            product = db.get_product_by_id(product_id)
            if product:
                price = product['valor']  # Preço do produto
                value = price * quantity  # Calcula o valor total automaticamente
                db.insert_purchase(user_id, product_id, quantity, value)
            else:
                print(f"Produto com ID {product_id} não encontrado.")

        elif choice == '5':
            user_id = select_from_list(db.get_all_users(), "usuário")
            new_name = input("Digite o novo nome (deixe vazio para não alterar): ")
            
            # Tratamento de erro para nova idade
            new_age = input("Digite a nova idade (deixe vazio para não alterar): ")
            if new_age:
                while True:
                    try:
                        new_age = int(new_age)
                        break  # Se a conversão for bem-sucedida, sai do loop
                    except ValueError:
                        print("Erro: A idade deve ser um número inteiro válido. Tente novamente.")
                        new_age = input("Digite a nova idade (deixe vazio para não alterar): ")

            new_address = input("Digite o novo endereço (deixe vazio para não alterar): ")
            db.update_user(user_id, new_name if new_name else None, new_age if new_age else None, new_address if new_address else None)

        elif choice == '6':
            product_id = select_from_list(db.get_all_products(), "produto")
            db.search_product(product_id)

        elif choice == '7':
            purchase_id = select_from_list(db.get_all_purchases(), "compra")
            db.delete_purchase(purchase_id)

        elif choice == '8':
            print("Saindo...")
            break

        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

# Função para exibir uma lista e selecionar o índice
def select_from_list(items, item_type):
    if not items:
        print(f"Nenhum {item_type} encontrado.")
        return None
    print(f"\nSelecione um {item_type}:")
    for idx, item in enumerate(items):
        print(f"{idx}. {item['nome'] if 'nome' in item else str(item['id'])}")
    while True:
        try:
            selected_index = int(input(f"Digite o número correspondente ao {item_type}: "))
            if 0 <= selected_index < len(items):
                return items[selected_index]['id']
            else:
                print("Erro: Seleção inválida. Tente novamente.")
        except ValueError:
            print("Erro: Você deve digitar um número. Tente novamente.")
