# app/config/db.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para probar conexión
def test_connection():
    try:
        conn = engine.connect()
        conn.close()
        print("✅ Conexión a PostgreSQL establecida correctamente.")
        return True
    except Exception as e:
        print("❌ Error conectando a la base de datos:", e)
        return False

# Función para sincronizar modelos
def sync_models():
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Modelos sincronizados con la base de datos")
        return True
    except Exception as e:
        print("❌ Error sincronizando modelos:", e)
        return False
