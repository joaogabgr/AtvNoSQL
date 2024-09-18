import connectMongo from "../database/connectMongo";

const getProductsCollection = async () => {
    const client = await connectMongo();
    const selectDatabase = client.db("MercadoLivre");
    return selectDatabase.collection("products");
};

export default getProductsCollection;