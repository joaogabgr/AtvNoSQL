import { ObjectId } from "mongodb";

export default class Evaluation {
    idClient: ObjectId;
    idProduct: ObjectId;
    nameProduct: string;
    NameClient: string;
    note: number;
    comment: string;

    constructor(idClient: ObjectId, idProduct: ObjectId, nameProduct: string, NameClient: string, note: number, comment: string) {
        this.idClient = idClient;
        this.idProduct = idProduct;
        this.nameProduct = nameProduct;
        this.NameClient = NameClient;
        this.note = note;
        this.comment = comment;
    }
}