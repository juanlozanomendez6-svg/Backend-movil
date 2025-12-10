# app/utils/helpers.py
import bcrypt
from datetime import datetime
import random
import string
import locale

# Configurar locale para México
locale.setlocale(locale.LC_ALL, 'es_MX.UTF-8')

# Hash de contraseña
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=10)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# Verificar contraseña
def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# Formatear moneda MXN
def format_currency(amount: float) -> str:
    return locale.currency(amount, grouping=True)

# Generar código de venta
def generate_sale_code() -> str:
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    return f"V{int(datetime.now().timestamp()*1000)}{random_str}"
