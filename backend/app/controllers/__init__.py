"""
Controllers (Endpoints REST de la API)
"""
from .nations_controller import router as nations_router
from .game_controller import router as game_router
from .events_controller import router as events_router
from .turns_controller import router as turns_router
from .relations_controller import router as relations_router

__all__ = [
    "nations_router",
    "game_router",
    "events_router",
    "turns_router",
    "relations_router"
]
