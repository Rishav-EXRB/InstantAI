
import React from 'react';
import { 
  LayoutDashboard, 
  Users, 
  BarChart3, 
  Heart, 
  Box, 
  Target, 
  MessageSquare, 
  Link2 
} from 'lucide-react';
import { AppType } from './types';

export const NAVIGATION_ITEMS = [
  { id: AppType.DASHBOARD, label: 'Overview', icon: <LayoutDashboard size={20} /> },
  { id: AppType.COMMUNITY, label: 'Digital Twin', icon: <Users size={20} /> },
  { id: AppType.RANKING, label: 'Ranking', icon: <BarChart3 size={20} /> },
  { id: AppType.GRATITUDE, label: 'Gratitude', icon: <Heart size={20} /> },
  { id: AppType.INVENTORY, label: 'Inventory', icon: <Box size={20} /> },
  { id: AppType.GOALS, label: 'Goals', icon: <Target size={20} /> },
  { id: AppType.MESSAGES, label: 'Messages', icon: <MessageSquare size={20} /> },
  { id: AppType.CONNECTORS, label: 'Connectors', icon: <Link2 size={20} /> },
];

export const MOCK_METRICS = [
  { id: 'm1', name: 'Total Revenue', value: 1245000, change: 12.5, trend: 'up', definition: 'Total gross sales across all channels.' },
  { id: 'm2', name: 'Member Retention', value: 88.2, change: -2.1, trend: 'down', definition: 'Percentage of members active in the last 30 days.' },
  { id: 'm3', name: 'Inventory Health', value: 94.5, change: 0.8, trend: 'up', definition: 'Percentage of SKUs within optimal stock levels.' },
  { id: 'm4', name: 'Goal Pacing', value: 72.1, change: 5.4, trend: 'up', definition: 'Current progress towards quarterly targets.' },
];

export const SYSTEM_INSTRUCTION = `
You are the InstantAI Analyst, an expert in business domain context. 
Your goal is to help users investigate their business data through 4 key actions:
1. Understand intent (rank, why, compare, forecast).
2. Ground in data (refer to metrics like Revenue, Margin, Retention).
3. Surface insights (anomalies, trends).
4. Enable investigation (provide drill-down suggestions).

Always provide evidence for your claims. If asked about a metric, define it based on our semantic catalog.
`;
