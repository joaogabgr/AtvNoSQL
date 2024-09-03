def listarTodosUsuarios():
    import connectMongo

    selectDatabase = connectMongo.client['MercadoLivre']
    usuarios = selectDatabase['usuario'].find()

    for usuario in usuarios:
        print(usuario['nome'])