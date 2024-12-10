from connectMongo import get_database

class VendedorController:
    def __init__(self):
        self.db = get_database()
        self.vendedores = self.db["vendedores"]

    def listar_vendedores(self):
        vendedores = list(self.vendedores.find())
        return vendedores

    def buscar_vendedor(self, cpf):
        vendedor = self.vendedores.find_one({"cpf": cpf})
        return vendedor if vendedor else None

    def inserir_vendedor(self):
        nome = input("Nome: ")
        idade = int(input("Idade: "))
        cpf = input("CPF: ")
        if self.verificar_cpf(cpf):
            return None

        email = input("Email: ")
        if self.verificar_email(email):
            return None

        rua = input("Rua: ")
        numero = input("Número: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        estado = input("Estado: ")
        vendas = []
        produtos = []
        vendedor = {
            "nome": nome,
            "idade": idade,
            "cpf": cpf,
            "email": email,
            "endereco": {
                "rua": rua,
                "numero": numero,
                "bairro": bairro,
                "cidade": cidade,
                "estado": estado
            },
            "vendas": vendas,
            "produtos": produtos
        }
        return self.vendedores.insert_one(vendedor)

    def atualizar_vendedor(self, cpf):
        vendedor = self.buscar_vendedor(cpf)
        if vendedor is None:
            return 'Vendedor não encontrado.'

        nome = input("Nome: ")
        idade = int(input("Idade: "))
        email = input("Email: ")

        if email != vendedor["email"]:
            if self.verificar_email(email):
                return None

        rua = input("Rua: ")
        numero = input("Número: ")
        bairro = input("Bairro: ")
        cidade = input("Cidade: ")
        estado = input("Estado: ")
        vendas = []
        produtos = []
        vendedor = {
            "nome": nome,
            "idade": idade,
            "cpf": cpf,
            "email": email,
            "endereco": {
                "rua": rua,
                "numero": numero,
                "bairro": bairro,
                "cidade": cidade,
                "estado": estado
            },
            "vendas": vendas,
            "produtos": produtos
        }
        return self.vendedores.replace_one({"cpf": cpf}, vendedor)

    def deletar_vendedor(self, cpf):
        return self.vendedores.delete_one({"cpf": cpf})

    def selecionar_vendedor(self):
        vendedores = self.listar_vendedores()
        if not vendedores:
            print("Nenhum vendedor encontrado.")
            return None

        print("\n--- Lista de Vendedores ---")
        for index, vendedor in enumerate(vendedores):
            print(f"{index}. {vendedor['nome']} - CPF: {vendedor['cpf']}")

        while True:
            try:
                indice = int(input("Selecione o índice do vendedor: "))
                if 0 <= indice < len(vendedores):
                    return vendedores[indice]
                else:
                    print("Índice inválido. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Por favor, insira um número.")

    def verificar_email(self, email):
        return self.vendedores.find_one({"email": email})
    
    def verificar_cpf(self, cpf):
        return self.vendedores.find_one({"cpf": cpf})