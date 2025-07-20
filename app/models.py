from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

class Size(BaseModel):
    size: str
    quantity: int

class ProductCreate(BaseModel):
    name: str
    price: float
    sizes: List[Size] = []

class ProductResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    price: float
    sizes: List[Size] = []

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class OrderItem(BaseModel):
    productId: str
    qty: int

class OrderCreate(BaseModel):
    userId: str
    items: List[OrderItem]

class ProductDetails(BaseModel):
    name: str
    id: str

class OrderItemResponse(BaseModel):
    productDetails: ProductDetails
    qty: int

class OrderResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class OrderListResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    userId: str
    items: List[OrderItemResponse]
    total: float

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class PaginationResponse(BaseModel):
    next: Optional[str]
    limit: int
    previous: Optional[str]

class ProductListResponse(BaseModel):
    data: List[ProductResponse]
    page: PaginationResponse

class OrdersListResponse(BaseModel):
    data: List[OrderListResponse]
    page: PaginationResponse 