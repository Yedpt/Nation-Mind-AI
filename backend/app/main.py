"""
Nation-Mind AI Backend
FastAPI application con arquitectura MVC
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Importar controllers (routers)
from .controllers import (
    nations_router,
    game_router,
    events_router,
    turns_router,
    relations_router
)

# Importar modelos para crear tablas
from .models import create_tables, Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Eventos del ciclo de vida de la aplicación
    Se ejecuta al iniciar y al cerrar el servidor
    """
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

# CORS para permitir peticiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev
        "http://localhost:3001",  # Alternativo
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


# ==================== DESARROLLO ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload en desarrollo
    )
