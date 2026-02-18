"""
Servicio principal del juego
Coordina la lógica de alto nivel del simulador
"""
from sqlalchemy.orm import Session
from typing import Dict, List, Any
from .nation_service import NationService
from .turn_service import TurnService
from .event_service import EventService
from .relation_service import RelationService
from ..schemas.nation_schema import NationCreate
from ..schemas.event_schema import EventCreate
from ..schemas.relation_schema import RelationCreate
from ..schemas.game_schema import ActionRequest


class GameService:
    """Servicio para la lógica principal del juego"""
    
    @staticmethod
    def initialize_game(db: Session) -> Dict[str, Any]:
        """Inicializar un nuevo juego con naciones predefinidas"""
        
        # Definir naciones iniciales
        initial_nations = [
            NationCreate(
                name="España",
                personality="diplomatic",
                gold=1200,
                troops=120,
                territories=3,
                military_power=60.0,
                economic_power=70.0,
                diplomatic_influence=65.0,
                ai_controlled=False  # Jugador
            ),
            NationCreate(
                name="Francia",
                personality="aggressive",
                gold=1500,
                troops=150,
                territories=4,
                military_power=80.0,
                economic_power=75.0,
                diplomatic_influence=70.0,
                ai_controlled=True
            ),
            NationCreate(
                name="Alemania",
                personality="expansionist",
                gold=1800,
                troops=180,
                territories=5,
                military_power=85.0,
                economic_power=90.0,
                diplomatic_influence=60.0,
                ai_controlled=True
            ),
            NationCreate(
                name="Italia",
                personality="defensive",
                gold=1000,
                troops=100,
                territories=2,
                military_power=55.0,
                economic_power=65.0,
                diplomatic_influence=60.0,
                ai_controlled=True
            ),
            NationCreate(
                name="Inglaterra",
                personality="diplomatic",
                gold=1600,
                troops=140,
                territories=3,
                military_power=75.0,
                economic_power=85.0,
                diplomatic_influence=80.0,
                ai_controlled=True
            )
        ]
        
        # Crear naciones
        created_nations = []
        for nation_data in initial_nations:
            nation = NationService.create(db, nation_data)
            created_nations.append(nation)
        
        # Crear turno inicial
        world_state = {
            "nations": [n.to_dict() for n in created_nations],
            "alliances": [],
            "wars": []
        }
        
        initial_turn = TurnService.create_next_turn(
            db,
            world_state=world_state,
            summary="Inicio del juego. Todas las naciones comienzan en paz."
        )
        
        # Crear relaciones neutrales iniciales
        for i, nation_a in enumerate(created_nations):
            for nation_b in created_nations[i+1:]:
                relation_data = RelationCreate(
                    nation_a_id=nation_a.id,
                    nation_b_id=nation_b.id,
                    status="neutral",
                    relationship_score=0
                )
                RelationService.create(db, relation_data)
        
        return {
            "message": "Juego inicializado exitosamente",
            "turn_number": initial_turn.turn_number,
            "nations_created": len(created_nations)
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
        cost_per_troop = 10
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
