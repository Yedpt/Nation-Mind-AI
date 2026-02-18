"""
Controller para endpoints de Relaciones Diplomáticas
Rutas: /api/relations/*
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..models.database import get_db
from ..services.relation_service import RelationService
from ..schemas.relation_schema import RelationCreate, RelationUpdate, RelationResponse

router = APIRouter(prefix="/api/relations", tags=["Relations"])


@router.get("/", response_model=List[RelationResponse])
def get_all_relations(db: Session = Depends(get_db)):
    """
    Obtener todas las relaciones diplomáticas
    """
    relations = RelationService.get_all(db)
    return relations


@router.get("/nation/{nation_id}", response_model=List[RelationResponse])
def get_nation_relations(nation_id: int, db: Session = Depends(get_db)):
    """
    Obtener todas las relaciones de una nación específica
    """
    relations = RelationService.get_nation_relations(db, nation_id)
    return relations


@router.get("/nation/{nation_id}/allies", response_model=List[RelationResponse])
def get_nation_allies(nation_id: int, db: Session = Depends(get_db)):
    """
    Obtener aliados de una nación
    """
    allies = RelationService.get_allies(db, nation_id)
    return allies


@router.get("/nation/{nation_id}/enemies", response_model=List[RelationResponse])
def get_nation_enemies(nation_id: int, db: Session = Depends(get_db)):
    """
    Obtener enemigos de una nación (en guerra)
    """
    enemies = RelationService.get_enemies(db, nation_id)
    return enemies


@router.get("/between/{nation_a_id}/{nation_b_id}", response_model=RelationResponse)
def get_relation_between_nations(
    nation_a_id: int,
    nation_b_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener la relación entre dos naciones específicas
    """
    relation = RelationService.get_between_nations(db, nation_a_id, nation_b_id)
    if not relation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe relación entre naciones {nation_a_id} y {nation_b_id}"
        )
    return relation


@router.get("/{relation_id}", response_model=RelationResponse)
def get_relation(relation_id: int, db: Session = Depends(get_db)):
    """
    Obtener una relación específica por ID
    """
    relation = RelationService.get_by_id(db, relation_id)
    if not relation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Relación con ID {relation_id} no encontrada"
        )
    return relation


@router.post("/", response_model=RelationResponse, status_code=status.HTTP_201_CREATED)
def create_relation(relation_data: RelationCreate, db: Session = Depends(get_db)):
    """
    Crear una nueva relación diplomática
    """
    # Verificar que no exista ya
    existing = RelationService.get_between_nations(
        db, 
        relation_data.nation_a_id, 
        relation_data.nation_b_id
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una relación entre estas naciones"
        )
    
    relation = RelationService.create(db, relation_data)
    return relation


@router.put("/{relation_id}", response_model=RelationResponse)
def update_relation(
    relation_id: int,
    relation_data: RelationUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar una relación diplomática existente
    """
    relation = RelationService.update(db, relation_id, relation_data)
    if not relation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Relación con ID {relation_id} no encontrada"
        )
    return relation


@router.post("/update-or-create", response_model=RelationResponse)
def update_or_create_relation(
    nation_a_id: int,
    nation_b_id: int,
    status: str = None,
    relationship_score: int = None,
    db: Session = Depends(get_db)
):
    """
    Actualizar una relación si existe, o crearla si no existe
    
    Útil para cambios dinámicos durante el juego
    """
    relation = RelationService.update_or_create(
        db,
        nation_a_id,
        nation_b_id,
        status,
        relationship_score
    )
    return relation
