# app/utils/jwt.py
import os
import jwt
from datetime import datetime, timedelta

JWT_SECRET = os.getenv("JWT_SECRET", "supersecretkey")
JWT_EXPIRES_IN = int(os.getenv("JWT_EXPIRES_IN", 8 * 3600))  # en segundos, por defecto 8h

def create_access_token(payload: dict, expires_in: int = None) -> str:
    """
    Genera un token JWT con payload y expiración definida.
    """
    expiration = datetime.utcnow() + timedelta(seconds=expires_in or JWT_EXPIRES_IN)
    payload_to_encode = payload.copy()
    payload_to_encode["exp"] = expiration
    token = jwt.encode(payload_to_encode, JWT_SECRET, algorithm="HS256")
    return token

def verify_token(token: str) -> dict:
    """
    Verifica y decodifica un token JWT.
    Lanza excepción si es inválido o expirado.
    """
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        raise Exception("Token expirado")
    except jwt.InvalidTokenError:
        raise Exception("Token inválido")

def decode_token(token: str) -> dict:
    """
    Decodifica el token JWT sin verificar la firma.
    Útil para obtener información rápida sin validar.
    """
    return jwt.decode(token, options={"verify_signature": False})
