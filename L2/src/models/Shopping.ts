import { ObjectId } from "mongodb";

export default class Shopping {
    idProduct: ObjectId;
    NameProduct: string;
    PriceProduct: number;
    QuantityProduct: number;
    TotalPrice: number;
}