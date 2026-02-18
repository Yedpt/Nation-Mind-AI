"""
Controller para endpoints de Eventos
Rutas: /api/events/*
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..models.database import get_db
from ..services.event_service import EventService
from ..schemas.event_schema import EventCreate, EventResponse, EventSummary

router = APIRouter(prefix="/api/events", tags=["Events"])


@router.get("/", response_model=List[EventResponse])
def get_all_events(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtener todos los eventos (ordenados por fecha descendente)
    """
    events = EventService.get_all(db, skip, limit)
    return events


@router.get("/recent", response_model=List[EventSummary])
def get_recent_events(limit: int = 20, db: Session = Depends(get_db)):
    """
    Obtener los eventos más recientes (para feed de noticias)
    """
    events = EventService.get_recent_events(db, limit)
    return events


@router.get("/important", response_model=List[EventResponse])
def get_important_events(
    min_importance: int = 7,
    limit: int = 30,
    db: Session = Depends(get_db)
):
    """
    Obtener eventos importantes (usados por el sistema RAG)
    
    - **min_importance**: Importancia mínima (1-10)
    - **limit**: Máximo de eventos a devolver
    """
    events = EventService.get_important_events(db, min_importance, limit)
    return events


@router.get("/turn/{turn_id}", response_model=List[EventResponse])
def get_events_by_turn(turn_id: int, db: Session = Depends(get_db)):
    """
    Obtener todos los eventos de un turno específico
    """
    events = EventService.get_by_turn(db, turn_id)
    return events


@router.get("/nation/{nation_id}", response_model=List[EventResponse])
def get_events_by_nation(
    nation_id: int,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Obtener eventos de una nación específica
    """
    events = EventService.get_by_nation(db, nation_id, limit)
    return events


@router.get("/type/{event_type}", response_model=List[EventResponse])
def get_events_by_type(
    event_type: str,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Obtener eventos filtrados por tipo
    
    Tipos comunes: attack, alliance, trade, recruit, declaration
    """
    events = EventService.get_by_type(db, event_type, limit)
    return events


@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """
    Obtener un evento específico por ID
    """
    event = EventService.get_by_id(db, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evento con ID {event_id} no encontrado"
        )
    return event


@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event_data: EventCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo evento
    
    Normalmente llamado internamente por el sistema de juego
    """
    event = EventService.create(db, event_data)
    return event
