"""
Controller para Agentes IA
Rutas: /api/agents/*
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from ..models.database import get_db
from ..config.security import require_api_key
from ..services.agent_service import get_agent_service
from ..services.turn_service import TurnService

router = APIRouter(prefix="/api/agents", tags=["AI Agents"])


@router.post("/process-turn")
def process_ai_turn(
    db: Session = Depends(get_db),
    _: None = Depends(require_api_key)
) -> Dict[str, Any]:
    """
    Procesar el turno de todas las naciones IA.
    
    Este endpoint:
    1. Obtiene el turno actual
    2. Cada agente IA analiza la situación
    3. Consulta su memoria histórica (RAG)
    4. Decide qué acción tomar
    5. Ejecuta la acción
    6. Crea el siguiente turno
    
    Returns:
        dict: Resultados de las decisiones de cada agente
    """
    try:
        # Obtener turno actual
        current_turn = TurnService.get_current(db)
        if not current_turn:
            raise HTTPException(
                status_code=400,
                detail="No hay turno activo. Inicializa el juego primero."
            )
        
        print(f"\n⚡ Procesando turno {current_turn.turn_number}...")
        
        # Obtener servicio de agentes
        agent_service = get_agent_service()
        
        # Procesar turno de todos los agentes
        results = agent_service.process_ai_turn(db, current_turn.turn_number)
        
        # Obtener el nuevo turno creado
        new_turn = TurnService.get_current(db)
        
        # Contar éxitos
        successes = sum(1 for r in results if r.get("success", False))
        
        print(f"✅ Turno procesado. Nuevo turno: {new_turn.turn_number if new_turn else 'ERROR'}")
        
        return {
            "message": "Turno procesado exitosamente",
            "previous_turn": current_turn.turn_number,
            "current_turn": new_turn.turn_number if new_turn else current_turn.turn_number,
            "total_agents": len(results),
            "successful_actions": successes,
            "failed_actions": len(results) - successes,
            "agents_results": results
        }
        
    except Exception as e:
        import traceback
        print(f"❌ ERROR en process_ai_turn: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Error procesando turno de IA: {str(e)}"
        )


@router.get("/status")
def get_ai_status() -> Dict[str, Any]:
    """
    Obtener estado del sistema de agentes IA.
    
    Returns:
        dict: Información del servicio de agentes
    """
    try:
        agent_service = get_agent_service()
        return {
            "status": "active",
            "model": "llama-3.3-70b-versatile",
            "provider": "Groq",
            "features": [
                "Multi-agent coordination",
                "RAG memory integration",
                "Personality-based decisions",
                "StateGraph workflow"
            ]
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
