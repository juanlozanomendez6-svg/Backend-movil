# app/main.py
import os
import logging
from importlib import import_module

import uvicorn
from app.config.db import test_connection, sync_models  # tu módulo db con SQLAlchemy
from app.app import app  # tu FastAPI app

# ================= CONFIGURAR LOGGER =================
logger = logging.getLogger("uvicorn")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ================= INICIALIZACIÓN DE BASE DE DATOS =================
def initialize_database():
    """
    Inicializa la base de datos: conexión, sincronización de modelos y seeds opcionales.
    """
    try:
        connected = test_connection()  # ya no es await
        if not connected:
            raise Exception("No se pudo conectar a la base de datos")

        # Sincronizar modelos solo en desarrollo
        if os.getenv("ENVIRONMENT") == "development":
            sync_models()

        # Ejecutar seed opcional
        try:
            seed_module = import_module("scripts.seed")
            if hasattr(seed_module, "seed_database"):
                seed_module.seed_database()
                logger.info("✅ Seed ejecutado correctamente")
        except Exception as seed_error:
            logger.warning(f"⚠️ No se pudo ejecutar seed, continuar sin seed: {seed_error}")

        return True
    except Exception as error:
        logger.error(f"❌ Error inicializando base de datos: {error}")
        return False

# ================= FUNCION MAIN =================
def main():
    # Inicializar la base de datos antes de levantar el servidor
    db_initialized = initialize_database()
    if not db_initialized:
        raise SystemExit("❌ Falló la inicialización de la base de datos")

    port = int(os.getenv("PORT", 8000))
    logger.info(f"🚀 Servidor POS ejecutándose en puerto {port}")
    logger.info(f"📊 Environment: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info(f"🌐 URL: http://localhost:{port}/")
    logger.info(f"🔍 Health: http://localhost:{port}/health")

    # Levantar servidor con uvicorn
    uvicorn.run("app.app:app", host="0.0.0.0", port=port, log_level="info")

# ================= ENTRY POINT =================
if __name__ == "__main__":
    main()
