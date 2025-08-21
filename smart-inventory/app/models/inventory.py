# app/models/inventory.py
"""
Pydantic schemas and helpers for Inventory Management (MongoDB + Motor async)
- Save as: app/models/inventory.py
- Category: REQUIRED (free-text)
- Batch-wise design with UTC-aware datetimes
"""
 
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Literal, Dict
from datetime import datetime, date, timezone
from uuid import uuid4
 
 
# -----------------------------
# Helpers
# -----------------------------
def utc_now() -> datetime:
    return datetime.now(timezone.utc)
 
 
def generate_batch_no(product_id: str, hub_id: str) -> str:
    """Generates a reasonably unique batch id."""
    ts = utc_now().strftime("%Y%m%d%H%M%S")
    return f"{product_id}-{hub_id}-{ts}-{uuid4().hex[:6]}"
 
 
# -----------------------------
# Request Schemas
# -----------------------------
class RegisterInventory(BaseModel):
    Hub_ID: str = Field(..., description="Hub identifier (must exist)")
    Product_ID: str = Field(..., description="Unique product SKU/ID")
    Product_Name: str = Field(..., description="Product name")
    Quantity: int = Field(..., gt=0, description="Quantity for this batch (must be > 0)")
    Value: float = Field(..., ge=0.0, description="Total purchase value for this batch (currency)")
    Selling_Price: float = Field(..., ge=0.0, description="Per-unit selling price")
    Category: str = Field(..., description="Category (required, free-text)")
    Product_Description: Optional[str] = Field(None, description="Optional description")
    Expiry_Date: date = Field(..., description="Expiry date YYYY-MM-DD for this batch")
    Brand: Optional[str] = Field(None, description="Brand name (optional)")
    Batch_No: Optional[str] = Field(None, description="Optional batch id; system generates if omitted")
    Purchase_Ref: Optional[str] = Field(None, description="Optional purchase reference (PO number)")
 
    @validator("Category")
    def category_required_and_strip(cls, v: str) -> str:
        if v is None or not isinstance(v, str) or not v.strip():
            raise ValueError("Category is required and cannot be empty")
        return v.strip()
 
    @validator("Product_ID", "Product_Name", "Hub_ID")
    def strip_mandatory_strings(cls, v: str) -> str:
        return v.strip()
 
    class Config:
        schema_extra = {
            "example": {
                "Hub_ID": "HUB_001",
                "Product_ID": "PROD_101",
                "Product_Name": "A1 Rice 25kg",
                "Quantity": 100,
                "Value": 4000.0,
                "Selling_Price": 45.0,
                "Category": "Grains",
                "Product_Description": "Premium rice 25kg pack",
                "Expiry_Date": "2026-01-01",
                "Brand": "GoodGrain",
                # "Batch_No": "optional-if-you-want"
            }
        }
 
 
class UpdateInventory(BaseModel):
    Hub_ID: str = Field(..., description="Hub identifier (must exist)")
    Product_ID: str = Field(..., description="Product SKU/ID to update")
    Product_Name: Optional[str] = Field(None, description="Optional master update")
    Quantity: Optional[int] = Field(None, gt=0, description="Quantity to ADD (if provided) - must be > 0")
    Value: Optional[float] = Field(None, ge=0.0, description="Purchase total for the added quantity")
    Selling_Price: Optional[float] = Field(None, ge=0.0)
    Category: Optional[str] = Field(None)
    Product_Description: Optional[str] = Field(None)
    Expiry_Date: Optional[date] = Field(None, description="Expiry date for this new stock (if present)")
    Brand: Optional[str] = Field(None)
    Batch_No: Optional[str] = Field(None, description="If matches existing batch -> merge; else create new")
 
    @validator("Category")
    def strip_category_if_present(cls, v):
        if v is None:
            return v
        s = v.strip()
        if s == "":
            raise ValueError("Category cannot be empty string")
        return s
 
    class Config:
        schema_extra = {
            "example": {
                "Hub_ID": "HUB_001",
                "Product_ID": "PROD_101",
                "Quantity": 50,
                "Value": 2000.0,
                "Expiry_Date": "2026-06-01",
            }
        }
 
 
class DispatchRequest(BaseModel):
    Product_ID: str = Field(..., description="Product SKU/ID to dispatch")
    Quantity: int = Field(..., gt=0, description="Quantity to dispatch (must be > 0)")
    From_Hub_ID: str = Field(..., description="Source hub")
    To_Hub_ID: str = Field(..., description="Destination hub")
    Product_Name: Optional[str] = None
    Request_Ref: Optional[str] = None
    Notes: Optional[str] = None
 
    @validator("Product_ID", "From_Hub_ID", "To_Hub_ID")
    def strip_ids(cls, v: str) -> str:
        return v.strip()
 
 
# -----------------------------
# Output / Response Schemas
# -----------------------------
class BatchOut(BaseModel):
    Product_ID: str
    Hub_ID: str
    Batch_No: str
    Quantity: int
    Expiry_Date: date
    Purchase_Value: float
    Purchase_Unit_Price: float
    Created_At: datetime
    Last_Updated: Optional[datetime] = None
    Status: Literal["active", "depleted", "archived"]
 
 
class ProductSummaryOut(BaseModel):
    Product_ID: str
    Product_Name: str
    Hub_ID: str
    Total_Quantity: int
    Category: str
    Brand: Optional[str]
    Nearest_Expiry: Optional[date]
    Batches_Count: int
 
 
class DispatchOut(BaseModel):
    dispatch_id: str
    Product_ID: str
    From_Hub_ID: str
    To_Hub_ID: str
    Quantity_Dispatched: int
    Batch_Consumption: List[Dict]  # list of { Batch_No, Qty, Unit_Cost }
    Vehicle_Assigned: Optional[str] = None
    Driver_Assigned: Optional[str] = None
    Status: Literal["In-Progress", "In-Transit", "Completed", "Cancelled"]
    Timestamp: datetime
 
 
class StockTransactionOut(BaseModel):
    transaction_id: str
    type: Literal["IN", "OUT", "ADJUSTMENT", "ARCHIVE"]
    Product_ID: str
    Hub_ID: str
    Batch_No: Optional[str]
    Quantity: int
    Unit_Price: Optional[float]
    Total_Value: Optional[float]
    reference: Optional[str]
    timestamp: datetime
    remarks: Optional[str]
 
 
# -----------------------------
# MongoDB Document Examples (comments for your endpoints.txt)
# -----------------------------
# InventoryProducts (product master) example:
# {
#   "Product_ID": "PROD_101",
#   "Product_Name": "A1 Rice 25kg",
#   "Category": "Grains",      # REQUIRED (free text)
#   "Brand": "GoodGrain",
#   "Selling_Price": 45.0,
#   "Product_Description": "Premium rice",
#   "created_at": datetime.now(timezone.utc),
#   "updated_at": datetime.now(timezone.utc)
# }
 
# InventoryBatches example:
# {
#   "_id": ObjectId(...),
#   "Product_ID": "PROD_101",
#   "Hub_ID": "HUB_001",
#   "Batch_No": "PROD_101-HUB_001-20250821093000-abc123",
#   "Quantity": 100,
#   "Expiry_Date": datetime(2026,1,1, tzinfo=timezone.utc),
#   "Purchase_Value": 4000.0,
#   "Purchase_Unit_Price": 40.0,
#   "status": "active",
#   "created_at": datetime.now(timezone.utc),
#   "last_updated": datetime.now(timezone.utc)
# }
 
# StockTransactions example:
# {
#   "transaction_id": "txn-uuid",
#   "type": "IN",
#   "Product_ID": "PROD_101",
#   "Hub_ID": "HUB_001",
#   "Batch_No": "PROD_101-HUB_001-20250821093000-abc123",
#   "Quantity": 100,
#   "Unit_Price": 40.0,
#   "Total_Value": 4000.0,
#   "reference": "PO-12345",
#   "timestamp": datetime.now(timezone.utc),
#   "remarks": "Initial purchase"
# }
 
# Dispatches example:
# {
#   "dispatch_id": "disp-uuid",
#   "Product_ID": "PROD_101",
#   "From_Hub_ID": "HUB_001",
#   "To_Hub_ID": "HUB_002",
#   "Quantity": 50,
#   "Batch_Consumption": [
#       {"Batch_No": "...", "Qty": 30, "Unit_Cost": 40.0},
#       {"Batch_No": "...", "Qty": 20, "Unit_Cost": 42.0}
#   ],
#   "Vehicle_Assigned": "In-Progress",
#   "Driver_Assigned": "In-Progress",
#   "Timestamp": datetime.now(timezone.utc),
#   "Status": "In-Progress"
# }
 
# -----------------------------
# Index suggestions (for mongodb.ensure_indexes)
# -----------------------------
# await db["InventoryProducts"].create_index("Product_ID", unique=True)
# await db["InventoryProducts"].create_index([("Product_Name", 1), ("Hub_ID", 1)])
# await db["InventoryBatches"].create_index([("Product_ID", 1), ("Hub_ID", 1), ("Expiry_Date", 1)])
# await db["InventoryBatches"].create_index([("Product_ID", 1), ("Hub_ID", 1), ("Batch_No", 1)], unique=True)
# await db["StockTransactions"].create_index([("Product_ID", 1), ("Hub_ID", 1), ("timestamp", -1)])
# await db["Dispatches"].create_index([("Status", 1), ("Timestamp", -1)])