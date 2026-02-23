"""
Controller para endpoints del Juego
Rutas: /api/game/*
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any

from ..models.database import get_db
from ..services.game_service import GameService
from ..services.nation_service import NationService
from ..schemas.game_schema import ActionRequest, GameStateResponse, MessageResponse

router = APIRouter(prefix="/api/game", tags=["Game"])


@router.get("/nations")
def get_available_nations():
    """
    Obtener lista de naciones disponibles para seleccionar
    
    Devuelve información de todas las naciones que el jugador puede elegir
    """
    nations = GameService.get_available_nations()
    return {
        "nations": nations,
        "total": len(nations)
    }


@router.post("/initialize", response_model=MessageResponse)
def initialize_game(
    player_nation: str = Query("ESP", description="Código de la nación del jugador (USA, CHN, RUS, DEU, GBR, FRA, JPN, ESP)"),
    force_reset: bool = Query(False, description="Si es True, elimina el juego existente antes de inicializar uno nuevo"),
    db: Session = Depends(get_db)
):
    """
    Inicializar un nuevo juego
    
    - **player_nation**: Código de la nación que controlará el jugador (default: ESP - España)
    - **force_reset**: Si es True, elimina cualquier juego existente automáticamente
    
    Crea las 8 naciones, el primer turno y las relaciones base.
    La nación seleccionada será controlada por el jugador, las demás por IA.
    """
    print(f"\n🎮 INICIALIZANDO JUEGO CON NACIÓN: {player_nation}")
    
    # Verificar que no haya ya un juego iniciado
    existing_nations = NationService.get_all(db, limit=1)
    if existing_nations:
        if force_reset:
            print(f"⚠️  Juego existente detectado. Eliminando...")
            # Eliminar todas las naciones (por CASCADE se eliminarán eventos, relaciones, etc.)
            from sqlalchemy import text
            db.execute(text("DELETE FROM battles"))
            db.execute(text("DELETE FROM events"))
            db.execute(text("DELETE FROM relations"))
            db.execute(text("DELETE FROM nations"))
            db.execute(text("DELETE FROM turns"))
            db.commit()
            print("✅ Juego anterior eliminado")
        else:
            print(f"❌ ERROR: Ya existe un juego con {len(NationService.get_all(db))} naciones")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un juego iniciado. Usa force_reset=true para eliminarlo automáticamente o ejecuta reset_game.py"
            )
    
    print("✅ No hay juego previo, iniciando...")
    
    try:
        result = GameService.initialize_game(db, player_nation_code=player_nation)
        print(f"✅ Juego inicializado exitosamente. Turno: {result.get('turn_number', 'N/A')}")
        return MessageResponse(
            message=result["message"],
            success=True,
            data=result
        )
    except ValueError as e:
        print(f"❌ ERROR ValueError: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"❌ ERROR inesperado: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al inicializar juego: {str(e)}"
        )


@router.get("/available-nations")
def get_available_nations():
    """
    Obtener lista de naciones disponibles para seleccionar.
    
    Use esta lista para mostrar al jugador las opciones antes de inicializar el juego.
    Por defecto se recomienda España (ESP).
    """
    from ..services.game_service import AVAILABLE_NATIONS
    
    print("📋 Obteniendo lista de naciones disponibles...")
    
    nations_list = []
    for code, data in AVAILABLE_NATIONS.items():
        nations_list.append({
            "code": code,
            "name": data["name"],
            "personality": data["personality"],
            "military_power": data["military_power"],
            "economic_power": data["economic_power"],
            "diplomatic_influence": data["diplomatic_influence"],
            "recommended": code == "ESP"  # España por defecto
        })
    
    print(f"✅ Devolviendo {len(nations_list)} naciones disponibles")
    
    return {
        "available_nations": nations_list,
        "default": "ESP",
        "default_name": "España"
    }


@router.get("/status")
def get_game_status(db: Session = Depends(get_db)):
    """
    Verificar si hay un juego activo.
    
    Retorna información básica sobre el estado del juego sin detalles completos.
    """
    from ..services.nation_service import NationService
    from ..services.turn_service import TurnService
    
    nations = NationService.get_all(db, limit=1)
    has_game = len(nations) > 0
    
    if has_game:
        current_turn = TurnService.get_current_turn(db)
        player_nations = [n for n in NationService.get_all(db) if n.is_player]
        
        return {
            "has_active_game": True,
            "current_turn": current_turn.turn_number if current_turn else 0,
            "player_nation": player_nations[0].name if player_nations else None,
            "total_nations": len(NationService.get_all(db))
        }
    
    return {
        "has_active_game": False,
        "current_turn": 0,
        "player_nation": None,
        "total_nations": 0
    }



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
    from ..schemas.nation_schema import NationSummary
    
    state = GameService.get_game_state(db)
    
    print(f"📊 Estado del juego - Turno: {state['current_turn']}, Naciones: {len(state['nations'])}")
    
    # Convertir dict nations a NationSummary
    nations_summary = []
    player_nation_id = None
    
    for n in state['nations']:
        nations_summary.append(NationSummary(
            id=n['id'],
            name=n['name'],
            personality=n['personality'],
            gold=n['gold'],
            troops=n['troops'],
            territories=n['territories'],
            military_power=n['military_power'],
            economic_power=n['economic_power'],
            diplomatic_influence=n['diplomatic_influence'],
            ai_controlled=n['ai_controlled'],
            is_active=n['is_active']
        ))
        
        if not n['ai_controlled']:
            player_nation_id = n['id']
    
    print(f"✅ Devolviendo {len(nations_summary)} naciones. Jugador: ID {player_nation_id}")
    
    # Convertir eventos a EventSummary
    from ..schemas.event_schema import EventSummary
    from datetime import datetime
    
    events_summary = []
    for e in state['recent_events']:
        # Parsear created_at si es string
        created_at = e['created_at']
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        
        events_summary.append(EventSummary(
            id=e['id'],
            event_type=e['event_type'],
            description=e['description'],
            created_at=created_at
        ))
    
    # Verificar condiciones de victoria
    from ..services.victory_service import VictoryService
    from ..services.turn_service import TurnService
    
    current_turn_obj = TurnService.get_current(db)
    turn_number = current_turn_obj.turn_number if current_turn_obj else state["current_turn"]
    
    victory_check = VictoryService.check_victory_conditions(db, turn_number)
    
    # Obtener progreso de victoria del jugador
    player_nation_obj = None
    victory_progress = None
    if player_nation_id:
        player_nation_obj = NationService.get_by_id(db, player_nation_id)
        if player_nation_obj:
            victory_progress = VictoryService.get_victory_progress(db, player_nation_obj, turn_number)
    
    return GameStateResponse(
        current_turn=state["current_turn"],
        nations=nations_summary,
        recent_events=events_summary,
        player_nation_id=player_nation_id,
        is_game_over=victory_check["game_over"],
        winner=victory_check["winner"].name if victory_check.get("winner") else None,
        victory_type=victory_check.get("victory_type"),
        victory_progress=victory_progress
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


@router.get("/leaderboard", response_model=List[Dict[str, Any]])
def get_leaderboard(db: Session = Depends(get_db)):
    """
    Obtener tabla de clasificación de todas las naciones.
    
    Returns:
        Lista ordenada por puntuación total (oro, tropas, territorios, poderes)
    """
    from ..services.victory_service import VictoryService
    
    leaderboard = VictoryService.get_leaderboard(db)
    return leaderboard


@router.get("/victory-progress", response_model=Dict[str, Any])
def get_victory_progress(nation_id: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Obtener progreso hacia todas las condiciones de victoria.
    
    Args:
        nation_id: ID de la nación (opcional, por defecto la nación del jugador)
    
    Returns:
        Progreso de cada tipo de victoria (domination, economic, military, etc.)
    """
    from ..services.victory_service import VictoryService
    from ..services.turn_service import TurnService
    
    # Obtener nación
    if nation_id is None:
        nation = NationService.get_player_nation(db)
    else:
        nation = NationService.get_by_id(db, nation_id)
    
    if not nation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nación no encontrada"
        )
    
    # Obtener turno actual
    current_turn = TurnService.get_current(db)
    turn_number = current_turn.turn_number if current_turn else 1
    
    # Calcular progreso
    progress = VictoryService.get_victory_progress(db, nation, turn_number)
    
    return {
        "nation_id": nation.id,
        "nation_name": nation.name,
        "current_turn": turn_number,
        "progress": progress
    }


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
