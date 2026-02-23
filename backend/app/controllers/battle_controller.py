"""
Controlador de Batallas
Endpoints para gestionar y simular batallas entre naciones
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..models.database import get_db
from ..services.battle_service import BattleService
from ..schemas.battle_schema import BattleResponse, BattleSimulation, BattleSimulationResult


router = APIRouter(prefix="/api/battles", tags=["battles"])


@router.post("/resolve", response_model=BattleResponse, status_code=201)
def resolve_battle(
    attacker_id: int,
    defender_id: int,
    turn_number: int,
    db: Session = Depends(get_db)
):
    """
    Resolver una batalla entre dos naciones.
    
    - **attacker_id**: ID de la nación atacante
    - **defender_id**: ID de la nación defensora
    - **turn_number**: Turno actual del juego
    
    Returns: Resultado completo de la batalla con bajas, conquistasyuda y botín
    """
    try:
        battle = BattleService.resolve_battle(db, attacker_id, defender_id, turn_number)
        return battle
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resolviendo batalla: {str(e)}")


@router.post("/simulate", response_model=BattleSimulationResult)
def simulate_battle(
    simulation: BattleSimulation,
    db: Session = Depends(get_db)
):
    """
    Simular una batalla SIN ejecutarla.
    
    Útil para que los agentes IA evalúen si atacar es una buena idea.
    Retorna probabilidades de victoria, bajas esperadas y recomendación.
    
    - **attacker_id**: ID de la nación atacante
    - **defender_id**: ID de la nación defensora
    - **include_allies**: Si considerar aliados en la simulación (por defecto True)
    """
    try:
        result = BattleService.simulate_battle(
            db, 
            simulation.attacker_id, 
            simulation.defender_id
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error simulando batalla: {str(e)}")


@router.get("/history", response_model=List[BattleResponse])
def get_battle_history(
    limit: int = Query(20, ge=1, le=100, description="Número máximo de batallas a retornar"),
    db: Session = Depends(get_db)
):
    """
    Obtener historial de batallas recientes.
    
    - **limit**: Número de batallas a retornar (1-100)
    """
    try:
        battles = BattleService.get_battle_history(db, limit)
        return battles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo historial: {str(e)}")


@router.get("/nation/{nation_id}", response_model=List[BattleResponse])
def get_nation_battles(
    nation_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener todas las batallas de una nación específica.
    
    Incluye batallas donde la nación fue atacante y defensora.
    
    - **nation_id**: ID de la nación
    """
    try:
        battles = BattleService.get_nation_battles(db, nation_id)
        return battles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo batallas: {str(e)}")


@router.get("/active-wars")
def get_active_wars(db: Session = Depends(get_db)):
    """
    Obtener todas las guerras activas en el mundo.
    
    Retorna lista de parejas de naciones en estado de guerra.
    """
    try:
        wars = BattleService.get_active_wars(db)
        return {
            "active_wars": wars,
            "total": len(wars)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo guerras activas: {str(e)}")


@router.get("/{battle_id}", response_model=BattleResponse)
def get_battle_by_id(
    battle_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener detalles de una batalla específica por su ID.
    
    - **battle_id**: ID de la batalla
    """
    from ..models.battle import Battle
    
    battle = db.query(Battle).filter(Battle.id == battle_id).first()
    
    if not battle:
        raise HTTPException(status_code=404, detail="Batalla no encontrada")
    
    return battle
