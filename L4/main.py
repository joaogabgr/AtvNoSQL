from menu import exibir_menu
from controllers.mercadoLivreDB import MercadoLivreDB

def main():
    TOKEN = "AstraCS:fyIJCEQXkwEjObmeqeqZaInm:44c960d3bd9b3a87cd3e2b605739fff3ceeb14acb23af63f5fc9fbca031cff15"
    PONTO_FINAL_API = "./secure-connect-mercadolivre.zip"
    db = MercadoLivreDB(TOKEN, PONTO_FINAL_API)
    exibir_menu(db)

if __name__ == "__main__":
    main()
