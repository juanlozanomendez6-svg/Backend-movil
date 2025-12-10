# app/main.py
import os
import logging
from importlib import import_module

import uvicorn
from app.config.db import test_connection, sync_models
from app.app import app  # Tu instancia FastAPI


# ================= CONFIGURAR LOGGER =================
logger = logging.getLogger("uvicorn")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


# ================= INICIALIZACIÓN DE BASE DE DATOS =================
def initialize_database():
    """
    Inicializa la base de datos: conexión, sincronización de modelos y seed opcional.
    """
    try:
        connected = test_connection()
        if not connected:
            raise Exception("No se pudo conectar a la base de datos")

        # Sincronizar modelos solo si estás en desarrollo
        if os.getenv("ENVIRONMENT") == "development":
            sync_models()

            # Intentar seed (solo desarrollo)
            try:
                seed_module = import_module("scripts.seed")
                if hasattr(seed_module, "seed_database"):
                    seed_module.seed_database()
                    logger.info("✅ Seed ejecutado correctamente")
            except Exception as seed_error:
                logger.warning(f"⚠️ No se pudo ejecutar seed: {seed_error}")

        return True

    except Exception as error:
        logger.error(f"❌ Error inicializando base de datos: {error}")
        return False


# ================= FUNCION MAIN =================
def main():
    # Inicializar base de datos antes de levantar el server
    if not initialize_database():
        raise SystemExit("❌ Falló la inicialización de la base de datos")

    port = int(os.getenv("PORT", 8000))
    env = os.getenv("ENVIRONMENT", "development")

    logger.info(f"🚀 Backend ejecutándose en puerto {port}")
    logger.info(f"📊 Environment: {env}")

    # Levantar uvicorn usando módulo completo
    uvicorn.run(
        "app.app:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        reload=False  # Importante en producción
    )


# ================= ENTRY POINT =================
if __name__ == "__main__":
    main()
