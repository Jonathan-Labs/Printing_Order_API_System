"""
Example test cases and usage demonstrations for the Printing Order API System
Run this file to test the API endpoints
"""

import requests
import json
from typing import Optional

BASE_URL = "http://localhost:8000"


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def print_response(response: requests.Response, title: str = "Response"):
    """Pretty print API response"""
    print(f"\n{title}:")
    print(f"Status Code: {response.status_code}")
    try:
        print("Body:")
        print(json.dumps(response.json(), indent=2, default=str))
    except:
        print(response.text)


def test_root():
    """Test root endpoint"""
    print_section("Test 1: Root Endpoint")
    response = requests.get(f"{BASE_URL}/")
    print_response(response)
    return response


def test_create_order_1():
    """Test creating a simple order"""
    print_section("Test 2: Create Simple Order")
    
    order_data = {
        "client_name": "John Doe",
        "items": [
            {
                "print_type": "black_white",
                "pages": 10,
                "quantity": 1
            }
        ],
        "notes": "Standard printing job"
    }
    
    print("Request Body:")
    print(json.dumps(order_data, indent=2))
    
    response = requests.post(f"{BASE_URL}/orders", json=order_data)
    print_response(response, "Response")
    
    if response.status_code == 201:
        return response.json()["order_id"]
    return None


def test_create_order_2():
    """Test creating a complex order with multiple items"""
    print_section("Test 3: Create Complex Order")
    
    order_data = {
        "client_name": "Mary Smith",
        "items": [
            {
                "print_type": "black_white",
                "pages": 20,
                "quantity": 2
            },
            {
                "print_type": "colored",
                "pages": 10,
                "quantity": 1
            },
            {
                "print_type": "photo_paper",
                "pages": 5,
                "quantity": 1
            }
        ],
        "notes": "Mixed printing project"
    }
    
    print("Request Body:")
    print(json.dumps(order_data, indent=2))
    
    response = requests.post(f"{BASE_URL}/orders", json=order_data)
    print_response(response, "Response")
    
    # Cost Breakdown:
    # Black & White: 20 pages × 2 copies × 2.00 = 80.00
    # Colored: 10 pages × 1 copy × 5.00 = 50.00
    # Photo Paper: 5 pages × 1 copy × 20.00 = 100.00
    # Total: 230.00
    print("\nCost Breakdown:")
    print("  Black & White: 20 pages × 2 copies × 2.00 = 80.00")
    print("  Colored: 10 pages × 1 copy × 5.00 = 50.00")
    print("  Photo Paper: 5 pages × 1 copy × 20.00 = 100.00")
    print("  Total Expected: 230.00")
    
    if response.status_code == 201:
        return response.json()["order_id"]
    return None


def test_create_order_3():
    """Test creating a photo paper order"""
    print_section("Test 4: Create Photo Paper Order")
    
    order_data = {
        "client_name": "Alice Johnson",
        "items": [
            {
                "print_type": "photo_paper",
                "pages": 10,
                "quantity": 1
            }
        ]
    }
    
    print("Request Body:")
    print(json.dumps(order_data, indent=2))
    
    response = requests.post(f"{BASE_URL}/orders", json=order_data)
    print_response(response, "Response")
    
    # Cost: 10 pages × 1 copy × 20.00 = 200.00
    print("\nCost Calculation: 10 pages × 1 copy × 20.00 = 200.00")
    
    if response.status_code == 201:
        return response.json()["order_id"]
    return None


def test_get_all_orders():
    """Test retrieving all orders"""
    print_section("Test 5: Get All Orders")
    response = requests.get(f"{BASE_URL}/orders")
    print_response(response)


def test_get_order_by_id(order_id: str):
    """Test retrieving a specific order"""
    print_section(f"Test 6: Get Specific Order (ID: {order_id})")
    response = requests.get(f"{BASE_URL}/orders/{order_id}")
    print_response(response)


def test_update_order_status(order_id: str):
    """Test updating order status"""
    print_section(f"Test 7: Update Order Status (ID: {order_id})")
    
    print(f"Updating order {order_id} to 'Completed'")
    response = requests.put(f"{BASE_URL}/orders/{order_id}", params={"status_update": "Completed"})
    print_response(response)


def test_get_statistics():
    """Test getting order statistics"""
    print_section("Test 8: Get Order Statistics")
    response = requests.get(f"{BASE_URL}/stats")
    print_response(response)


def test_error_handling():
    """Test error handling with invalid order ID"""
    print_section("Test 9: Error Handling - Invalid Order ID")
    response = requests.get(f"{BASE_URL}/orders/INVALID123")
    print_response(response, "Expected Error Response")


def run_all_tests():
    """Run all test cases"""
    print("\n" + "█"*60)
    print(" PRINTING ORDER API SYSTEM - TEST SUITE")
    print("█"*60)
    print("\nMake sure the FastAPI server is running!")
    print("Start with: python main.py")
    
    try:
        # Test basic endpoint
        test_root()
        
        # Create orders
        order_id_1 = test_create_order_1()
        order_id_2 = test_create_order_2()
        order_id_3 = test_create_order_3()
        
        # Retrieve orders
        test_get_all_orders()
        
        if order_id_1:
            test_get_order_by_id(order_id_1)
        
        if order_id_2:
            test_update_order_status(order_id_2)
        
        # Get statistics
        test_get_statistics()
        
        # Test error handling
        test_error_handling()
        
        print("\n" + "█"*60)
        print(" ALL TESTS COMPLETED")
        print("█"*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to the server!")
        print("   Make sure the FastAPI server is running:")
        print("   python main.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")


if __name__ == "__main__":
    run_all_tests()
