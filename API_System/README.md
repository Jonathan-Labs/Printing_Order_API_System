# Printing Order API System

A FastAPI-based backend system for managing printing shop orders with automatic cost calculation.

## Features

- ✅ Create printing orders with automatic cost calculation
- ✅ View all orders
- ✅ Retrieve specific order details by order ID
- ✅ Update order status
- ✅ View order statistics and revenue reports
- ✅ In-memory storage (no database required)

## Pricing

- **Black & White**: PHP 2.00 per page
- **Colored**: PHP 5.00 per page
- **Photo Paper**: PHP 20.00 per page

## Project Structure

```
├── main.py           # FastAPI application with all endpoints
├── models.py         # Pydantic models for data validation
├── config.py         # Configuration and pricing constants
├── requirements.txt  # Project dependencies
└── README.md         # This file
```

## Installation & Setup

### 1. Activate Virtual Environment

If using the provided virtual environment:
```powershell
.\fastapi_env\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

### Start the Server

```bash
python main.py
```

Or use uvicorn directly:

```bash
uvicorn main:app --reload
```

The API will be available at: `http://localhost:8000`

### Interactive API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### 1. Create Order
**POST** `/orders`

Create a new printing order and get automatic cost calculation.

**Request Body:**
```json
{
  "client_name": "John Doe",
  "items": [
    {
      "print_type": "black_white",
      "pages": 10,
      "quantity": 2
    },
    {
      "print_type": "colored",
      "pages": 5,
      "quantity": 1
    }
  ],
  "notes": "Rush order - due tomorrow"
}
```

**Response:** (Status 201 Created)
```json
{
  "order_id": "A3F2K1L9",
  "client_name": "John Doe",
  "items": [...],
  "total_cost": 65.00,
  "status": "Pending",
  "created_at": "2024-03-06T10:30:00",
  "notes": "Rush order - due tomorrow"
}
```

### 2. Get All Orders
**GET** `/orders`

Retrieve all orders in the system.

**Response:** (Status 200 OK)
```json
[
  {
    "order_id": "A3F2K1L9",
    "client_name": "John Doe",
    ...
  },
  {...}
]
```

### 3. Get Specific Order
**GET** `/orders/{order_id}`

Retrieve details of a specific order by order ID.

**Parameters:**
- `order_id` (string, required): The unique order identifier

**Response:** (Status 200 OK)
```json
{
  "order_id": "A3F2K1L9",
  "client_name": "John Doe",
  ...
}
```

### 4. Update Order Status
**PUT** `/orders/{order_id}`

Update the status of an existing order.

**Parameters:**
- `order_id` (string, required): The unique order identifier
- `status_update` (string, query): New status (e.g., 'Completed', 'Processing')

**Response:** (Status 200 OK)
```json
{
  "order_id": "A3F2K1L9",
  "status": "Completed",
  ...
}
```

### 5. Get Statistics
**GET** `/stats`

Get overall order statistics and revenue information.

**Response:** (Status 200 OK)
```json
{
  "total_orders": 5,
  "total_revenue": 325.50,
  "status_breakdown": {
    "Pending": 2,
    "Completed": 3
  }
}
```

## Example Usage

### Using cURL

```bash
# Create an order
curl -X POST "http://localhost:8000/orders" \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "Mary Smith",
    "items": [
      {"print_type": "black_white", "pages": 20, "quantity": 1}
    ]
  }'

# Get all orders
curl "http://localhost:8000/orders"

# Get specific order
curl "http://localhost:8000/orders/ABC12345"

# Get statistics
curl "http://localhost:8000/stats"
```

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Create order
order_data = {
    "client_name": "Alice Johnson",
    "items": [
        {"print_type": "photo_paper", "pages": 5, "quantity": 1}
    ],
    "notes": "Business cards needed"
}

response = requests.post(f"{BASE_URL}/orders", json=order_data)
print(response.json())
```

## Data Models

### PrintType (Enum)
- `black_white` - Black and white printing
- `colored` - Color printing
- `photo_paper` - Photo paper printing

### OrderItem
```python
{
  "print_type": str,  # One of the PrintType values
  "pages": int,       # Number of pages (must be > 0)
  "quantity": int     # Number of copies (default: 1, must be > 0)
}
```

### Order
```python
{
  "order_id": str (optional),
  "client_name": str,
  "items": list[OrderItem],
  "total_cost": float (calculated automatically),
  "status": str (default: "Pending"),
  "created_at": datetime (optional),
  "notes": str (optional)
}
```

## Cost Calculation Example

For an order with:
- 10 pages Black & White (quantity 2): 10 × 2 × 2.00 = PHP 40.00
- 5 pages Colored (quantity 1): 5 × 1 × 5.00 = PHP 25.00

**Total Cost: PHP 65.00**

## Features for Future Enhancement

- Database integration (SQLite, PostgreSQL)
- User authentication and authorization
- Order history and archiving
- Payment integration
- Email notifications
- Discount and promotion system
- Advanced reporting and analytics

## Notes

- Orders are stored in-memory and will be lost when the server restarts
- Order IDs are randomly generated 8-character strings
- All monetary values are in Philippine Peso (PHP)

## Support

For issues or questions, please refer to the FastAPI documentation: https://fastapi.tiangolo.com/
