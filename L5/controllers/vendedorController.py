from connectNeo4J import MercadoLivreDB

class vendedorController:
    def __init__(self, db):
        self.db = db

    def insert_seller(self, seller_id, name, email, age, address):
        with self.db.driver.session() as session:
            session.write_transaction(self._create_seller, seller_id, name, email, age, address)

    @staticmethod
    def _create_seller(tx, seller_id, name, email, age, address):
        tx.run(
            "CREATE (s:Seller {id: $seller_id, name: $name, email: $email, age: $age, address: $address})",
            seller_id=seller_id, name=name, email=email, age=age, address=address
        )

    def search_sellers(self):
        with self.db.driver.session() as session:
            result = session.read_transaction(self._find_sellers)
            return [record["s"] for record in result]

    @staticmethod
    def _find_sellers(tx):
        result = tx.run("MATCH (s:Seller) RETURN s")
        return result
