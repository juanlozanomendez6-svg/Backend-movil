# app/utils/helpers.py

import bcrypt
from datetime import datetime
import random
import string

# ============================
# HASH DE CONTRASEÑA
# ============================
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=10)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# ============================
# FORMATEAR MONEDA MXN (SIN locale)
# ============================
def format_currency(amount: float) -> str:
    """
    Formatea un número como moneda MXN sin usar locales,
    para evitar errores en Railway u otros servidores.
    Ejemplo: 12345.6 -> $12,345.60
    """
    return f"${amount:,.2f}"

# ============================
# GENERAR CÓDIGO DE VENTA
# ============================
def generate_sale_code() -> str:
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    timestamp = int(datetime.now().timestamp() * 1000)
    return f"V{timestamp}{random_str}"
