from menu import show_menu
from controllers.mercadoLivreDB import MercadoLivreDB

def main():
    TOKEN = "AstraCS:fyIJCEQXkwEjObmeqeqZaInm:44c960d3bd9b3a87cd3e2b605739fff3ceeb14acb23af63f5fc9fbca031cff15"
    API_ENDPOINT = "./secure-connect-mercadolivre.zip"  # Caminho para o arquivo de conexão Astra DB
    # API_ENDPOINT = "9f3876e3-09f2-44c9-98ea-3eea980fdf24-us-east-2.apps.astra.datastax.com"

    
    db = MercadoLivreDB(TOKEN, API_ENDPOINT)
    
    # Exibir menu para o usuário
    show_menu(db)

if __name__ == "__main__":
    main()
