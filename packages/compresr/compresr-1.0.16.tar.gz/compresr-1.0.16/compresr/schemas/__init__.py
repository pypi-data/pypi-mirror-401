"""
Compresr SDK Schemas

Exact copies of schemas from backend.
Single source of truth maintained in backend.
"""

# Import local schemas
from .base import BaseResponse, MessageResponse
from ..exceptions import (
    # Response models
    ErrorResponse,
    ValidationErrorResponse, 
    AuthenticationErrorResponse,
    RateLimitErrorResponse,
    ScopeErrorResponse,
    ServerErrorResponse,
    NotFoundErrorResponse,
    ConnectionErrorResponse,
    # Exception classes
    CompresrError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    ScopeError,
    ServerError,
    NotFoundError,
    ConnectionError,
)
from .inference import (
    # Streaming
    StreamChunk,
    # Compression
    CompressRequest,
    CompressResponse,
    CompressResult,
    BatchCompressRequest,
    BatchCompressResponse,
    BatchCompressResult,
)
from .usage import (
    MoneyBalanceResponse,
    MoneyBalanceResult,
)

__all__ = [
    # Base
    "BaseResponse",
    "MessageResponse", 
    
    # Response models
    "ErrorResponse",
    "ValidationErrorResponse",
    "AuthenticationErrorResponse", 
    "RateLimitErrorResponse",
    "ScopeErrorResponse",
    "ServerErrorResponse",
    "NotFoundErrorResponse",
    "ConnectionErrorResponse",
    
    # Exception classes
    "CompresrError",
    "AuthenticationError",
    "RateLimitError",
    "ValidationError",
    "ScopeError",
    "ServerError",
    "NotFoundError",
    "ConnectionError",
    
    # Streaming
    "StreamChunk",
    
    # Compression
    "CompressRequest",
    "CompressResponse", 
    "CompressResult",
    "BatchCompressRequest",
    "BatchCompressResponse",
    "BatchCompressResult",
    
    # Usage
    "MoneyBalanceResponse",
    "MoneyBalanceResult",
]
