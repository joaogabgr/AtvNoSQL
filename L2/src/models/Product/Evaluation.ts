import { ObjectId } from "mongodb";

export default class Evaluation {
    idClient: ObjectId;
    NameClient: string;
    note: number;
    comment: string;
}