"""
Configuración de base de datos PostgreSQL con SQLAlchemy
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# URL de conexión a PostgreSQL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://nationmind:dev123@localhost:5432/nationmind_db"
)

# Crear engine de SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verificar conexión antes de usar
    echo=False  # True para ver SQL queries en consola (útil para debugging)
)

# Crear SessionLocal para interactuar con la DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Dependency para FastAPI
def get_db():
    """
    Generator que crea una sesión de base de datos
    y la cierra automáticamente después de usarla
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Crear todas las tablas definidas en los modelos
    """
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas exitosamente")


def drop_tables():
    """
    Eliminar todas las tablas (útil para desarrollo)
    """
    Base.metadata.drop_all(bind=engine)
    print("⚠️ Todas las tablas eliminadas")
