import { apiClient } from './client';

export const wardsApi = {
  getAllWards: async () => {
    const { data } = await apiClient.get('/wards');
    return data;
  },
  
  getWardGeometry: async (wardId: string) => {
    const { data } = await apiClient.get(`/wards/${wardId}/geometry`);
    return data;
  },
};
