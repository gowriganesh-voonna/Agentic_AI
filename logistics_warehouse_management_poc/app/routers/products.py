from fastapi import APIRouter,HTTPException
from app.model.products import Product,GetProduct,UpdateProduct
from app.utiles.decoratores import handle_exceptions
from app.utiles.logger import get_logger
from app.data.file_handler import load_json,save_json
from typing import List
from datetime import datetime
router = APIRouter()

# initilizing logger 
logger = get_logger(__name__)

FILE_PATH = "app/data/products.json"

@handle_exceptions
@router.post("/add_products")
async def add_product(product : Product):
    """Input : Product class as dict
    if id was already added then raise HTTP Exception
    else : Product Added"""
    data =load_json(FILE_PATH)

    for p in data:
        if p["id"] == product.id:
            raise HTTPException(status_code= 400,
                                detail="Product ID ALready Exist.")
    product_data = product.dict()
    product_data["expiry_date"] = product.expiry_date.isoformat()
    data.append(product_data)
    save_json(FILE_PATH,data)
    logger.info(f"Product {product.id} Added.")
    return {"Message":f"Product Added successfully {product.id}"}

@handle_exceptions
@router.put("/update_products/{product_id}",response_model=dict)
async def update_product(product_id : str,update:UpdateProduct):
    data =load_json(FILE_PATH)
    found =False

    for p in data:
        if p["id"] == product_id:
            found=True
            p["stock"]= update.stock + p["stock"]
            p["price"] = update.price or p["price"]
            p["description"] = update.description or p["description"]
            break
    if not found :
        raise HTTPException(status_code=404,
                            detail=f"Product: {product_id} Not Found")
    save_json(FILE_PATH,data)
    logger.info(f"Product {product_id} Updated successfully")
    return {"Product ID":f"{product_id} Updated SUccessfully",
            }

@handle_exceptions
@router.delete("/delete_product/{product_id}")
async def delete_product(product_id:str,name:str):  # pass in url only
    data= load_json(FILE_PATH)

    new_products =[p for p in data if not (p["id"] == product_id and p["name"]== name)]

    if len(new_products) == len(data):
        logger.info(f"Product_id {product_id} Not found")
        raise HTTPException(status_code=404,
                            detail=f"Product: {product_id} Not Found")
    
    save_json(FILE_PATH,new_products)
    logger.info(f"Product_id: {product_id} Product_name : {name} Deleted Successfully.")
    return {"Detail":f"Product_id : {product_id} Deleted Successfully"}

@handle_exceptions
@router.get("/low_stock")
async def low_stock():
    data = load_json(FILE_PATH)
    low_stock_items = [p for p in data if p["stock"]<10]

    if low_stock_items:
        logger.info(f"Low Stock alert {low_stock_items}")
    else:
        raise HTTPException(status_code=404,
                            detail="Their is no low stock")
    return low_stock_items

@handle_exceptions
@router.get("/get_product",response_model=List[Product])
async def get_product(product:GetProduct):
    data = load_json(FILE_PATH)

    filtered_product = list(filter(lambda p: product.id == p["id"] or product.name == p["name"],data ))

    #list(filter(lambda b: text in b['book_id'] or text in b["title"] or text in b["genre"],books))

    
        
    if not filtered_product:
        logger.info(f"Product not found {product}")
        raise HTTPException(status_code=404,
                            detail="details not found")
    return filtered_product



@handle_exceptions
@router.get("/expiring-this-month")
async def products_expiring_this_month():
    data = load_json(FILE_PATH)
    current_date = datetime.now()
    expiring_products =[]

    for p in data:
        product_expiry = datetime.strptime(p['expiry_date'],'%Y-%m-%d')

        if(product_expiry.year) == current_date.year and product_expiry.month == current_date.month:
            expiring_products.append(p)

    if expiring_products:
        logger.info("Expried Products returned")
        return {"Expiring_Products":expiring_products}
    else:
        return {"Message":"No products expiring this month"}
    
    