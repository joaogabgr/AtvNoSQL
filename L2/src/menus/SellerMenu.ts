import SellerControllers from "../controllers/sellersControllers";
import Entry from "../io/entry";

export default class SellerMenu extends Entry {
    public static async showMainSellers() {
        let running = true;
        while (running) {
            console.log("1 - Create Seller");
            console.log("2 - List All Sellers");
            console.log("3 - Read Seller");
            console.log("4 - Update Seller");
            console.log("5 - Delete Seller");
            console.log("0 - Back");

            let option = parseInt(Entry.reciveText("Enter the option:"));
            while (isNaN(option) || option < 0 || option > 5) {
                option = parseInt(Entry.reciveText("Enter a valid option (0-5):"));
            }

            switch (option) {
                case 1:
                    await SellerControllers.createSeller();
                    break;
                case 2:
                    await SellerControllers.listAllSellers();
                    break;
                case 3:
                    await SellerControllers.readSeller();
                    break;
                case 4:
                    await SellerControllers.updateSeller();
                    break;
                case 5:
                    await SellerControllers.deleteSeller();
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
