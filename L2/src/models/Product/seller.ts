import { ObjectId } from "mongodb";

export default class SellerProduct {
    idSeller: ObjectId;
    nameSeller: string;
    emailSeller: string;

    constructor(idSeller: ObjectId, nameSeller: string, emailSeller: string) {
        this.idSeller = idSeller;
        this.nameSeller = nameSeller;
        this.emailSeller = emailSeller;
    }
}