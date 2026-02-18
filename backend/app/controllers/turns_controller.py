"""
Controller para endpoints de Turnos
Rutas: /api/turns/*
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..models.database import get_db
from ..services.turn_service import TurnService
from ..schemas.turn_schema import TurnResponse, TurnSummary

router = APIRouter(prefix="/api/turns", tags=["Turns"])


@router.get("/", response_model=List[TurnResponse])
def get_all_turns(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtener todos los turnos (ordenados por número descendente)
    """
    turns = TurnService.get_all(db, skip, limit)
    return turns


@router.get("/current", response_model=TurnResponse)
def get_current_turn(db: Session = Depends(get_db)):
    """
    Obtener el turno actual (último creado)
    """
    turn = TurnService.get_current(db)
    if not turn:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay turnos creados. Inicializa el juego primero."
        )
    return turn


@router.get("/{turn_id}", response_model=TurnResponse)
def get_turn(turn_id: int, db: Session = Depends(get_db)):
    """
    Obtener un turno específico por ID
    """
    turn = TurnService.get_by_id(db, turn_id)
    if not turn:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Turno con ID {turn_id} no encontrado"
        )
    return turn


@router.get("/number/{turn_number}", response_model=TurnResponse)
def get_turn_by_number(turn_number: int, db: Session = Depends(get_db)):
    """
    Obtener un turno específico por su número
    """
    turn = TurnService.get_by_number(db, turn_number)
    if not turn:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Turno número {turn_number} no encontrado"
        )
    return turn
