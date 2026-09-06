import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { riskApi } from '../../api/riskApi';
import { useForecast } from '../../hooks/useForecast';

interface WardPopupProps {
  wardId: string;
  wardName: string;
}

export const WardPopupContent: React.FC<WardPopupProps> = ({ wardId, wardName }) => {
  // Fetch only today's forecast for the popup metrics
  const { data: forecastData, isLoading: forecastLoading } = useForecast(wardId, 1);
  
  // Fetch surge predictions for all wards, then filter for this one
  const { data: surgesData, isLoading: surgesLoading } = useQuery({
    queryKey: ['surges'],
    queryFn: riskApi.getSurges
  });

  if (forecastLoading || surgesLoading) {
    return <div className="p-2 text-sm">Loading data...</div>;
  }

  // Get the most recent hourly forecast row
  const currentForecast = forecastData?.forecast?.[0];
  const surgeInfo = surgesData?.find((s: any) => s.ward_id === wardId);

  return (
    <div className="p-2 text-gray-800 min-w-[200px]">
      <h3 className="font-bold text-lg mb-2 border-b pb-1">{wardName}</h3>
      
      <div className="space-y-1 text-sm">
        <div className="flex justify-between">
          <span className="font-semibold text-gray-600">WBGT:</span>
          <span>{currentForecast?.wbgt ?? 'N/A'} °C</span>
        </div>
        <div className="flex justify-between">
          <span className="font-semibold text-gray-600">UTCI:</span>
          <span>{currentForecast?.utci ?? 'N/A'} °C</span>
        </div>
        <div className="flex justify-between">
          <span className="font-semibold text-gray-600">Proj. ER Surge:</span>
          <span className={`${surgeInfo?.trigger_red_alert ? 'text-red-600 font-bold' : ''}`}>
            {surgeInfo?.projected_er_surge_percent ?? 'N/A'}%
          </span>
        </div>
      </div>
    </div>
  );
};
