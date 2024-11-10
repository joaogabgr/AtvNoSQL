from connectNeo4J import MercadoLivreDB

class compraController:
    def __init__(self, db):
        self.db = db

    def insert_shopping(self, shopping_id, client_id, product_id, date):
        with self.db.driver.session() as session:
            session.write_transaction(self._create_shopping, shopping_id, client_id, product_id, date)

    @staticmethod
    def _create_shopping(tx, shopping_id, client_id, product_id, date):
        tx.run(
            "CREATE (sh:Shopping {id: $shopping_id, date: $date}) "
            "WITH sh "
            "MATCH (c:Client {id: $client_id}), (p:Product {id: $product_id}) "
            "CREATE (c)-[:BOUGHT]->(sh)-[:CONTAINS]->(p)",
            shopping_id=shopping_id, client_id=client_id, product_id=product_id, date=date
        )

    def search_shopping(self):
        with self.db.driver.session() as session:
            result = session.read_transaction(self._find_shopping)
            return [record["sh"] for record in result]

    @staticmethod
    def _find_shopping(tx):
        result = tx.run("MATCH (sh:Shopping) RETURN sh")
        return result
