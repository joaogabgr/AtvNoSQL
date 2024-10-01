from database import connectMongo, connectRedis
from controllers import login

if __name__ == "__main__":
    # Conectar ao MongoDB
    client = connectMongo.connect_mongo()
    db = client['MercadoLivre']  # Substitua pelo nome do seu banco de dados

    # Configurar Redis
    redis_client = connectRedis.get_redis_client()  # Obtém o cliente Redis

    # Criar instância do sistema de login
    login_system = login.Login(db, redis_client)

    # Exemplo de entrada do usuário
    email = input("Digite seu email: ")
    password = input("Digite sua senha: ")
    
    # Tenta fazer login
    login_success = login_system.login(email, password)
    
    if login_success:
        print("Você está logado!")
    else:
        print("Falha no login.")
