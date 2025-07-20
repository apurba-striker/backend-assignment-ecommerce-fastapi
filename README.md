# E-commerce API with FastAPI and MongoDB

This is a simple e-commerce API built with FastAPI and MongoDB that provides endpoints for managing products and orders.

## Features

- Create and list products
- Filter products by name and size
- Create orders
- List orders by user ID
- Pagination support

## Prerequisites

- Python 3.10 or higher
- MongoDB (local installation or MongoDB Atlas)

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application entry point
│   ├── database.py       # Database connection and utilities
│   ├── models.py         # Pydantic models
│   └── api/              # API routes
│       ├── __init__.py
│       ├── products.py   # Product endpoints
│       └── orders.py     # Order endpoints
├── requirements.txt      # Dependencies
├── .env                  # Environment variables
├── run.py                # Script to run the application
├── test_api.py           # Simple test script
└── README.md             # Documentation
```

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables:
   - Create a `.env` file in the root directory
   - Add the following variables:
     ```
     MONGODB_URL=mongodb://localhost:27017
     DB_NAME=ecommerce
     ```
   - For MongoDB Atlas, use the connection string provided by Atlas:
     ```
     MONGODB_URL=mongodb+srv://<username>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority
     DB_NAME=ecommerce
     ```

## Running the Application

There are two ways to start the application:

1. Using the run script:

```bash
python run.py
```

2. Using uvicorn directly:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## Testing the API

A simple test script is provided to test all endpoints:

```bash
python test_api.py
```

## API Documentation

FastAPI automatically generates API documentation. Visit:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Products

- **Create Product**

  - `POST /products`
  - Request Body:
    ```json
    {
      "name": "string",
      "price": 100.0,
      "sizes": [
        {
          "size": "string",
          "quantity": 0
        }
      ]
    }
    ```
  - Response:
    ```json
    {
      "id": "1234567890"
    }
    ```

- **List Products**
  - `GET /products`
  - Query Parameters:
    - `name`: Filter by name (supports regex/partial search)
    - `size`: Filter by size
    - `limit`: Number of documents to return
    - `offset`: Number of documents to skip
  - Response:
    ```json
    {
      "data": [
        {
          "id": "12345",
          "name": "Sample",
          "price": 100.0
        }
      ],
      "page": {
        "next": "10",
        "limit": 0,
        "previous": "-10"
      }
    }
    ```

### Orders

- **Create Order**

  - `POST /orders`
  - Request Body:
    ```json
    {
      "userId": "user_1",
      "items": [
        {
          "productId": "123456789",
          "qty": 3
        }
      ]
    }
    ```
  - Response:
    ```json
    {
      "id": "1234567890"
    }
    ```

- **List Orders**
  - `GET /orders/<user_id>`
  - Query Parameters:
    - `limit`: Number of documents to return
    - `offset`: Number of documents to skip
  - Response:
    ```json
    {
      "data": [
        {
          "id": "12345",
          "items": [
            {
              "productDetails": {
                "name": "Sample Product",
                "id": "123456"
              },
              "qty": 3
            }
          ],
          "total": 250.0
        }
      ],
      "page": {
        "next": "10",
        "limit": 0,
        "previous": "-10"
      }
    }
    ```
