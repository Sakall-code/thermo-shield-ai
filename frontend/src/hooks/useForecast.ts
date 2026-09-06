import { useQuery } from '@tanstack/react-query';
import { riskApi } from '../api/riskApi';

// STUB: We are skipping useLiveAlerts.ts (Server-Sent Events) for the prototype.
// Polling every 60s via useForecast (or other react-query hooks) is enough.
// In the full build, replace this polling approach with SSE or WebSockets for live alerts.

export const useForecast = (wardId: string | null, days: number = 5) => {
  return useQuery({
    queryKey: ['forecast', wardId, days],
    queryFn: () => riskApi.getForecast(wardId!, days),
    enabled: !!wardId,
    refetchInterval: 60000, // Poll every 60 seconds
  });
};
