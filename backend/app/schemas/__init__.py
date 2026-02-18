"""
Schemas Pydantic para validación de datos
"""
from .nation_schema import (
    NationBase,
    NationCreate,
    NationUpdate,
    NationResponse,
    NationSummary
)
from .event_schema import (
    EventBase,
    EventCreate,
    EventResponse,
    EventSummary
)
from .turn_schema import (
    TurnBase,
    TurnCreate,
    TurnResponse,
    TurnSummary
)
from .relation_schema import (
    RelationBase,
    RelationCreate,
    RelationUpdate,
    RelationResponse
)
from .game_schema import (
    ActionRequest,
    GameStateResponse,
    MessageResponse
)

__all__ = [
    # Nation
    "NationBase",
    "NationCreate",
    "NationUpdate",
    "NationResponse",
    "NationSummary",
    # Event
    "EventBase",
    "EventCreate",
    "EventResponse",
    "EventSummary",
    # Turn
    "TurnBase",
    "TurnCreate",
    "TurnResponse",
    "TurnSummary",
    # Relation
    "RelationBase",
    "RelationCreate",
    "RelationUpdate",
    "RelationResponse",
    # Game
    "ActionRequest",
    "GameStateResponse",
    "MessageResponse"
]
