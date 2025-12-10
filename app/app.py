# app/app.py
import os
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

# -------------------
# Routers
# -------------------
from app.routes.auth_routes import router as auth_router
from app.routes.usuarios_routes import usuarios_router
from app.routes.productos_routes import productos_router
from app.routes.producto_imagen_routes import producto_imagen_router
from app.routes.categorias_routes import router as categorias_router
from app.routes.ventas_routes import router as ventas_router
from app.routes.inventario_routes import router as inventario_router
from app.routes.roles_routes import router as roles_router


# =====================
# INSTANCIA FASTAPI
# =====================
app = FastAPI(
    title="POS API",
    version="1.0.0"
)

# =====================
# CORS
# =====================
allowed_origins = os.getenv("FRONTEND_URL", "http://localhost:19006")

# Permite múltiples URLs separadas por coma
allowed_origins = [origin.strip() for origin in allowed_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# =====================
# GZIP
# =====================
app.add_middleware(GZipMiddleware, minimum_size=1000)


# =====================
# HEALTH CHECK
# =====================
@app.get("/health")
async def health_check():
    """
    Verifica que el servidor está activo.
    """
    return {
        "success": True,
        "message": "🚀 Servidor POS funcionando correctamente",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": os.getenv("ENVIRONMENT", "development")
    }


# =====================
# RUTAS PRINCIPALES
# =====================
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(usuarios_router, prefix="/api/usuarios", tags=["usuarios"])
app.include_router(productos_router, prefix="/api/productos", tags=["productos"])
app.include_router(producto_imagen_router, prefix="/api/productos", tags=["imagenes"])
app.include_router(categorias_router, prefix="/api/categorias", tags=["categorias"])
app.include_router(ventas_router, prefix="/api/ventas", tags=["ventas"])
app.include_router(inventario_router, prefix="/api/inventario", tags=["inventario"])
app.include_router(roles_router, prefix="/api/roles", tags=["roles"])


# =====================
# MANEJO GLOBAL DE ERRORES
# =====================
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": f"Ruta no encontrada: {request.url}"
        }
    )


@app.exception_handler(Exception)
async def global_error_handler(request: Request, exc):
    """
    Manejo global de errores sin exponer stacktrace en producción.
    """
    env = os.getenv("ENVIRONMENT", "development")

    error_message = str(exc) if env == "development" else "Error interno del servidor"

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": error_message
        }
    )
