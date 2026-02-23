"""
Servicio para gestión de Eventos
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.event import Event
from ..schemas.event_schema import EventCreate


class EventService:
    """Servicio para operaciones de eventos"""
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[Event]:
        """Obtener todos los eventos (ordenados por fecha)"""
        return db.query(Event).order_by(Event.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, event_id: int) -> Optional[Event]:
        """Obtener evento por ID"""
        return db.query(Event).filter(Event.id == event_id).first()
    
    @staticmethod
    def get_by_turn(db: Session, turn_id: int) -> List[Event]:
        """Obtener todos los eventos de un turno específico"""
        return db.query(Event).filter(Event.turn_id == turn_id).order_by(Event.created_at).all()
    
    @staticmethod
    def get_by_nation(db: Session, nation_id: int, limit: int = 50) -> List[Event]:
        """Obtener eventos de una nación específica"""
        return db.query(Event).filter(
            Event.nation_id == nation_id
        ).order_by(Event.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_by_type(db: Session, event_type: str, limit: int = 50) -> List[Event]:
        """Obtener eventos por tipo"""
        return db.query(Event).filter(
            Event.event_type == event_type
        ).order_by(Event.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def create(db: Session, event_data: EventCreate, add_to_rag: bool = True) -> Event:
        """
        Crear un nuevo evento
        
        Args:
            db: Sesión de base de datos
            event_data: Datos del evento
            add_to_rag: Si True, añade el evento a ChromaDB para RAG
        """
        event = Event(**event_data.model_dump())
        db.add(event)
        db.commit()
        db.refresh(event)
        
        # Añadir a sistema RAG automáticamente
        if add_to_rag:
            try:
                from .rag_service import get_rag_service
                rag = get_rag_service()
                rag.add_event(event)
            except Exception as e:
                print(f"⚠️ Warning: No se pudo añadir evento a RAG: {e}")
        
        return event
    
    @staticmethod
    def get_recent_events(db: Session, limit: int = 20) -> List[Event]:
        """Obtener los eventos más recientes"""
        return db.query(Event).order_by(Event.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_important_events(db: Session, min_importance: int = 7, limit: int = 30) -> List[Event]:
        """Obtener eventos importantes (para el sistema RAG)"""
        return db.query(Event).filter(
            Event.importance >= min_importance
        ).order_by(Event.importance.desc(), Event.created_at.desc()).limit(limit).all()
