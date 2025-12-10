import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")  # Copia exacta de Atlas
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "posdb")

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    mongo_db = client[MONGO_DB_NAME]
    client.server_info()  # fuerza la conexión
    print("✅ Conexión a MongoDB Atlas establecida correctamente")
except Exception as e:
    print(f"❌ Error conectando a MongoDB Atlas: {e}")
    mongo_db = None

def get_collection(name: str):
    if mongo_db is None:
        raise Exception("MongoDB no está inicializado")
    return mongo_db[name]

inventario_historial_col = get_collection("inventario_historial")
