# app/middleware/error_middleware.py
import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, DataError
from jose import JWTError

logger = logging.getLogger("uvicorn.error")  # Usa tu propio logger si quieres

async def http_exception_handler(request: Request, exc):
    """
    Maneja errores HTTP personalizados (con status_code).
    """
    logger.error(f"Error: {exc.detail if hasattr(exc, 'detail') else str(exc)}")
    return JSONResponse(
        status_code=getattr(exc, "status_code", 500),
        content={"success": False, "message": str(exc.detail) if hasattr(exc, "detail") else str(exc)}
    )

async def validation_error_handler(request: Request, exc: DataError):
    """
    Maneja errores de validación en SQLAlchemy (equivalente SequelizeValidationError)
    """
    logger.error(f"Validation Error: {exc}")
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": "Error de validación",
            "errors": str(exc)
        }
    )

async def integrity_error_handler(request: Request, exc: IntegrityError):
    """
    Maneja errores de duplicado o constraints (equivalente SequelizeUniqueConstraintError)
    """
    logger.error(f"Integrity Error: {exc}")
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": "El registro ya existe",
            "detail": str(exc.orig)  # mensaje de la BD
        }
    )

async def jwt_error_handler(request: Request, exc: JWTError):
    """
    Maneja errores de JWT
    """
    logger.error(f"JWT Error: {exc}")
    return JSONResponse(
        status_code=401,
        content={"success": False, "message": "Token inválido"}
    )

# Manejo de rutas no encontradas (404)
async def not_found_handler(request: Request, exc):
    logger.warning(f"Ruta no encontrada: {request.method} {request.url.path}")
    return JSONResponse(
        status_code=404,
        content={"success": False, "message": f"Ruta no encontrada: {request.method} {request.url.path}"}
    )
