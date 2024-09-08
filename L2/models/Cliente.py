class Cliente:
    nome = ''
    email = ''
    idade = 0
    Endereco = [{
        'pais': '',
        'estado': '',
        'cidade': '',
        'rua': '',
        'numero': '',
        'complemento': ''
    }]
    favoritos = [
        {
            'idProduto': 0,
            'nomeProduto': '',
            'valorProduto': 0.0
        }
    ]
    compras = [
        {
            "idCompra": 0,
            "dataCompra": '',
            "valorCompra": 0.0,
            "produtos": {
                    'idProduto': 0,
                    'nomeProduto': '',
                    'valorProduto': 0.0
            }
        }
    ]
    def __init__(self, nome, email, idade):
        self.nome = nome
        self.email = email
        self.idade = idade