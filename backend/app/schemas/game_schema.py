"""
Schemas Pydantic adicionales para acciones y estado del juego
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from .nation_schema import NationSummary
from .event_schema import EventSummary


class ActionRequest(BaseModel):
    """Schema para acciones del jugador"""
    action_type: str = Field(..., pattern="^(attack|alliance|trade|move_troops|recruit|build)$")
    target_nation_id: Optional[int] = None
    data: Dict[str, Any] = Field(default_factory=dict)


class GameStateResponse(BaseModel):
    """Schema para el estado completo del juego"""
    current_turn: int
    nations: List[NationSummary]
    recent_events: List[EventSummary] = Field(default_factory=list)
    player_nation_id: Optional[int]
    is_game_over: bool = False
    winner: Optional[str] = None
    victory_type: Optional[str] = None
    victory_progress: Optional[Dict[str, Any]] = None


class VictoryProgressResponse(BaseModel):
    """Schema para progreso de victoria"""
    domination: Dict[str, Any]
    elimination: Dict[str, Any]
    economic: Dict[str, Any]
    military: Dict[str, Any]
    survival: Dict[str, Any]
    
    
class LeaderboardEntry(BaseModel):
    """Schema para entrada del leaderboard"""
    rank: int
    nation_id: int
    nation_name: str
    total_score: int
    gold: int
    troops: int
    territories: int
    military_power: float
    economic_power: float
    diplomatic_influence: float


class MessageResponse(BaseModel):
    """Schema genérico para mensajes"""
    message: str
    success: bool = True
    data: Optional[Dict[str, Any]] = None
