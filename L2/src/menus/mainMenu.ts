import Entry from "../io/entry";
import ClientMenu from "./ClientMenu";
import ProductMenu from "./ProductMenu";
import SellerMenu from "./SellerMenu";

export default class MainMenu extends Entry {
    public static async showMainMenu() {
        let running = true;
        while (running) {
            console.log("1 - Products");
            console.log("2 - Sellers");
            console.log("3 - Clients");
            console.log("0 - Exit");
            
            let option = parseInt(Entry.reciveText("Enter the option:"));
            while (isNaN(option) || option < 0 || option > 3) {
                option = parseInt(Entry.reciveText("Enter a valid option (0-3):"));
            }

            switch (option) {
                case 1:
                    await ProductMenu.showMainProducts();
                    break;
                case 2:
                    await SellerMenu.showMainSellers();
                    break;
                case 3:
                    await ClientMenu.showMainClients();
                    break;
                case 0:
                    running = false;
                    break;
                default:
                    console.log("Invalid option");
            }
        }
    }
}
