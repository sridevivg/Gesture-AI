import axios from 'axios';
import { ActionMapping, GestureDefinition, SystemHealth } from '@/types';

const apiBaseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: `${apiBaseUrl}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 5000,
});

export const apiService = {
  async getHealth(): Promise<SystemHealth> {
    const response = await apiClient.get<SystemHealth>('/health');
    return response.data;
  },

  async getGestures(): Promise<GestureDefinition[]> {
    const response = await apiClient.get<GestureDefinition[]>('/gestures');
    return response.data;
  },

  async getActionMappings(): Promise<ActionMapping[]> {
    const response = await apiClient.get<ActionMapping[]>('/actions/mappings');
    return response.data;
  },
};
