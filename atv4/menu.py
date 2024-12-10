from controller import CassandraController
import uuid
import datetime

def main_menu():
    controller = CassandraController()
    
    while True:
        print("\nMenu Principal")
        print("1. Inserir Usuário")
        print("2. Inserir Vendedor")
        print("3. Inserir Produto")
        print("4. Inserir Compra")
        print("5. Atualizar Usuário")
        print("6. Buscar Produto")
        print("7. Deletar Compra")
        print("8. Sair")
        
        choice = input("Escolha uma opção: ")
        
        if choice == '1':
            controller.insert_usuario()
        
        elif choice == '2':
            controller.insert_vendedor()
        
        elif choice == '3':
            controller.insert_produto()
        
        elif choice == '4':
            controller.insert_compra()
        
        elif choice == '5':
            controller.update_usuario()
        
        elif choice == '6':
            produtos = controller.search_produto()
        
        elif choice == '7':
            controller.delete_compra()
        
        elif choice == '8':
            print("Saindo...")
            break
        
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main_menu()
