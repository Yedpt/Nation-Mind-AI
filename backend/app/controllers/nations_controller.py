"""
Controller para endpoints de Naciones
Rutas: /api/nations/*
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..models.database import get_db
from ..services.nation_service import NationService
from ..schemas.nation_schema import (
    NationCreate,
    NationUpdate,
    NationResponse,
    NationSummary
)

router = APIRouter(prefix="/api/nations", tags=["Nations"])


@router.get("/", response_model=List[NationResponse])
def get_all_nations(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """
    Obtener todas las naciones
    
    - **skip**: Número de registros a saltar (paginación)
    - **limit**: Máximo de registros a devolver
    - **active_only**: Solo naciones activas (por defecto True)
    """
    nations = NationService.get_all(db, skip, limit, active_only)
    return nations


@router.get("/summary", response_model=List[NationSummary])
def get_nations_summary(db: Session = Depends(get_db)):
    """
    Obtener resumen de todas las naciones (más ligero)
    """
    nations = NationService.get_all(db)
    return nations


@router.get("/player", response_model=NationResponse)
def get_player_nation(db: Session = Depends(get_db)):
    """
    Obtener la nación controlada por el jugador
    """
    nation = NationService.get_player_nation(db)
    if not nation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay nación de jugador"
        )
    return nation


@router.get("/ai", response_model=List[NationResponse])
def get_ai_nations(db: Session = Depends(get_db)):
    """
    Obtener todas las naciones controladas por IA
    """
    nations = NationService.get_ai_nations(db)
    return nations


@router.get("/{nation_id}", response_model=NationResponse)
def get_nation(nation_id: int, db: Session = Depends(get_db)):
    """
    Obtener una nación específica por ID
    """
    nation = NationService.get_by_id(db, nation_id)
    if not nation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nación con ID {nation_id} no encontrada"
        )
    return nation


@router.post("/", response_model=NationResponse, status_code=status.HTTP_201_CREATED)
def create_nation(nation_data: NationCreate, db: Session = Depends(get_db)):
    """
    Crear una nueva nación
    """
    # Verificar que no exista ya una nación con ese nombre
    existing = NationService.get_by_name(db, nation_data.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una nación llamada '{nation_data.name}'"
        )
    
    nation = NationService.create(db, nation_data)
    return nation


@router.put("/{nation_id}", response_model=NationResponse)
def update_nation(
    nation_id: int,
    nation_data: NationUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar una nación existente
    """
    nation = NationService.update(db, nation_id, nation_data)
    if not nation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nación con ID {nation_id} no encontrada"
        )
    return nation


@router.delete("/{nation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_nation(nation_id: int, db: Session = Depends(get_db)):
    """
    Eliminar (desactivar) una nación
    """
    success = NationService.delete(db, nation_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nación con ID {nation_id} no encontrada"
        )
    return None


@router.patch("/{nation_id}/resources", response_model=NationResponse)
def update_nation_resources(
    nation_id: int,
    gold_change: int = 0,
    troops_change: int = 0,
    db: Session = Depends(get_db)
):
    """
    Actualizar recursos de una nación
    
    - **gold_change**: Cantidad de oro a sumar/restar
    - **troops_change**: Cantidad de tropas a sumar/restar
    """
    nation = NationService.update_resources(db, nation_id, gold_change, troops_change)
    if not nation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nación con ID {nation_id} no encontrada"
        )
    return nation
