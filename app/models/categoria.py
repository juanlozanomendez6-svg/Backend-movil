from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.config.db import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)

    # Relación con productos
    productos = relationship("Producto", back_populates="categoria")
