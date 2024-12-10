from neo4j import GraphDatabase

def connect_neo4j():
    URI = "neo4j+ssc://bb21ac75.databases.neo4j.io"
    AUTH = ("neo4j", "9i8iuwhPlhBBdjizjoGS_5P_4ow4UAKdv8Ddjwvey90")
    
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()
    
    print("Conexão estabelecida com sucesso.")
    return driver

def close_neo4j(driver):
    if driver:
        driver.close()
        print("Conexão fechada com sucesso.")