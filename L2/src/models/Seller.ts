import { ObjectId } from "mongodb";
import Address from "./Address";
import Product from "./Product";
import Shopping from "./Shopping";

export default class Seller {
    _id: ObjectId;
    nameSeller: string;
    emailSeller: string;
    ageSeller: number;
    addressSeller: Address;
    productsSeller: Product[];
    salesSeller: Product[];

    constructor(nameSeller: string, emailSeller: string, ageSeller: number, addressSeller: Address) {
        this._id = new ObjectId();
        this.nameSeller = nameSeller;
        this.emailSeller = emailSeller;
        this.ageSeller = ageSeller;
        this.addressSeller = addressSeller;
        this.productsSeller = [];
    }
}
