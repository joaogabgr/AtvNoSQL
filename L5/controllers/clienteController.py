import uuid

class clienteController:
    def __init__(self, db):
        self.db = db

    def insert_client(self, nameClient, emailClient, passwordClient, ageClient, country, state, city, street, number):
        client_id = str(uuid.uuid4())  # Gera um UUID automático para o ID do cliente
        address = {
            "country": country,
            "state": state,
            "city": city,
            "street": street,
            "number": number
        }
        favorites = []
        shopping = []
        evaluations = []
        
        with self.db.session() as session:
            session.write_transaction(
                self._create_client, client_id, nameClient, emailClient, passwordClient, ageClient, address, favorites, shopping, evaluations
            )

    @staticmethod
    def _create_client(tx, client_id, nameClient, emailClient, passwordClient, ageClient, address, favorites, shopping, evaluations):
        tx.run(
            """
            CREATE (u:Usuario {
                id: $client_id,
                nameClient: $nameClient,
                emailClient: $emailClient,
                passwordClient: $passwordClient,
                ageClient: $ageClient,
                address: $address,
                favorites: $favorites,
                shopping: $shopping,
                evaluations: $evaluations
            })
            """,
            client_id=client_id,
            nameClient=nameClient,
            emailClient=emailClient,
            passwordClient=passwordClient,
            ageClient=ageClient,
            address=address,
            favorites=favorites,
            shopping=shopping,
            evaluations=evaluations
        )

    def search_clients(self):
        with self.db.driver.session() as session:
            result = session.read_transaction(self._find_clients)
            return [record["c"] for record in result]

    @staticmethod
    def _find_clients(tx):
        result = tx.run("MATCH (c:Client) RETURN c")
        return result
