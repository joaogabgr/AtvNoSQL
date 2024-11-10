from controllers.clienteController import clienteController
from controllers.vendedorController import vendedorController
from controllers.produtoController import produtoController
from controllers.compraController import compraController

class Menu:
    def __init__(self, db):
        self.client_controller = clienteController(db)
        self.seller_controller = vendedorController(db)
        self.product_controller = produtoController(db)
        self.shopping_controller = compraController(db)

    def show_menu(self):
        while True:
            print("1. Inserir Cliente")
            print("2. Inserir Vendedor")
            print("3. Inserir Produto")
            print("4. Inserir Compra")
            print("5. Buscar Clientes")
            print("6. Buscar Vendedores")
            print("7. Buscar Produtos")
            print("8. Buscar Compras")
            print("0. Sair")
            choice = input("Escolha uma opção: ")

            if choice == "1":
                self.insert_cliente()
            elif choice == "2":
                self.insert_vendedor()
            elif choice == "3":
                self.insert_produto()
            elif choice == "4":
                self.insert_compra()
            elif choice == "5":
                self.buscar_clientes()
            elif choice == "6":
                self.buscar_vendedores()
            elif choice == "7":
                self.buscar_produtos()
            elif choice == "8":
                self.buscar_compras()
            elif choice == "0":
                break
            else:
                print("Opção inválida. Tente novamente.")

    def insert_cliente(self):
        name = input("Nome do Cliente: ")
        email = input("Email do Cliente: ")
        password = input("Senha do Cliente: ")
        age = int(input("Idade do Cliente: "))
        country = input("País: ")
        state = input("Estado: ")
        city = input("Cidade: ")
        street = input("Rua: ")
        number = input("Número: ")
        
        # Chama o método do controller para inserir o cliente com o endereço detalhado
        self.client_controller.insert_client(name, email, password, age, country, state, city, street, number)

    def insert_vendedor(self):
        seller_id = input("ID do Vendedor: ")
        name = input("Nome do Vendedor: ")
        email = input("Email do Vendedor: ")
        age = int(input("Idade do Vendedor: "))
        address = input("Endereço do Vendedor: ")
        self.seller_controller.insert_seller(seller_id, name, email, age, address)
        print("Vendedor inserido com sucesso!")

    def insert_produto(self):
        product_id = input("ID do Produto: ")
        name = input("Nome do Produto: ")
        price = float(input("Preço do Produto: "))
        stock = int(input("Quantidade em Estoque: "))
        seller_id = input("ID do Vendedor: ")
        self.product_controller.insert_product(product_id, name, price, stock, seller_id)
        print("Produto inserido com sucesso!")

    def insert_compra(self):
        shopping_id = input("ID da Compra: ")
        client_id = input("ID do Cliente: ")
        product_id = input("ID do Produto: ")
        date = input("Data da Compra (YYYY-MM-DD): ")
        self.shopping_controller.insert_shopping(shopping_id, client_id, product_id, date)
        print("Compra inserida com sucesso!")

    def buscar_clientes(self):
        clientes = self.client_controller.search_clients()
        for cliente in clientes:
            print(cliente)

    def buscar_vendedores(self):
        vendedores = self.seller_controller.search_sellers()
        for vendedor in vendedores:
            print(vendedor)

    def buscar_produtos(self):
        produtos = self.product_controller.search_products()
        for produto in produtos:
            print(produto)

    def buscar_compras(self):
        compras = self.shopping_controller.search_shopping()
        for compra in compras:
            print(compra)
