class Produtos:
    nome = ''
    preco = 0.0
    estoque = 0
    vendedor = {
        'IdVendedor': 0,
        'emailVendedor': '',
        'NomeVendedor': ''
    }
    avaliacoes = [
        {
            'IdUsuario': 0,
            'NomeUsuario': '',
            'NotaAvaliacao': 0,
            'ComentarioAvaliacao': ''
        }
    ]
    def __init__(self, nome, preco, estoque, vendedor):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque
        self.vendedor = vendedor
        