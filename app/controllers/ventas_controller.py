from app.services.ventas_service import venta_service
from sqlalchemy.orm import Session

def get_all_sales(db: Session, filters: dict = {}):
    return venta_service.get_all_ventas(db, filters)["data"]

def get_sale_by_id(db: Session, venta_id: int):
    return venta_service.get_venta_by_id(db, venta_id)["data"]

def create_sale(usuario_id: int, detalles: list, db: Session):
    return venta_service.create_venta(db, usuario_id, detalles)["data"]

def get_sales_report(db: Session, fecha_inicio: str, fecha_fin: str):
    return venta_service.get_ventas_por_periodo(db, fecha_inicio, fecha_fin)["data"]
