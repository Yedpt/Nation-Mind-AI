"""
Servicio RAG (Retrieval Augmented Generation)
Sistema de memoria para agentes IA usando ChromaDB
"""
import chromadb
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import os
from sqlalchemy.orm import Session

from ..models.event import Event
from ..config import settings


class RAGService:
    """
    Servicio para gestionar la memoria del sistema usando ChromaDB
    
    Los eventos del juego se almacenan como vectores (embeddings) para que
    los agentes IA puedan recuperar eventos relevantes del pasado y tomar
    decisiones informadas.
    """
    
    def __init__(self):
        """Inicializar ChromaDB y modelo de embeddings"""
        
        # Configurar ChromaDB según el modo (HTTP para Docker, Persistent para local)
        if settings.USE_CHROMADB_HTTP:
            # Modo Docker: conectar a ChromaDB como servicio HTTP
            print(f"🔗 Conectando a ChromaDB HTTP en {settings.CHROMADB_HOST}:{settings.CHROMADB_PORT}")
            self.chroma_client = chromadb.HttpClient(
                host=settings.CHROMADB_HOST,
                port=settings.CHROMADB_PORT
            )
        else:
            # Modo Local: usar ChromaDB persistente en carpeta local
            print(f"📁 Usando ChromaDB persistente en {settings.CHROMA_PERSIST_DIR}")
            self.chroma_client = chromadb.PersistentClient(
                path=settings.CHROMA_PERSIST_DIR
            )
        
        # Crear o recuperar colección de eventos
        self.collection = self.chroma_client.get_or_create_collection(
            name="game_events",
            metadata={"description": "Historical events from the geopolitical simulator"}
        )
        
        # Cargar modelo para crear embeddings
        # sentence-transformers/all-MiniLM-L6-v2 es pequeño y rápido (80MB)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        print("✅ RAG Service inicializado")
        if settings.USE_CHROMADB_HTTP:
            print(f"🌐 ChromaDB HTTP: {settings.CHROMADB_HOST}:{settings.CHROMADB_PORT}")
        else:
            print(f"📁 ChromaDB Local: {settings.CHROMA_PERSIST_DIR}")
        print(f"📊 Eventos en colección: {self.collection.count()}")
    
    
    def add_event(self, event: Event) -> bool:
        """
        Añadir un evento a la memoria vectorial
        
        Args:
            event: Objeto Event de SQLAlchemy
            
        Returns:
            bool: True si se añadió correctamente
        """
        try:
            # Crear texto descriptivo del evento para vectorizar
            event_text = self._create_event_description(event)
            
            # Crear embedding (vector matemático del texto)
            embedding = self.embedding_model.encode(event_text).tolist()
            
            # Metadata para filtrar búsquedas
            metadata = {
                "event_id": event.id,
                "nation_id": event.nation_id,
                "turn_id": event.turn_id,
                "event_type": event.event_type,
                "importance": event.importance,
                "created_at": str(event.created_at)
            }
            
            # Añadir a ChromaDB
            self.collection.add(
                embeddings=[embedding],
                documents=[event_text],
                metadatas=[metadata],
                ids=[f"event_{event.id}"]
            )
            
            return True
            
        except Exception as e:
            print(f"❌ Error añadiendo evento a RAG: {e}")
            return False
    
    
    def add_events_batch(self, events: List[Event]) -> int:
        """
        Añadir múltiples eventos en batch (más eficiente)
        
        Args:
            events: Lista de eventos
            
        Returns:
            int: Número de eventos añadidos
        """
        if not events:
            return 0
        
        try:
            # Preparar datos en batch
            texts = [self._create_event_description(e) for e in events]
            embeddings = self.embedding_model.encode(texts).tolist()
            
            metadatas = [{
                "event_id": e.id,
                "nation_id": e.nation_id,
                "turn_id": e.turn_id,
                "event_type": e.event_type,
                "importance": e.importance,
                "created_at": str(e.created_at)
            } for e in events]
            
            ids = [f"event_{e.id}" for e in events]
            
            # Añadir todos de golpe
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            return len(events)
            
        except Exception as e:
            print(f"❌ Error añadiendo eventos en batch: {e}")
            return 0
    
    
    def search_relevant_events(
        self,
        query: str,
        n_results: int = 5,
        nation_id: Optional[int] = None,
        event_type: Optional[str] = None,
        min_importance: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Buscar eventos relevantes usando similitud semántica
        
        Args:
            query: Pregunta o contexto en lenguaje natural
            n_results: Número máximo de resultados
            nation_id: Filtrar por nación específica
            event_type: Filtrar por tipo de evento
            min_importance: Importancia mínima (0-10)
            
        Returns:
            Lista de eventos relevantes con metadata
        """
        try:
            # Crear embedding de la query
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Construir filtros
            where_filter = {}
            if nation_id:
                where_filter["nation_id"] = nation_id
            if event_type:
                where_filter["event_type"] = event_type
            if min_importance > 0:
                where_filter["importance"] = {"$gte": min_importance}
            
            # Buscar en ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where_filter if where_filter else None
            )
            
            # Formatear resultados
            events = []
            if results['documents']:
                for i, doc in enumerate(results['documents'][0]):
                    events.append({
                        "description": doc,
                        "metadata": results['metadatas'][0][i],
                        "distance": results['distances'][0][i],  # Menor = más relevante
                        "id": results['ids'][0][i]
                    })
            
            return events
            
        except Exception as e:
            print(f"❌ Error buscando eventos: {e}")
            return []
    
    
    def get_nation_history(self, nation_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Obtener historial de una nación específica
        
        Args:
            nation_id: ID de la nación
            limit: Máximo de eventos a devolver
            
        Returns:
            Lista de eventos de esa nación
        """
        try:
            results = self.collection.get(
                where={"nation_id": nation_id},
                limit=limit
            )
            
            events = []
            for i, doc in enumerate(results['documents']):
                events.append({
                    "description": doc,
                    "metadata": results['metadatas'][i],
                    "id": results['ids'][i]
                })
            
            return events
            
        except Exception as e:
            print(f"❌ Error obteniendo historial: {e}")
            return []
    
    
    def get_context_for_agent(
        self,
        nation_id: int,
        current_situation: str,
        max_events: int = 5
    ) -> str:
        """
        Obtener contexto relevante para un agente IA
        
        Este método es usado por los agentes para recuperar memoria
        antes de tomar decisiones.
        
        Args:
            nation_id: ID de la nación que pide contexto
            current_situation: Descripción de la situación actual
            max_events: Máximo de eventos a incluir
            
        Returns:
            str: Contexto en formato texto para el LLM
        """
        # Buscar eventos relevantes a la situación actual
        relevant_events = self.search_relevant_events(
            query=current_situation,
            n_results=max_events,
            min_importance=5  # Solo eventos importantes
        )
        
        # También incluir eventos propios recientes
        own_events = self.get_nation_history(nation_id, limit=3)
        
        # Formatear como contexto para el LLM
        context_parts = ["### Memoria de eventos relevantes:\n"]
        
        if relevant_events:
            context_parts.append("**Eventos del mundo:**")
            for event in relevant_events:
                context_parts.append(f"- {event['description']}")
        
        if own_events:
            context_parts.append("\n**Tus acciones recientes:**")
            for event in own_events:
                context_parts.append(f"- {event['description']}")
        
        return "\n".join(context_parts)
    
    
    def clear_collection(self) -> bool:
        """
        Limpiar toda la colección (útil para testing)
        
        Returns:
            bool: True si se limpió correctamente
        """
        try:
            self.chroma_client.delete_collection("game_events")
            self.collection = self.chroma_client.create_collection(
                name="game_events",
                metadata={"description": "Historical events from the geopolitical simulator"}
            )
            print("🗑️ Colección ChromaDB limpiada")
            return True
        except Exception as e:
            print(f"❌ Error limpiando colección: {e}")
            return False
    
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Obtener estadísticas de la colección RAG
        
        Returns:
            dict: Estadísticas de uso
        """
        return {
            "total_events": self.collection.count(),
            "persist_directory": settings.CHROMA_PERSIST_DIR,
            "collection_name": self.collection.name,
            "embedding_model": "all-MiniLM-L6-v2"
        }
    
    
    def _create_event_description(self, event: Event) -> str:
        """
        Crear descripción textual enriquecida de un evento
        
        Esto mejora la calidad de los embeddings y las búsquedas
        """
        parts = [
            f"Turno {event.turn_id}:",
            event.description
        ]
        
        # Añadir contexto adicional si está disponible
        if event.data:
            if "target" in event.data:
                parts.append(f"Objetivo: {event.data['target']}")
            if "result" in event.data:
                parts.append(f"Resultado: {event.data['result']}")
        
        # Añadir nivel de importancia
        if event.importance >= 8:
            parts.append("(Evento crítico)")
        elif event.importance >= 6:
            parts.append("(Evento importante)")
        
        return " ".join(parts)


# Instancia global del servicio RAG
# Se inicializa una vez y se reutiliza
_rag_service_instance = None

def get_rag_service() -> RAGService:
    """
    Obtener instancia singleton del RAG Service
    
    Returns:
        RAGService: Instancia compartida del servicio
    """
    global _rag_service_instance
    if _rag_service_instance is None:
        _rag_service_instance = RAGService()
    return _rag_service_instance
