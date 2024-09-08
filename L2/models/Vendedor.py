class Vendedor:
    nome = ''
    idade = 0
    email = ''
    produtos = [
        {
            'idProduto': 0,
            'nomeProduto': '',
            'valorProduto': 0.0,
            'estoqueProduto': 0
        }
    ]
    Endereco = {
        'pais': '',
        'estado': '',
        'cidade': '',
        'rua': '',
        'numero': '',
        'complemento': ''
    }
    Vendas = [
        {
            'idVenda': 0,
            'dataVenda': '',
            'valorVenda': 0.0,
            'produtosVendidos': {
                    'idProduto': 0,
                    'nomeProduto': '',
                    'valorProduto': 0.0
            }
        }
    ]
    def __init__(self, nome, idade, email):
        self.nome = nome
        self.idade = idade
        self.email = email