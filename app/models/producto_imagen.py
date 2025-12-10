from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.db import Base

class ProductoImagen(Base):
    __tablename__ = "producto_imagen"
    
    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey('productos.id', ondelete='CASCADE'), nullable=False)
    url = Column(Text, nullable=False)
    descripcion = Column(Text, nullable=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relación inversa con Producto
    producto = relationship("Producto", back_populates="imagenes")
