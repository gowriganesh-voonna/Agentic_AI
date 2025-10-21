import logging
from fastapi import APIRouter
from app.utiles.decoratores import handle_exceptions
from app.services.vehicle_inventory_service import mark_dispatch_received_service, get_dispatch_status_service, list_dispatches_service, auto_assign_driver_vehicle_service, fix_existing_dispatches_service
from app.models.inventory import DispatchReceiveRequest

# Configure logger for this module
logger = logging.getLogger(__name__)

# Create API router for Vehicle Inventory Management
router = APIRouter(tags=["Vehicle Inventory Management"])

@handle_exceptions
@router.put("/mark_dispatch_received", response_model=dict)
async def mark_dispatch_received(request: DispatchReceiveRequest):
    """
    Endpoint to mark a dispatched vehicle inventory as received.
    
    Args:
        request (DispatchReceiveRequest): Request body containing the dispatch_id.
        
    Returns:
        dict: Success or error response from the service layer.
    """
    logger.info(f"Received request to mark dispatch as received. Dispatch ID: {request.dispatch_id}")

    try:
        # Call the service layer to update the dispatch status
        response = await mark_dispatch_received_service(request.dispatch_id)
        logger.info(f"Successfully marked dispatch {request.dispatch_id} as received.")
        return response

    except Exception as e:
        # Log the error before letting handle_exceptions decorator manage the exception
        logger.error(f"Error while marking dispatch {request.dispatch_id} as received: {str(e)}", exc_info=True)
        raise


@handle_exceptions
@router.get("/dispatch_status/{dispatch_id}")
async def get_dispatch_status(dispatch_id: str):
    """
    Returns computed dispatch status with driver/vehicle availability messages
    so UI can show precise guidance before assignment.
    """
    logger.info(f"Received request to get dispatch status. Dispatch ID: {dispatch_id}")
    response = await get_dispatch_status_service(dispatch_id)
    logger.info(f"Dispatch status computed for {dispatch_id}")
    return response


@handle_exceptions
@router.get("/dispatches")
async def list_dispatches(skip: int = 0, limit: int = 50):
    """
    List all dispatches with their current status and assignment details.
    """
    logger.info(f"Received request to list dispatches: skip={skip}, limit={limit}")
    response = await list_dispatches_service(skip, limit)
    logger.info(f"Found {len(response.get('dispatches', []))} dispatches")
    return response


@handle_exceptions
@router.post("/auto_assign/{dispatch_id}")
async def auto_assign_driver_vehicle(dispatch_id: str):
    """
    Automatically assign available driver and vehicle to a dispatch.
    """
    logger.info(f"Received request to auto-assign driver and vehicle for dispatch: {dispatch_id}")
    response = await auto_assign_driver_vehicle_service(dispatch_id)
    logger.info(f"Auto-assignment completed for dispatch: {dispatch_id}")
    return response


@handle_exceptions
@router.post("/fix_existing_dispatches")
async def fix_existing_dispatches():
    """
    Fix existing dispatch records that have "In-Progress" values.
    This is a one-time fix for existing data.
    """
    logger.info("Received request to fix existing dispatch records")
    response = await fix_existing_dispatches_service()
    logger.info(f"Fixed {response.get('fixed_count', 0)} dispatch records")
    return response
