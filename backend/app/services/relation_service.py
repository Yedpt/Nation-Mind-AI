"""
Servicio para gestión de Relaciones Diplomáticas
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.relation import Relation
from ..schemas.relation_schema import RelationCreate, RelationUpdate


class RelationService:
    """Servicio para operaciones de relaciones diplomáticas"""
    
    @staticmethod
    def get_all(db: Session) -> List[Relation]:
        """Obtener todas las relaciones"""
        return db.query(Relation).all()
    
    @staticmethod
    def get_by_id(db: Session, relation_id: int) -> Optional[Relation]:
        """Obtener relación por ID"""
        return db.query(Relation).filter(Relation.id == relation_id).first()
    
    @staticmethod
    def get_between_nations(db: Session, nation_a_id: int, nation_b_id: int) -> Optional[Relation]:
        """Obtener relación entre dos naciones específicas"""
        # Las relaciones pueden estar en cualquier orden (A-B o B-A)
        return db.query(Relation).filter(
            ((Relation.nation_a_id == nation_a_id) & (Relation.nation_b_id == nation_b_id)) |
            ((Relation.nation_a_id == nation_b_id) & (Relation.nation_b_id == nation_a_id))
        ).first()
    
    @staticmethod
    def get_nation_relations(db: Session, nation_id: int) -> List[Relation]:
        """Obtener todas las relaciones de una nación"""
        return db.query(Relation).filter(
            (Relation.nation_a_id == nation_id) | (Relation.nation_b_id == nation_id)
        ).all()
    
    @staticmethod
    def create(db: Session, relation_data: RelationCreate) -> Relation:
        """Crear una nueva relación"""
        # Asegurarse de que siempre guardemos nation_a_id < nation_b_id para consistencia
        nation_a = min(relation_data.nation_a_id, relation_data.nation_b_id)
        nation_b = max(relation_data.nation_a_id, relation_data.nation_b_id)
        
        relation = Relation(
            nation_a_id=nation_a,
            nation_b_id=nation_b,
            status=relation_data.status,
            relationship_score=relation_data.relationship_score
        )
        
        db.add(relation)
        db.commit()
        db.refresh(relation)
        return relation
    
    @staticmethod
    def update(db: Session, relation_id: int, relation_data: RelationUpdate) -> Optional[Relation]:
        """Actualizar una relación existente"""
        relation = RelationService.get_by_id(db, relation_id)
        if not relation:
            return None
        
        update_data = relation_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(relation, key, value)
        
        db.commit()
        db.refresh(relation)
        return relation
    
    @staticmethod
    def update_or_create(db: Session, nation_a_id: int, nation_b_id: int, 
                        status: str = None, relationship_score: int = None) -> Relation:
        """Actualizar relación si existe, o crearla si no"""
        relation = RelationService.get_between_nations(db, nation_a_id, nation_b_id)
        
        if relation:
            # Actualizar existente
            if status:
                relation.status = status
            if relationship_score is not None:
                relation.relationship_score = relationship_score
            db.commit()
            db.refresh(relation)
            return relation
        else:
            # Crear nueva
            relation_data = RelationCreate(
                nation_a_id=nation_a_id,
                nation_b_id=nation_b_id,
                status=status or "neutral",
                relationship_score=relationship_score if relationship_score is not None else 0
            )
            return RelationService.create(db, relation_data)
    
    @staticmethod
    def get_allies(db: Session, nation_id: int) -> List[Relation]:
        """Obtener naciones aliadas"""
        return db.query(Relation).filter(
            ((Relation.nation_a_id == nation_id) | (Relation.nation_b_id == nation_id)) &
            (Relation.status == "allied")
        ).all()
    
    @staticmethod
    def get_enemies(db: Session, nation_id: int) -> List[Relation]:
        """Obtener naciones enemigas (en guerra)"""
        return db.query(Relation).filter(
            ((Relation.nation_a_id == nation_id) | (Relation.nation_b_id == nation_id)) &
            (Relation.status == "war")
        ).all()
