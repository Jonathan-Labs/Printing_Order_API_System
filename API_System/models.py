from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class PrintType(str, Enum):
    """Enum for printing types"""
    BLACK_WHITE = "black_white"
    COLORED = "colored"
    PHOTO_PAPER = "photo_paper"


class OrderItem(BaseModel):
    """Model for individual order items"""
    print_type: PrintType = Field(..., description="Type of printing")
    pages: int = Field(..., gt=0, description="Number of pages to print")
    quantity: int = Field(default=1, gt=0, description="Number of copies")

    class Config:
        description = "Individual printing order item"


class Order(BaseModel):
    """Model for a complete printing order"""
    order_id: Optional[str] = None
    client_name: str = Field(..., description="Name of the client")
    items: list[OrderItem] = Field(..., min_items=1, description="List of items to print")
    total_cost: Optional[float] = None
    status: str = Field(default="Pending", description="Order status")
    created_at: Optional[datetime] = None
    notes: Optional[str] = Field(default=None, description="Additional notes for the order")

    class Config:
        description = "Complete printing order"


class OrderResponse(BaseModel):
    """Model for API response"""
    order_id: str
    client_name: str
    items: list[OrderItem]
    total_cost: float
    status: str
    created_at: datetime
    notes: Optional[str] = None

    class Config:
        description = "Order response model"
