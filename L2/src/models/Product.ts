import { ObjectId } from "mongodb";
import SellerProduct from "./Product/seller";
import Evaluation from "./Product/Evaluation";

export default class Product {
    _id: ObjectId;
    nameProduct: string;
    priceProduct: number;
    stockProduct: number;
    seller: SellerProduct;
    evaluation: Evaluation[];

    constructor(nameProduct: string, priceProduct: number, stockProduct: number, seller: SellerProduct) {
        this._id = new ObjectId();
        this.nameProduct = nameProduct;
        this.priceProduct = priceProduct;
        this.stockProduct = stockProduct;
        this.seller = seller;
        this.evaluation = [];
    }
}
