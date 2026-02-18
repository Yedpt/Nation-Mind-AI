"""
Schemas Pydantic para Relation
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional


class RelationBase(BaseModel):
    """Schema base de Relation"""
    nation_a_id: int = Field(..., ge=1)
    nation_b_id: int = Field(..., ge=1)
    status: str = Field(default="neutral", pattern="^(allied|war|neutral|trade_agreement)$")
    relationship_score: int = Field(default=0, ge=-100, le=100)
    
    @field_validator('nation_b_id')
    @classmethod
    def nations_must_be_different(cls, v, info):
        """Validar que no sea la misma nación"""
        if 'nation_a_id' in info.data and v == info.data['nation_a_id']:
            raise ValueError('Una nación no puede tener relación consigo misma')
        return v


class RelationCreate(RelationBase):
    """Schema para crear una relación"""
    pass


class RelationUpdate(BaseModel):
    """Schema para actualizar una relación"""
    status: Optional[str] = None
    relationship_score: Optional[int] = Field(None, ge=-100, le=100)


class RelationResponse(RelationBase):
    """Schema para respuestas"""
    id: int

    class Config:
        from_attributes = True
