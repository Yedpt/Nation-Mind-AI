"""
Herramientas (Tools) para Agentes IA
Acciones que los agentes pueden ejecutar en el mundo del juego
"""
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from langchain.tools import tool

from .nation_service import NationService
from .relation_service import RelationService
from .event_service import EventService
from .turn_service import TurnService
from ..schemas.event_schema import EventCreate
from ..schemas.relation_schema import RelationUpdate


# ==================== HERRAMIENTAS DE CONSULTA ====================

@tool
def get_my_nation_status(nation_id: int, db: Session) -> Dict[str, Any]:
    """
    Obtener el estado actual de mi nación.
    
    Args:
        nation_id: ID de la nación que consulta
        db: Sesión de base de datos
        
    Returns:
        dict: Estado completo de la nación (oro, tropas, territorios, etc.)
    """
    nation = NationService.get_by_id(db, nation_id)
    if not nation:
        return {"error": "Nación no encontrada"}
    
    return {
        "id": nation.id,
        "name": nation.name,
        "gold": nation.gold,
        "troops": nation.troops,
        "territories": nation.territories,
        "military_power": nation.military_power,
        "economic_power": nation.economic_power,
        "diplomatic_influence": nation.diplomatic_influence,
        "is_active": nation.is_active
    }


@tool
def get_all_nations_status(db: Session) -> List[Dict[str, Any]]:
    """
    Obtener el estado de todas las naciones activas.
    
    Args:
        db: Sesión de base de datos
        
    Returns:
        list: Lista con información de todas las naciones
    """
    nations = NationService.get_all(db)
    return [
        {
            "id": n.id,
            "name": n.name,
            "gold": n.gold,
            "troops": n.troops,
            "territories": n.territories,
            "military_power": n.military_power,
            "is_active": n.is_active,
            "ai_controlled": n.ai_controlled
        }
        for n in nations
    ]


@tool
def get_relations_status(nation_id: int, db: Session) -> List[Dict[str, Any]]:
    """
    Obtener las relaciones diplomáticas de mi nación con otras.
    
    Args:
        nation_id: ID de la nación que consulta
        db: Sesión de base de datos
        
    Returns:
        list: Relaciones con otras naciones (aliado, enemigo, neutral)
    """
    relations = RelationService.get_nation_relations(db, nation_id)
    return [
        {
            "with_nation_id": r.nation_b_id if r.nation_a_id == nation_id else r.nation_a_id,
            "status": r.status,
            "relationship_score": r.relationship_score
        }
        for r in relations
    ]


# ==================== HERRAMIENTAS DE ACCIÓN ====================

@tool
def propose_alliance(
    nation_id: int,
    target_nation_id: int,
    message: str,
    db: Session
) -> Dict[str, Any]:
    """
    Proponer una alianza diplomática a otra nación.
    
    Args:
        nation_id: ID de la nación que propone
        target_nation_id: ID de la nación objetivo
        message: Mensaje de la propuesta
        db: Sesión de base de datos
        
    Returns:
        dict: Resultado de la propuesta
    """
    try:
        # Verificar que no sean la misma nación
        if nation_id == target_nation_id:
            return {"success": False, "message": "No puedes aliarte contigo mismo"}
        
        # Obtener relación actual
        relation = RelationService.get_between_nations(db, nation_id, target_nation_id)
        if not relation:
            return {"success": False, "message": "Relación no encontrada"}
        
        # Si ya son aliados
        if relation.status == "allied":
            return {"success": False, "message": "Ya son aliados"}
        
        # Si son enemigos, no puede
        if relation.status == "war":
            return {"success": False, "message": "No puedes aliarte con un enemigo en guerra"}
        
        # Mejorar relación significativamente
        new_score = min(100, relation.relationship_score + 40)
        
        update_data = RelationUpdate(
            status="allied" if new_score >= 70 else "neutral",
            relationship_score=new_score
        )
        
        RelationService.update(db, relation.id, update_data)
        
        # Crear evento
        nation = NationService.get_by_id(db, nation_id)
        target_nation = NationService.get_by_id(db, target_nation_id)
        
        # Obtener turno actual
        current_turn = TurnService.get_current(db)
        current_turn_id = current_turn.id if current_turn else 1
        
        event_data = EventCreate(
            turn_id=current_turn_id,
            nation_id=nation_id,
            event_type="DIPLOMATIC",
            description=f"{nation.name} propone alianza a {target_nation.name}: '{message}'",
            importance=7,
            data={"target_nation": target_nation_id, "action": "propose_alliance"}
        )
        EventService.create(db, event_data)
        
        return {
            "success": True,
            "message": f"Alianza propuesta a {target_nation.name}",
            "new_status": update_data.status,
            "new_score": new_score
        }
        
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


@tool
def declare_war(
    nation_id: int,
    target_nation_id: int,
    reason: str,
    db: Session
) -> Dict[str, Any]:
    """
    Declarar la guerra a otra nación y ejecutar una batalla inmediata.
    
    Args:
        nation_id: ID de la nación que declara
        target_nation_id: ID de la nación objetivo
        reason: Razón de la declaración de guerra
        db: Sesión de base de datos
        
    Returns:
        dict: Resultado de la declaración y batalla
    """
    try:
        # Verificar que no sean la misma nación
        if nation_id == target_nation_id:
            return {"success": False, "message": "No puedes declararte guerra a ti mismo"}
        
        # Obtener naciones
        nation = NationService.get_by_id(db, nation_id)
        target_nation = NationService.get_by_id(db, target_nation_id)
        
        if not nation or not target_nation:
            return {"success": False, "message": "Nación no encontrada"}
        
        # Verificar que tenga suficientes tropas
        if nation.troops < 50:
            return {"success": False, "message": "No tienes suficientes tropas para declarar guerra"}
        
        # Obtener relación
        relation = RelationService.get_between_nations(db, nation_id, target_nation_id)
        if not relation:
            return {"success": False, "message": "Relación no encontrada"}
        
        # Verificar si ya está en guerra
        if relation.status == "war":
            return {"success": False, "message": f"Ya estás en guerra con {target_nation.name}"}
        
        # Cambiar a estado de guerra
        update_data = RelationUpdate(
            status="war",
            relationship_score=-80
        )
        RelationService.update(db, relation.id, update_data)
        
        # Obtener turno actual
        from .turn_service import TurnService
        current_turn = TurnService.get_current(db)
        current_turn_id = current_turn.id if current_turn else 1
        current_turn_number = current_turn.turn_number if current_turn else 1
        
        # ⚔️ EJECUTAR BATALLA INMEDIATA
        from .battle_service import BattleService
        battle = BattleService.resolve_battle(db, nation_id, target_nation_id, current_turn_number)
        
        # Crear evento importante combinando declaración + resultado batalla
        winner_name = nation.name if battle.winner_id == nation_id else target_nation.name
        
        event_data = EventCreate(
            turn_id=current_turn_id,
            nation_id=nation_id,
            event_type="MILITARY",
            description=(
                f"⚔️ {nation.name} declara la guerra a {target_nation.name}. "
                f"Razón: {reason}. "
                f"Batalla: {battle.description} Ganador: {winner_name}."
            ),
            importance=10,
            data={
                "target_nation": target_nation_id,
                "action": "declare_war",
                "reason": reason,
                "battle_id": battle.id,
                "winner_id": battle.winner_id,
                "casualties": {
                    "attacker": battle.attacker_casualties,
                    "defender": battle.defender_casualties
                }
            }
        )
        EventService.create(db, event_data)
        
        return {
            "success": True,
            "message": f"Guerra declarada a {target_nation.name}. Batalla ejecutada.",
            "status": "war",
            "battle_result": {
                "winner": winner_name,
                "winner_id": battle.winner_id,
                "attacker_casualties": battle.attacker_casualties,
                "defender_casualties": battle.defender_casualties,
                "territories_conquered": battle.territories_conquered,
                "gold_looted": battle.gold_looted,
                "is_decisive": battle.is_decisive
            }
        }
        
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


@tool
def invest_in_military(
    nation_id: int,
    amount: int,
    db: Session
) -> Dict[str, Any]:
    """
    Invertir oro en mejorar capacidad militar (reclutar tropas).
    
    Args:
        nation_id: ID de la nación
        amount: Cantidad de oro a invertir
        db: Sesión de base de datos
        
    Returns:
        dict: Resultado de la inversión
    """
    try:
        nation = NationService.get_by_id(db, nation_id)
        if not nation:
            return {"success": False, "message": "Nación no encontrada"}
        
        if nation.gold < amount:
            return {"success": False, "message": "Fondos insuficientes"}
        
        # Convertir oro en tropas (1 oro = 0.5 tropas, mínimo 10 oro)
        if amount < 10:
            return {"success": False, "message": "Inversión mínima: 10 oro"}
        
        new_troops = int(amount * 0.5)
        new_gold = nation.gold - amount
        total_troops = nation.troops + new_troops
        
        # Actualizar
        NationService.update(db, nation_id, {
            "gold": new_gold,
            "troops": total_troops,
            "military_power": min(100, nation.military_power + (new_troops * 0.1))
        })
        
        # Crear evento
        current_turn = TurnService.get_current(db)
        current_turn_id = current_turn.id if current_turn else 1
        
        event_data = EventCreate(
            turn_id=current_turn_id,
            nation_id=nation_id,
            event_type="MILITARY",
            description=f"{nation.name} invierte {amount} oro en reclutar {new_troops} tropas",
            importance=5,
            data={"investment": amount, "troops_gained": new_troops}
        )
        EventService.create(db, event_data)
        
        return {
            "success": True,
            "message": f"Reclutadas {new_troops} tropas",
            "investment": amount,
            "troops_gained": new_troops,
            "new_total_troops": total_troops
        }
        
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


@tool
def invest_in_economy(
    nation_id: int,
    amount: int,
    db: Session
) -> Dict[str, Any]:
    """
    Invertir oro en mejorar la economía (infraestructura, comercio).
    
    Args:
        nation_id: ID de la nación
        amount: Cantidad de oro a invertir
        db: Sesión de base de datos
        
    Returns:
        dict: Resultado de la inversión
    """
    try:
        nation = NationService.get_by_id(db, nation_id)
        if not nation:
            return {"success": False, "message": "Nación no encontrada"}
        
        if nation.gold < amount:
            return {"success": False, "message": "Fondos insuficientes"}
        
        if amount < 20:
            return {"success": False, "message": "Inversión mínima: 20 oro"}
        
        # La inversión económica genera retorno a largo plazo
        # Por cada 20 oro invertido, +2% poder económico permanente
        eco_boost = (amount / 20) * 2
        new_gold = nation.gold - amount
        new_eco_power = min(100, nation.economic_power + eco_boost)
        
        # Actualizar
        NationService.update(db, nation_id, {
            "gold": new_gold,
            "economic_power": new_eco_power
        })
        
        # Crear evento
        current_turn = TurnService.get_current(db)
        current_turn_id = current_turn.id if current_turn else 1
        
        event_data = EventCreate(
            turn_id=current_turn_id,
            nation_id=nation_id,
            event_type="ECONOMIC",
            description=f"{nation.name} invierte {amount} oro en infraestructura económica (+{eco_boost:.1f}% poder económico)",
            importance=6,
            data={"investment": amount, "eco_boost": eco_boost}
        )
        EventService.create(db, event_data)
        
        return {
            "success": True,
            "message": f"Economía mejorada en {eco_boost:.1f}%",
            "investment": amount,
            "eco_boost": eco_boost,
            "new_economic_power": new_eco_power
        }
        
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


@tool
def do_nothing(nation_id: int, db: Session) -> Dict[str, Any]:
    """
    No tomar ninguna acción este turno (esperar y observar).
    
    Args:
        nation_id: ID de la nación
        db: Sesión de base de datos
        
    Returns:
        dict: Confirmación
    """
    nation = NationService.get_by_id(db, nation_id)
    if not nation:
        return {"success": False, "message": "Nación no encontrada"}
    
    # Pequeña recuperación pasiva de oro y tropas
    new_gold = nation.gold + 10
    new_troops = nation.troops + 5
    
    NationService.update(db, nation_id, {
        "gold": new_gold,
        "troops": new_troops
    })
    
    current_turn = TurnService.get_current(db)
    current_turn_id = current_turn.id if current_turn else 1
    
    event_data = EventCreate(
        turn_id=current_turn_id,
        nation_id=nation_id,
        event_type="ECONOMIC",
        description=f"{nation.name} mantiene la paz y desarrolla internamente (+10 oro, +5 tropas)",
        importance=3
    )
    EventService.create(db, event_data)
    
    return {
        "success": True,
        "message": "Turno de desarrollo interno",
        "gold_gained": 10,
        "troops_gained": 5
    }


@tool
def simulate_battle(nation_id: int, target_nation_id: int, db: Session) -> Dict[str, Any]:
    """
    Simular una batalla SIN ejecutarla. Útil para evaluar si atacar es una buena idea.
    
    Args:
        nation_id: ID de tu nación (atacante)
        target_nation_id: ID de la nación objetivo
        db: Sesión de base de datos
        
    Returns:
        dict: Probabilidades de victoria, bajas esperadas y recomendación
    """
    try:
        from .battle_service import BattleService
        
        result = BattleService.simulate_battle(db, nation_id, target_nation_id)
        return {
            "success": True,
            "simulation": result
        }
    except Exception as e:
        return {"success": False, "message": f"Error en simulación: {str(e)}"}


@tool
def propose_trade_agreement(
    nation_id: int,
    target_nation_id: int,
    gold_offer: int,
    reason: str,
    db: Session
) -> Dict[str, Any]:
    """
    Proponer un acuerdo comercial con otra nación.
    Intercambio económico que beneficia relaciones.
    
    Args:
        nation_id: ID de tu nación
        target_nation_id: ID de la nación con quien negociar
        gold_offer: Cantidad de oro a intercambiar (positivo = dar, negativo = pedir)
        reason: Razón del acuerdo comercial
        db: Sesión de base de datos
        
    Returns:
        dict: Resultado del acuerdo comercial
    """
    try:
        if nation_id == target_nation_id:
            return {"success": False, "message": "No puedes comerciar contigo mismo"}
        
        nation = NationService.get_by_id(db, nation_id)
        target_nation = NationService.get_by_id(db, target_nation_id)
        
        if not nation or not target_nation:
            return {"success": False, "message": "Nación no encontrada"}
        
        # Verificar fondos suficientes
        if gold_offer > 0 and nation.gold < gold_offer:
            return {"success": False, "message": "No tienes suficiente oro"}
        
        # Ejecutar transferencia
        if gold_offer > 0:
            NationService.update(db, nation_id, {"gold": nation.gold - gold_offer})
            NationService.update(db, target_nation_id, {"gold": target_nation.gold + gold_offer})
            transfer_text = f"{nation.name} transfiere {gold_offer} oro a {target_nation.name}"
        else:
            # Caso de solicitar oro (menos común)
            transfer_text = f"{nation.name} solicita {abs(gold_offer)} oro de {target_nation.name}"
        
        # Mejorar relación
        relation = RelationService.get_between_nations(db, nation_id, target_nation_id)
        if relation:
            new_score = min(100, relation.relationship_score + 15)
            RelationService.update(db, relation.id, RelationUpdate(relationship_score=new_score))
        
        # Crear evento
        current_turn = TurnService.get_current(db)
        current_turn_id = current_turn.id if current_turn else 1
        
        event_data = EventCreate(
            turn_id=current_turn_id,
            nation_id=nation_id,
            event_type="ECONOMIC",
            description=f"💰 Acuerdo comercial: {transfer_text}. Razón: {reason}",
            importance=6,
            data={
                "target_nation": target_nation_id,
                "action": "trade_agreement",
                "gold_amount": gold_offer,
                "reason": reason
            }
        )
        EventService.create(db, event_data)
        
        return {
            "success": True,
            "message": f"Acuerdo comercial con {target_nation.name} ejecutado",
            "gold_transferred": gold_offer,
            "relation_improved": True
        }
        
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


@tool
def request_peace_treaty(
    nation_id: int,
    target_nation_id: int,
    reparations: int,
    db: Session
) -> Dict[str, Any]:
    """
    Solicitar tratado de paz con una nación enemiga.
    Finaliza estado de guerra.
    
    Args:
        nation_id: ID de tu nación
        target_nation_id: ID de la nación enemiga
        reparations: Reparaciones de guerra en oro (positivo = pagar, negativo = recibir)
        db: Sesión de base de datos
        
    Returns:
        dict: Resultado de la negociación de paz
    """
    try:
        nation = NationService.get_by_id(db, nation_id)
        target_nation = NationService.get_by_id(db, target_nation_id)
        
        if not nation or not target_nation:
            return {"success": False, "message": "Nación no encontrada"}
        
        # Obtener relación
        relation = RelationService.get_between_nations(db, nation_id, target_nation_id)
        if not relation:
            return {"success": False, "message": "Relación no encontrada"}
        
        if relation.status != "war":
            return {"success": False, "message": f"No estás en guerra con {target_nation.name}"}
        
        # Verificar fondos para reparaciones
        if reparations > 0 and nation.gold < reparations:
            return {"success": False, "message": "No tienes suficiente oro para reparaciones"}
        
        # Ejecutar reparaciones
        if reparations > 0:
            NationService.update(db, nation_id, {"gold": nation.gold - reparations})
            NationService.update(db, target_nation_id, {"gold": target_nation.gold + reparations})
        elif reparations < 0:
            NationService.update(db, nation_id, {"gold": nation.gold + abs(reparations)})
            NationService.update(db, target_nation_id, {"gold": target_nation.gold - abs(reparations)})
        
        # Cambiar estado a neutral
        RelationService.update(db, relation.id, RelationUpdate(
            status="neutral",
            relationship_score=-20  # Relación dañada pero sin guerra
        ))
        
        # Crear evento
        current_turn = TurnService.get_current(db)
        current_turn_id = current_turn.id if current_turn else 1
        
        event_data = EventCreate(
            turn_id=current_turn_id,
            nation_id=nation_id,
            event_type="DIPLOMATIC",
            description=f"🕊️ Tratado de paz firmado entre {nation.name} y {target_nation.name}. Reparaciones: {reparations} oro",
            importance=8,
            data={
                "target_nation": target_nation_id,
                "action": "peace_treaty",
                "reparations": reparations
            }
        )
        EventService.create(db, event_data)
        
        return {
            "success": True,
            "message": f"Paz firmada con {target_nation.name}",
            "status": "neutral",
            "reparations_paid": reparations
        }
        
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


@tool
def organize_diplomatic_summit(
    nation_id: int,
    attendees: str,
    topic: str,
    db: Session
) -> Dict[str, Any]:
    """
    Organizar una cumbre diplomática con múltiples naciones.
    Mejora relaciones y aumenta influencia diplomática.
    
    Args:
        nation_id: ID de tu nación (organizador)
        attendees: Nombres de naciones participantes, separados por comas
        topic: Tema de la cumbre
        db: Sesión de base de datos
        
    Returns:
        dict: Resultado de la cumbre
    """
    try:
        nation = NationService.get_by_id(db, nation_id)
        if not nation:
            return {"success": False, "message": "Nación no encontrada"}
        
        # Costo de organizar cumbre
        cost = 50
        if nation.gold < cost:
            return {"success": False, "message": "No tienes suficiente oro para organizar cumbre (50 oro)"}
        
        NationService.update(db, nation_id, {
            "gold": nation.gold - cost,
            "diplomatic_influence": min(100, nation.diplomatic_influence + 10)
        })
        
        # Crear evento
        current_turn = TurnService.get_current(db)
        current_turn_id = current_turn.id if current_turn else 1
        
        event_data = EventCreate(
            turn_id=current_turn_id,
            nation_id=nation_id,
            event_type="DIPLOMATIC",
            description=f"🏛️ {nation.name} organiza cumbre diplomática sobre '{topic}'. Participantes: {attendees}",
            importance=7,
            data={
                "action": "diplomatic_summit",
                "attendees": attendees,
                "topic": topic,
                "cost": cost
            }
        )
        EventService.create(db, event_data)
        
        return {
            "success": True,
            "message": f"Cumbre diplomática organizada exitosamente",
            "topic": topic,
            "diplomatic_influence_gained": 10,
            "cost": cost
        }
        
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


# ==================== REGISTRO DE HERRAMIENTAS ====================

def get_agent_tools() -> List:
    """
    Obtener lista de todas las herramientas disponibles para los agentes.
    
    Returns:
        list: Lista de herramientas LangChain
    """
    return [
        get_my_nation_status,
        get_all_nations_status,
        get_relations_status,
        propose_alliance,
        declare_war,
        invest_in_military,
        invest_in_economy,
        do_nothing,
        simulate_battle,
        propose_trade_agreement,
        request_peace_treaty,
        organize_diplomatic_summit
    ]
