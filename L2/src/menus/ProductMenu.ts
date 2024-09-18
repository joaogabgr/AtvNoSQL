import ProductsControllers from "../controllers/productsControllers";
import Entry from "../io/entry";

export default class ProductMenu extends Entry {
    public static async showMainProducts() {
        let running = true;
        while (running) {
            console.log("1 - Create Product");
            console.log("2 - List All Products");
            console.log("3 - Read Product");
            console.log("4 - Update Product");
            console.log("5 - Delete Product");
            console.log("0 - Back");
            
            let option = parseInt(Entry.reciveText("Enter the option:"));
            while (isNaN(option) || option < 0 || option > 5) {
                option = parseInt(Entry.reciveText("Enter a valid option (0-5):"));
            }

            switch (option) {
                case 1:
                    await ProductsControllers.createProduct();
                    break;
                case 2:
                    await ProductsControllers.listAllProducts();
                    break;
                case 3:
                    await ProductsControllers.readProduct();
                    break;
                case 4:
                    await ProductsControllers.updateProduct();
                    break;
                case 5:
                    await ProductsControllers.deleteProduct();
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