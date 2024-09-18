import Entry from "../io/entry";
import Address from "../models/Address";
import Client from "../models/Client";
import Product from "../models/Product";
import getClientsCollection from "../repositorys/ClientsRepositorys";
import getProductsCollection from "../repositorys/ProductsRepositorys";
import getSellersCollection from "../repositorys/SellersRepositorys";
import ProductsControllers from "./productsControllers";

export default class ClientsControllers extends Entry {
    public static async createClient() {
        try {
            let name = Entry.reciveText("Enter your name:");
            let email = Entry.reciveText("Enter your email:");

            let age = parseInt(Entry.reciveText("Enter your age:"));
            while (isNaN(age)) {
                age = parseInt(Entry.reciveText("Enter a valid age:"));
            }

            let country = Entry.reciveText("Enter your country:");
            let state = Entry.reciveText("Enter your state:");
            let city = Entry.reciveText("Enter your city:");
            let street = Entry.reciveText("Enter your street:");

            let number = parseInt(Entry.reciveText("Enter your number:"));
            while (isNaN(number)) {
                number = parseInt(Entry.reciveText("Enter a valid number:"));
            }

            let address = new Address(street, number, city, state, country);
            let client = new Client(name, email, age, address);

            const clientsCollection = await getClientsCollection();

            if (await clientsCollection.findOne({ emailClient: client.emailClient })) {
                console.log("Email already exists");
                return;
            }

            await clientsCollection.insertOne(client);
            console.log("Client created successfully");

        } catch (error) {
            console.error("Error creating client:", error);
        }
    }

    public static async listAllClients() {
        try {
            const clientsCollection = await getClientsCollection();
            const clients = await clientsCollection.find().toArray();
            clients.forEach((client) => {
                console.log(`Client: ${client.nameClient} (${client.emailClient})`);
            });

            return clients;

        } catch (error) {
            console.error("Error listing clients:", error);
        }
    }

    public static async listClientByIndex() {
        try {
            const clientsCollection = await getClientsCollection();
            let clients = await clientsCollection.find().toArray();
            clients.forEach((client, index) => {
                console.log(`Client ${index + 1}: ${client.nameClient} (${client.emailClient})`);
            });

            let indexClient = parseInt(Entry.reciveText("Enter the client index:"));
            while (isNaN(indexClient) || indexClient < 1 || indexClient > clients.length) {
                indexClient = parseInt(Entry.reciveText("Enter a valid index:"));
            }

            let client = clients[indexClient - 1];
            return client;

        } catch (error) {
            console.error("Error listing client by index:", error);
        }
    }

    public static async readClient() {
        try {
            const clientsCollection = await getClientsCollection();
            let client = await this.listClientByIndex() as Client;
            if (!client) {
                console.log("Client not found");
                return;
            }

            console.log(`Client Details:
            Name: ${client.nameClient}
            Email: ${client.emailClient}
            Age: ${client.ageClient}
            Address: ${client.addressClient.street}, ${client.addressClient.number}, ${client.addressClient.city}, ${client.addressClient.state}, ${client.addressClient.country}`);

            console.log("Favorites:");
            if (client.favorites && client.favorites.length > 0) {
                client.favorites.forEach((product: Product, index) => {
                    console.log(`   Favorite ${index + 1}:`);
                    console.log(`     Product: ${product.nameProduct}`);
                    console.log(`     Price: ${product.priceProduct}`);
                });
            } else {
                console.log("   No favorite products.");
            }

            console.log("Shopping:");
            if (client.shopping && client.shopping.length > 0) {
                client.shopping.forEach((product: Product, index) => {
                    console.log(`   Shopping ${index + 1}:`);
                    console.log(`     Product: ${product.nameProduct}`);
                    console.log(`     Price: ${product.priceProduct}`);
                });
            } else {
                console.log("   No shopping history.");
            }

            console.log("Evaluations:");
            if (client.evaluations && client.evaluations.length > 0) {
                client.evaluations.forEach((evaluation, index) => {
                    console.log(`   Evaluation ${index + 1}:`);
                    console.log(`     Product: ${evaluation.nameProduct}`);
                    console.log(`     Note: ${evaluation.note}`);
                    console.log(`     Comment: ${evaluation.comment}`);
                });
            } else {
                console.log("   No evaluations.");
            }
            
        } catch (error) {
            console.error("Error reading client:", error);
        }
    }

    public static async updateClient() {
        try {
            const clientsCollection = await getClientsCollection();
            let email = Entry.reciveText("Enter the client email:");
            const client = await clientsCollection.findOne({ emailClient: email });
            if (client === null) {
                console.log("Client not found");
                return;
            }

            let name = Entry.reciveText("Enter the new name:");
            let age = parseInt(Entry.reciveText("Enter the new age:"));
            while (isNaN(age)) {
                age = parseInt(Entry.reciveText("Enter a valid age:"));
            }

            let country = Entry.reciveText("Enter the new country:");
            let state = Entry.reciveText("Enter the new state:");
            let city = Entry.reciveText("Enter the new city:");
            let street = Entry.reciveText("Enter the new street:");

            let number = parseInt(Entry.reciveText("Enter the new number:"));
            while (isNaN(number)) {
                number = parseInt(Entry.reciveText("Enter a valid number:"));
            }

            let address = new Address(street, number, city, state, country);
            await clientsCollection.updateOne({ emailClient: email }, { $set: { nameClient: name, ageClient: age, addressClient: address } });
            console.log("Client updated successfully");

        } catch (error) {
            console.error("Error updating client:", error);
        }
    }

    public static async deleteClient() {
        try {
            const clientsCollection = await getClientsCollection();
            let email = Entry.reciveText("Enter the client email:");
            const client = await clientsCollection.findOne({ emailClient: email });
            if (client === null) {
                console.log("Client not found");
                return;
            }

            await clientsCollection.deleteOne({ emailClient: email });
            console.log("Client deleted successfully");

        } catch (error) {
            console.error("Error deleting client:", error);
        }
    }

    public static async addFavoriteProduct() {
        try {
            const clientsCollection = await getClientsCollection();
            let client = await this.listClientByIndex() as Client;
            if (!client) {
                console.log("Client not found");
                return;
            }

            let product = await ProductsControllers.listProductByIndex() as Product;
            if (!product) {
                console.log("Product not found");
                return;
            }

            client.favorites = client.favorites || [];
            client.favorites.push(product);
            await clientsCollection.updateOne({ emailClient: client.emailClient }, { $set: { favorites: client.favorites } });
            console.log("Product added to favorites successfully");
        } catch (error) {
            console.error("Error adding favorite product:", error);
        }
    }

    public static async removeFavoriteProduct() {
        try {
            const clientsCollection = await getClientsCollection();
            let client = await this.listClientByIndex() as Client;
            if (!client) {
                console.log("Client not found");
                return;
            }

            client.favorites.forEach((favorite, index) => {
                console.log(`Favorite ${index + 1}: ${favorite.nameProduct} (${favorite.priceProduct})`);
            });

            let indexFavorite = parseInt(Entry.reciveText("Enter the favorite index:"));
            while (isNaN(indexFavorite) || indexFavorite < 1 || indexFavorite > client.favorites.length) {
                indexFavorite = parseInt(Entry.reciveText("Enter a valid index:"));
            }

            let product = client.favorites[indexFavorite - 1];

            client.favorites = client.favorites.filter((favorite) => favorite._id !== product._id);
            await clientsCollection.updateOne({ emailClient: client.emailClient }, { $set: { favorites: client.favorites } });
            console.log("Product removed from favorites successfully");
        } catch (error) {
            console.error("Error removing favorite product:", error);
        }
    }

    public static async buyProduct() {
        try {
            const clientsCollection = await getClientsCollection();
            const productsCollection = await getProductsCollection();
            const sellersCollection = await getSellersCollection();
            let client = await this.listClientByIndex() as Client;
            if (!client) {
                console.log("Client not found");
                return;
            }

            let product = await ProductsControllers.listProductByIndex() as Product;
            if (!product) {
                console.log("Product not found");
                return;
            }

            if (product.stockProduct === 0) {
                console.log("Product out of stock");
                return;
            }

            let seller = await sellersCollection.findOne({ emailSeller: product.seller.emailSeller });

            product.stockProduct--;
            await productsCollection.updateOne({ _id: product._id }, { $set: { stockProduct: product.stockProduct } });

            client.shopping = client.shopping || [];
            client.shopping.push(product);

            seller.salesSeller = seller.salesSeller || [];
            seller.salesSeller.push(product);
            await sellersCollection.updateOne({
                emailSeller: seller.emailSeller
            }, {
                $set: {
                    salesSeller: seller.salesSeller
                }
            });

            await clientsCollection.updateOne({ emailClient: client.emailClient }, { $set: { shopping: client.shopping } });
            console.log("Product bought successfully");
        } catch (error) {
            console.error("Error buying product:", error);
        }
    }
}
