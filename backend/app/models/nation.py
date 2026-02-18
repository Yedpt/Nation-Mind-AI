"""
Modelo de Nación (Nation)
Representa a cada país/estado en el simulador
"""
from sqlalchemy import Column, Integer, String, Boolean, JSON, Float
from sqlalchemy.orm import relationship
from .database import Base


class Nation(Base):
    __tablename__ = "nations"

    # Campos básicos
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    
    # Personalidad del agente IA
    personality = Column(String(50), default="neutral")  # aggressive, diplomatic, defensive, expansionist
    
    # Recursos
    gold = Column(Integer, default=1000)
    troops = Column(Integer, default=100)
    territories = Column(Integer, default=1)
    
    # Estadísticas de poder
    military_power = Column(Float, default=50.0)  # 0-100
    economic_power = Column(Float, default=50.0)  # 0-100
    diplomatic_influence = Column(Float, default=50.0)  # 0-100
    
    # Objetivos estratégicos (almacenados como JSON)
    objectives = Column(JSON, default=list)  # ["conquer_X", "ally_with_Y", etc.]
    
    # Control
    ai_controlled = Column(Boolean, default=True)  # True = IA, False = Jugador
    is_active = Column(Boolean, default=True)  # False si fue eliminada
    
    # Relaciones con otras tablas
    # turns = relationship("Turn", back_populates="nation")
    # events = relationship("Event", back_populates="nation")
    
    def __repr__(self):
        return f"<Nation(name='{self.name}', personality='{self.personality}', ai={self.ai_controlled})>"
    
    def to_dict(self):
        """Convertir a diccionario para JSON"""
        return {
            "id": self.id,
            "name": self.name,
            "personality": self.personality,
            "gold": self.gold,
            "troops": self.troops,
            "territories": self.territories,
            "military_power": self.military_power,
            "economic_power": self.economic_power,
            "diplomatic_influence": self.diplomatic_influence,
            "objectives": self.objectives,
            "ai_controlled": self.ai_controlled,
            "is_active": self.is_active
        }
