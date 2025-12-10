from app.config.database_mongo import get_collection
from app.utils.helpers import hash_password, verify_password
from app.utils.jwt import create_access_token
from fastapi import HTTPException

usuarios_col = get_collection("usuarios")

class UsuarioServiceMongo:

    def register(self, nombre: str, email: str, password: str, rol_id: int = 2):
        # Verificar si el usuario ya existe
        existing = usuarios_col.find_one({"email": email})
        if existing:
            raise HTTPException(status_code=400, detail="El email ya está registrado")

        password_hash = hash_password(password)
        usuario_data = {
            "nombre": nombre,
            "email": email,
            "password_hash": password_hash,
            "rol_id": rol_id,
            "activo": True
        }

        result = usuarios_col.insert_one(usuario_data)
        usuario_data["_id"] = str(result.inserted_id)

        # Crear token
        rol_nombre = "usuario"  # Aquí podrías obtenerlo de otra colección si quieres
        token = create_access_token({"id": usuario_data["_id"], "email": email, "rol": rol_nombre})

        return {"success": True, "data": {"usuario": usuario_data, "token": token}}

    def login(self, email: str, password: str):
        usuario = usuarios_col.find_one({"email": email, "activo": True})
        if not usuario or not verify_password(password, usuario["password_hash"]):
            raise HTTPException(status_code=400, detail="Credenciales inválidas")

        rol_nombre = "usuario"
        token = create_access_token({"id": str(usuario["_id"]), "email": email, "rol": rol_nombre})
        usuario["_id"] = str(usuario["_id"])

        return {"success": True, "data": {"usuario": usuario, "token": token}}

# Instancia única
usuario_service_mongo = UsuarioServiceMongo()
