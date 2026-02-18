"""
Schemas Pydantic adicionales para acciones y estado del juego
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from .nation_schema import NationSummary


class ActionRequest(BaseModel):
    """Schema para acciones del jugador"""
    action_type: str = Field(..., pattern="^(attack|alliance|trade|move_troops|recruit|build)$")
    target_nation_id: Optional[int] = None
    data: Dict[str, Any] = Field(default_factory=dict)


class GameStateResponse(BaseModel):
    """Schema para el estado completo del juego"""
    current_turn: int
    nations: List[NationSummary]
    player_nation_id: Optional[int]
    is_game_over: bool = False
    winner: Optional[str] = None


class MessageResponse(BaseModel):
    """Schema genérico para mensajes"""
    message: str
    success: bool = True
    data: Optional[Dict[str, Any]] = None
