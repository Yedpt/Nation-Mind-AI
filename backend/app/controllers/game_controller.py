"""
Controller para endpoints del Juego
Rutas: /api/game/*
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..models.database import get_db
from ..services.game_service import GameService
from ..services.nation_service import NationService
from ..schemas.game_schema import ActionRequest, GameStateResponse, MessageResponse

router = APIRouter(prefix="/api/game", tags=["Game"])


@router.post("/initialize", response_model=MessageResponse)
def initialize_game(db: Session = Depends(get_db)):
    """
    Inicializar un nuevo juego
    
    Crea las naciones iniciales, el primer turno y las relaciones base
    """
    # Verificar que no haya ya un juego iniciado
    existing_nations = NationService.get_all(db, limit=1)
    if existing_nations:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un juego iniciado. Elimina las naciones primero."
        )
    
    result = GameService.initialize_game(db)
    return MessageResponse(
        message=result["message"],
        success=True,
        data=result
    )


@router.get("/state", response_model=GameStateResponse)
def get_game_state(db: Session = Depends(get_db)):
    """
    Obtener el estado actual completo del juego
    
    Incluye:
    - Turno actual
    - Todas las naciones
    - Eventos recientes
    - Estado de victoria
    """
    state = GameService.get_game_state(db)
    
    return GameStateResponse(
        current_turn=state["current_turn"],
        nations=[],  # Se puede expandir para incluir NationSummary
        player_nation_id=None,  # TODO: implementar
        is_game_over=state["is_game_over"]
    )


@router.post("/action", response_model=MessageResponse)
def process_action(
    action: ActionRequest,
    nation_id: int,
    db: Session = Depends(get_db)
):
    """
    Procesar una acción del jugador
    
    - **nation_id**: ID de la nación que realiza la acción
    - **action**: Datos de la acción a realizar
    """
    result = GameService.process_action(db, nation_id, action)
    
    if not result.get("success", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("message", "Error al procesar la acción")
        )
    
    return MessageResponse(
        message=result["message"],
        success=True,
        data=result
    )


@router.post("/next-turn", response_model=MessageResponse)
def advance_turn(db: Session = Depends(get_db)):
    """
    Avanzar al siguiente turno
    
    - Procesa las acciones de los agentes IA
    - Resuelve conflictos
    - Actualiza el estado del mundo
    - Crea el nuevo turno
    
    TODO: Implementar lógica de agentes IA (Fase 4)
    """
    from ..services.turn_service import TurnService
    
    current_turn = TurnService.get_current(db)
    if not current_turn:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No hay turno actual. Inicializa el juego primero."
        )
    
    # Por ahora, solo crear el siguiente turno
    # TODO: Aquí se llamará al sistema de agentes (LangGraph)
    
    nations = NationService.get_all(db)
    world_state = {
        "nations": [n.to_dict() for n in nations],
        "turn": current_turn.turn_number + 1
    }
    
    new_turn = TurnService.create_next_turn(
        db,
        world_state=world_state,
        summary="Turno avanzado (agentes IA pendientes de implementar)"
    )
    
    return MessageResponse(
        message=f"Turno {new_turn.turn_number} iniciado",
        success=True,
        data={"turn_number": new_turn.turn_number}
    )
