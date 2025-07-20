from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from app.database import get_database
from app.models import ProductCreate

router = APIRouter()

@router.post("", status_code=201)
async def create_product(product: ProductCreate, db=Depends(get_database)):
    product_dict = product.dict()
    result = await db.products.insert_one(product_dict)
    return {"id": str(result.inserted_id)}

@router.get("")
async def list_products(
    name: Optional[str] = None,
    size: Optional[str] = None,
    limit: Optional[int] = Query(10, ge=1),
    offset: Optional[int] = Query(0, ge=0),
    db=Depends(get_database)
):
    query = {}
    
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    
    if size:
        query["sizes.size"] = size
    
    cursor = db.products.find(query).skip(offset).limit(limit)
    products = await cursor.to_list(length=limit)
    formatted_products = []
    for product in products:
        formatted_product = {
            "id": str(product.pop("_id")),
            "name": product["name"],
            "price": product["price"]
        }
        formatted_products.append(formatted_product)
    

    total = await db.products.count_documents(query)
    

    next_offset = offset + limit if offset + limit < total else None
    previous_offset = offset - limit if offset > 0 else None
    
    return {
        "data": formatted_products,
        "page": {
            "next": str(next_offset) if next_offset is not None else None,
            "limit": len(formatted_products),
            "previous": str(previous_offset) if previous_offset is not None else None
        }
    } 