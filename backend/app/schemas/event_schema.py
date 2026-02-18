"""
Schemas Pydantic para Event
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any


class EventBase(BaseModel):
    """Schema base de Event"""
    turn_id: int = Field(..., ge=1)
    nation_id: int = Field(..., ge=1)
    event_type: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=10, max_length=500)
    data: Dict[str, Any] = Field(default_factory=dict)
    importance: int = Field(default=5, ge=1, le=10)


class EventCreate(EventBase):
    """Schema para crear un evento"""
    pass


class EventResponse(EventBase):
    """Schema para respuestas"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class EventSummary(BaseModel):
    """Schema resumido de evento"""
    id: int
    event_type: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True
