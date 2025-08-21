# app/endpoints/inventory_endpoints.py
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.models.inventory import RegisterInventory, UpdateInventory, DispatchRequest
from app.services.inventory_service import register_inventory, update_inventory, dispatch_inventory ,list_inventory_batches,list_products_in_hub
from app.utiles.decoratores import handle_exceptions

router = APIRouter()

# -----------------------------
# Register new inventory / add batch
# -----------------------------
@router.post("/register", status_code=201)
@handle_exceptions
async def register_inventory_endpoint(payload: RegisterInventory):
    try:
        res = await register_inventory(payload)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# -----------------------------
# Update existing inventory
# -----------------------------
@router.put("/update")
@handle_exceptions
async def update_inventory_endpoint(payload: UpdateInventory):
    try:
        res = await update_inventory(payload)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# -----------------------------
# Dispatch stock from one hub to another
# -----------------------------
@router.post("/dispatch")
@handle_exceptions
async def dispatch_inventory_endpoint(payload: DispatchRequest):
    try:
        res = await dispatch_inventory(payload)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# -----------------------------
# Extra endpoint: product summary
# -----------------------------
@router.get("/summary")
@handle_exceptions
async def product_summary_endpoint(
    product_id: str = Query(..., description="Product ID"),
    hub_id: str = Query(..., description="Hub ID")
):
    from app.services.inventory_service import get_product_summary
    try:
        res = await get_product_summary(product_id, hub_id)
        return res
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))



@router.get("/batches")
@handle_exceptions
async def list_inventory_batches_endpoint(
    product_id: str,
    hub_id: str,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 50
):
    return await list_inventory_batches(product_id, hub_id, status, skip, limit)


@router.get("/products")
@handle_exceptions
async def list_products_in_hub_endpoint(
    hub_id: str,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50
):
    return await list_products_in_hub(hub_id, search, skip, limit)
