import { apiClient } from './client';

export const riskApi = {
  getHeatmap: async () => {
    const { data } = await apiClient.get('/risk/heatmap');
    return data;
  },
  
  getSurges: async () => {
    const { data } = await apiClient.get('/risk/surges');
    return data;
  },
  
  getForecast: async (wardId: string, days: number = 5) => {
    const { data } = await apiClient.get(`/forecast/${wardId}?days=${days}`);
    return data;
  },
  
  // Exposing alerts here for convenience in the prototype
  getAlertsHistory: async () => {
    const { data } = await apiClient.get('/alerts/history');
    return data;
  }
};
