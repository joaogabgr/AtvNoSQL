import connectMongo from "../database/connectMongo";

const getSellersCollection = async () => {
    const client = await connectMongo();
    const selectDatabase = client.db("MercadoLivre");
    return selectDatabase.collection("sellers");
};

export default getSellersCollection;