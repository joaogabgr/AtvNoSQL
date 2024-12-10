from connectCassandra import connect_cassandra
import uuid
from datetime import datetime

class CassandraController:
    def __init__(self):
        self.session = connect_cassandra()

    def insert_usuario(self):
        nome = input("Digite o nome: ")
        email = input("Digite o email: ")
        senha = input("Digite a senha: ")
        rua = input("Digite a rua: ")
        numero = input("Digite o numero: ")
        bairro = input("Digite o bairro: ")
        cidade = input("Digite a cidade: ")
        estado = input("Digite o estado: ")
        cep = input("Digite o cep: ")
        query = """
        INSERT INTO usuario (id, nome, email, senha, rua, numero, bairro, cidade, estado, cep)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.session.execute(query, (uuid.uuid4(), nome, email, senha, rua, numero, bairro, cidade, estado, cep))

    def insert_vendedor(self):
        name = input("Digite o nome: ")
        email = input("Digite o email: ")
        senha = input("Digite a senha: ")
        rua = input("Digite a rua: ")
        numero = input("Digite o numero: ")
        bairro = input("Digite o bairro: ")
        cidade = input("Digite a cidade: ")
        estado = input("Digite o estado: ")
        cep = input("Digite o cep: ")
        query = """
        INSERT INTO vendedor (id, name, email, senha, rua, numero, bairro, cidade, estado, cep)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.session.execute(query, (uuid.uuid4(), name, email, senha, rua, numero, bairro, cidade, estado, cep))

    def insert_produto(self):
        name = input("Digite o nome do produto: ")
        price = float(input("Digite o preço: "))
        seller_id = self.select_vendedor()
        query = """
        INSERT INTO produto (id, name, price, seller_id)
        VALUES (%s, %s, %s, %s)
        """
        self.session.execute(query, (uuid.uuid4(), name, price, seller_id))

    def insert_compra(self):
        user_id = self.select_usuario()
        product_id = self.select_produto()
        date = datetime.now().strftime("%Y-%m-%d")
        query = """
        INSERT INTO compra (purchase_id, user_id, product_id, date)
        VALUES (%s, %s, %s, %s)
        """
        self.session.execute(query, (uuid.uuid4(), user_id, product_id, date))

    def update_usuario(self):
        user_id = self.select_usuario()
        nome = input("Digite o novo nome (ou deixe em branco para não alterar): ")
        email = input("Digite o novo email (ou deixe em branco para não alterar): ")
        senha = input("Digite a nova senha (ou deixe em branco para não alterar): ")
        rua = input("Digite a nova rua (ou deixe em branco para não alterar): ")
        numero = input("Digite o novo numero (ou deixe em branco para não alterar): ")
        bairro = input("Digite o novo bairro (ou deixe em branco para não alterar): ")
        cidade = input("Digite a nova cidade (ou deixe em branco para não alterar): ")
        estado = input("Digite o novo estado (ou deixe em branco para não alterar): ")
        cep = input("Digite o novo cep (ou deixe em branco para não alterar): ")
        query = "UPDATE usuario SET "
        updates = []
        params = []
        if nome:
            updates.append("nome = %s")
            params.append(nome)
        if email:
            updates.append("email = %s")
            params.append(email)
        if senha:
            updates.append("senha = %s")
            params.append(senha)
        if rua:
            updates.append("rua = %s")
            params.append(rua)
        if numero:
            updates.append("numero = %s")
            params.append(numero)
        if bairro:
            updates.append("bairro = %s")
            params.append(bairro)
        if cidade:
            updates.append("cidade = %s")
            params.append(cidade)
        if estado:
            updates.append("estado = %s")
            params.append(estado)
        if cep:
            updates.append("cep = %s")
            params.append(cep)
        if updates:
            query += ", ".join(updates) + " WHERE id = %s"
            params.append(user_id)
            self.session.execute(query, params)
        else:
            print("Nenhuma atualização foi feita.")

    def search_produto(self):
        query = "SELECT id, name FROM produto"
        result = self.session.execute(query)
        produtos = result.all()
        if produtos:
            print("Produtos disponíveis:")
            for i, produto in enumerate(produtos):
                print(f"{i}: Nome: {produto.name}")
            index = int(input("Selecione o índice do produto: "))
            if 0 <= index < len(produtos):
                selected_produto = produtos[index]
                query = "SELECT id, name, price, seller_id FROM produto WHERE id = %s"
                result = self.session.execute(query, (selected_produto.id,))
                produto_info = result.one()
                if produto_info:
                    print(f"ID: {produto_info.id}, Nome: {produto_info.name}, Preço: {produto_info.price}, Vendedor ID: {produto_info.seller_id}")
                    return [produto_info]
                else:
                    print("Produto não encontrado.")
                    return None
            else:
                print("Índice inválido.")
                return None
        else:
            print("Nenhum produto disponível.")
            return None

    def delete_compra(self):
        purchase_id = self.select_compra()
        query = "DELETE FROM compra WHERE purchase_id = %s"
        self.session.execute(query, (purchase_id,))

    def select_usuario(self):
        query = "SELECT id, nome FROM usuario"
        result = self.session.execute(query)
        usuarios = result.all()
        for i, usuario in enumerate(usuarios):
            print(f"{i}: {usuario.nome} (ID: {usuario.id})")
        index = int(input("Selecione o índice do usuário: "))
        return usuarios[index].id

    def select_vendedor(self):
        query = "SELECT id, name FROM vendedor"
        result = self.session.execute(query)
        vendedores = result.all()
        for i, vendedor in enumerate(vendedores):
            print(f"{i}: {vendedor.name} (ID: {vendedor.id})")
        index = int(input("Selecione o índice do vendedor: "))
        return vendedores[index].id

    def select_produto(self):
        query = "SELECT id, name FROM produto"
        result = self.session.execute(query)
        produtos = result.all()
        for i, produto in enumerate(produtos):
            print(f"{i}: {produto.name} (ID: {produto.id})")
        index = int(input("Selecione o índice do produto: "))
        return produtos[index].id

    def select_compra(self):
        query = "SELECT purchase_id, user_id, product_id, date FROM compra"
        result = self.session.execute(query)
        compras = result.all()
        for i, compra in enumerate(compras):
            print(f"{i}: Compra ID: {compra.purchase_id}, Usuário ID: {compra.user_id}, Produto ID: {compra.product_id}, Data: {compra.date}")
        index = int(input("Selecione o índice da compra: "))
        return compras[index].purchase_id
