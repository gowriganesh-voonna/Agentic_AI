from fastapi import APIRouter,HTTPException
from models.products import Product,GetProduct
from utiles.decoratores import handle_exceptions
from utiles.logger import get_logger
from data.file_handler import load_json,save_json
from typing import List
router = APIRouter()
logger = get_logger(__name__)

FILE_PATH = "data/products.json"

@handle_exceptions
@router.post("/add_products",response_model=dict)
async def add_product(product : Product):
    data = load_json(FILE_PATH)

    for p in data:
        if p["id"] == product.id:
            raise HTTPException(status_code= 400,
                                detail="Product ID ALready Exist.")
    data.append(product.dict())
    save_json(FILE_PATH,data)
    logger.info(f"Product {product.id} Added.")
    return {"Message":f"Product Added successfully {product}"}

@handle_exceptions
@router.put("/update_products/{product_id}",response_model=dict)
async def update_product(product_id : str,stock:int):
    data = load_json(FILE_PATH)
    found =False

    for p in data:
        if p["id"] == product_id:
            found=True
            p["stock"]= stock
            break
    if not found :
        raise HTTPException(status_code=404,
                            detail=f"Product: {product_id} Not Found")
    save_json(FILE_PATH,data)
    logger.info(f"Product {product_id} Updated successfully")
    return {"Product ID":{product_id},
            "Stock":f"stock : {stock} updated successfully"}

@handle_exceptions
@router.delete("/delete_product/{product_id}")
async def delete_product(product_id:str,product_name:str)
    data= load_json(FILE_PATH)

    new_products =[p for p in data if not any(p["id"] == product_id and p["name"]== product_name)]

    if len(new_products) == len(data):
        raise HTTPException(status_code=404,
                            detail=f"Product: {product_id} Not Found")
    
    save_json(FILE_PATH,new_products)
    logger.info(f"Product_id: {product_id} Product_name : {product_name} Deleted Successfully.")
    return {"Detail":f"Product_id : {product_id} Deleted Successfully"}

@handle_exceptions
@router.get("/low_stock")
async def low_stock():
    data = await load_json(FILE_PATH)
    low_stock_items = [p for p in data if p["stock"]<10]

    if low_stock_items:
        logger.info(f"Low Stock alert {low_stock_items}")
    else:
        raise HTTPException(status_code=404,
                            detail="Their is no low stock")
    return low_stock_items

@handle_exceptions
@router.get("/get_product")
async def get_product(product:GetProduct):
    data = await load_json(FILE_PATH)

    filtered_product = list(filter(lambda p: product.id in p["id"] or product.name in p["name"] ),data)

    #list(filter(lambda b: text in b['book_id'] or text in b["title"] or text in b["genre"],books))

    if not (product.id and product.name):
        logger.info(f"Details was not entered")
        raise HTTPException(status_code=503, # 503 - service unavialble
                            detail="Details not entered") 
        
    elif not filtered_product:
        logger.info(f"Product not found {product}")
        raise HTTPException(status_code=404,
                            detail="details not found")
