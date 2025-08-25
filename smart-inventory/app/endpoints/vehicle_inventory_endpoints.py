from app.utiles.decoratores import handle_exceptions
from fastapi import APIRouter
from app.services.vehicle_inventory_service import mark_dispatch_received_service
from app.models.inventory import DispatchReceiveRequest

router = APIRouter(tags=["Vehicle Inventory Management"])

@handle_exceptions
@router.put("/mark_dispatch_received", response_model=dict)
async def mark_dispatch_received(request: DispatchReceiveRequest):
    return await mark_dispatch_received_service(request.dispatch_id)
