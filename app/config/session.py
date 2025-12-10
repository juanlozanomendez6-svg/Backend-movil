# app/config/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.db import DATABASE_URL  # tu URL de la DB

# Crear engine
engine = create_engine(DATABASE_URL, echo=True)

# Crear SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
