"""
PureAPI - A lightweight and elegant Python web framework.

Features:
- Modern routing with type annotations
- OpenAPI documentation (Swagger UI & ReDoc)
- Simple and intuitive API design
"""

from .app import PureAPI
from .request import Request
from .response import Response, JSONResponse, HTMLResponse
from .routing import Router, Route
from .exceptions import HTTPException

__version__ = "0.1.0"
__author__ = "MarkHoo"
__all__ = [
    "PureAPI",
    "Request", 
    "Response",
    "JSONResponse",
    "HTMLResponse",
    "Router",
    "Route",
    "HTTPException",
]
