"""
Configuración de la aplicación
Carga variables de entorno desde .env
"""
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """
    Configuración de la aplicación usando Pydantic
    """
    # Base de datos
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://nationmind:dev123@localhost:5432/nationmind_db"
    )
    
    # API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    
    # Configuración de la aplicación
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))

    # Seguridad
    API_KEY: str = os.getenv("API_KEY", "")

    # Rate limiting (0 = desactivado)
    RATE_LIMIT_MAX_REQUESTS: int = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "0"))
    RATE_LIMIT_WINDOW_SECONDS: int = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
    
    # CORS
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    ALLOWED_ORIGINS: str = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://127.0.0.1:3000"
    )
    
    # ChromaDB (RAG)
    CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
    CHROMADB_HOST: str = os.getenv("CHROMADB_HOST", "localhost")
    CHROMADB_PORT: int = int(os.getenv("CHROMADB_PORT", "8001"))
    # Si USE_CHROMADB_HTTP es True, usa HttpClient (Docker); si no, usa PersistentClient (local)
    USE_CHROMADB_HTTP: bool = os.getenv("USE_CHROMADB_HTTP", "False").lower() == "true"

    # Vector store
    VECTOR_BACKEND: str = os.getenv("VECTOR_BACKEND", "chroma")
    VECTOR_TABLE_NAME: str = os.getenv("VECTOR_TABLE_NAME", "event_embeddings")
    VECTOR_EMBEDDING_DIM: int = int(os.getenv("VECTOR_EMBEDDING_DIM", "384"))
    
    # LLM Configuration
    LLM_MODEL: str = os.getenv("LLM_MODEL", "llama-3.1-70b-versatile")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "1024"))
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  #  Ignorar variables extra del .env


# Instancia global de configuración
settings = Settings()
