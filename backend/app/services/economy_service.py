"""
Servicio de Economía
Gestiona generación de ingresos, costos y balance económico
"""
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import random

from ..models.nation import Nation
from .nation_service import NationService
from .event_service import EventService
from ..schemas.event_schema import EventCreate


class EconomyService:
    """Servicio para manejar la economía del juego"""
    
    @staticmethod
    def calculate_income(nation: Nation) -> int:
        """
        Calcular ingreso de oro por turno para una nación.
        
        Fórmula:
        - Ingreso base: 100 oro
        - Bonus territorios: 50 oro por territorio
        - Bonus poder económico: (poder_económico / 100) * 300
        - Variabilidad: ±10%
        
        Ejemplo:
        - 5 territorios = 250 oro
        - 80% poder económico = 240 oro
        - Base = 100 oro
        - Total = 590 oro (±59)
        """
        # Ingreso base
        base_income = 100
        
        # Bonus por territorios (50 oro cada uno)
        territory_income = nation.territories * 50
        
        # Bonus por poder económico (0-300 oro según 0-100%)
        economic_bonus = int((nation.economic_power / 100.0) * 300)
        
        # Total antes de variabilidad
        total_income = base_income + territory_income + economic_bonus
        
        # Añadir variabilidad ±10%
        variability = random.uniform(0.9, 1.1)
        final_income = int(total_income * variability)
        
        return max(50, final_income)  # Mínimo 50 oro por turno
    
    
    @staticmethod
    def calculate_maintenance_cost(nation: Nation) -> int:
        """
        Calcular costo de mantenimiento por turno.
        
        Fórmula:
        - Costo por tropa: 1 oro cada 10 tropas
        - Costo base fijo: 20 oro
        
        Ejemplo:
        - 500 tropas = 50 oro
        - Base = 20 oro
        - Total = 70 oro
        """
        troops_cost = int(nation.troops / 10)
        base_cost = 20
        
        total_cost = troops_cost + base_cost
        
        return max(0, total_cost)
    
    
    @staticmethod
    def process_turn_income(db: Session, turn_id: int) -> List[Dict[str, Any]]:
        """
        Procesar ingresos y gastos de todas las naciones activas.
        
        Returns:
            Lista de resultados con gold_gained, gold_spent, net_change por nación
        """
        nations = NationService.get_all(db)
        results = []
        
        for nation in nations:
            if not nation.is_active:
                continue
            
            # Calcular ingresos
            income = EconomyService.calculate_income(nation)
            
            # Calcular gastos
            maintenance = EconomyService.calculate_maintenance_cost(nation)
            
            # Cambio neto
            net_change = income - maintenance
            
            # Actualizar oro de la nación
            NationService.update_resources(db, nation.id, gold_change=net_change)
            
            # Crear evento si el cambio es significativo
            if abs(net_change) >= 50:
                importance = 3 if net_change > 0 else 4
                event_desc = (
                    f"{nation.name} generó {income} oro (mantenimiento: {maintenance}). "
                    f"Balance: {'+' if net_change > 0 else ''}{net_change} oro"
                )
                
                event_data = EventCreate(
                    turn_id=turn_id,
                    nation_id=nation.id,
                    event_type="economic_report",
                    description=event_desc,
                    data={
                        "income": income,
                        "maintenance": maintenance,
                        "net_change": net_change
                    },
                    importance=importance
                )
                EventService.create(db, event_data)
            
            results.append({
                "nation_id": nation.id,
                "nation_name": nation.name,
                "income": income,
                "maintenance": maintenance,
                "net_change": net_change,
                "total_gold": nation.gold + net_change
            })
        
        return results
    
    
    @staticmethod
    def can_afford(nation: Nation, cost: int) -> bool:
        """Verificar si una nación puede pagar un costo"""
        return nation.gold >= cost
    
    
    @staticmethod
    def get_economic_rank(db: Session) -> List[Dict[str, Any]]:
        """
        Obtener ranking económico de todas las naciones.
        
        Returns:
            Lista ordenada por riqueza total (gold + economic_power)
        """
        nations = NationService.get_all(db)
        
        rankings = []
        for nation in nations:
            if not nation.is_active:
                continue
            
            # "Riqueza total" = oro actual + poder económico como indicador
            total_wealth = nation.gold + (nation.economic_power * 10)
            
            rankings.append({
                "nation_id": nation.id,
                "nation_name": nation.name,
                "gold": nation.gold,
                "economic_power": nation.economic_power,
                "total_wealth": int(total_wealth),
                "territories": nation.territories
            })
        
        # Ordenar por riqueza total descendente
        rankings.sort(key=lambda x: x['total_wealth'], reverse=True)
        
        return rankings
