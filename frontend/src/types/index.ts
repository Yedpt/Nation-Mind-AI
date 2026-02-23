// Types para Nation-Mind AI Frontend

export interface Nation {
  id: number;
  name: string;
  personality: 'aggressive' | 'diplomatic' | 'defensive' | 'expansionist' | 'neutral';
  gold: number;
  troops: number;
  territories: number;
  military_power: number;
  economic_power: number;
  diplomatic_power: number;
  objectives: string[];
  ai_controlled: boolean;
  is_active: boolean;
  is_eliminated: boolean;
}

export interface AvailableNation {
  code: string;
  name: string;
  personality: string;
  military_power: number;
  economic_power: number;
  diplomatic_power: number;
  recommended: boolean;
  description: string;
}

export interface Relation {
  id: number;
  nation_a_id: number;
  nation_b_id: number;
  status: 'allied' | 'neutral' | 'war' | 'trade_agreement';
  relationship_score: number;
  with_nation_id?: number;
}

export interface Battle {
  id: number;
  turn_number: number;
  attacker_id: number;
  defender_id: number;
  winner_id: number;
  battle_type: 'skirmish' | 'battle' | 'total_war';
  attacker_troops_initial: number;
  defender_troops_initial: number;
  attacker_power: number;
  defender_power: number;
  attacker_allies: number[];
  defender_allies: number[];
  attacker_bonus: number;
  defender_bonus: number;
  attacker_casualties: number;
  defender_casualties: number;
  territories_conquered: number;
  gold_looted: number;
  attacker_win_chance: number;
  defender_win_chance: number;
  is_decisive: boolean;
  description: string;
  created_at: string;
}

export interface Event {
  id: number;
  turn_id: number;
  turn_number: number;
  nation_id: number;
  event_type: string;
  title?: string;
  description: string;
  importance: number;
  data?: Record<string, unknown>;
  battle_casualties?: number;
  created_at: string;
}

export interface VictoryProgress {
  domination: {
    progress: number;
    target: number;
    completed: boolean;
    description: string;
  };
  elimination: {
    progress: number;
    target: number;
    completed: boolean;
    description: string;
  };
  economic: {
    progress: number;
    target: number;
    completed: boolean;
    description: string;
  };
  military: {
    progress: number;
    target: number;
    completed: boolean;
    description: string;
  };
  survival: {
    progress: number;
    target: number;
    completed: boolean;
    description: string;
  };
}

export interface GameState {
  current_turn: number;
  nations: Nation[];
  recent_events: Event[];
  is_game_over: boolean;
  winner?: string | null;
  victory_type?: string | null;
  victory_progress?: VictoryProgress | null;
  player_nation_id?: number | null;
}

export interface BattleSimulation {
  attacker_win_chance: number;
  defender_win_chance: number;
  attacker_expected_casualties: number;
  defender_expected_casualties: number;
  expected_territories: number;
  expected_gold: number;
  recommendation: 'attack' | 'risky' | 'avoid';
  factors: {
    attacker_allies: number;
    defender_allies: number;
    attacker_bonus: string;
    defender_bonus: string;
    troop_ratio: number;
  };
}

export interface ApiResponse<T> {
  message?: string;
  success?: boolean;
  data?: T;
}

export interface Turn {
  id: number;
  turn_number: number;
  world_state: Record<string, unknown>;
  summary: string;
  created_at: string;
}
