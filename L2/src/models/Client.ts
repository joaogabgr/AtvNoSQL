import { ObjectId } from "mongodb";
import Address from "./Address";
import Shopping from "./Shopping";
import Product from "./Product";

export default class Client {
    _id: ObjectId;
    nameClient: string;
    emailClient: string;
    ageClient: number;
    addressClient: Address;
    favorites: Product[]
    shopping: Product[];

    constructor(nameClient: string, emailClient: string, ageClient: number, addressClient: Address) {
        this._id = new ObjectId();
        this.nameClient = nameClient;
        this.emailClient = emailClient;
        this.ageClient = ageClient;
        this.addressClient = addressClient;
        this.favorites = [];
    }
}