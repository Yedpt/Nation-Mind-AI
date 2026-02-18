"""
Modelo de Turno (Turn)
Representa cada turno del juego
"""
from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
from .database import Base


class Turn(Base):
    __tablename__ = "turns"

    id = Column(Integer, primary_key=True, index=True)
    turn_number = Column(Integer, index=True, nullable=False)
    
    # Estado del mundo en este turno (snapshot)
    world_state = Column(JSON, default=dict)  # {"nations": {...}, "alliances": [...], etc.}
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Resumen de lo que pasó en este turno (generado por LLM)
    summary = Column(String(500), nullable=True)
    
    def __repr__(self):
        return f"<Turn(number={self.turn_number}, created={self.created_at})>"
    
    def to_dict(self):
        """Convertir a diccionario para JSON"""
        return {
            "id": self.id,
            "turn_number": self.turn_number,
            "world_state": self.world_state,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "summary": self.summary
        }
