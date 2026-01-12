
export enum AppType {
  DASHBOARD = 'DASHBOARD',
  COMMUNITY = 'COMMUNITY',
  RANKING = 'RANKING',
  GRATITUDE = 'GRATITUDE',
  INVENTORY = 'INVENTORY',
  GOALS = 'GOALS',
  MESSAGES = 'MESSAGES',
  CONNECTORS = 'CONNECTORS',
  PROFILE = "PROFILE"
}

export interface Metric {
  id: string;
  name: string;
  value: number;
  change: number;
  trend: 'up' | 'down' | 'neutral';
  definition: string;
}

export interface Insight {
  id: string;
  type: 'anomaly' | 'trend' | 'recommendation';
  severity: 'high' | 'medium' | 'low';
  summary: string;
  evidence: string;
  actions: string[];
}

export interface RankingEntity {
  id: string;
  name: string;
  score: number;
  metrics: Record<string, number>;
  rank: number;
}

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: number;
}

export interface UserProfile {
  name: string;
  designation: string;
  authLevel: string;
  avatar?: string;
}
