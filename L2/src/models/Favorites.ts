import { ObjectId } from "mongodb";

export default class Favorites {
    idProduct: ObjectId;
    NameProduct: string;
    PriceProduct: number;
}