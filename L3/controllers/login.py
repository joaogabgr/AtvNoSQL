import bcrypt

class Login:
    def __init__(self, db, redis_client):
        self.collection = db['clients']
        self.redis_client = redis_client

    def login(self, email, password):
        user = self.collection.find_one({'emailClient': email})
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user['passwordClient'].encode('utf-8')):
                print("Login bem-sucedido!")

                session_key = f"session:{user['_id']}"
                self.redis_client.set(session_key, email)
                self.redis_client.expire(session_key, 3600)

                stored_email = self.redis_client.get(session_key)
                if stored_email:
                    print(f"Sessão armazenada no Redis: {stored_email.decode('utf-8')}")
                else:
                    print("Falha ao armazenar a sessão no Redis.")

                return True, user
            else:
                print("Senha incorreta.")
                return False, None
        else:
            print("Usuário não encontrado.")
            return False, None

    def is_logged_in(self, user_id):
        session_key = f"session:{user_id}"
        stored_email = self.redis_client.get(session_key)

        if stored_email:
            print(f"Usuário com ID {user_id} está logado.")
            return True
        else:
            print(f"Usuário com ID {user_id} não está logado ou a sessão expirou.")
            return False
