# app/services/categorias_service.py
from sqlalchemy.orm import Session
from app.models.categoria import Categoria
from app.models.producto import Producto
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class CategoriaService:

    def get_all_categorias(self, db: Session):
        try:
            categorias = db.query(Categoria).order_by(Categoria.nombre.asc()).all()
            return {"success": True, "data": categorias}
        except Exception as e:
            logger.error(f"Error en CategoriaService.get_all_categorias: {e}")
            raise HTTPException(status_code=500, detail="Error al obtener categorías")

    def get_categoria_by_id(self, db: Session, id: int):
        try:
            categoria = db.query(Categoria).filter(Categoria.id == id).first()
            if not categoria:
                raise HTTPException(status_code=404, detail="Categoría no encontrada")
            # incluir productos relacionados
            categoria.productos  # accede a la relación para cargar los productos
            return {"success": True, "data": categoria}
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Error en CategoriaService.get_categoria_by_id: {e}")
            raise HTTPException(status_code=500, detail="Error al obtener categoría")

    def create_categoria(self, db: Session, categoria_data: dict):
        try:
            categoria = Categoria(**categoria_data)
            db.add(categoria)
            db.commit()
            db.refresh(categoria)
            return {"success": True, "data": categoria, "message": "Categoría creada exitosamente"}
        except Exception as e:
            logger.error(f"Error en CategoriaService.create_categoria: {e}")
            raise HTTPException(status_code=500, detail="Error al crear categoría")

    def update_categoria(self, db: Session, id: int, categoria_data: dict):
        try:
            categoria = db.query(Categoria).filter(Categoria.id == id).first()
            if not categoria:
                raise HTTPException(status_code=404, detail="Categoría no encontrada")
            
            for key, value in categoria_data.items():
                setattr(categoria, key, value)

            db.commit()
            db.refresh(categoria)
            return {"success": True, "data": categoria, "message": "Categoría actualizada exitosamente"}
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Error en CategoriaService.update_categoria: {e}")
            raise HTTPException(status_code=500, detail="Error al actualizar categoría")

    def delete_categoria(self, db: Session, id: int):
        try:
            categoria = db.query(Categoria).filter(Categoria.id == id).first()
            if not categoria:
                raise HTTPException(status_code=404, detail="Categoría no encontrada")
            
            # Verificar productos asociados
            if len(categoria.productos) > 0:
                raise HTTPException(status_code=400, detail="No se puede eliminar categoría con productos asociados")
            
            db.delete(categoria)
            db.commit()
            return {"success": True, "message": "Categoría eliminada exitosamente"}
        except HTTPException as e:
            raise e
        except Exception as e:
            logger.error(f"Error en CategoriaService.delete_categoria: {e}")
            raise HTTPException(status_code=500, detail="Error al eliminar categoría")


# Instancia única para usar en los routers
categoria_service = CategoriaService()
