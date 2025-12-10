from app.config.db import SessionLocal, engine, Base
from app.models.rol import Rol
from app.models.usuario import Usuario
from app.models.categoria import Categoria
from app.utils.helpers import hash_password

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Roles
    roles = ["admin", "supervisor", "cajero"]
    for r in roles:
        if not db.query(Rol).filter(Rol.nombre == r).first():
            db.add(Rol(nombre=r))
    db.commit()

    # Usuario admin
    if not db.query(Usuario).filter(Usuario.email=="admin@pos.com").first():
        admin = Usuario(
            nombre="Administrador",
            email="admin@pos.com",
            password_hash=hash_password("admin123"),
            rol_id=db.query(Rol).filter(Rol.nombre=="admin").first().id
        )
        db.add(admin)
        db.commit()

    # Categorías de ejemplo
    categorias = ["Electrónicos","Ropa","Hogar","Deportes","Juguetes","Libros"]
    for cat in categorias:
        if not db.query(Categoria).filter(Categoria.nombre==cat).first():
            db.add(Categoria(nombre=cat))
    db.commit()
    db.close()

if __name__ == "__main__":
    seed()
