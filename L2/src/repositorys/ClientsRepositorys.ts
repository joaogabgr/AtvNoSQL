import connectMongo from "../database/connectMongo";

async function getClientsCollection() {
  const client = await connectMongo();
  const selectDatabase = client.db("MercadoLivre");
  return selectDatabase.collection("clients");
}

export default getClientsCollection;
