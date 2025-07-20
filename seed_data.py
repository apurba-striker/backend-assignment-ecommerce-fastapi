import requests
import json
import random

BASE_URL = "http://localhost:8000"

def create_product(name, price, sizes):
    """Create a product and return its ID"""
    url = f"{BASE_URL}/products"
    
    product_data = {
        "name": name,
        "price": price,
        "sizes": sizes
    }
    
    response = requests.post(url, json=product_data)
    
    if response.status_code == 201:
        print(f"Created product: {name}")
        return response.json()["id"]
    else:
        print(f"Failed to create product {name}: {response.status_code}")
        return None

def create_order(user_id, items):
    """Create an order with multiple items"""
    url = f"{BASE_URL}/orders"
    
    order_data = {
        "userId": user_id,
        "items": items
    }
    
    response = requests.post(url, json=order_data)
    
    if response.status_code == 201:
        print(f"Created order for user: {user_id}")
        return response.json()["id"]
    else:
        print(f"Failed to create order for {user_id}: {response.status_code}")
        return None

def seed_database():
    print("Seeding database with multiple products and orders...")
    
    # Create products
    products = [
        {
            "name": "T-Shirt Basic",
            "price": 19.99,
            "sizes": [
                {"size": "small", "quantity": 20},
                {"size": "medium", "quantity": 30},
                {"size": "large", "quantity": 25}
            ]
        },
        {
            "name": "Jeans Classic",
            "price": 49.99,
            "sizes": [
                {"size": "small", "quantity": 15},
                {"size": "medium", "quantity": 25},
                {"size": "large", "quantity": 20}
            ]
        },
        {
            "name": "Hoodie Premium",
            "price": 39.99,
            "sizes": [
                {"size": "medium", "quantity": 20},
                {"size": "large", "quantity": 30},
                {"size": "xlarge", "quantity": 15}
            ]
        },
        {
            "name": "Sneakers Sport",
            "price": 79.99,
            "sizes": [
                {"size": "7", "quantity": 10},
                {"size": "8", "quantity": 15},
                {"size": "9", "quantity": 20},
                {"size": "10", "quantity": 15}
            ]
        },
        {
            "name": "Cap Urban",
            "price": 24.99,
            "sizes": [
                {"size": "small", "quantity": 20},
                {"size": "medium", "quantity": 25},
                {"size": "large", "quantity": 15}
            ]
        }
    ]
    
    # Store product IDs
    product_ids = []
    
    # Create products
    for product in products:
        product_id = create_product(product["name"], product["price"], product["sizes"])
        if product_id:
            product_ids.append(product_id)
    
    if not product_ids:
        print("No products were created. Exiting.")
        return
    
    # Create users
    users = ["user_1", "user_2", "user_3"]
    
    # Create orders for each user
    for user in users:
        # Create 2 orders per user
        for _ in range(2):
            # Select 1-3 random products for this order
            num_items = random.randint(1, 3)
            order_items = []
            
            # Ensure unique products in each order
            selected_products = random.sample(product_ids, num_items)
            
            for product_id in selected_products:
                order_items.append({
                    "productId": product_id,
                    "qty": random.randint(1, 3)
                })
            
            create_order(user, order_items)
    
    print("Database seeding completed!")

if __name__ == "__main__":
    seed_database() 