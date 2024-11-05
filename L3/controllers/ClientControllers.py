from bson import ObjectId

class ClientControllers:
    def __init__(self, db, redis_client):
        self.collection = db['clients']
        self.products_collection = db['products']
        self.redis_client = redis_client

    def is_user_logged_in(self, user_id):
        session_key = f"session:{user_id}"
        stored_email = self.redis_client.get(session_key)
        return stored_email is not None

    def list_products(self):
        try:
            products = list(self.products_collection.find())
            if len(products) == 0:
                return []

            for idx, product in enumerate(products):
                print(f"Índice: {idx}, ID: {product['_id']}, Nome: {product['nameProduct']}, Preço: {product['priceProduct']}")
            return products
        except Exception as e:
            return []

    def list_favorites(self, user_id):
        client = self.collection.find_one({'_id': ObjectId(user_id)})
        if not client:
            return []

        favorites = client.get('favorites', [])
        if not favorites:
            return []

        for idx, fav in enumerate(favorites):
            print(f"Índice: {idx}, ID: {fav['_id']}, Nome: {fav['nameProduct']}, Preço: {fav['priceProduct']}")
        return favorites

    def add_favorite_product(self, user_id):
        if not self.is_user_logged_in(user_id):
            return

        products = self.list_products()
        if not products:
            return

        try:
            index = int(input("Digite o índice do produto para adicionar aos favoritos: "))
            if index < 0 or index >= len(products):
                return

            product = products[index]

            client = self.collection.find_one({'_id': ObjectId(user_id)})
            if not client:
                return

            favorites = client.get('favorites', [])

            if any(fav['_id'] == product['_id'] for fav in favorites):
                return

            favorites.append(product)

            self.collection.update_one({'_id': ObjectId(user_id)}, {'$set': {'favorites': favorites}})
            print("Produto adicionado aos favoritos com sucesso.")

        except Exception as e:
            print("Erro ao adicionar produto aos favoritos:", e)

    def remove_favorite_product(self, user_id):
        if not self.is_user_logged_in(user_id):
            return

        favorites = self.list_favorites(user_id)
        if not favorites:
            return

        try:
            index = int(input("Digite o índice do produto para remover dos favoritos: "))
            if index < 0 or index >= len(favorites):
                return

            product_to_remove = favorites[index]

            updated_favorites = [fav for fav in favorites if fav['_id'] != product_to_remove['_id']]
            self.collection.update_one({'_id': ObjectId(user_id)}, {'$set': {'favorites': updated_favorites}})
            print("Produto removido dos favoritos com sucesso.")

        except Exception as e:
            print("Erro ao remover produto dos favoritos:", e)

    def add_evaluation(self, user_id):
        if not self.is_user_logged_in(user_id):
            return

        products = self.list_products()
        if not products:
            return

        try:
            index = int(input("Digite o índice do produto para avaliar: "))
            if index < 0 or index >= len(products):
                return

            product = products[index]

            rating = float(input("Digite a avaliação (0-5): "))
            while rating < 0 or rating > 5:
                rating = float(input("Digite uma avaliação válida (0-5): "))
            comment = input("Digite um comentário: ")

            evaluation = {
                '_id': ObjectId(),
                'client_id': user_id,
                'product_id': product['_id'],
                'client_name': user_id,
                'rating': rating,
                'comment': comment
            }

            product_evaluations = product.get('evaluations', [])
            product_evaluations.append(evaluation)
            self.products_collection.update_one({'_id': product['_id']}, {'$set': {'evaluations': product_evaluations}})

            client = self.collection.find_one({'_id': ObjectId(user_id)})
            client_evaluations = client.get('evaluations', [])
            client_evaluations.append(evaluation)
            self.collection.update_one({'_id': ObjectId(user_id)}, {'$set': {'evaluations': client_evaluations}})

            print("Avaliação adicionada com sucesso.")

        except Exception as e:
            print("Erro ao adicionar avaliação:", e)

    def remove_evaluation(self, user_id):
        if not self.is_user_logged_in(user_id):
            return

        client = self.collection.find_one({'_id': ObjectId(user_id)})
        evaluations = client.get('evaluations', [])
        if not evaluations:
            return

        print("Avaliações:")
        for idx, evaluation in enumerate(evaluations):
            print(f"Índice: {idx}, Produto ID: {evaluation['product_id']}, Avaliação: {evaluation['rating']}, Comentário: {evaluation['comment']}")

        try:
            index = int(input("Digite o índice da avaliação para remover: "))
            if index < 0 or index >= len(evaluations):
                return

            evaluation_to_remove = evaluations[index]

            updated_evaluations = [eval for eval in evaluations if eval['_id'] != evaluation_to_remove['_id']]
            self.collection.update_one({'_id': ObjectId(user_id)}, {'$set': {'evaluations': updated_evaluations}})

            product = self.products_collection.find_one({'_id': evaluation_to_remove['product_id']})
            if product:
                product_evaluations = product.get('evaluations', [])
                updated_product_evaluations = [eval for eval in product_evaluations if eval['_id'] != evaluation_to_remove['_id']]
                self.products_collection.update_one({'_id': evaluation_to_remove['product_id']}, {'$set': {'evaluations': updated_product_evaluations}})

            print("Avaliação removida com sucesso.")

        except Exception as e:
            print("Erro ao remover avaliação:", e)
