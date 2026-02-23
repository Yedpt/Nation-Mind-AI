"""
Servicio de Batallas
Gestiona el sistema de combate entre naciones, incluyendo aliados
"""
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import random
import math

from ..models.battle import Battle
from ..models.nation import Nation
from ..models.relation import Relation
from ..schemas.battle_schema import BattleCreate, BattleSimulation
from .nation_service import NationService
from .relation_service import RelationService
from .event_service import EventService
from .turn_service import TurnService
from ..schemas.event_schema import EventCreate


class BattleService:
    
    @staticmethod
    def calculate_battle_type(attacker_troops: int, defender_troops: int) -> str:
        """Determinar tipo de batalla según tropas involucradas"""
        total_troops = attacker_troops + defender_troops
        
        if total_troops < 200:
            return "skirmish"  # Escaramuza
        elif total_troops < 600:
            return "battle"  # Batalla
        else:
            return "total_war"  # Guerra total
    
    
    @staticmethod
    def get_active_allies(db: Session, nation_id: int, exclude_enemy_id: int) -> List[Nation]:
        """
        Obtener aliados activos que pueden ayudar en batalla.
        Solo incluye aliados que NO están en guerra con el enemigo.
        """
        # Obtener todas las relaciones de alianza
        relations = RelationService.get_nation_relations(db, nation_id)
        
        allies = []
        for rel in relations:
            if rel.status == "allied":
                # Determinar ID del aliado
                ally_id = rel.nation_b_id if rel.nation_a_id == nation_id else rel.nation_a_id
                
                # Verificar que el aliado no esté en guerra con el enemigo
                ally_enemy_relation = RelationService.get_between_nations(db, ally_id, exclude_enemy_id)
                if ally_enemy_relation and ally_enemy_relation.status == "war":
                    continue  # Este aliado ya está en guerra, no puede ayudar otra vez
                
                # Obtener datos del aliado
                ally = NationService.get_by_id(db, ally_id)
                if ally and ally.is_active and ally.troops > 20:  # Mínimo 20 tropas para ayudar
                    allies.append(ally)
        
        return allies
    
    
    @staticmethod
    def calculate_ally_bonus(allies: List[Nation]) -> tuple[float, int]:
        """
        Calcular bonificación por aliados.
        Returns: (bonus_multiplier, effective_troops_contribution)
        """
        if not allies:
            return (0.0, 0)
        
        bonus_multiplier = 0.0
        effective_troops = 0
        
        for ally in allies:
            # Cada aliado aporta un 12% de bonus (máx 3 aliados = 36%)
            bonus_multiplier += 0.12
            
            # Los aliados aportan 30% de sus tropas efectivamente
            effective_troops += int(ally.troops * 0.3)
        
        # Máximo 3 aliados cuentan para bonificación
        bonus_multiplier = min(bonus_multiplier, 0.36)
        
        return (bonus_multiplier, effective_troops)
    
    
    @staticmethod
    def calculate_win_probability(
        attacker_troops: int,
        defender_troops: int,
        attacker_power: float,
        defender_power: float,
        attacker_allies_bonus: float = 0.0,
        defender_allies_bonus: float = 0.0,
        attacker_extra_troops: int = 0,
        defender_extra_troops: int = 0
    ) -> tuple[float, float]:
        """
        Calcular probabilidad de victoria para atacante y defensor.
        Sistema balanceado que considera tropas, poder y aliados.
        """
        # Tropas efectivas (incluyendo aliados)
        effective_attacker_troops = attacker_troops + attacker_extra_troops
        effective_defender_troops = defender_troops + defender_extra_troops
        
        # Bonus defensivo base (+15%)
        defender_defensive_bonus = 0.15
        
        # Calcular fuerza efectiva
        attacker_strength = (
            effective_attacker_troops * (attacker_power / 100) * 
            (1 + attacker_allies_bonus)
        )
        
        defender_strength = (
            effective_defender_troops * (defender_power / 100) * 
            (1 + defender_allies_bonus + defender_defensive_bonus)
        )
        
        # Calcular probabilidades (no lineal, usa softmax)
        total_strength = attacker_strength + defender_strength
        
        if total_strength == 0:
            return (0.5, 0.5)
        
        attacker_prob = attacker_strength / total_strength
        defender_prob = defender_strength / total_strength
        
        # Añadir factor de aleatoriedad (±10%)
        randomness = random.uniform(-0.10, 0.10)
        attacker_prob = max(0.05, min(0.95, attacker_prob + randomness))
        defender_prob = 1.0 - attacker_prob
        
        return (attacker_prob, defender_prob)
    
    
    @staticmethod
    def calculate_casualties(
        winner_troops: int,
        loser_troops: int,
        is_decisive: bool = False
    ) -> tuple[int, int]:
        """
        Calcular bajas para ganador y perdedor.
        """
        if is_decisive:
            # Victoria decisiva: ganador pierde 5-15%, perdedor 40-60%
            winner_casualties = random.randint(int(winner_troops * 0.05), int(winner_troops * 0.15))
            loser_casualties = random.randint(int(loser_troops * 0.40), int(loser_troops * 0.60))
        else:
            # Victoria ajustada: ganador pierde 15-25%, perdedor 25-40%
            winner_casualties = random.randint(int(winner_troops * 0.15), int(winner_troops * 0.25))
            loser_casualties = random.randint(int(loser_troops * 0.25), int(loser_troops * 0.40))
        
        return (winner_casualties, loser_casualties)
    
    
    @staticmethod
    def resolve_battle(db: Session, attacker_id: int, defender_id: int, turn_number: int) -> Battle:
        """
        Resolver una batalla completa entre dos naciones.
        Incluye: cálculo de victoria, actualización de recursos, conquistas, eventos.
        """
        # Obtener naciones
        attacker = NationService.get_by_id(db, attacker_id)
        defender = NationService.get_by_id(db, defender_id)
        
        if not attacker or not defender:
            raise ValueError("Nación atacante o defensora no encontrada")
        
        if attacker.troops < 50:
            raise ValueError(f"{attacker.name} no tiene suficientes tropas para atacar (mínimo 50)")
        
        # Obtener aliados activos
        attacker_allies = BattleService.get_active_allies(db, attacker_id, defender_id)
        defender_allies = BattleService.get_active_allies(db, defender_id, attacker_id)
        
        # Calcular bonificaciones por aliados
        attacker_ally_bonus, attacker_ally_troops = BattleService.calculate_ally_bonus(attacker_allies)
        defender_ally_bonus, defender_ally_troops = BattleService.calculate_ally_bonus(defender_allies)
        
        # Calcular probabilidades de victoria
        attacker_prob, defender_prob = BattleService.calculate_win_probability(
            attacker.troops,
            defender.troops,
            attacker.military_power,
            defender.military_power,
            attacker_ally_bonus,
            defender_ally_bonus,
            attacker_ally_troops,
            defender_ally_troops
        )
        
        # Determinar ganador
        is_attacker_win = random.random() < attacker_prob
        winner_id = attacker_id if is_attacker_win else defender_id
        
        # Victoria decisiva si probabilidad > 75%
        is_decisive = attacker_prob > 0.75 or defender_prob > 0.75
        
        # Calcular bajas
        if is_attacker_win:
            attacker_casualties, defender_casualties = BattleService.calculate_casualties(
                attacker.troops, defender.troops, is_decisive
            )
        else:
            defender_casualties, attacker_casualties = BattleService.calculate_casualties(
                defender.troops, attacker.troops, is_decisive
            )
        
        # Calcular territorios conquistados
        if is_decisive:
            territories_conquered = random.randint(1, min(3, defender.territories))
        else:
            territories_conquered = random.randint(0, min(2, defender.territories))
        
        # Calcular oro saqueado (15-30% del oro del perdedor)
        loser_nation = defender if is_attacker_win else attacker
        gold_looted = random.randint(int(loser_nation.gold * 0.15), int(loser_nation.gold * 0.30))
        
        # Determinar tipo de batalla
        battle_type = BattleService.calculate_battle_type(attacker.troops, defender.troops)
        
        # Crear registro de batalla
        battle = Battle(
            turn_number=turn_number,
            attacker_id=attacker_id,
            defender_id=defender_id,
            winner_id=winner_id,
            battle_type=battle_type,
            attacker_troops_initial=attacker.troops,
            defender_troops_initial=defender.troops,
            attacker_power=attacker.military_power,
            defender_power=defender.military_power,
            attacker_allies=[a.id for a in attacker_allies],
            defender_allies=[a.id for a in defender_allies],
            attacker_bonus=attacker_ally_bonus,
            defender_bonus=defender_ally_bonus + 0.15,  # Incluye bonus defensivo
            attacker_casualties=attacker_casualties,
            defender_casualties=defender_casualties,
            territories_conquered=territories_conquered,
            gold_looted=gold_looted,
            attacker_win_chance=attacker_prob,
            defender_win_chance=defender_prob,
            is_decisive=is_decisive,
            description=BattleService._generate_battle_description(
                attacker, defender, winner_id, is_decisive, 
                len(attacker_allies), len(defender_allies)
            )
        )
        
        db.add(battle)
        db.flush()  # Para obtener el ID
        
        # Actualizar recursos de las naciones
        BattleService._apply_battle_results(
            db, attacker, defender, 
            attacker_casualties, defender_casualties,
            territories_conquered, gold_looted, winner_id
        )
        
        # Generar evento
        BattleService._create_battle_event(db, battle, attacker, defender)
        
        db.commit()
        db.refresh(battle)
        
        return battle
    
    
    @staticmethod
    def _apply_battle_results(
        db: Session,
        attacker: Nation,
        defender: Nation,
        attacker_casualties: int,
        defender_casualties: int,
        territories_conquered: int,
        gold_looted: int,
        winner_id: int
    ):
        """Aplicar los resultados de la batalla a las naciones"""
        winner = attacker if winner_id == attacker.id else defender
        loser = defender if winner_id == attacker.id else attacker
        
        # Actualizar tropas
        NationService.update(db, attacker.id, {"troops": max(10, attacker.troops - attacker_casualties)})
        NationService.update(db, defender.id, {"troops": max(10, defender.troops - defender_casualties)})
        
        # Transferir territorios
        if territories_conquered > 0:
            NationService.update(db, winner.id, {"territories": winner.territories + territories_conquered})
            NationService.update(db, loser.id, {"territories": max(1, loser.territories - territories_conquered)})
        
        # Transferir oro
        if gold_looted > 0:
            NationService.update(db, winner.id, {"gold": winner.gold + gold_looted})
            NationService.update(db, loser.id, {"gold": max(50, loser.gold - gold_looted)})
        
        # Reducir poder militar del perdedor
        new_military_power = max(30, loser.military_power - random.uniform(5, 15))
        NationService.update(db, loser.id, {"military_power": new_military_power})
    
    
    @staticmethod
    def _generate_battle_description(
        attacker: Nation, 
        defender: Nation, 
        winner_id: int,
        is_decisive: bool,
        attacker_allies_count: int,
        defender_allies_count: int
    ) -> str:
        """Generar descripción narrativa de la batalla"""
        winner_name = attacker.name if winner_id == attacker.id else defender.name
        loser_name = defender.name if winner_id == attacker.id else attacker.name
        
        decisive_text = "victoria aplastante" if is_decisive else "victoria"
        
        ally_text = ""
        if attacker_allies_count > 0 and winner_id == attacker.id:
            ally_text = f" con ayuda de {attacker_allies_count} aliado(s)"
        elif defender_allies_count > 0 and winner_id == defender.id:
            ally_text = f" con ayuda de {defender_allies_count} aliado(s)"
        
        return (
            f"{attacker.name} ataca a {defender.name}. "
            f"Después de intensos combates, {winner_name} obtiene una {decisive_text}{ally_text}. "
            f"{loser_name} sufre pérdidas significativas."
        )
    
    
    @staticmethod
    def _create_battle_event(db: Session, battle: Battle, attacker: Nation, defender: Nation):
        """Crear evento de batalla para el sistema RAG"""
        winner_name = attacker.name if battle.winner_id == attacker.id else defender.name
        
        # Obtener el turn_id real desde la base de datos
        current_turn = TurnService.get_by_number(db, battle.turn_number)
        turn_id = current_turn.id if current_turn else 1
        
        event_data = EventCreate(
            nation_id=battle.winner_id,
            turn_id=turn_id,
            event_type="MILITARY",
            description=f"Batalla: {attacker.name} vs {defender.name}. {battle.description}",
            importance=9 if battle.is_decisive else 7,
            data={
                "battle_id": battle.id,
                "attacker_id": battle.attacker_id,
                "defender_id": battle.defender_id,
                "winner": winner_name,
                "casualties": {
                    "attacker": battle.attacker_casualties,
                    "defender": battle.defender_casualties
                },
                "spoils": {
                    "territories": battle.territories_conquered,
                    "gold": battle.gold_looted
                }
            }
        )
        
        EventService.create(db, event_data)
    
    
    @staticmethod
    def simulate_battle(db: Session, attacker_id: int, defender_id: int) -> Dict[str, Any]:
        """
        Simular una batalla SIN ejecutarla.
        Útil para que los agentes IA evalúen si atacar o no.
        """
        attacker = NationService.get_by_id(db, attacker_id)
        defender = NationService.get_by_id(db, defender_id)
        
        if not attacker or not defender:
            raise ValueError("Nación no encontrada")
        
        # Obtener aliados
        attacker_allies = BattleService.get_active_allies(db, attacker_id, defender_id)
        defender_allies = BattleService.get_active_allies(db, defender_id, attacker_id)
        
        # Calcular bonificaciones
        attacker_ally_bonus, attacker_ally_troops = BattleService.calculate_ally_bonus(attacker_allies)
        defender_ally_bonus, defender_ally_troops = BattleService.calculate_ally_bonus(defender_allies)
        
        # Calcular probabilidades
        attacker_prob, defender_prob = BattleService.calculate_win_probability(
            attacker.troops,
            defender.troops,
            attacker.military_power,
            defender.military_power,
            attacker_ally_bonus,
            defender_ally_bonus,
            attacker_ally_troops,
            defender_ally_troops
        )
        
        # Estimar bajas esperadas
        avg_attacker_casualties = int(attacker.troops * 0.20)
        avg_defender_casualties = int(defender.troops * 0.35)
        
        # Recomendación
        if attacker_prob > 0.70:
            recommendation = "attack"  # Ataque favorable
        elif attacker_prob > 0.45:
            recommendation = "risky"  # Arriesgado
        else:
            recommendation = "avoid"  # Evitar
        
        return {
            "attacker_win_chance": round(attacker_prob * 100, 2),
            "defender_win_chance": round(defender_prob * 100, 2),
            "attacker_expected_casualties": avg_attacker_casualties,
            "defender_expected_casualties": avg_defender_casualties,
            "expected_territories": 1 if attacker_prob > 0.60 else 0,
            "expected_gold": int(defender.gold * 0.25) if attacker_prob > 0.60 else 0,
            "recommendation": recommendation,
            "factors": {
                "attacker_allies": len(attacker_allies),
                "defender_allies": len(defender_allies),
                "attacker_bonus": f"+{int(attacker_ally_bonus * 100)}%",
                "defender_bonus": f"+{int((defender_ally_bonus + 0.15) * 100)}%",
                "troop_ratio": round(attacker.troops / max(1, defender.troops), 2)
            }
        }
    
    
    @staticmethod
    def get_active_wars(db: Session) -> List[Dict[str, Any]]:
        """Obtener todas las guerras activas (relaciones en estado war)"""
        wars = db.query(Relation).filter(Relation.status == "war").all()
        
        result = []
        for war in wars:
            nation_a = NationService.get_by_id(db, war.nation_a_id)
            nation_b = NationService.get_by_id(db, war.nation_b_id)
            
            result.append({
                "nation_a": nation_a.name if nation_a else "Unknown",
                "nation_b": nation_b.name if nation_b else "Unknown",
                "relationship_score": war.relationship_score,
                "nation_a_id": war.nation_a_id,
                "nation_b_id": war.nation_b_id
            })
        
        return result
    
    
    @staticmethod
    def get_battle_history(db: Session, limit: int = 20) -> List[Battle]:
        """Obtener historial de batallas"""
        return db.query(Battle).order_by(Battle.created_at.desc()).limit(limit).all()
    
    
    @staticmethod
    def get_nation_battles(db: Session, nation_id: int) -> List[Battle]:
        """Obtener todas las batallas de una nación"""
        return db.query(Battle).filter(
            (Battle.attacker_id == nation_id) | (Battle.defender_id == nation_id)
        ).order_by(Battle.created_at.desc()).all()
    
    
    @staticmethod
    def resolve_active_wars(db: Session, turn_number: int) -> List[Dict[str, Any]]:
        """
        Resolver automáticamente todas las guerras activas del turno.
        
        Cada par de naciones en guerra tiene una batalla automática.
        El resultado afecta recursos, territorios y puede eliminar naciones.
        
        Args:
            db: Sesión de base de datos
            turn_number: Número del turno actual
            
        Returns:
            Lista de resultados de batallas con ganadores y efectos
        """
        from .nation_service import NationService
        
        # Obtener todas las guerras activas
        wars = db.query(Relation).filter(Relation.status == "war").all()
        
        if not wars:
            return []
        
        battles_resolved = []
        
        for war in wars:
            nation_a = NationService.get_by_id(db, war.nation_a_id)
            nation_b = NationService.get_by_id(db, war.nation_b_id)
            
            if not nation_a or not nation_b:
                continue
            
            # Verificar que ambas estén activas
            if not nation_a.is_active or not nation_b.is_active:
                continue
            
            # Determinar atacante (iniciador de la guerra = mayor en ID)
            if nation_a.id > nation_b.id:
                attacker = nation_a
                defender = nation_b
            else:
                attacker = nation_b
                defender = nation_a
            
            print(f"\n   ⚔️  {attacker.name} vs {defender.name}")
            
            # Resolver batalla usando el sistema existente
            try:
                battle = BattleService.resolve_battle(
                    db=db,
                    attacker_id=attacker.id,
                    defender_id=defender.id,
                    turn_number=turn_number
                )
                
                # Extraer datos del resultado
                winner_id = battle.winner_id
                winner = NationService.get_by_id(db, winner_id) if winner_id else None
                loser = defender if winner_id == attacker.id else attacker
                
                territories_gained = battle.territories_captured
                gold_plundered = battle.gold_plundered
                
                battles_resolved.append({
                    "attacker_id": attacker.id,
                    "attacker_name": attacker.name,
                    "defender_id": defender.id,
                    "defender_name": defender.name,
                    "winner_id": winner_id,
                    "winner_name": winner.name if winner else "Empate",
                    "loser_name": loser.name if loser else "N/A",
                    "territories_gained": territories_gained,
                    "gold_plundered": gold_plundered,
                    "attacker_casualties": battle.attacker_casualties,
                    "defender_casualties": battle.defender_casualties
                })
                
                print(f"      👑 Ganador: {winner.name if winner else 'Empate'}")
                print(f"      💀 Bajas: {battle.attacker_casualties} (atacante), {battle.defender_casualties} (defensor)")
                
                # Si el perdedor se quedó sin territorios, eliminarlo
                if loser and loser.territories <= 0:
                    loser.is_active = False
                    db.commit()
                    print(f"      ☠️  {loser.name} ha sido eliminado del juego")
                    
            except Exception as e:
                print(f"      ❌ Error resolviendo batalla: {e}")
                continue
        
        return battles_resolved
