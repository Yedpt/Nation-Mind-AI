"""
Schemas Pydantic para Nation
Usados para validar datos de entrada/salida en la API
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class NationBase(BaseModel):
    """Schema base de Nation (campos comunes)"""
    name: str = Field(..., min_length=3, max_length=100)
    personality: str = Field(default="neutral", pattern="^(aggressive|diplomatic|defensive|expansionist|neutral)$")
    gold: int = Field(default=1000, ge=0)
    troops: int = Field(default=100, ge=0)
    territories: int = Field(default=1, ge=1)
    military_power: float = Field(default=50.0, ge=0, le=100)
    economic_power: float = Field(default=50.0, ge=0, le=100)
    diplomatic_influence: float = Field(default=50.0, ge=0, le=100)
    objectives: List[str] = Field(default_factory=list)
    ai_controlled: bool = True


class NationCreate(NationBase):
    """Schema para crear una nación"""
    pass


class NationUpdate(BaseModel):
    """Schema para actualizar una nación (todos los campos opcionales)"""
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    personality: Optional[str] = None
    gold: Optional[int] = Field(None, ge=0)
    troops: Optional[int] = Field(None, ge=0)
    territories: Optional[int] = Field(None, ge=1)
    military_power: Optional[float] = Field(None, ge=0, le=100)
    economic_power: Optional[float] = Field(None, ge=0, le=100)
    diplomatic_influence: Optional[float] = Field(None, ge=0, le=100)
    objectives: Optional[List[str]] = None
    ai_controlled: Optional[bool] = None
    is_active: Optional[bool] = None


class NationResponse(NationBase):
    """Schema para respuestas (incluye id y is_active)"""
    id: int
    is_active: bool

    class Config:
        from_attributes = True  # Permite convertir desde modelos SQLAlchemy


class NationSummary(BaseModel):
    """Schema resumido de nación (para listas)"""
    id: int
    name: str
    personality: str
    ai_controlled: bool
    is_active: bool

    class Config:
        from_attributes = True
