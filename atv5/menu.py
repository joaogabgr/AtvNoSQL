from controller import Neo4jController

def main_menu():
    controller = Neo4jController()
    
    while True:
        print("\nMenu Principal")
        print("1. Inserir Usuário")
        print("2. Inserir Vendedor")
        print("3. Inserir Produto")
        print("4. Inserir Compra")
        print("5. Buscar Usuário")
        print("6. Buscar Vendedor")
        print("7. Buscar Produto")
        print("8. Buscar Compra")
        print("9. Sair")
        
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
            controller.search_usuario()
        
        elif choice == '6':
            controller.search_vendedor()
        
        elif choice == '7':
            controller.search_produto()
        
        elif choice == '8':
            controller.search_compra()
        
        elif choice == '9':
            print("Saindo...")
            controller.close()
            break
        
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main_menu()