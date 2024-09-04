import connectMongo

def verifyEmail(email):
    selectDatabase = connectMongo.client['MercadoLivre']
    usuarios = selectDatabase['usuario'].find()

    for usuario in usuarios:
        if usuario['email'] == email:
            return True
    return False