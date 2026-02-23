"""
Modelo de Batalla
Registra todas las batallas entre naciones
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Battle(Base):
    """Modelo de Batalla entre naciones"""
    __tablename__ = "battles"
    
    id = Column(Integer, primary_key=True, index=True)
    turn_number = Column(Integer, nullable=False, index=True)
    
    # Participantes
    attacker_id = Column(Integer, ForeignKey("nations.id"), nullable=False)
    defender_id = Column(Integer, ForeignKey("nations.id"), nullable=False)
    winner_id = Column(Integer, ForeignKey("nations.id"), nullable=True)
    
    # Tipo de batalla
    battle_type = Column(String, nullable=False)  # skirmish, battle, total_war
    
    # Fuerzas iniciales
    attacker_troops_initial = Column(Integer, nullable=False)
    defender_troops_initial = Column(Integer, nullable=False)
    attacker_power = Column(Float, nullable=False)
    defender_power = Column(Float, nullable=False)
    
    # Aliados participantes (JSON array de nation_ids)
    attacker_allies = Column(JSON, default=list)
    defender_allies = Column(JSON, default=list)
    
    # Bonificaciones
    attacker_bonus = Column(Float, default=0.0)
    defender_bonus = Column(Float, default=0.0)
    
    # Resultados
    attacker_casualties = Column(Integer, default=0)
    defender_casualties = Column(Integer, default=0)
    territories_conquered = Column(Integer, default=0)
    gold_looted = Column(Integer, default=0)
    
    # Probabilidades
    attacker_win_chance = Column(Float, nullable=False)
    defender_win_chance = Column(Float, nullable=False)
    
    # Estado
    is_decisive = Column(Boolean, default=False)  # Victoria decisiva
    description = Column(String, nullable=True)  # Descripción de la batalla
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    attacker = relationship("Nation", foreign_keys=[attacker_id], back_populates="battles_as_attacker")
    defender = relationship("Nation", foreign_keys=[defender_id], back_populates="battles_as_defender")
    winner = relationship("Nation", foreign_keys=[winner_id], back_populates="battles_won")
    
    def __repr__(self):
        return f"<Battle {self.id}: {self.attacker_id} vs {self.defender_id} (Turn {self.turn_number})>"
