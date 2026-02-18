"""
Modelo de Evento (Event)
Representa acciones que ocurren en el juego
Estos eventos se almacenan también en ChromaDB para el sistema RAG
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from datetime import datetime
from .database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    
    # Turno en el que ocurrió
    turn_id = Column(Integer, ForeignKey("turns.id"), index=True)
    
    # Nación que realizó la acción
    nation_id = Column(Integer, ForeignKey("nations.id"), index=True)
    
    # Tipo de evento
    event_type = Column(String(50), index=True)  # "attack", "alliance", "trade", "declaration", etc.
    
    # Descripción del evento (texto natural)
    description = Column(String(500), nullable=False)
    
    # Datos estructurados del evento
    data = Column(JSON, default=dict)  # {"target": "France", "troops_lost": 50, etc.}
    
    # Importancia del evento (afecta a la búsqueda RAG)
    importance = Column(Integer, default=5)  # 1-10
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<Event(type='{self.event_type}', nation_id={self.nation_id}, turn={self.turn_id})>"
    
    def to_dict(self):
        """Convertir a diccionario para JSON"""
        return {
            "id": self.id,
            "turn_id": self.turn_id,
            "nation_id": self.nation_id,
            "event_type": self.event_type,
            "description": self.description,
            "data": self.data,
            "importance": self.importance,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
