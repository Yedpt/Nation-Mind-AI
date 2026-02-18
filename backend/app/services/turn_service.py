"""
Servicio para gestión de Turnos
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.turn import Turn
from ..schemas.turn_schema import TurnCreate


class TurnService:
    """Servicio para operaciones de turnos"""
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Turn]:
        """Obtener todos los turnos (ordenados por número)"""
        return db.query(Turn).order_by(Turn.turn_number.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, turn_id: int) -> Optional[Turn]:
        """Obtener turno por ID"""
        return db.query(Turn).filter(Turn.id == turn_id).first()
    
    @staticmethod
    def get_by_number(db: Session, turn_number: int) -> Optional[Turn]:
        """Obtener turno por número"""
        return db.query(Turn).filter(Turn.turn_number == turn_number).first()
    
    @staticmethod
    def get_current(db: Session) -> Optional[Turn]:
        """Obtener el turno actual (último)"""
        return db.query(Turn).order_by(Turn.turn_number.desc()).first()
    
    @staticmethod
    def create(db: Session, turn_data: TurnCreate) -> Turn:
        """Crear un nuevo turno"""
        turn = Turn(**turn_data.model_dump())
        db.add(turn)
        db.commit()
        db.refresh(turn)
        return turn
    
    @staticmethod
    def get_current_turn_number(db: Session) -> int:
        """Obtener el número del turno actual"""
        current_turn = TurnService.get_current(db)
        return current_turn.turn_number if current_turn else 0
    
    @staticmethod
    def create_next_turn(db: Session, world_state: dict, summary: str = None) -> Turn:
        """Crear el siguiente turno automáticamente"""
        current_number = TurnService.get_current_turn_number(db)
        next_number = current_number + 1
        
        turn_data = TurnCreate(
            turn_number=next_number,
            world_state=world_state,
            summary=summary
        )
        
        return TurnService.create(db, turn_data)
