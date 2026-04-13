"""
Nation-Mind AI Backend
FastAPI application con arquitectura MVC
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import time
import logging
from collections import deque
from typing import Deque, Dict, Tuple

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Importar controllers (routers)
from .controllers import (
    nations_router,
    game_router,
    events_router,
    turns_router,
    relations_router,
    memory_router,
    agent_router,
    battle_router
)

# Importar modelos para crear tablas
from .models import create_tables, Base, engine
from .config.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Eventos del ciclo de vida de la aplicación
    Se ejecuta al iniciar y al cerrar el servidor
    """
    if settings.ENVIRONMENT.lower() == "production" and not settings.API_KEY:
        raise RuntimeError("API_KEY is required in production")

    # Startup: Crear tablas si no existen
    print("🚀 Iniciando Nation-Mind AI Backend...")
    print("📊 Creando tablas de base de datos...")
    create_tables()
    print("✅ Tablas creadas/verificadas")
    
    yield  # Aplicación corriendo
    
    # Shutdown
    print("🛑 Cerrando Nation-Mind AI Backend...")


# Crear aplicación FastAPI
app = FastAPI(
    title="Nation-Mind AI API",
    description="Simulador geopolítico con agentes de IA y sistema RAG",
    version="0.1.0",
    lifespan=lifespan
)

# Rate limiting simple en memoria (solo para endpoints sensibles)
RATE_LIMIT_PATHS = {
    "/api/agents/process-turn",
    "/api/memory/clear",
    "/api/memory/reindex",
    "/api/game/initialize",
}
RATE_LIMIT_STORE: Dict[str, Deque[float]] = {}


def _check_rate_limit(client_key: str) -> Tuple[bool, int]:
    """Retorna (is_limited, retry_after_seconds)."""
    from .config.settings import settings

    max_requests = settings.RATE_LIMIT_MAX_REQUESTS
    window_seconds = settings.RATE_LIMIT_WINDOW_SECONDS

    if max_requests <= 0:
        return False, 0

    now = time.time()
    q = RATE_LIMIT_STORE.setdefault(client_key, deque())

    while q and now - q[0] > window_seconds:
        q.popleft()

    if len(q) >= max_requests:
        retry_after = int(window_seconds - (now - q[0])) if q else window_seconds
        return True, max(retry_after, 1)

    q.append(now)
    return False, 0

# CORS para permitir peticiones desde el frontend
allowed_origins = [o.strip() for o in settings.ALLOWED_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware para logging de peticiones
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log de la petición entrante
    logger.info(f"🌐 {request.method} {request.url.path}")

    # Rate limiting en endpoints sensibles
    if request.url.path in RATE_LIMIT_PATHS:
        forwarded_for = request.headers.get("x-forwarded-for", "")
        client_ip = forwarded_for.split(",")[0].strip() if forwarded_for else (request.client.host or "unknown")
        key = f"{client_ip}:{request.url.path}"
        limited, retry_after = _check_rate_limit(key)
        if limited:
            from fastapi.responses import JSONResponse

            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded",
                    "retry_after_seconds": retry_after,
                },
                headers={"Retry-After": str(retry_after)},
            )
    
    response = await call_next(request)

    # Cabeceras de seguridad para API
    if request.url.path.startswith("/api"):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        # CSP estricta para respuestas JSON/API
        response.headers["Content-Security-Policy"] = (
            "default-src 'none'; frame-ancestors 'none'; base-uri 'none'"
        )
    
    # Log de la respuesta
    process_time = time.time() - start_time
    logger.info(f"✅ {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.3f}s")
    
    return response


# ==================== RUTAS BÁSICAS ====================

@app.get("/")
def read_root():
    """Endpoint raíz - Información de la API"""
    return {
        "message": "Nation-Mind AI Backend",
        "status": "running",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/api/health")
def health_check():
    """Health check - Verificar que la API está funcionando"""
    return {
        "status": "ok",
        "message": "Backend funcionando correctamente"
    }


# ==================== REGISTRAR ROUTERS ====================

# Nations (Naciones)
app.include_router(nations_router)

# Game (Juego principal)
app.include_router(game_router)

# Events (Eventos históricos)
app.include_router(events_router)

# Turns (Turnos)
app.include_router(turns_router)

# Relations (Relaciones diplomáticas)
app.include_router(relations_router)

# Battles (Sistema de combate)
app.include_router(battle_router)

# Memory (Sistema RAG - Memoria de eventos)
app.include_router(memory_router)

# Agents (Agentes IA con LangGraph)
app.include_router(agent_router)


# ==================== DESARROLLO ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload en desarrollo
    )
