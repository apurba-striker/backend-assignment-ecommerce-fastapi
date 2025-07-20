from fastapi import APIRouter, Depends, Query, Path, HTTPException
from typing import Optional
from bson import ObjectId
from app.database import get_database
from app.models import OrderCreate

router = APIRouter()

@router.post("", status_code=201)
async def create_order(order: OrderCreate, db=Depends(get_database)):
    # Calculate total and prepare order document
    total = 0
    order_items = []
    
    for item in order.items:
        try:
            product = await db.products.find_one({"_id": ObjectId(item.productId)})
        except:
            raise HTTPException(status_code=400, detail=f"Invalid product ID format: {item.productId}")
            
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.productId} not found")
        
        # Add product details to order item
        order_items.append({
            "productId": item.productId,
            "qty": item.qty,
            "productDetails": {
                "name": product["name"],
                "id": item.productId
            }
        })
        
        total += product["price"] * item.qty
    
    # Create order document
    order_doc = {
        "userId": order.userId,
        "items": order_items,
        "total": total
    }
    
    result = await db.orders.insert_one(order_doc)
    return {"id": str(result.inserted_id)}

@router.get("/{user_id}")
async def get_orders(
    user_id: str = Path(..., description="User ID"),
    limit: Optional[int] = Query(10, ge=1),
    offset: Optional[int] = Query(0, ge=0),
    db=Depends(get_database)
):
    query = {"userId": user_id}
    
    cursor = db.orders.find(query).skip(offset).limit(limit)
    orders = await cursor.to_list(length=limit)
    
    # Format orders according to required response structure
    formatted_orders = []
    for order in orders:
        formatted_order = {
            "id": str(order.pop("_id")),
            "items": [],
            "total": order["total"]
        }
        
        # Format items to match required structure
        for item in order["items"]:
            formatted_order["items"].append({
                "productDetails": {
                    "name": item["productDetails"]["name"],
                    "id": item["productDetails"]["id"]
                },
                "qty": item["qty"]
            })
            
        formatted_orders.append(formatted_order)
    
    # Get total count for pagination
    total = await db.orders.count_documents(query)
    
    # Calculate pagination values
    next_offset = offset + limit if offset + limit < total else None
    previous_offset = offset - limit if offset - limit >= 0 else None
    
    return {
        "data": formatted_orders,
        "page": {
            "next": str(next_offset) if next_offset is not None else None,
            "limit": limit,
            "previous": str(previous_offset) if previous_offset is not None else None
        }
    } 