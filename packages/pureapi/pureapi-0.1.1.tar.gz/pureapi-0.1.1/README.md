# PureAPI

A lightweight and elegant Python web framework for building modern APIs.

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Features

- 🚀 **Modern Routing** - Type-annotated path parameters with automatic conversion
- 📖 **OpenAPI Support** - Built-in Swagger UI and ReDoc documentation
- 🎯 **Simple Design** - Intuitive API that's easy to learn and use
- 🔧 **WSGI Compatible** - Works with any WSGI server (Gunicorn, uWSGI, etc.)
- 📦 **Zero Dependencies** - Uses only Python standard library

## Installation

```bash
pip install pureapi
```

## Quick Start

```python
from pureapi import PureAPI

app = PureAPI(title="My API", version="1.0.0")

@app.get("/")
def root():
    """Welcome endpoint."""
    return {"message": "Hello, World!"}

@app.get("/users/{user_id:int}")
def get_user(user_id: int):
    """Get user by ID."""
    return {"user_id": user_id}

@app.post("/users")
def create_user(request):
    """Create a new user."""
    data = request.json
    return {"created": True, "data": data}

if __name__ == "__main__":
    app.run()  # Runs on http://127.0.0.1:8888
```

## API Documentation

Once your app is running, visit:
- **Swagger UI**: http://127.0.0.1:8888/docs
- **ReDoc**: http://127.0.0.1:8888/redoc
- **OpenAPI JSON**: http://127.0.0.1:8888/openapi.json

## Path Parameters

```python
# String parameter (default)
@app.get("/items/{item_id}")
def get_item(item_id: str):
    return {"item_id": item_id}

# Integer parameter
@app.get("/users/{user_id:int}")
def get_user(user_id: int):
    return {"user_id": user_id}

# Float parameter
@app.get("/prices/{price:float}")
def get_price(price: float):
    return {"price": price}
```

## Request Handling

```python
from pureapi import PureAPI, Request

app = PureAPI()

@app.post("/data")
def handle_data(request: Request):
    # JSON body
    data = request.json
    
    # Query parameters
    params = request.query_params
    
    # Headers
    headers = request.headers
    
    return {"received": data}
```

## Error Handling

```python
from pureapi import HTTPException

@app.get("/items/{item_id:int}")
def get_item(item_id: int):
    if item_id < 0:
        raise HTTPException(status_code=400, detail="Invalid item ID")
    return {"item_id": item_id}

# Custom exception handler
@app.exception_handler(404)
def not_found(request, exc):
    return {"error": "Not found", "path": request.path}
```

## Sub-Routers

```python
from pureapi import PureAPI, Router

app = PureAPI()
api_router = Router()

@api_router.get("/users")
def list_users():
    return []

app.include_router(api_router, prefix="/api/v1")
# Route: /api/v1/users
```

## Running in Production

```bash
# With Gunicorn
gunicorn myapp:app -w 4 -b 0.0.0.0:8888

# With uWSGI
uwsgi --http :8888 --wsgi-file myapp.py --callable app
```

## Documentation

See the [docs](docs/README.md) folder for detailed documentation.

## License

MIT License - see [LICENSE](LICENSE) for details.
