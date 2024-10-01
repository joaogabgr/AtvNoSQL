import bcrypt

class Login:
    def __init__(self, db, redis_client):
        self.collection = db['clients']  # Coleção de usuários
        self.redis_client = redis_client  # Cliente Redis

    def login(self, email, password):
        """Realiza o login do usuário."""
        user = self.collection.find_one({'emailClient': email})
        if user:
            # Verifica se a senha fornecida corresponde ao hash armazenado
            if bcrypt.checkpw(password.encode('utf-8'), user['passwordClient'].encode('utf-8')):
                print("Login bem-sucedido!")

                # Armazenar a sessão no Redis
                session_key = f"session:{user['_id']}"  # Usando o ID do usuário como parte da chave
                self.redis_client.set(session_key, email)  # Armazena o email do usuário
                self.redis_client.expire(session_key, 3600)  # Define o tempo de expiração para 1 hora (3600 segundos)

                # Verificar se a sessão foi armazenada corretamente
                stored_email = self.redis_client.get(session_key)
                if stored_email:
                    print(f"Sessão armazenada no Redis: {stored_email.decode('utf-8')}")
                else:
                    print("Falha ao armazenar a sessão no Redis.")

                return True
            else:
                print("Senha incorreta.")
                return False
        else:
            print("Usuário não encontrado.")
            return False
