# app/utils/jwt.py

import os
import jwt
from datetime import datetime, timedelta

# =========================
# CONFIGURACIÓN DEL JWT
# =========================
JWT_SECRET = os.getenv("JWT_SECRET", "supersecretkey")
JWT_EXPIRES_IN = int(os.getenv("JWT_EXPIRES_IN", 8 * 3600))  # 8 horas por defecto


# =========================
# GENERAR TOKEN
# =========================
def create_access_token(payload: dict, expires_in: int = None) -> str:
    """
    Genera un token JWT con el payload proporcionado.
    """
    expiration = datetime.utcnow() + timedelta(
        seconds=expires_in or JWT_EXPIRES_IN
    )

    payload_to_encode = payload.copy()
    payload_to_encode["exp"] = expiration

    token = jwt.encode(
        payload_to_encode,
        JWT_SECRET,
        algorithm="HS256"
    )

    return token


# =========================
# VERIFICAR TOKEN
# =========================
def verify_token(token: str) -> dict:
    """
    Verifica un token JWT y retorna su contenido.
    Lanza excepciones si el token expiró o es inválido.
    """
    try:
        decoded = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=["HS256"]
        )
        return decoded

    except jwt.ExpiredSignatureError:
        raise Exception("Token expirado")

    except jwt.InvalidTokenError:
        raise Exception("Token inválido")


# =========================
# DECODIFICAR SIN VALIDAR
# =========================
def decode_token(token: str) -> dict:
    """
    Decodifica token sin validar su firma.
    Útil para obtener información sin verificar autenticidad.
    """
    return jwt.decode(token, options={"verify_signature": False})
