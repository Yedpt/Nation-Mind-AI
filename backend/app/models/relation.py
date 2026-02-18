"""
Modelo de Relación Diplomática (Relation)
Representa las relaciones entre naciones
"""
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from .database import Base


class Relation(Base):
    __tablename__ = "relations"

    id = Column(Integer, primary_key=True, index=True)
    
    # Naciones involucradas
    nation_a_id = Column(Integer, ForeignKey("nations.id"), nullable=False, index=True)
    nation_b_id = Column(Integer, ForeignKey("nations.id"), nullable=False, index=True)
    
    # Estado de la relación
    status = Column(String(30), default="neutral")  # "allied", "war", "neutral", "trade_agreement"
    
    # Nivel de relación (-100 a +100)
    relationship_score = Column(Integer, default=0)  # Negativo = hostil, Positivo = amistoso
    
    # Evitar duplicados (A-B es lo mismo que B-A)
    __table_args__ = (
        UniqueConstraint('nation_a_id', 'nation_b_id', name='_nation_pair_uc'),
    )
    
    def __repr__(self):
        return f"<Relation(nation_a={self.nation_a_id}, nation_b={self.nation_b_id}, status='{self.status}')>"
    
    def to_dict(self):
        """Convertir a diccionario para JSON"""
        return {
            "id": self.id,
            "nation_a_id": self.nation_a_id,
            "nation_b_id": self.nation_b_id,
            "status": self.status,
            "relationship_score": self.relationship_score
        }
