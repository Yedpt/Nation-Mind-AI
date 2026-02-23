"""
Script para resetear el juego eliminando todas las tablas y recreándolas limpias.
Útil para empezar desde cero.
"""
import sys
import os

# Agregar el directorio padre al path para importar los módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models.database import Base, engine
from sqlalchemy import inspect

def reset_database():
    """Eliminar todas las tablas y recrearlas vacías"""
    
    print("🗑️  Eliminando todas las tablas...")
    
    # Obtener inspector para ver qué tablas existen
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    if existing_tables:
        print(f"📋 Tablas encontradas: {', '.join(existing_tables)}")
        
        # Eliminar todas las tablas
        Base.metadata.drop_all(bind=engine)
        print("✅ Todas las tablas eliminadas")
    else:
        print("ℹ️  No hay tablas para eliminar")
    
    # Recrear todas las tablas vacías
    print("🔨 Recreando tablas vacías...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas recreadas exitosamente")
    
    print("\n🎮 ¡Base de datos reseteada! Ahora puedes iniciar un nuevo juego.")

if __name__ == "__main__":
    print("⚠️  ADVERTENCIA: Esto eliminará TODOS los datos del juego actual")
    confirm = input("¿Estás seguro? (escribe 'SI' para confirmar): ")
    
    if confirm.upper() == "SI":
        reset_database()
    else:
        print("❌ Operación cancelada")
