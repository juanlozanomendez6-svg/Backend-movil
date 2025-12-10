# app/services/roles_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from app.models.rol import Rol
import logging

logger = logging.getLogger(__name__)

class RolService:

    def get_all_roles(self, db: Session):
        try:
            roles = db.query(Rol).order_by(Rol.id.asc()).all()
            return {"success": True, "data": roles}
        except SQLAlchemyError as e:
            logger.error(f"Error en RolService.get_all_roles: {e}")
            raise HTTPException(status_code=500, detail="Error al obtener roles")

    def get_rol_by_id(self, db: Session, rol_id: int):
        try:
            rol = db.query(Rol).filter(Rol.id == rol_id).first()
            if not rol:
                raise HTTPException(status_code=404, detail="Rol no encontrado")
            return {"success": True, "data": rol}
        except SQLAlchemyError as e:
            logger.error(f"Error en RolService.get_rol_by_id: {e}")
            raise HTTPException(status_code=500, detail="Error al obtener rol")

    def create_rol(self, db: Session, rol_data: dict):
        try:
            rol = Rol(**rol_data)
            db.add(rol)
            db.commit()
            db.refresh(rol)
            return {"success": True, "data": rol, "message": "Rol creado exitosamente"}
        except SQLAlchemyError as e:
            logger.error(f"Error en RolService.create_rol: {e}")
            raise HTTPException(status_code=500, detail="Error al crear rol")


# Instancia única para usar en routers
rol_service = RolService()
