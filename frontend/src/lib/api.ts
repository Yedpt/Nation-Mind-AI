// Cliente API para Nation-Mind AI Backend
import axios from 'axios';
import type {
  Nation,
  AvailableNation,
  ApiResponse,
  GameState,
  Battle,
  BattleSimulation,
  Event,
  Relation,
  Turn
} from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ==================== HEALTH & STATUS ====================

export const healthCheck = async () => {
  const response = await api.get('/api/health');
  return response.data;
};

// ==================== GAME ====================

export const getAvailableNations = async (): Promise<{
  available_nations: AvailableNation[];
  default: string;
  default_name: string;
}> => {
  const response = await api.get('/api/game/available-nations');
  return response.data;
};

export const initializeGame = async (playerNation: string = 'ESP', forceReset: boolean = true): Promise<ApiResponse<{
  message: string;
  turn_number: number;
  nations_created: number;
  player_nation: Nation;
}>> => {
  console.log('==========================================');
  console.log('📡 API.TS - initializeGame LLAMADO');
  console.log('📡 Parámetro recibido:', playerNation);
  console.log('📡 Force Reset:', forceReset);
  console.log('📡 Tipo:', typeof playerNation);
  console.log('📡 Length:', playerNation.length);
  
  // Usar params en lugar de query string manual
  const response = await api.post('/api/game/initialize', null, {
    params: { 
      player_nation: playerNation,
      force_reset: forceReset
    }
  });
  
  console.log('✅ Respuesta recibida:', response.status);
  console.log('==========================================');
  
  return response.data;
};

export const getGameState = async (): Promise<GameState> => {
  const response = await api.get('/api/game/state');
  return response.data;
};

// Player Actions
export interface PlayerAction {
  action_type: 'attack' | 'alliance' | 'trade' | 'recruit' | 'build' | 'invest_economy' | 'invest_military' | 'peace_treaty';
  target_nation_id?: number;
  data?: Record<string, any>;
}

export const executePlayerAction = async (
  nationId: number,
  action: PlayerAction
): Promise<ApiResponse<{ message: string; success: boolean }>> => {
  const response = await api.post('/api/game/action', action, {
    params: { nation_id: nationId }
  });
  return response.data;
};

// ==================== NATIONS ====================

export const getAllNations = async (): Promise<Nation[]> => {
  const response = await api.get('/api/nations');
  return response.data;
};

export const getNationById = async (id: number): Promise<Nation> => {
  const response = await api.get(`/api/nations/${id}`);
  return response.data;
};

export const getPlayerNation = async (): Promise<Nation> => {
  const response = await api.get('/api/nations/player');
  return response.data;
};

export const getAINations = async (): Promise<Nation[]> => {
  const response = await api.get('/api/nations/ai');
  return response.data;
};

// ==================== RELATIONS ====================

export const getAllRelations = async (): Promise<Relation[]> => {
  const response = await api.get('/api/relations');
  return response.data;
};

export const getNationRelations = async (nationId: number): Promise<Relation[]> => {
  const response = await api.get(`/api/relations/nation/${nationId}`);
  return response.data;
};

export const proposeAlliance = async (nationId: number, targetId: number) => {
  const response = await api.post('/api/relations/propose-alliance', {
    nation_id: nationId,
    target_nation_id: targetId
  });
  return response.data;
};

// ==================== BATTLES ====================

export const resolveBattle = async (
  attackerId: number,
  defenderId: number,
  turnNumber: number
): Promise<Battle> => {
  const response = await api.post('/api/battles/resolve', null, {
    params: { attacker_id: attackerId, defender_id: defenderId, turn_number: turnNumber }
  });
  return response.data;
};

export const simulateBattle = async (
  attackerId: number,
  defenderId: number
): Promise<BattleSimulation> => {
  const response = await api.post('/api/battles/simulate', {
    attacker_id: attackerId,
    defender_id: defenderId,
    include_allies: true
  });
  return response.data;
};

export const getBattleHistory = async (limit: number = 20): Promise<Battle[]> => {
  const response = await api.get(`/api/battles/history?limit=${limit}`);
  return response.data;
};

export const getNationBattles = async (nationId: number): Promise<Battle[]> => {
  const response = await api.get(`/api/battles/nation/${nationId}`);
  return response.data;
};

export const getActiveWars = async (): Promise<{
  active_wars: Array<{
    nation_a: string;
    nation_b: string;
    relationship_score: number;
    nation_a_id: number;
    nation_b_id: number;
  }>;
  total: number;
}> => {
  const response = await api.get('/api/battles/active-wars');
  return response.data;
};

// ==================== EVENTS ====================

export const getRecentEvents = async (limit: number = 20): Promise<Event[]> => {
  const response = await api.get(`/api/events/recent?limit=${limit}`);
  return response.data;
};

export const getNationEvents = async (nationId: number): Promise<Event[]> => {
  const response = await api.get(`/api/events/nation/${nationId}`);
  return response.data;
};

// ==================== TURNS ====================

export const getCurrentTurn = async (): Promise<Turn> => {
  const response = await api.get('/api/turns/current');
  return response.data;
};

export const advanceTurn = async (): Promise<ApiResponse<Turn>> => {
  const response = await api.post('/api/turns/advance');
  return response.data;
};

// ==================== AGENTS ====================

export const processAgentTurn = async (): Promise<{
  message: string;
  turn_number: number;
  decisions: Array<{
    nation: string;
    action: string;
    success: boolean;
    details: any;
  }>;
}> => {
  const response = await api.post('/api/agents/process-turn');
  return response.data;
};

export const getAgentsStatus = async () => {
  const response = await api.get('/api/agents/status');
  return response.data;
};

// ==================== MEMORY (RAG) ====================

export const queryMemory = async (query: string, limit: number = 5) => {
  const response = await api.post('/api/memory/query', { query, limit });
  return response.data;
};

export default api;