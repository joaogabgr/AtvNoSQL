import ClientsControllers from "../controllers/clientsControllers";
import ProductsControllers from "../controllers/productsControllers";
import Entry from "../io/entry";
import Product from "../models/Product";

export default class ClientMenu extends Entry {
    public static async showMainClients() {
        let running = true;
        while (running) {
            console.log("1 - Create Client");
            console.log("2 - List All Clients");
            console.log("3 - Read Client");
            console.log("4 - Update Client");
            console.log("5 - Delete Client");
            console.log("6 - Add favorite product");
            console.log("7 - Remove favorite product");
            console.log("8 - Buy product");
            console.log("9 - Add evaluation");
            console.log("10 - Remove evaluation");
            
            console.log("0 - Back");
            
            let option = parseInt(Entry.reciveText("Enter the option:"));
            while (isNaN(option) || option < 0 || option > 10) {
                option = parseInt(Entry.reciveText("Enter a valid option (0-10):"));
            }

            switch (option) {
                case 1:
                    await ClientsControllers.createClient();
                    break;
                case 2:
                    await ClientsControllers.listAllClients();
                    break;
                case 3:
                    await ClientsControllers.readClient();
                    break;
                case 4:
                    await ClientsControllers.updateClient();
                    break;
                case 5:
                    await ClientsControllers.deleteClient();
                    break;
                case 6:
                    await ClientsControllers.addFavoriteProduct();
                    break;
                case 7:
                    await ClientsControllers.removeFavoriteProduct();
                    break;
                case 8:
                    await ClientsControllers.buyProduct();
                    break;
                case 9:
                    await ProductsControllers.addEvaluation();
                    break;
                case 10:
                    await ProductsControllers.removeEvaluation();
                case 0:
                    running = false;
                    break;
                default:
                    console.log("Invalid option");
            }
        }
    }
}
