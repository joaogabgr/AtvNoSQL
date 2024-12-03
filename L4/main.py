from menu import exibir_menu
from controllers.mercadoLivreDB import MercadoLivreDB

def main():
    TOKEN = "AstraCS:sRuYgQDrwgkaodrYydbolRCU:334b695a57043cbdbaeee660aca4f661d223e59fbccd7306ffdeabfe2a0249cb"
    PONTO_FINAL_API = "./secure-connect-mercadolivre.zip"
    db = MercadoLivreDB(TOKEN, PONTO_FINAL_API)
    exibir_menu(db)

if __name__ == "__main__":
    main()
