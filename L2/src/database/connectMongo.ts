import { MongoClient, ServerApiVersion } from 'mongodb';

const uri = "mongodb+srv://joaoggbs62:gZ8PatNu0bI3lHOb@cluster0.wqjd7lm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";

// Criar um novo cliente MongoDB
const client = new MongoClient(uri, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    deprecationErrors: true,
  }
});

async function connectMongo() {
  try {
    await client.connect();
    return client;
  } catch (e) {
    console.error("Erro ao conectar ao MongoDB", e);
    throw e;
  }
}

export default connectMongo;
