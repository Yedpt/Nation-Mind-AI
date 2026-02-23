"""
Schemas Pydantic para Battle (Batallas)
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class BattleBase(BaseModel):
    """Schema base para Battle"""
    attacker_id: int = Field(..., description="ID de la nación atacante")
    defender_id: int = Field(..., description="ID de la nación defensora")
    battle_type: str = Field(..., description="Tipo de batalla: skirmish, battle, total_war")


class BattleCreate(BattleBase):
    """Schema para crear una Battle"""
    turn_number: int = Field(..., description="Número del turno")


class BattleResponse(BattleBase):
    """Schema de respuesta con todos los datos de Battle"""
    id: int
    turn_number: int
    winner_id: Optional[int] = None
    
    # Fuerzas iniciales
    attacker_troops_initial: int
    defender_troops_initial: int
    attacker_power: float
    defender_power: float
    
    # Aliados
    attacker_allies: List[int] = []
    defender_allies: List[int] = []
    
    # Bonificaciones
    attacker_bonus: float = 0.0
    defender_bonus: float = 0.0
    
    # Resultados
    attacker_casualties: int = 0
    defender_casualties: int = 0
    territories_conquered: int = 0
    gold_looted: int = 0
    
    # Probabilidades
    attacker_win_chance: float
    defender_win_chance: float
    
    # Estado
    is_decisive: bool = False
    description: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class BattleSimulation(BaseModel):
    """Schema para simular una batalla SIN ejecutarla"""
    attacker_id: int
    defender_id: int
    include_allies: bool = True


class BattleSimulationResult(BaseModel):
    """Resultado de una simulación de batalla"""
    attacker_win_chance: float
    defender_win_chance: float
    attacker_expected_casualties: int
    defender_expected_casualties: int
    expected_territories: int
    expected_gold: int
    recommendation: str  # "attack", "defensive", "avoid"
    factors: dict  # Desglose de bonificaciones
