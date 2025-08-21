# app/endpoints/hub_endpoints.py
from fastapi import APIRouter, HTTPException, Query
from app.models.hub import RegisterHub, UpdateHub
from app.services.hub_service import (
    create_hub, update_hub, delete_hub,
    search_hub, list_closed_hubs, list_by_status
)
from app.utiles.decoratores import handle_exceptions  # your decorator
from typing import Optional
 
router = APIRouter()
 
@router.post("/register", status_code=201)
@handle_exceptions
async def register_hub(payload: RegisterHub):
    try:
        res = await create_hub(payload)
        return res
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
 
 
@router.put("/update/{hub_id}")
@handle_exceptions
async def update_hub_endpoint(hub_id: str, payload: UpdateHub):
    try:
        res = await update_hub(hub_id, payload)
        return res
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
 
 
@router.delete("/delete/{hub_id}")
@handle_exceptions
async def delete_hub_endpoint(hub_id: str, hub_name: str, hub_manager: Optional[str] = None):
    try:
        res = await delete_hub(hub_id, hub_name, hub_manager)
        return res
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
 
 
@router.get("/search")
@handle_exceptions
async def search_hub_endpoint(hub_id: Optional[str] = Query(None), hub_name: Optional[str] = Query(None), skip: int = 0, limit: int = 50):
    if not hub_id and not hub_name:
        # return all (paginated) or raise depending on your rule
        results = await search_hub(None, None, skip, limit)
        return {"hubs": results}
    results = await search_hub(hub_id, hub_name, skip, limit)
    return {"hubs": results}
 
 
@router.get("/closed")
@handle_exceptions
async def closed_hubs_endpoint(skip: int = 0, limit: int = 50):
    res = await list_closed_hubs(skip, limit)
    return {"closed_hubs": res}
 
 
@router.get("/status")
@handle_exceptions
async def hubs_by_status_endpoint(status: str = Query(...), skip: int = 0, limit: int = 50):
    try:
        res = await list_by_status(status, skip, limit)
        return {"hubs": res}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))