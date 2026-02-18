"""
Schemas Pydantic para Turn
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any


class TurnBase(BaseModel):
    """Schema base de Turn"""
    turn_number: int = Field(..., ge=1)
    world_state: Dict[str, Any] = Field(default_factory=dict)
    summary: Optional[str] = Field(None, max_length=500)


class TurnCreate(TurnBase):
    """Schema para crear un turno"""
    pass


class TurnResponse(TurnBase):
    """Schema para respuestas"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TurnSummary(BaseModel):
    """Schema resumido de turno (para listas)"""
    id: int
    turn_number: int
    summary: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
