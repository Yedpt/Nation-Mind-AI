"""
Servicio de Agentes IA con LangGraph
Gestiona la toma de decisiones de las naciones controladas por IA
"""
from typing import TypedDict, List, Dict, Any, Optional
from sqlalchemy.orm import Session
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from ..config import settings
from .nation_service import NationService
from .rag_service import get_rag_service
from .agent_tools import (
    get_my_nation_status,
    get_all_nations_status,
    get_relations_status,
    propose_alliance,
    declare_war,
    invest_in_military,
    invest_in_economy,
    do_nothing
)


# ==================== ESTADO DEL AGENTE ====================

class AgentState(TypedDict):
    """Estado compartido del agente durante su procesamiento"""
    nation_id: int
    nation_name: str
    personality: str
    current_status: Dict[str, Any]
    world_status: List[Dict[str, Any]]
    relations: List[Dict[str, Any]]
    historical_context: str
    messages: List
    decision: Optional[Dict[str, Any]]
    turn_number: int


# ==================== SERVICIO DE AGENTES ====================

class AgentService:
    """
    Servicio para gestionar agentes IA de naciones
    
    Cada nación IA es un agente autónomo que:
    1. Analiza su situación actual
    2. Consulta su memoria histórica (RAG)
    3. Decide qué acción tomar
    4. Ejecuta la acción usando herramientas
    """
    
    def __init__(self):
        """Inicializar el servicio de agentes"""
        # LLM para los agentes (Groq con Llama)
        self.llm = ChatGroq(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            api_key=settings.GROQ_API_KEY
        )
        
        # Servicio RAG para memoria
        self.rag = get_rag_service()
        
        print("✅ Agent Service inicializado")
        print(f"🤖 Modelo: {settings.LLM_MODEL}")
    
    
    def create_agent_for_nation(self, nation_id: int, db: Session) -> StateGraph:
        """
        Crear un grafo de decisión (agente) para una nación específica.
        
        Args:
            nation_id: ID de la nación
            db: Sesión de base de datos
            
        Returns:
            StateGraph: Grafo compilado del agente
        """
        nation = NationService.get_by_id(db, nation_id)
        if not nation:
            raise ValueError(f"Nación {nation_id} no encontrada")
        
        # Definir el grafo de estados
        workflow = StateGraph(AgentState)
        
        # Nodos del grafo
        workflow.add_node("gather_info", lambda state: self._gather_information(state, db))
        workflow.add_node("think", lambda state: self._think_and_decide(state, db))
        workflow.add_node("act", lambda state: self._execute_action(state, db))
        
        # Flujo: gather_info → think → act → END
        workflow.set_entry_point("gather_info")
        workflow.add_edge("gather_info", "think")
        workflow.add_edge("think", "act")
        workflow.add_edge("act", END)
        
        return workflow.compile()
    
    
    def _gather_information(self, state: AgentState, db: Session) -> AgentState:
        """
        Paso 1: Recopilar información del mundo y memoria histórica.
        
        Args:
            state: Estado actual del agente
            db: Sesión de base de datos
            
        Returns:
            AgentState: Estado actualizado con información
        """
        nation_id = state["nation_id"]
        
        # Obtener estado de mi nación
        my_status = get_my_nation_status.invoke({
            "nation_id": nation_id,
            "db": db
        })
        
        # Obtener estado de todas las naciones
        world_status = get_all_nations_status.invoke({"db": db})
        
        # Obtener relaciones diplomáticas
        relations = get_relations_status.invoke({
            "nation_id": nation_id,
            "db": db
        })
        
        # Obtener contexto histórico desde RAG
        situation_query = f"Situación de {state['nation_name']}: evaluando opciones estratégicas"
        historical_context = self.rag.get_context_for_agent(
            nation_id=nation_id,
            current_situation=situation_query,
            max_events=5
        )
        
        # Actualizar estado
        state["current_status"] = my_status
        state["world_status"] = world_status
        state["relations"] = relations
        state["historical_context"] = historical_context
        
        return state
    
    
    def _think_and_decide(self, state: AgentState, db: Session) -> AgentState:
        """
        Paso 2: Analizar información y decidir qué acción tomar.
        
        Args:
            state: Estado con información recopilada
            db: Sesión de base de datos
            
        Returns:
            AgentState: Estado con decisión tomada
        """
        # Construir prompt basado en personalidad
        system_prompt = self._get_personality_prompt(state["personality"])
        
        # Construir contexto completo
        context = f"""
# Turno {state['turn_number']}

## Tu Nación: {state['nation_name']}
- Oro: {state['current_status'].get('gold', 0)}
- Tropas: {state['current_status'].get('troops', 0)}
- Territorios: {state['current_status'].get('territories', 0)}
- Poder Militar: {state['current_status'].get('military_power', 0)}/100
- Poder Económico: {state['current_status'].get('economic_power', 0)}/100

## Otras Naciones:
{self._format_nations_info(state['world_status'], state['nation_id'])}

## Tus Relaciones Diplomáticas:
{self._format_relations_info(state['relations'])}

{state['historical_context']}

## Acciones Disponibles:
1. **propose_alliance**: Proponer alianza a otra nación
   - Params: {{"target_nation_id": <int>, "message": "<string>"}}
   - Ejemplo: {{"action": "propose_alliance", "params": {{"target_nation_id": 3, "message": "We seek peace"}}}}

2. **declare_war**: Declarar guerra (requiere min. 50 tropas)
   - Params: {{"target_nation_id": <int>, "reason": "<string>"}}
   - Ejemplo: {{"action": "declare_war", "params": {{"target_nation_id": 5, "reason": "Territorial dispute"}}}}

3. **invest_in_military**: Invertir oro en tropas (min. 10 oro)
   - Params: {{"amount": <int>}}
   - Ejemplo: {{"action": "invest_in_military", "params": {{"amount": 100}}}}

4. **invest_in_economy**: Invertir oro en economía (min. 20 oro)
   - Params: {{"amount": <int>}}
   - Ejemplo: {{"action": "invest_in_economy", "params": {{"amount": 200}}}}

5. **do_nothing**: Mantener status quo y desarrollar internamente
   - Params: {{}}
   - Ejemplo: {{"action": "do_nothing", "params": {{}}}}

Basándote en tu personalidad ({state['personality']}), tu situación actual y el contexto histórico, 
¿qué acción tomarás este turno?

IMPORTANTE: Usa los nombres de parámetros EXACTOS especificados arriba (target_nation_id, message, reason, amount).

Responde SOLO con un JSON en este formato:
{{
    "action": "nombre_accion",
    "params": {{"param1": valor1, "param2": "valor2"}},
    "reasoning": "breve explicación de tu decisión"
}}
"""
        
        # Llamar al LLM
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=context)
        ]
        
        try:
            response = self.llm.invoke(messages)
            decision_text = response.content
            
            # Parsear decisión (asumiendo formato JSON)
            import json
            # Extraer JSON del texto (puede venir con texto adicional)
            json_start = decision_text.find('{')
            json_end = decision_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                decision_json = decision_text[json_start:json_end]
                decision = json.loads(decision_json)
            else:
                # Si no hay JSON, acción por defecto
                decision = {
                    "action": "do_nothing",
                    "params": {},
                    "reasoning": "No se pudo determinar una acción clara"
                }
            
            state["decision"] = decision
            state["messages"] = messages + [response]
            
        except Exception as e:
            print(f"❌ Error en decisión del agente: {e}")
            # Acción por defecto en caso de error
            state["decision"] = {
                "action": "do_nothing",
                "params": {},
                "reasoning": f"Error: {str(e)}"
            }
        
        return state
    
    
    def _execute_action(self, state: AgentState, db: Session) -> AgentState:
        """
        Paso 3: Ejecutar la acción decidida.
        
        Args:
            state: Estado con decisión tomada
            db: Sesión de base de datos
            
        Returns:
            AgentState: Estado final con resultado de la acción
        """
        decision = state["decision"]
        action_name = decision.get("action", "do_nothing")
        params = decision.get("params", {})
        
        # Añadir nation_id y db a los params
        params["nation_id"] = state["nation_id"]
        params["db"] = db
        
        # Mapeo de acciones a funciones
        actions_map = {
            "propose_alliance": propose_alliance,
            "declare_war": declare_war,
            "invest_in_military": invest_in_military,
            "invest_in_economy": invest_in_economy,
            "do_nothing": do_nothing
        }
        
        # Ejecutar acción
        action_func = actions_map.get(action_name, do_nothing)
        
        try:
            result = action_func.invoke(params)
            print(f"✅ {state['nation_name']}: {action_name} - {result.get('message', 'OK')}")
            state["decision"]["result"] = result
        except Exception as e:
            print(f"❌ Error ejecutando {action_name}: {e}")
            state["decision"]["result"] = {"success": False, "message": str(e)}
        
        return state
    
    
    def _get_personality_prompt(self, personality: str) -> str:
        """Obtener prompt del sistema basado en la personalidad de la nación"""
        personalities = {
            "aggressive": """Eres un líder AGRESIVO y expansionista. 
Priorizas la conquista militar y dominio territorial. 
⚔️ ANTES de declarar guerra, SIEMPRE simula la batalla con simulate_battle().
Solo declara guerra si tienes >60% probabilidad de victoria o tienes aliados fuertes.
Considera: buscar aliados antes de atacar naciones poderosas.""",
            
            "diplomatic": """Eres un líder DIPLOMÁTICO y pacificador.
Priorizas las alianzas y las relaciones pacíficas.
🕊️ Evita la guerra a toda costa. Usa herramientas: propose_trade_agreement, request_peace_treaty, organize_diplomatic_summit.
Si hay guerra, busca la paz inmediatamente. Fortalece alianzas y comercio.
Solo considera guerra en defensa propia.""",
            
            "defensive": """Eres un líder DEFENSIVO y cauteloso.
Priorizas la seguridad y estabilidad de tu nación.
🛡️ Invierte en militar para disuadir ataques. Forma alianzas defensivas.
NO inicies guerras. Si te atacan, pide ayuda a aliados.
Usa diplomacia y comercio para mantener relaciones estables.""",
            
            "expansionist": """Eres un líder EXPANSIONISTA y oportunista estratégico.
Priorizas el crecimiento económico, territorial y diplomático.
📈 Preferentemente usa comercio (propose_trade_agreement) y diplomacia (organize_diplomatic_summit).
Solo usa guerra si la simulación muestra victoria fácil (>70%).
Equilibra: 60% economía/diplomacia, 40% militar.""",
            
            "neutral": """Eres un líder EQUILIBRADO y pragmático.
Evalúas cada situación objetivamente y tomas la decisión más beneficiosa.
⚖️ Usa todas las herramientas disponibles según el contexto:
- Comercio para mejorar economía y relaciones
- Diplomacia para resolver conflictos
- Alianzas para seguridad mutua
- Militar solo cuando sea estratégicamente necesario (simulación >65% victoria)
Prioriza el desarrollo integral de tu nación."""
        }
        
        return personalities.get(personality, personalities["neutral"])
    
    
    def _format_nations_info(self, nations: List[Dict], exclude_id: int) -> str:
        """Formatear información de naciones para el prompt"""
        lines = []
        for nation in nations:
            if nation["id"] == exclude_id:
                continue
            lines.append(
                f"- **{nation['name']}**: {nation['troops']} tropas, "
                f"{nation['territories']} territorios, "
                f"poder militar {nation['military_power']}/100"
            )
        return "\n".join(lines) if lines else "No hay otras naciones activas"
    
    
    def _format_relations_info(self, relations: List[Dict]) -> str:
        """Formatear información de relaciones para el prompt"""
        if not relations:
            return "Sin relaciones diplomáticas establecidas"
        
        lines = []
        for rel in relations:
            status_emoji = {
                "allied": "🤝 Aliado",
                "neutral": "😐 Neutral",
                "war": "⚔️ EN GUERRA",
                "trade_agreement": "💰 Acuerdo Comercial"
            }.get(rel["status"], rel["status"])
            
            lines.append(
                f"- Nación {rel['with_nation_id']}: {status_emoji} "
                f"(score: {rel['relationship_score']})"
            )
        return "\n".join(lines)
    
    
    def process_ai_turn(self, db: Session, turn_number: int) -> List[Dict[str, Any]]:
        """
        Procesar el turno de todas las naciones IA.
        
        Flujo completo de turno:
        1. Generar ingresos económicos para todas las naciones
        2. Procesar decisiones de agentes IA
        3. Resolver batallas activas
        4. Verificar condiciones de victoria
        5. Crear siguiente turno
        
        Args:
            db: Sesión de base de datos
            turn_number: Número del turno actual
            
        Returns:
            list: Lista con las decisiones y resultados de cada agente
        """
        from .turn_service import TurnService
        from .game_service import GameService
        from .economy_service import EconomyService
        from .battle_service import BattleService
        from .victory_service import VictoryService
        
        current_turn = TurnService.get_current(db)
        turn_id = current_turn.id if current_turn else 1
        
        # ========== FASE 1: ECONOMÍA ==========
        print(f"\n💰 Generando ingresos del turno {turn_number}...")
        economy_results = EconomyService.process_turn_income(db, turn_id)
        
        total_income = sum(r['income'] for r in economy_results)
        total_maintenance = sum(r['maintenance'] for r in economy_results)
        print(f"✅ Ingreso total: {total_income} oro | Mantenimiento: {total_maintenance} oro")
        
        # ========== FASE 2: AGENTES IA ==========
        # Obtener todas las naciones controladas por IA
        all_nations = NationService.get_all(db)
        ai_nations = [n for n in all_nations if n.ai_controlled and n.is_active]
        
        if not ai_nations:
            return []
        
        print(f"\n🤖 Procesando turn {turn_number} para {len(ai_nations)} agentes IA...")
        
        results = []
        
        # Procesar cada agente secuencialmente
        for nation in ai_nations:
            print(f"\n--- {nation.name} ({nation.personality}) ---")
            
            # Crear agente
            agent_graph = self.create_agent_for_nation(nation.id, db)
            
            # Estado inicial
            initial_state: AgentState = {
                "nation_id": nation.id,
                "nation_name": nation.name,
                "personality": nation.personality,
                "current_status": {},
                "world_status": [],
                "relations": [],
                "historical_context": "",
                "messages": [],
                "decision": None,
                "turn_number": turn_number
            }
            
            # Ejecutar agente
            try:
                final_state = agent_graph.invoke(initial_state)
                
                # Extraer solo los datos serializables
                decision = final_state.get("decision", {})
                results.append({
                    "nation_id": nation.id,
                    "nation_name": nation.name,
                    "action": decision.get("action"),
                    "reasoning": decision.get("reasoning"),
                    "result": decision.get("result", {}),
                    "success": True
                })
                
            except Exception as e:
                print(f"❌ Error procesando {nation.name}: {e}")
                results.append({
                    "nation_id": nation.id,
                    "nation_name": nation.name,
                    "error": str(e),
                    "success": False
                })
        
        print(f"\n✅ Turno {turn_number} completado: {len(results)} agentes procesados")
        
        # ========== FASE 3: BATALLAS ==========
        print(f"\n⚔️ Resolviendo batallas activas...")
        battles_resolved = BattleService.resolve_active_wars(db, turn_number)
        if battles_resolved:
            print(f"✅ {len(battles_resolved)} batallas resueltas")
            for battle in battles_resolved:
                winner_name = battle.get('winner_name', 'Desconocido')
                loser_name = battle.get('loser_name', 'Desconocido')
                print(f"   🏆 {winner_name} derrotó a {loser_name}")
        else:
            print("   ℹ️  No hay guerras activas")
        
        # ========== FASE 4: VERIFICAR VICTORIA ==========
        victory_check = VictoryService.check_victory_conditions(db, turn_number)
        if victory_check["game_over"]:
            winner = victory_check.get("winner")
            victory_type = victory_check.get("victory_type")
            print(f"\n🏆 ¡JUEGO TERMINADO! Victoria por {victory_type}")
            if winner:
                print(f"   👑 Ganador: {winner.name}")
                print(f"   📝 {victory_check['details']}")
        
        # ========== FASE 5: CREAR SIGUIENTE TURNO ==========
        print(f"\n📅 Creando turno {turn_number + 1}...")
        try:
            # Obtener estado del mundo actualizado
            world_state = GameService.get_game_state(db)
            
            # Crear resumen del turno
            actions_summary = []
            for r in results:
                if r.get("success"):
                    actions_summary.append(f"{r['nation_name']}: {r['action']}")
            
            summary = f"Turno {turn_number}: " + "; ".join(actions_summary[:5])
            if len(actions_summary) > 5:
                summary += f" y {len(actions_summary) - 5} acciones más."
            
            # Crear siguiente turno
            TurnService.create_next_turn(
                db,
                world_state=world_state,
                summary=summary
            )
            print(f"✅ Turno {turn_number + 1} creado exitosamente")
            
        except Exception as e:
            print(f"❌ Error creando siguiente turno: {e}")
        
        return results


# ==================== INSTANCIA GLOBAL ====================

_agent_service_instance = None

def get_agent_service() -> AgentService:
    """
    Obtener instancia singleton del Agent Service.
    
    Returns:
        AgentService: Instancia compartida
    """
    global _agent_service_instance
    if _agent_service_instance is None:
        _agent_service_instance = AgentService()
    return _agent_service_instance
