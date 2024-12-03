from database import connectMongo, connectRedis
from controllers.login import Login
from controllers.ClientControllers import ClientControllers

def main():
    client = connectMongo.connect_mongo()
    db = client['MercadoLivre']

    redis_client = connectRedis.get_redis_client()

    login_system = Login(db, redis_client)
    user_id = None

    while True:
        print("\nMenu:")
        print("1. Login")
        print("2. Adicionar produto aos favoritos")
        print("3. Remover produto dos favoritos")
        print("4. Adicionar avaliação a um produto")
        print("5. Remover avaliação de um produto")
        print("6. Sair")

        choice = input("Escolha uma opção: ")
        client_controller = ClientControllers(db, redis_client)

        if choice == '1':
            email = input("Digite seu email: ")
            password = input("Digite sua senha: ")
            
            login_success, user_info = login_system.login(email, password)
            if login_success:
                user_id = str(user_info['_id'])
                print("Você está logado!")
            else:
                print("Falha no login.")

        elif choice == '2':
            if user_id:
                client_controller.add_favorite_product(user_id)
            else:
                print("Você precisa estar logado para adicionar produtos aos favoritos.")

        elif choice == '3':
            if user_id:
                client_controller.remove_favorite_product(user_id)
            else:
                print("Você precisa estar logado para remover produtos dos favoritos.")

        elif choice == '4':
            if user_id:
                client_controller.add_evaluation(user_id)
            else:
                print("Você precisa estar logado para adicionar uma avaliação.")

        elif choice == '5':
            if user_id:
                client_controller.remove_evaluation(user_id)
            else:
                print("Você precisa estar logado para remover uma avaliação.")

        elif choice == '6':
            print("Saindo...")
            break

        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    main()
