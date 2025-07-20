import requests
import json

BASE_URL = "http://localhost:8000"

def test_create_product():
    print("Testing Create Product API...")
    url = f"{BASE_URL}/products"
    
    # Test data
    product_data = {
        "name": "Test Product",
        "price": 99.99,
        "sizes": [
            {"size": "small", "quantity": 10},
            {"size": "medium", "quantity": 15},
            {"size": "large", "quantity": 5}
        ]
    }
    
    # Send request
    response = requests.post(url, json=product_data)
    
    # Print results
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    
    return response.json()["id"]

def test_list_products():
    print("Testing List Products API...")
    url = f"{BASE_URL}/products"
    
    # Send request
    response = requests.get(url)
    
    # Print results
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_filter_products_by_name():
    print("Testing Filter Products by Name...")
    url = f"{BASE_URL}/products?name=Test"
    
    # Send request
    response = requests.get(url)
    
    # Print results
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_filter_products_by_size():
    print("Testing Filter Products by Size...")
    url = f"{BASE_URL}/products?size=large"
    
    # Send request
    response = requests.get(url)
    
    # Print results
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_create_order(product_id):
    print("Testing Create Order API...")
    url = f"{BASE_URL}/orders"
    
    # Test data
    order_data = {
        "userId": "user_1",
        "items": [
            {"productId": product_id, "qty": 2}
        ]
    }
    
    # Send request
    response = requests.post(url, json=order_data)
    
    # Print results
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    
    return response.json()["id"]

def test_list_orders():
    print("Testing List Orders API...")
    url = f"{BASE_URL}/orders/user_1"
    
    # Send request
    response = requests.get(url)
    
    # Print results
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def run_tests():
    # Run tests in sequence
    product_id = test_create_product()
    test_list_products()
    test_filter_products_by_name()
    test_filter_products_by_size()
    test_create_order(product_id)
    test_list_orders()

if __name__ == "__main__":
    run_tests() 