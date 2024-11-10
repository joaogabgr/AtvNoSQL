from connectNeo4J import MercadoLivreDB
from menu import Menu

def main():
    db = MercadoLivreDB("neo4j+s://8f49fef0.databases.neo4j.io", "neo4j", "qF3BJ0EwKe6nPtl9x3ya13a07qryVlfXi97-jxSb8h8")
    menu = Menu(db)
    menu.show_menu()
    db.close()

if __name__ == "__main__":
    main()
