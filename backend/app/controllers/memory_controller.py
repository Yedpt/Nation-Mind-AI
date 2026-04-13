"""
Controller para endpoints RAG (Sistema de Memoria)
Rutas: /api/memory/*
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from pydantic import BaseModel

from ..services.rag_service import get_rag_service
from ..config.security import require_api_key

router = APIRouter(prefix="/api/memory", tags=["Memory (RAG)"])


# ==================== SCHEMAS ====================

class SearchMemoryRequest(BaseModel):
    """Request para buscar en la memoria"""
    query: str
    n_results: int = 5
    nation_id: Optional[int] = None
    event_type: Optional[str] = None
    min_importance: int = 0


class AgentContextRequest(BaseModel):
    """Request para obtener contexto de un agente"""
    nation_id: int
    current_situation: str
    max_events: int = 5


# ==================== ENDPOINTS ====================

@router.get("/stats")
def get_memory_stats():
    """
    Obtener estadísticas del sistema de memoria RAG
    
    Returns:
        - total_events: Número de eventos almacenados
        - persist_directory: Ubicación de ChromaDB
        - collection_name: Nombre de la colección
        - embedding_model: Modelo usado para vectorizar
    """
    rag = get_rag_service()
    return rag.get_stats()


@router.post("/search")
def search_memory(request: SearchMemoryRequest):
    """
    Buscar eventos relevantes en la memoria usando búsqueda semántica
    
    Permite buscar eventos similares a una query en lenguaje natural.
    
    Ejemplo:
    ```json
    {
        "query": "¿Qué guerras ha tenido Francia?",
        "n_results": 5,
        "nation_id": 2,
        "min_importance": 7
    }
    ```
    """
    rag = get_rag_service()
    
    results = rag.search_relevant_events(
        query=request.query,
        n_results=request.n_results,
        nation_id=request.nation_id,
        event_type=request.event_type,
        min_importance=request.min_importance
    )
    
    return {
        "query": request.query,
        "results_count": len(results),
        "events": results
    }


@router.get("/nation/{nation_id}/history")
def get_nation_memory(nation_id: int, limit: int = 10):
    """
    Obtener historial de memoria de una nación específica
    
    - **nation_id**: ID de la nación
    - **limit**: Máximo de eventos a devolver
    """
    rag = get_rag_service()
    
    history = rag.get_nation_history(nation_id, limit)
    
    return {
        "nation_id": nation_id,
        "events_count": len(history),
        "history": history
    }


@router.post("/agent/context")
def get_agent_context(request: AgentContextRequest):
    """
    Obtener contexto formateado para un agente IA
    
    Este endpoint es usado internamente por el sistema de agentes
    para recuperar memoria relevante antes de tomar decisiones.
    
    Ejemplo:
    ```json
    {
        "nation_id": 2,
        "current_situation": "Francia necesita decidir si atacar a Alemania",
        "max_events": 5
    }
    ```
    
    Returns:
        - context: Texto formateado listo para enviar al LLM
        - events_used: Número de eventos incluidos en el contexto
    """
    rag = get_rag_service()
    
    context = rag.get_context_for_agent(
        nation_id=request.nation_id,
        current_situation=request.current_situation,
        max_events=request.max_events
    )
    
    # Contar eventos en el contexto (aproximado)
    events_used = context.count("- ")
    
    return {
        "nation_id": request.nation_id,
        "context": context,
        "events_used": events_used
    }


@router.delete("/clear")
def clear_memory(_: None = Depends(require_api_key)):
    """
    ⚠️ PELIGRO: Limpiar toda la memoria RAG
    
    Elimina todos los eventos almacenados en ChromaDB.
    Solo usar para testing o resetear el juego.
    """
    rag = get_rag_service()
    
    success = rag.clear_collection()
    
    if success:
        return {
            "message": "Memoria RAG limpiada exitosamente",
            "warning": "Todos los eventos históricos han sido eliminados"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al limpiar la memoria RAG"
        )


@router.post("/reindex")
def reindex_events_from_db(_: None = Depends(require_api_key)):
    """
    Reindexar todos los eventos desde PostgreSQL a ChromaDB
    
    Útil si ChromaDB se perdió o se quiere reconstruir la memoria.
    """
    from sqlalchemy.orm import Session
    from ..models.database import SessionLocal
    from ..services.event_service import EventService
    
    rag = get_rag_service()
    db = SessionLocal()
    
    try:
        # Obtener todos los eventos de la DB
        events = EventService.get_all(db, limit=1000)
        
        if not events:
            return {
                "message": "No hay eventos para reindexar",
                "events_added": 0
            }
        
        # Añadir en batch
        count = rag.add_events_batch(events)
        
        return {
            "message": "Eventos reindexados exitosamente",
            "events_added": count
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al reindexar: {str(e)}"
        )
    finally:
        db.close()
