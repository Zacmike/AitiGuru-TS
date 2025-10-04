from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AddToOrderRequest(BaseModel):
    order_id: int
    nomenclature_id: int
    quantity: int

class AddToOrderResponse(BaseModel):
    success: bool
    message: str
    order_item_id: Optional[int] = None
    new_quantity: Optional[int] = None
    
class ErrorResponse(BaseModel):
    detail: str
    
class ClientResponse(BaseModel):
    id: int
    name: str
    address: str
    created_at: datetime
    
class OrderResponse(BaseModel):
    id: int
    client_id: int
    order_date: datetime
    status: str
    total_amount: float
    