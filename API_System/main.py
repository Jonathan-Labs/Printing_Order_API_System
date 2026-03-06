from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from models import Order, OrderItem, OrderResponse, PrintType
from config import PRICES, API_TITLE, API_VERSION, API_DESCRIPTION
from datetime import datetime
import uuid

# Initialize FastAPI app
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION
)

# In-memory storage for orders
orders_db: dict[str, dict] = {}


def calculate_order_cost(items: list[OrderItem]) -> float:
    """
    Calculate the total cost of an order based on printing type, pages, and quantity.
    
    Args:
        items: List of OrderItem objects
        
    Returns:
        Total cost in PHP
    """
    total_cost = 0.0
    
    for item in items:
        # Get price per page based on print type
        price_per_page = PRICES.get(item.print_type)
        
        if price_per_page is None:
            raise ValueError(f"Invalid print type: {item.print_type}")
        
        # Calculate cost: price_per_page * pages * quantity
        item_cost = price_per_page * item.pages * item.quantity
        total_cost += item_cost
    
    return round(total_cost, 2)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API status"""
    return {
        "message": "Welcome to Printing Order API System",
        "version": API_VERSION,
        "status": "operational"
    }


@app.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED, tags=["Orders"])
async def create_order(order: Order):
    """
    Create a new printing order.
    
    - **client_name**: Name of the client placing the order
    - **items**: List of items to print (type, pages, quantity)
    - **notes**: Optional additional notes for the order
    
    Returns the created order with calculated total cost and assigned order ID.
    """
    try:
        # Generate unique order ID
        order_id = str(uuid.uuid4())[:8].upper()
        
        # Calculate total cost
        total_cost = calculate_order_cost(order.items)
        
        # Create order record
        order_record = {
            "order_id": order_id,
            "client_name": order.client_name,
            "items": order.items,
            "total_cost": total_cost,
            "status": "Pending",
            "created_at": datetime.now(),
            "notes": order.notes
        }
        
        # Store in memory
        orders_db[order_id] = order_record
        
        return OrderResponse(**order_record)
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.get("/orders", response_model=list[OrderResponse], tags=["Orders"])
async def get_all_orders():
    """
    Retrieve all printing orders.
    
    Returns a list of all orders stored in the system.
    """
    if not orders_db:
        return []
    
    return [OrderResponse(**order) for order in orders_db.values()]


@app.get("/orders/{order_id}", response_model=OrderResponse, tags=["Orders"])
async def get_order_by_id(order_id: str):
    """
    Retrieve a specific printing order by order ID.
    
    - **order_id**: The unique order identifier
    
    Returns the order details if found.
    """
    if order_id not in orders_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID '{order_id}' not found"
        )
    
    return OrderResponse(**orders_db[order_id])


@app.put("/orders/{order_id}", response_model=OrderResponse, tags=["Orders"])
async def update_order_status(order_id: str, status_update: str):
    """
    Update the status of a printing order.
    
    - **order_id**: The unique order identifier
    - **status_update**: New status (e.g., 'Completed', 'Pending', 'Processing')
    
    Returns the updated order.
    """
    if order_id not in orders_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID '{order_id}' not found"
        )
    
    orders_db[order_id]["status"] = status_update
    
    return OrderResponse(**orders_db[order_id])


@app.get("/stats", tags=["Statistics"])
async def get_order_statistics():
    """
    Get order statistics and summary information.
    
    Returns total orders, total revenue, and order status breakdown.
    """
    if not orders_db:
        return {
            "total_orders": 0,
            "total_revenue": 0.0,
            "status_breakdown": {}
        }
    
    total_revenue = sum(order["total_cost"] for order in orders_db.values())
    
    # Count orders by status
    status_breakdown = {}
    for order in orders_db.values():
        status = order["status"]
        status_breakdown[status] = status_breakdown.get(status, 0) + 1
    
    return {
        "total_orders": len(orders_db),
        "total_revenue": round(total_revenue, 2),
        "status_breakdown": status_breakdown
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
