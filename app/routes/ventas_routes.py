# app/routes/ventas_routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.controllers.ventas_controller import (
    get_all_sales,
    get_sale_by_id,
    create_sale,
    get_sales_report
)

from app.schemas.venta import VentaCreate, VentaResponse
from app.middleware.auth_middleware import require_roles, get_current_user
from app.config.session import get_db

# ⚠️ SIN PREFIX AQUI → ya se agrega en app/app.py
router = APIRouter(tags=["ventas"])

# ===============================
#        LISTAR VENTAS
# ===============================
@router.get("/", response_model=List[VentaResponse])
def list_sales(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    ventas = get_all_sales(db)
    # Devuelve lista vacía si no hay ventas
    return ventas or []

# ===============================
#        OBTENER VENTA POR ID
# ===============================
@router.get("/{venta_id}", response_model=VentaResponse)
def get_sale(
    venta_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    venta = get_sale_by_id(db, venta_id)
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada"
        )
    return venta

# ===============================
#        CREAR VENTA
# ===============================
@router.post("/", response_model=VentaResponse)
def create_new_sale(
    data: VentaCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin", "supervisor"]))
):
    # ⚠️ Cambiado .id por ["id"] porque current_user es un dict
    venta = create_sale(usuario_id=current_user["id"], detalles=data.detalles, db=db)
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo crear la venta"
        )
    return venta

# ===============================
#        REPORTE DE VENTAS
# ===============================
@router.get("/reporte", response_model=dict)
def sales_report(
    fecha_inicio: str,
    fecha_fin: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin", "supervisor"]))
):
    reporte = get_sales_report(db, fecha_inicio, fecha_fin)
    # Devuelve dict vacío si no hay registros
    return reporte or {"data": []}
