import Entry from "../io/entry";
import Address from "../models/Address";
import Product from "../models/Product";
import Seller from "../models/Seller";
import getSellersCollection from "../repositorys/SellersRepositorys";

export default class SellerControllers extends Entry {
    public static async createSeller() {
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
            let seller = new Seller(name, email, age, address);

            const sellersCollection = await getSellersCollection();

            if (await sellersCollection.findOne({ emailSeller: seller.emailSeller })) {
                console.log("Email already exists");
                return;
            }

            await sellersCollection.insertOne(seller);
            console.log("Seller created successfully");

        } catch (error) {
            console.error("Error creating seller:", error);
        }
    }

    public static async listAllSellers() {
        try {
            const sellersCollection = await getSellersCollection();
            const sellers = await sellersCollection.find().toArray();
            sellers.forEach((seller) => {
                console.log(`Seller: ${seller.nameSeller} (${seller.emailSeller})`);
            });
            return sellers;

        } catch (error) {
            console.error("Error listing all sellers:", error);
        }
    }

    public static async listSellerByIndex() {
        try {
            const sellersCollection = await getSellersCollection();
            let sellers = await sellersCollection.find().toArray();
            sellers.forEach((seller, index) => {
                console.log(`Seller ${index + 1}: ${seller.nameSeller} (${seller.emailSeller})`);
            });

            let indexSeller = parseInt(Entry.reciveText("Enter the seller index:"));
            while (isNaN(indexSeller) || indexSeller < 1 || indexSeller > sellers.length) {
                indexSeller = parseInt(Entry.reciveText("Enter a valid seller index:"));
            }

            let seller = sellers[indexSeller - 1];
            return seller;

        } catch (error) {
            console.error("Error listing seller by index:", error);
        }
    }

    public static async readSeller() {
        try {
            const sellersCollection = await getSellersCollection();
            const seller = await this.listSellerByIndex();
            if (!seller) {
                console.log("Seller not found");
                return;
            }

            console.log(`Name: ${seller.nameSeller}`);
            console.log(`Email: ${seller.emailSeller}`);
            console.log(`Age: ${seller.ageSeller}`);
            console.log(`Address: ${seller.addressSeller.street}, ${seller.addressSeller.number}, ${seller.addressSeller.city}, ${seller.addressSeller.state}, ${seller.addressSeller.country}`);
            console.log("Sales:");
            seller.salesSeller.forEach((sale: Product, index) => {
                console.log(`  Sale ${index + 1}:`);
                console.log(`    Product: ${sale.nameProduct}`);
                console.log(`    Amount: ${sale.priceProduct}`);
            });

        } catch (error) {
            console.error("Error reading seller:", error);
        }
    }

    public static async updateSeller() {
        try {
            const sellersCollection = await getSellersCollection();
            const seller = await this.listSellerByIndex();
            if (!seller) {
                console.log("Seller not found");
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
            let newSeller = new Seller(name, seller.emailSeller, age, address);
            await sellersCollection.updateOne({ emailSeller: seller.emailSeller }, { $set: newSeller });
            console.log("Seller updated successfully");

        } catch (error) {
            console.error("Error updating seller:", error);
        }
    }

    public static async deleteSeller() {
        try {
            const sellersCollection = await getSellersCollection();
            let email = Entry.reciveText("Enter the seller's email:");
            const seller = await sellersCollection.findOne({ emailSeller: email });
            if (!seller) {
                console.log("Seller not found");
                return;
            }

            await sellersCollection.deleteOne({ emailSeller: email });
            console.log("Seller deleted successfully");

        } catch (error) {
            console.error("Error deleting seller:", error);
        }
    }

}
