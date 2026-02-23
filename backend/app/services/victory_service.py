"""
Servicio de Victoria
Gestiona las condiciones de victoria y fin del juego
"""
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
from datetime import datetime

from ..models.nation import Nation
from .nation_service import NationService


class VictoryService:
    """Servicio para determinar condiciones de victoria"""
    
    # Constantes de victoria
    VICTORY_TYPES = {
        "domination": {
            "name": "Victoria por Dominación",
            "description": "Controlar más del 50% de territorios del mundo",
            "icon": "👑"
        },
        "elimination": {
            "name": "Victoria por Eliminación",
            "description": "Ser la única nación activa",
            "icon": "⚔️"
        },
        "economic": {
            "name": "Victoria Económica",
            "description": "Acumular 10,000 oro y 90% poder económico",
            "icon": "💰"
        },
        "military": {
            "name": "Victoria Militar",
            "description": "Tener 2,000 tropas y 90% poder militar",
            "icon": "🪖"
        },
        "survival": {
            "name": "Victoria por Supervivencia",
            "description": "Sobrevivir 100 turnos con recursos estables",
            "icon": "🛡️"
        }
    }
    
    @staticmethod
    def check_victory_conditions(db: Session, current_turn: int) -> Dict[str, Any]:
        """
        Verificar todas las condiciones de victoria.
        
        Returns:
            {
                "game_over": bool,
                "victory_type": Optional[str],
                "winner": Optional[Nation],
                "details": str
            }
        """
        nations = NationService.get_all(db)
        active_nations = [n for n in nations if n.is_active]
        
        # Si no hay naciones activas, es un empate (no debería pasar)
        if len(active_nations) == 0:
            return {
                "game_over": True,
                "victory_type": "draw",
                "winner": None,
                "details": "Todas las naciones han sido eliminadas. Empate técnico."
            }
        
        # 1. Victoria por Eliminación (solo queda 1 nación)
        if len(active_nations) == 1:
            winner = active_nations[0]
            return {
                "game_over": True,
                "victory_type": "elimination",
                "winner": winner,
                "details": f"{winner.name} es la última nación superviviente. ¡Victoria total!"
            }
        
        # Calcular total de territorios
        total_territories = sum(n.territories for n in active_nations)
        
        # 2. Victoria por Dominación (más del 50% de territorios)
        for nation in active_nations:
            territory_percentage = (nation.territories / total_territories * 100) if total_territories > 0 else 0
            
            if territory_percentage > 50:
                return {
                    "game_over": True,
                    "victory_type": "domination",
                    "winner": nation,
                    "details": f"{nation.name} controla {nation.territories} territorios ({territory_percentage:.1f}% del mundo)."
                }
        
        # 3. Victoria Económica (10,000 oro + 90% poder económico)
        for nation in active_nations:
            if nation.gold >= 10000 and nation.economic_power >= 90.0:
                return {
                    "game_over": True,
                    "victory_type": "economic",
                    "winner": nation,
                    "details": f"{nation.name} ha dominado la economía mundial con {nation.gold} oro y {nation.economic_power:.1f}% de poder económico."
                }
        
        # 4. Victoria Militar (2,000 tropas + 90% poder militar)
        for nation in active_nations:
            if nation.troops >= 2000 and nation.military_power >= 90.0:
                return {
                    "game_over": True,
                    "victory_type": "military",
                    "winner": nation,
                    "details": f"{nation.name} ha establecido supremacía militar con {nation.troops} tropas y {nation.military_power:.1f}% de poder militar."
                }
        
        # 5. Victoria por Supervivencia (100 turnos)
        if current_turn >= 100:
            # Determinar ganador por puntuación total
            winner = max(active_nations, key=lambda n: VictoryService._calculate_total_score(n))
            return {
                "game_over": True,
                "victory_type": "survival",
                "winner": winner,
                "details": f"Después de {current_turn} turnos, {winner.name} ha demostrado ser la nación más fuerte con {VictoryService._calculate_total_score(winner):.0f} puntos."
            }
        
        # Juego continúa
        return {
            "game_over": False,
            "victory_type": None,
            "winner": None,
            "details": ""
        }
    
    
    @staticmethod
    def _calculate_total_score(nation: Nation) -> float:
        """
        Calcular puntuación total de una nación para determinar ganador por supervivencia.
        
        Fórmula:
        - Oro: 1 punto por cada 10 oro
        - Tropas: 1 punto por tropa
        - Territorios: 200 puntos por territorio
        - Poder militar: 10 puntos por punto de poder
        - Poder económico: 10 puntos por punto de poder
        - Poder diplomático: 5 puntos por punto de poder
        """
        gold_score = nation.gold / 10
        troops_score = nation.troops
        territory_score = nation.territories * 200
        military_score = nation.military_power * 10
        economic_score = nation.economic_power * 10
        diplomatic_score = nation.diplomatic_influence * 5
        
        total = (
            gold_score +
            troops_score +
            territory_score +
            military_score +
            economic_score +
            diplomatic_score
        )
        
        return total
    
    
    @staticmethod
    def get_victory_progress(db: Session, nation: Nation, current_turn: int) -> Dict[str, Any]:
        """
        Obtener progreso hacia todas las condiciones de victoria para una nación.
        
        Returns:
            {
                "domination": {"progress": 40, "target": 50, "completed": false},
                "economic": {"progress": 45, "target": 100, "completed": false},
                ...
            }
        """
        nations = NationService.get_all(db)
        active_nations = [n for n in nations if n.is_active]
        total_territories = sum(n.territories for n in active_nations)
        
        # Progreso de dominación (% de territorios)
        domination_progress = (nation.territories / total_territories * 100) if total_territories > 0 else 0
        
        # Progreso económico (promedio de oro alcanzado y poder económico)
        economic_gold_progress = min((nation.gold / 10000) * 100, 100)
        economic_power_progress = min((nation.economic_power / 90) * 100, 100)
        economic_progress = (economic_gold_progress + economic_power_progress) / 2
        
        # Progreso militar (promedio de tropas y poder militar)
        military_troops_progress = min((nation.troops / 2000) * 100, 100)
        military_power_progress = min((nation.military_power / 90) * 100, 100)
        military_progress = (military_troops_progress + military_power_progress) / 2
        
        # Progreso de supervivencia (turnos transcurridos)
        survival_progress = min((current_turn / 100) * 100, 100)
        
        return {
            "domination": {
                "progress": round(domination_progress, 1),
                "target": 50.0,
                "completed": domination_progress > 50,
                "description": f"{nation.territories}/{total_territories} territorios"
            },
            "elimination": {
                "progress": ((8 - len(active_nations)) / 7 * 100),  # Asumiendo 8 naciones iniciales
                "target": 100.0,
                "completed": len(active_nations) == 1,
                "description": f"{len(active_nations)} naciones activas"
            },
            "economic": {
                "progress": round(economic_progress, 1),
                "target": 100.0,
                "completed": nation.gold >= 10000 and nation.economic_power >= 90,
                "description": f"{nation.gold}/10,000 oro, {nation.economic_power:.0f}/90% poder"
            },
            "military": {
                "progress": round(military_progress, 1),
                "target": 100.0,
                "completed": nation.troops >= 2000 and nation.military_power >= 90,
                "description": f"{nation.troops}/2,000 tropas, {nation.military_power:.0f}/90% poder"
            },
            "survival": {
                "progress": round(survival_progress, 1),
                "target": 100.0,
                "completed": current_turn >= 100,
                "description": f"{current_turn}/100 turnos"
            }
        }
    
    
    @staticmethod
    def get_leaderboard(db: Session) -> List[Dict[str, Any]]:
        """
        Obtener tabla de clasificación de todas las naciones activas.
        
        Returns:
            Lista ordenada por puntuación total descendente
        """
        nations = NationService.get_all(db)
        active_nations = [n for n in nations if n.is_active]
        
        leaderboard = []
        for nation in active_nations:
            score = VictoryService._calculate_total_score(nation)
            
            leaderboard.append({
                "nation_id": nation.id,
                "nation_name": nation.name,
                "total_score": int(score),
                "gold": nation.gold,
                "troops": nation.troops,
                "territories": nation.territories,
                "military_power": nation.military_power,
                "economic_power": nation.economic_power,
                "diplomatic_influence": nation.diplomatic_influence
            })
        
        # Ordenar por puntuación descendente
        leaderboard.sort(key=lambda x: x['total_score'], reverse=True)
        
        # Agregar posición
        for i, entry in enumerate(leaderboard, 1):
            entry['rank'] = i
        
        return leaderboard
