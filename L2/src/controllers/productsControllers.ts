import Entry from "../io/entry";
import Product from "../models/Product";
import Seller from "../models/Seller";
import SellerProduct from "../models/Product/seller";
import getProductsCollection from "../repositorys/ProductsRepositorys";
import getSellersCollection from "../repositorys/SellersRepositorys";
import getClientsCollection from "../repositorys/ClientsRepositorys";
import ClientsControllers from "./clientsControllers";
import Evaluation from "../models/Product/Evaluation";

export default class ProductsControllers extends Entry {
    
    public static async createProduct() {
        try {
            const sellersCollection = await getSellersCollection();
            const productsCollection = await getProductsCollection();

            const sellers = await sellersCollection.find().toArray();
            sellers.forEach((seller, index) => {
                console.log(`Seller ${index + 1}: ${seller.nameSeller} (${seller.emailSeller})`);
            });

            let indexSeller = parseInt(Entry.reciveText("Enter the seller index:"));
            while (isNaN(indexSeller) || indexSeller < 1 || indexSeller > sellers.length) {
                indexSeller = parseInt(Entry.reciveText("Enter a valid seller index:"));
            }

            const seller = sellers[indexSeller - 1] as Seller;
            const sellerProduct = new SellerProduct(seller._id, seller.nameSeller, seller.emailSeller);

            const name = Entry.reciveText("Enter the product name:");
            let price = parseFloat(Entry.reciveText("Enter the product price:"));
            while (isNaN(price)) {
                price = parseFloat(Entry.reciveText("Enter a valid product price:"));
            }

            let stock = parseInt(Entry.reciveText("Enter the product stock:"));
            while (isNaN(stock)) {
                stock = parseInt(Entry.reciveText("Enter a valid product stock:"));
            }

            const product = new Product(name, price, stock, sellerProduct);
            await productsCollection.insertOne(product);

            seller.productsSeller.push(product);
            await sellersCollection.updateOne({ emailSeller: seller.emailSeller }, { $set: { productsSeller: seller.productsSeller } });

            console.log("Product created successfully");

        } catch (error) {
            console.error("Error creating product:", error);
        }
    }

    public static async listAllProducts() {
        try {
            const productsCollection = await getProductsCollection();
            const products = await productsCollection.find().toArray();
            products.forEach((product) => {
                console.log(`Product: ${product.nameProduct} (${product.priceProduct})`);
            });
            return products;

        } catch (error) {
            console.error("Error listing products:", error);
        }
    }

    public static async listProductByIndex() {
        try {
            const productsCollection = await getProductsCollection();
            const products = await productsCollection.find().toArray();
            products.forEach((product, index) => {
                console.log(`Product ${index + 1}: ${product.nameProduct} (${product.priceProduct})`);
            });

            let indexProduct = parseInt(Entry.reciveText("Enter the product index:"));
            while (isNaN(indexProduct) || indexProduct < 1 || indexProduct > products.length) {
                indexProduct = parseInt(Entry.reciveText("Enter a valid product index:"));
            }

            const product = products[indexProduct - 1];
            return product;

        } catch (error) {
            console.error("Error listing product by index:", error);
        }
    }

    public static async readProduct() {
        try {
            const product = await this.listProductByIndex();
            if (!product) {
                console.log("Product not found");
                return;
            }
            console.log(`Product Details:
            Name: ${product.nameProduct}
            Price: ${product.priceProduct}
            Stock: ${product.stockProduct}
            Seller: ${product.seller.nameSeller} (${product.seller.emailSeller})`);

            if (product.evaluation && product.evaluation.length > 0) {
                console.log("Evaluations:");
                product.evaluation.forEach((evaluation: Evaluation, index) => {
                    console.log(`  Evaluation ${index + 1}:
                    Client: ${evaluation.NameClient}
                    Note: ${evaluation.note}
                    Comment: ${evaluation.comment}`);
                });
            } else {
                console.log("No evaluations found for this product.");
            }

        } catch (error) {
            console.error("Error reading product:", error);
        }
    }

    public static async updateProduct() {
        try {
            const productsCollection = await getProductsCollection();
            const sellersCollection = await getSellersCollection();
            const clientsCollection = await getClientsCollection();

            const product = await this.listProductByIndex();
            if (!product) {
                console.log("Product not found");
                return;
            }

            const name = Entry.reciveText("Enter the new product name:");
            let price = parseFloat(Entry.reciveText("Enter the new product price:"));
            while (isNaN(price)) {
                price = parseFloat(Entry.reciveText("Enter a valid product price:"));
            }

            let stock = parseInt(Entry.reciveText("Enter the new product stock:"));
            while (isNaN(stock)) {
                stock = parseInt(Entry.reciveText("Enter a valid product stock:"));
            }

            product.nameProduct = name;
            product.priceProduct = price;
            product.stockProduct = stock;

            await productsCollection.updateOne({ _id: product._id }, { $set: product });

            const seller = await sellersCollection.findOne({ emailSeller: product.seller.emailSeller });
            if (seller) {
                const productIndex = seller.productsSeller.findIndex((p) => p._id.equals(product._id));
                if (productIndex !== -1) {
                    seller.productsSeller[productIndex] = product;
                    await sellersCollection.updateOne({ emailSeller: seller.emailSeller }, { $set: { productsSeller: seller.productsSeller } });
                }
            }

            await clientsCollection.updateMany(
                { "favorites._id": product._id },
                { $set: { "favorites.$": product } }
            );

            console.log("Product updated successfully");

        } catch (error) {
            console.error("Error updating product:", error);
        }
    }

    public static async deleteProduct() {
        try {
            const productsCollection = await getProductsCollection();
            const sellersCollection = await getSellersCollection();
            const clientsCollection = await getClientsCollection();
    
            const product = await this.listProductByIndex() as Product;
            if (!product) {
                console.log("Product not found");
                return;
            }
    
            const seller = await sellersCollection.findOne({ emailSeller: product.seller.emailSeller });
            if (seller) {
                seller.productsSeller = seller.productsSeller.filter((p) => !p._id.equals(product._id));
                await sellersCollection.updateOne({ emailSeller: seller.emailSeller }, { $set: { productsSeller: seller.productsSeller } });
            }
    
            await clientsCollection.updateMany(
                { "favorites._id": product._id },
                { $pull: { favorites: { _id: product._id } } } as any
            );
    
            await productsCollection.deleteOne({ _id: product._id });
            console.log("Product deleted successfully");
    
        } catch (error) {
            console.error("Error deleting product:", error);
        }
    }    

    public static async addEvaluation() {
        try {
            const productsCollection = await getProductsCollection();
            const clientsCollection = await getClientsCollection();
            const clients = await ClientsControllers.listClientByIndex();
            if (!clients) {
                console.log("Client not found");
                return;
            }

            const product = await this.listProductByIndex() as Product;
            if (!product) {
                console.log("Product not found");
                return;
            }

            let evaluation = parseFloat(Entry.reciveText("Enter the evaluation:"));
            while (isNaN(evaluation) || evaluation < 0 || evaluation > 5) {
                evaluation = parseFloat(Entry.reciveText("Enter a valid evaluation (0-5):"));
            }
            let comment = Entry.reciveText("Enter the comment:");
            let evaluationClient = { idClient: clients._id, NameClient: clients.nameClient, note: evaluation, comment: comment };

            product.evaluation = product.evaluation || [];
            product.evaluation.push(evaluationClient);
            await productsCollection.updateOne({ _id: product._id }, { $set: { evaluation: product.evaluation } });
            console.log("Evaluation added successfully");
        } catch (error) {
            console.error("Error adding evaluation:", error);
        }
    }
}
