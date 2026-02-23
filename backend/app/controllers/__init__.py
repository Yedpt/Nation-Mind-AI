"""
Controllers (Endpoints REST de la API)
"""
from .nations_controller import router as nations_router
from .game_controller import router as game_router
from .events_controller import router as events_router
from .turns_controller import router as turns_router
from .relations_controller import router as relations_router
from .memory_controller import router as memory_router
from .agent_controller import router as agent_router
from .battle_controller import router as battle_router

__all__ = [
    "nations_router",
    "game_router",
    "events_router",
    "turns_router",
    "relations_router",
    "memory_router",
    "agent_router",
    "battle_router"
]
