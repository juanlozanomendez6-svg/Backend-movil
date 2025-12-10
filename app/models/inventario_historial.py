from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.db import Base

class InventarioHistorial(Base):
    __tablename__ = "inventario_historial"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    cambio = Column(Integer, nullable=False)
    motivo = Column(String(200))
    fecha = Column(DateTime, default=datetime.utcnow)

    producto = relationship("Producto", back_populates="historial")
    usuario = relationship("Usuario", back_populates="inventario_historial")
