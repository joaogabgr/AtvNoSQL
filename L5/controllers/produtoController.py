from connectNeo4J import MercadoLivreDB

class produtoController:
    def __init__(self, db):
        self.db = db

    def insert_product(self, product_id, name, price, stock, seller_id):
        with self.db.driver.session() as session:
            session.write_transaction(self._create_product, product_id, name, price, stock, seller_id)

    @staticmethod
    def _create_product(tx, product_id, name, price, stock, seller_id):
        tx.run(
            "CREATE (p:Product {id: $product_id, name: $name, price: $price, stock: $stock}) "
            "WITH p "
            "MATCH (s:Seller {id: $seller_id}) "
            "CREATE (s)-[:SELLS]->(p)",
            product_id=product_id, name=name, price=price, stock=stock, seller_id=seller_id
        )

    def search_products(self):
        with self.db.driver.session() as session:
            result = session.read_transaction(self._find_products)
            return [record["p"] for record in result]

    @staticmethod
    def _find_products(tx):
        result = tx.run("MATCH (p:Product) RETURN p")
        return result
