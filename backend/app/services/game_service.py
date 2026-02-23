"""
Servicio principal del juego
Coordina la lógica de alto nivel del simulador
"""
from sqlalchemy.orm import Session
from typing import Dict, List, Any, Optional
from .nation_service import NationService
from .turn_service import TurnService
from .event_service import EventService
from .relation_service import RelationService
from ..models.relation import Relation
from ..schemas.nation_schema import NationCreate
from ..schemas.event_schema import EventCreate
from ..schemas.relation_schema import RelationCreate
from ..schemas.game_schema import ActionRequest


# Configuración de naciones disponibles
AVAILABLE_NATIONS = {
    "USA": {
        "name": "Estados Unidos",
        "code": "USA",
        "personality": "diplomatic",
        "gold": 2000,
        "troops": 200,
        "territories": 7,
        "military_power": 95.0,
        "economic_power": 100.0,
        "diplomatic_influence": 90.0
    },
    "CHN": {
        "name": "China",
        "code": "CHN",
        "personality": "expansionist",
        "gold": 1900,
        "troops": 220,
        "territories": 8,
        "military_power": 90.0,
        "economic_power": 95.0,
        "diplomatic_influence": 75.0
    },
    "RUS": {
        "name": "Rusia",
        "code": "RUS",
        "personality": "aggressive",
        "gold": 1600,
        "troops": 180,
        "territories": 9,
        "military_power": 88.0,
        "economic_power": 70.0,
        "diplomatic_influence": 65.0
    },
    "DEU": {
        "name": "Alemania",
        "code": "DEU",
        "personality": "neutral",
        "gold": 1700,
        "troops": 150,
        "territories": 4,
        "military_power": 82.0,
        "economic_power": 90.0,
        "diplomatic_influence": 80.0
    },
    "GBR": {
        "name": "Reino Unido",
        "code": "GBR",
        "personality": "diplomatic",
        "gold": 1650,
        "troops": 140,
        "territories": 6,
        "military_power": 80.0,
        "economic_power": 88.0,
        "diplomatic_influence": 85.0
    },
    "FRA": {
        "name": "Francia",
        "code": "FRA",
        "personality": "neutral",
        "gold": 1550,
        "troops": 145,
        "territories": 5,
        "military_power": 78.0,
        "economic_power": 82.0,
        "diplomatic_influence": 82.0
    },
    "JPN": {
        "name": "Japón",
        "code": "JPN",
        "personality": "defensive",
        "gold": 1600,
        "troops": 135,
        "territories": 4,
        "military_power": 75.0,
        "economic_power": 92.0,
        "diplomatic_influence": 70.0
    },
    "ESP": {
        "name": "España",
        "code": "ESP",
        "personality": "diplomatic",
        "gold": 1300,
        "troops": 110,
        "territories": 3,
        "military_power": 68.0,
        "economic_power": 75.0,
        "diplomatic_influence": 72.0
    }
}


class GameService:
    """Servicio para la lógica principal del juego"""
    
    @staticmethod
    def get_available_nations() -> List[Dict[str, Any]]:
        """Obtener lista de naciones disponibles para jugar"""
        return [
            {
                "code": code,
                "name": data["name"],
                "personality": data["personality"],
                "stats": {
                    "military": data["military_power"],
                    "economic": data["economic_power"],
                    "diplomatic": data["diplomatic_influence"]
                }
            }
            for code, data in AVAILABLE_NATIONS.items()
        ]
    
    @staticmethod
    def initialize_game(db: Session, player_nation_code: str = "ESP") -> Dict[str, Any]:
        """
        Inicializar un nuevo juego con naciones predefinidas
        
        Args:
            db: Sesión de base de datos
            player_nation_code: Código de la nación que controlará el jugador (default: ESP)
        
        Returns:
            Información del juego inicializado
        """
        
        print(f"🔧 GameService.initialize_game llamado con: {player_nation_code}")
        
        # Validar que la nación seleccionada existe
        if player_nation_code not in AVAILABLE_NATIONS:
            available_codes = list(AVAILABLE_NATIONS.keys())
            print(f"❌ Nación no válida: {player_nation_code}. Disponibles: {available_codes}")
            raise ValueError(f"Nación {player_nation_code} no disponible. Opciones: {', '.join(available_codes)}")
        
        print(f"✅ Nación válida: {AVAILABLE_NATIONS[player_nation_code]['name']}")
        
        # Crear todas las naciones
        created_nations = []
        print(f"🏗️  Creando {len(AVAILABLE_NATIONS)} naciones...")
        for code, nation_data in AVAILABLE_NATIONS.items():
            is_player = (code == player_nation_code)
            print(f"  - {nation_data['name']} ({code}) {'[JUGADOR]' if is_player else '[IA]'}")
            
            nation_create = NationCreate(
                name=nation_data["name"],
                personality=nation_data["personality"],
                gold=nation_data["gold"],
                troops=nation_data["troops"],
                territories=nation_data["territories"],
                military_power=nation_data["military_power"],
                economic_power=nation_data["economic_power"],
                diplomatic_influence=nation_data["diplomatic_influence"],
                ai_controlled=(code != player_nation_code)  # Solo la elegida es del jugador
            )
            nation = NationService.create(db, nation_create)
            created_nations.append(nation)
        
        print(f"✅ {len(created_nations)} naciones creadas")
        
        # Crear turno inicial
        world_state = {
            "nations": [n.to_dict() for n in created_nations],
            "alliances": [],
            "wars": []
        }
        
        print("📅 Creando turno inicial...")
        initial_turn = TurnService.create_next_turn(
            db,
            world_state=world_state,
            summary="Inicio del juego. Todas las naciones comienzan en paz."
        )
        print(f"✅ Turno {initial_turn.turn_number} creado")
        
        # Crear relaciones neutrales iniciales
        print("🤝 Creando relaciones diplomáticas iniciales...")
        relations_count = 0
        for i, nation_a in enumerate(created_nations):
            for nation_b in created_nations[i+1:]:
                relation_data = RelationCreate(
                    nation_a_id=nation_a.id,
                    nation_b_id=nation_b.id,
                    status="neutral",
                    relationship_score=0
                )
                RelationService.create(db, relation_data)
                relations_count += 1
        print(f"✅ {relations_count} relaciones creadas")
        
        # Encontrar la nación del jugador
        player_nation = next((n for n in created_nations if not n.ai_controlled), None)
        
        print(f"🎉 ¡Juego inicializado! Jugador controla: {player_nation.name if player_nation else 'N/A'}")
        
        return {
            "message": "Juego inicializado exitosamente",
            "turn_number": initial_turn.turn_number,
            "nations_created": len(created_nations),
            "player_nation": player_nation.to_dict() if player_nation else None
        }
    
    @staticmethod
    def get_game_state(db: Session) -> Dict[str, Any]:
        """Obtener el estado actual del juego"""
        nations = NationService.get_all(db)
        current_turn = TurnService.get_current(db)
        recent_events = EventService.get_recent_events(db, limit=10)
        
        return {
            "current_turn": current_turn.turn_number if current_turn else 0,
            "nations": [n.to_dict() for n in nations],
            "recent_events": [e.to_dict() for e in recent_events],
            "is_game_over": GameService.check_game_over(nations)
        }
    
    @staticmethod
    def check_game_over(nations: List) -> bool:
        """Verificar si el juego ha terminado"""
        active_nations = [n for n in nations if n.is_active]
        return len(active_nations) <= 1
    
    @staticmethod
    def process_action(db: Session, nation_id: int, action: ActionRequest) -> Dict[str, Any]:
        """Procesar una acción del jugador"""
        nation = NationService.get_by_id(db, nation_id)
        if not nation:
            return {"success": False, "message": "Nación no encontrada"}
        
        current_turn = TurnService.get_current(db)
        
        # Procesar según el tipo de acción
        if action.action_type == "attack":
            return GameService._process_attack(db, nation, action.target_nation_id, current_turn.id)
        elif action.action_type == "alliance":
            return GameService._process_alliance(db, nation, action.target_nation_id, current_turn.id)
        elif action.action_type == "recruit":
            return GameService._process_recruit(db, nation, action.data.get("amount", 10), current_turn.id)
        elif action.action_type == "build":
            return GameService._process_build(db, nation, action.data, current_turn.id)
        elif action.action_type == "peace_treaty":
            return GameService._process_peace_treaty(db, nation, action.target_nation_id, current_turn.id)
        # ... más acciones
        
        return {"success": False, "message": "Tipo de acción no reconocido"}
    
    @staticmethod
    def _process_attack(db: Session, attacker, defender_id: int, turn_id: int) -> Dict[str, Any]:
        """Procesar un ataque"""
        defender = NationService.get_by_id(db, defender_id)
        if not defender:
            return {"success": False, "message": "Nación objetivo no encontrada"}
        
        # Lógica simple de combate
        if attacker.troops < 20:
            return {"success": False, "message": "No tienes suficientes tropas"}
        
        # Crear evento
        event_data = EventCreate(
            turn_id=turn_id,
            nation_id=attacker.id,
            event_type="attack",
            description=f"{attacker.name} atacó a {defender.name}",
            data={"defender_id": defender.id},
            importance=8
        )
        EventService.create(db, event_data)
        
        # Actualizar relación a guerra
        RelationService.update_or_create(db, attacker.id, defender.id, status="war", relationship_score=-50)
        
        return {"success": True, "message": f"Has atacado a {defender.name}"}
    
    @staticmethod
    def _process_alliance(db: Session, nation, target_id: int, turn_id: int) -> Dict[str, Any]:
        """Procesar propuesta de alianza"""
        target = NationService.get_by_id(db, target_id)
        if not target:
            return {"success": False, "message": "Nación objetivo no encontrada"}
        
        # Crear evento
        event_data = EventCreate(
            turn_id=turn_id,
            nation_id=nation.id,
            event_type="alliance",
            description=f"{nation.name} propuso alianza a {target.name}",
            data={"target_id": target.id},
            importance=6
        )
        EventService.create(db, event_data)
        
        # Actualizar relación
        RelationService.update_or_create(db, nation.id, target.id, status="allied", relationship_score=60)
        
        return {"success": True, "message": f"Alianza formada con {target.name}"}
    
    @staticmethod
    def _process_recruit(db: Session, nation, amount: int, turn_id: int) -> Dict[str, Any]:
        """Procesar reclutamiento de tropas"""
        cost_per_troop = 2  # 800 oro = 400 tropas
        total_cost = amount * cost_per_troop
        
        if nation.gold < total_cost:
            return {"success": False, "message": "No tienes suficiente oro"}
        
        # Actualizar recursos
        NationService.update_resources(db, nation.id, gold_change=-total_cost, troops_change=amount)
        
        # Crear evento
        event_data = EventCreate(
            turn_id=turn_id,
            nation_id=nation.id,
            event_type="recruit",
            description=f"{nation.name} reclutó {amount} tropas",
            data={"amount": amount, "cost": total_cost},
            importance=4
        )
        EventService.create(db, event_data)
        
        return {"success": True, "message": f"Has reclutado {amount} tropas por {total_cost} oro"}

    @staticmethod
    def _process_build(db: Session, nation, data: Dict, turn_id: int) -> Dict[str, Any]:
        """Procesar inversión económica o construcción"""
        build_type = data.get("type", "economy")
        cost = data.get("amount", 800)
        
        if nation.gold < cost:
            return {"success": False, "message": f"No tienes suficiente oro (necesitas {cost})"}
        
        # Actualizar oro
        NationService.update_resources(db, nation.id, gold_change=-cost)
        
        # Mejorar poder económico (similar a invest_in_economy de agent_tools)
        import random
        improvement = random.uniform(20, 40)
        nation.economic_power = min(100.0, nation.economic_power + improvement)
        db.commit()
        
        # Crear evento
        event_data = EventCreate(
            turn_id=turn_id,
            nation_id=nation.id,
            event_type="economic_investment",
            description=f"{nation.name} invirtió {cost} oro en infraestructura económica (+{improvement:.1f}% poder económico)",
            data={"cost": cost, "improvement": improvement},
            importance=5
        )
        EventService.create(db, event_data)
        
        return {"success": True, "message": f"Has invertido {cost} oro en economía (+{improvement:.1f}% poder económico)"}

    @staticmethod
    def _process_peace_treaty(db: Session, nation, target_id: int, turn_id: int) -> Dict[str, Any]:
        """Procesar solicitud de tratado de paz"""
        target = NationService.get_by_id(db, target_id)
        if not target:
            return {"success": False, "message": "Nación objetivo no encontrada"}
        
        # Verificar que estén en guerra
        relation = db.query(Relation).filter(
            ((Relation.nation_a_id == nation.id) & (Relation.nation_b_id == target_id)) |
            ((Relation.nation_a_id == target_id) & (Relation.nation_b_id == nation.id))
        ).first()
        
        if not relation or relation.status != "war":
            return {"success": False, "message": "No estás en guerra con esta nación"}
        
        # Actualizar relación a neutral
        RelationService.update_or_create(db, nation.id, target_id, status="neutral", relationship_score=0)
        
        # Crear evento
        event_data = EventCreate(
            turn_id=turn_id,
            nation_id=nation.id,
            event_type="peace_treaty",
            description=f"{nation.name} firmó la paz con {target.name}",
            data={"target_id": target.id},
            importance=7
        )
        EventService.create(db, event_data)
        
        return {"success": True, "message": f"Has firmado la paz con {target.name}"}
