"""API routers for the model server proxy."""

from .chat import router as chat_router

__all__ = ["chat_router"]
