import { ObjectId } from "mongodb";
import Entry from "../io/entry";
import Client from "../models/Client";
import Product from "../models/Product";
import getClientsCollection from "../repositorys/ClientsRepositorys";
import bcrypt from 'bcrypt';
import Address from "../models/Address";

export default class ClientsControllers extends Entry {
    public static async createClient() {
        try {
            let name = Entry.reciveText("Enter your name:");
            let email = Entry.reciveText("Enter your email:");
            let password = Entry.reciveText("Enter your password:");
            let confirmPassword = Entry.reciveText("Confirm your password:");

            // Verifica se as senhas coincidem
            while (password !== confirmPassword) {
                console.log("Passwords do not match");
                password = Entry.reciveText("Enter your password:");
                confirmPassword = Entry.reciveText("Confirm your password:");
            }

            // Hash da senha
            const hash = await bcrypt.hash(password, 10);

            // Captura idade
            let age = parseInt(Entry.reciveText("Enter your age:"));
            while (isNaN(age)) {
                age = parseInt(Entry.reciveText("Enter a valid age:"));
            }

            // Captura endereço
            let country = Entry.reciveText("Enter your country:");
            let state = Entry.reciveText("Enter your state:");
            let city = Entry.reciveText("Enter your city:");
            let street = Entry.reciveText("Enter your street:");
            let number = parseInt(Entry.reciveText("Enter your number:"));
            while (isNaN(number)) {
                number = parseInt(Entry.reciveText("Enter a valid number:"));
            }

            // Criação do objeto de endereço e cliente
            let address = new Address(street, number, city, state, country);
            let client = new Client(name, email, hash, age, address); // Usar o hash da senha

            const clientsCollection = await getClientsCollection();

            // Verifica se o email já existe
            if (await clientsCollection.findOne({ emailClient: client.emailClient })) {
                console.log("Email already exists");
                return;
            }

            // Insere o cliente na coleção
            await clientsCollection.insertOne(client);
            console.log("Client created successfully");

        } catch (error) {
            console.error("Error creating client:", error);
        }
    }
}
