export const getRiskColor = (riskLevel: string): string => {
  switch (riskLevel.toUpperCase()) {
    case 'NORMAL':
      return '#22c55e'; // Green
    case 'YELLOW':
      return '#eab308'; // Yellow
    case 'ORANGE':
      return '#f97316'; // Orange
    case 'RED':
      return '#ef4444'; // Red
    default:
      return '#9ca3af'; // Gray fallback
  }
};
