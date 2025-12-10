from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.controllers.inventario_controller import (
    get_inventory_history,
    register_inventory_movement,
    get_low_stock,
    get_inventory_statistics
)
from app.config.session import get_db
from app.middleware.auth_middleware import require_roles
from app.schemas.inventario import (
    InventarioHistorialResponse,
    StockBajoResponse,
    InventarioEstadisticasResponse
)

# ⚠️ Cambiado a "router" para que coincida con la importación en app.py
router = APIRouter(tags=["inventario"])

# ===============================
#        ENDPOINT RAÍZ
# ===============================
@router.get("/", response_model=dict)
def inventory_root(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin", "supervisor"]))
):
    return {
        "success": True,
        "message": "Endpoints disponibles: /historial, /stock-bajo, /estadisticas, /movimiento"
    }

# ===============================
#        HISTORIAL DE INVENTARIO
# ===============================
@router.get("/historial", response_model=List[InventarioHistorialResponse])
def inventory_history(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin", "supervisor"]))
):
    return get_inventory_history(db)

# ===============================
#        STOCK BAJO
# ===============================
@router.get("/stock-bajo", response_model=List[StockBajoResponse])
def low_stock(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin", "supervisor"]))
):
    return get_low_stock(db)

# ===============================
#        ESTADÍSTICAS DE INVENTARIO
# ===============================
@router.get("/estadisticas", response_model=InventarioEstadisticasResponse)
def inventory_stats(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin", "supervisor"]))
):
    return get_inventory_statistics(db)

# ===============================
#        REGISTRAR MOVIMIENTO DE INVENTARIO
# ===============================
@router.post("/movimiento", response_model=InventarioHistorialResponse)
def register_movement(
    producto_id: int,
    cambio: int,
    motivo: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin", "supervisor"]))
):
    return register_inventory_movement(db, producto_id, current_user.id, cambio, motivo)
