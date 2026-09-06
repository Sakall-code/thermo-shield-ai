import { useQuery } from '@tanstack/react-query';
import { wardsApi } from '../api/wardsApi';

export const useWardData = () => {
  return useQuery({
    queryKey: ['wards'],
    queryFn: wardsApi.getAllWards,
  });
};

export const useWardGeometry = (wardId: string | null) => {
  return useQuery({
    queryKey: ['wardGeometry', wardId],
    queryFn: () => wardsApi.getWardGeometry(wardId!),
    enabled: !!wardId,
  });
};
