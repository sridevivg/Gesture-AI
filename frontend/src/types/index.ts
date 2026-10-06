import { z } from 'zod';

export interface LandmarkPoint {
  x: number;
  y: number;
  z: number;
}

export interface GestureDefinition {
  id: string;
  name: string;
  category: 'static' | 'dynamic';
  description?: string;
  min_confidence: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ActionMapping {
  id: string;
  gesture_id: string;
  action_type: string;
  action_payload: Record<string, unknown>;
  is_enabled: boolean;
  cooldown_seconds: number;
  created_at: string;
  updated_at: string;
}

export interface GestureStreamEvent {
  type: string;
  timestamp: number;
  gesture: string;
  confidence: number;
  category: 'static' | 'dynamic';
  action?: {
    executed: boolean;
    action_type?: string;
    status: string;
  } | null;
}

export interface SystemHealth {
  status: string;
  timestamp: string;
  version: string;
  environment: string;
  services: {
    api: string;
    ml_inference: string;
    action_execution: string;
  };
}

export const GestureCreateSchema = z.object({
  name: z.string().min(2).max(64),
  category: z.enum(['static', 'dynamic']),
  description: z.string().optional(),
  min_confidence: z.number().min(0).max(1).default(0.8),
  is_active: z.boolean().default(true),
});

export type GestureCreateInput = z.infer<typeof GestureCreateSchema>;
