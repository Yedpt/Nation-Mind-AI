"""
Vector store sobre PostgreSQL/Supabase usando pgvector.
"""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from pgvector.psycopg2 import register_vector
from pgvector.sqlalchemy import Vector as VectorType
from sqlalchemy import JSON, Column, DateTime, Integer, MetaData, String, Table, Text, and_, event as sqlalchemy_event, func, select, text
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sentence_transformers import SentenceTransformer

from ..config import settings
from ..models.database import engine
from ..models.event import Event

logger = logging.getLogger(__name__)
_vector_listener_registered = False


class SupabaseVectorStore:
    """Persistencia y búsqueda semántica sobre PostgreSQL con pgvector."""

    def __init__(self, embedding_model: SentenceTransformer):
        self.embedding_model = embedding_model
        self.metadata = MetaData()
        self.table_name = settings.VECTOR_TABLE_NAME
        self.embedding_dimension = settings.VECTOR_EMBEDDING_DIM
        self.table = Table(
            self.table_name,
            self.metadata,
            Column("event_id", Integer, primary_key=True),
            Column("nation_id", Integer, index=True, nullable=False),
            Column("turn_id", Integer, index=True, nullable=False),
            Column("event_type", String(50), index=True, nullable=False),
            Column("importance", Integer, index=True, nullable=False, default=5),
            Column("description", Text, nullable=False),
            Column("event_metadata", JSON, nullable=False, default=dict),
            Column("embedding", VectorType(self.embedding_dimension), nullable=False),
            Column("created_at", DateTime, index=True, nullable=False, default=datetime.utcnow),
        )

        self._register_vector_support()
        self._ensure_schema()
        logger.info("Supabase Vector Store inicializado en %s", self.table_name)

    def _register_vector_support(self) -> None:
        global _vector_listener_registered
        if _vector_listener_registered:
            return

        @sqlalchemy_event.listens_for(engine, "connect")
        def _register_vector(dbapi_connection, connection_record):  # type: ignore[unused-ignore]
            register_vector(dbapi_connection)

        _vector_listener_registered = True

    def _ensure_schema(self) -> None:
        with engine.begin() as connection:
            connection.execute(text("create extension if not exists vector"))
        self.metadata.create_all(bind=engine, tables=[self.table])

    def _build_record(self, event: Event, embedding: List[float], description: str) -> Dict[str, Any]:
        return {
            "event_id": event.id,
            "nation_id": event.nation_id,
            "turn_id": event.turn_id,
            "event_type": event.event_type,
            "importance": event.importance,
            "description": description,
            "event_metadata": {
                "event_id": event.id,
                "nation_id": event.nation_id,
                "turn_id": event.turn_id,
                "event_type": event.event_type,
                "importance": event.importance,
                "created_at": str(event.created_at),
            },
            "embedding": embedding,
            "created_at": event.created_at or datetime.utcnow(),
        }

    def add_event(self, event: Event) -> bool:
        try:
            description = self._create_event_description(event)
            embedding = self.embedding_model.encode(description).tolist()
            record = self._build_record(event, embedding, description)

            stmt = pg_insert(self.table).values([record])
            stmt = stmt.on_conflict_do_update(
                index_elements=[self.table.c.event_id],
                set_={
                    "nation_id": stmt.excluded.nation_id,
                    "turn_id": stmt.excluded.turn_id,
                    "event_type": stmt.excluded.event_type,
                    "importance": stmt.excluded.importance,
                    "description": stmt.excluded.description,
                    "event_metadata": stmt.excluded.event_metadata,
                    "embedding": stmt.excluded.embedding,
                    "created_at": stmt.excluded.created_at,
                },
            )

            with engine.begin() as connection:
                connection.execute(stmt)

            return True
        except Exception as exc:
            logger.exception("Error añadiendo evento a Supabase Vector: %s", exc)
            return False

    def add_events_batch(self, events: List[Event]) -> int:
        if not events:
            return 0

        try:
            descriptions = [self._create_event_description(event) for event in events]
            embeddings = self.embedding_model.encode(descriptions).tolist()
            records = [
                self._build_record(event, embedding, description)
                for event, embedding, description in zip(events, embeddings, descriptions)
            ]

            stmt = pg_insert(self.table).values(records)
            stmt = stmt.on_conflict_do_update(
                index_elements=[self.table.c.event_id],
                set_={
                    "nation_id": stmt.excluded.nation_id,
                    "turn_id": stmt.excluded.turn_id,
                    "event_type": stmt.excluded.event_type,
                    "importance": stmt.excluded.importance,
                    "description": stmt.excluded.description,
                    "event_metadata": stmt.excluded.event_metadata,
                    "embedding": stmt.excluded.embedding,
                    "created_at": stmt.excluded.created_at,
                },
            )

            with engine.begin() as connection:
                connection.execute(stmt)

            return len(records)
        except Exception as exc:
            logger.exception("Error añadiendo eventos en batch a Supabase Vector: %s", exc)
            return 0

    def search_relevant_events(
        self,
        query: str,
        n_results: int = 5,
        nation_id: Optional[int] = None,
        event_type: Optional[str] = None,
        min_importance: int = 0,
    ) -> List[Dict[str, Any]]:
        try:
            query_embedding = self.embedding_model.encode(query).tolist()
            distance_expr = self.table.c.embedding.cosine_distance(query_embedding).label("distance")

            conditions = []
            if nation_id is not None:
                conditions.append(self.table.c.nation_id == nation_id)
            if event_type:
                conditions.append(self.table.c.event_type == event_type)
            if min_importance > 0:
                conditions.append(self.table.c.importance >= min_importance)

            stmt = select(
                self.table.c.event_id,
                self.table.c.description,
                self.table.c.event_metadata,
                self.table.c.nation_id,
                self.table.c.turn_id,
                self.table.c.event_type,
                self.table.c.importance,
                self.table.c.created_at,
                distance_expr,
            )
            if conditions:
                stmt = stmt.where(and_(*conditions))
            stmt = stmt.order_by(distance_expr).limit(n_results)

            with engine.connect() as connection:
                rows = connection.execute(stmt).mappings().all()

            return [
                {
                    "id": f"event_{row['event_id']}",
                    "description": row["description"],
                    "metadata": row["event_metadata"],
                    "distance": float(row["distance"]),
                }
                for row in rows
            ]
        except Exception as exc:
            logger.exception("Error buscando eventos en Supabase Vector: %s", exc)
            return []

    def get_nation_history(self, nation_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        try:
            stmt = (
                select(
                    self.table.c.event_id,
                    self.table.c.description,
                    self.table.c.event_metadata,
                    self.table.c.created_at,
                )
                .where(self.table.c.nation_id == nation_id)
                .order_by(self.table.c.created_at.desc())
                .limit(limit)
            )

            with engine.connect() as connection:
                rows = connection.execute(stmt).mappings().all()

            return [
                {
                    "id": f"event_{row['event_id']}",
                    "description": row["description"],
                    "metadata": row["event_metadata"],
                }
                for row in rows
            ]
        except Exception as exc:
            logger.exception("Error obteniendo historial desde Supabase Vector: %s", exc)
            return []

    def clear_collection(self) -> bool:
        try:
            with engine.begin() as connection:
                connection.execute(self.table.delete())
            logger.info("Supabase Vector limpiado: %s", self.table_name)
            return True
        except Exception as exc:
            logger.exception("Error limpiando Supabase Vector: %s", exc)
            return False

    def get_stats(self) -> Dict[str, Any]:
        try:
            stmt = select(func.count()).select_from(self.table)
            with engine.connect() as connection:
                total_events = connection.execute(stmt).scalar_one()
        except Exception:
            total_events = 0

        return {
            "backend": "supabase",
            "collection_name": self.table_name,
            "total_events": total_events,
            "embedding_model": "all-MiniLM-L6-v2",
            "embedding_dimension": self.embedding_dimension,
        }

    def _create_event_description(self, event: Event) -> str:
        parts = [f"Turno {event.turn_id}:", event.description]

        if event.data:
            if "target" in event.data:
                parts.append(f"Objetivo: {event.data['target']}")
            if "result" in event.data:
                parts.append(f"Resultado: {event.data['result']}")

        if event.importance >= 8:
            parts.append("(Evento crítico)")
        elif event.importance >= 6:
            parts.append("(Evento importante)")

        return " ".join(parts)
