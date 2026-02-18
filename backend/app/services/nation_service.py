"""
Servicio para gestión de Naciones
Contiene toda la lógica de negocio relacionada con naciones
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.nation import Nation
from ..schemas.nation_schema import NationCreate, NationUpdate


class NationService:
    """Servicio para operaciones CRUD y lógica de naciones"""
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[Nation]:
        """Obtener todas las naciones"""
        query = db.query(Nation)
        if active_only:
            query = query.filter(Nation.is_active == True)
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, nation_id: int) -> Optional[Nation]:
        """Obtener nación por ID"""
        return db.query(Nation).filter(Nation.id == nation_id).first()
    
    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[Nation]:
        """Obtener nación por nombre"""
        return db.query(Nation).filter(Nation.name == name).first()
    
    @staticmethod
    def create(db: Session, nation_data: NationCreate) -> Nation:
        """Crear una nueva nación"""
        nation = Nation(**nation_data.model_dump())
        db.add(nation)
        db.commit()
        db.refresh(nation)
        return nation
    
    @staticmethod
    def update(db: Session, nation_id: int, nation_data: NationUpdate) -> Optional[Nation]:
        """Actualizar una nación existente"""
        nation = NationService.get_by_id(db, nation_id)
        if not nation:
            return None
        
        # Actualizar solo los campos que se enviaron
        update_data = nation_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(nation, key, value)
        
        db.commit()
        db.refresh(nation)
        return nation
    
    @staticmethod
    def delete(db: Session, nation_id: int) -> bool:
        """Eliminar (desactivar) una nación"""
        nation = NationService.get_by_id(db, nation_id)
        if not nation:
            return False
        
        nation.is_active = False
        db.commit()
        return True
    
    @staticmethod
    def get_ai_nations(db: Session) -> List[Nation]:
        """Obtener solo naciones controladas por IA"""
        return db.query(Nation).filter(
            Nation.ai_controlled == True,
            Nation.is_active == True
        ).all()
    
    @staticmethod
    def get_player_nation(db: Session) -> Optional[Nation]:
        """Obtener la nación del jugador"""
        return db.query(Nation).filter(
            Nation.ai_controlled == False,
            Nation.is_active == True
        ).first()
    
    @staticmethod
    def update_resources(db: Session, nation_id: int, gold_change: int = 0, troops_change: int = 0) -> Optional[Nation]:
        """Actualizar recursos de una nación"""
        nation = NationService.get_by_id(db, nation_id)
        if not nation:
            return None
        
        nation.gold = max(0, nation.gold + gold_change)
        nation.troops = max(0, nation.troops + troops_change)
        
        db.commit()
        db.refresh(nation)
        return nation
    
    @staticmethod
    def calculate_total_power(nation: Nation) -> float:
        """Calcular poder total de una nación"""
        return (nation.military_power + nation.economic_power + nation.diplomatic_influence) / 3
