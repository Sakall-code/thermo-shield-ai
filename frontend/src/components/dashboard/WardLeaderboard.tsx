import React from 'react';
import { useWardData } from '../../hooks/useWardData';

export const WardLeaderboard: React.FC = () => {
  const { data: wards, isLoading } = useWardData();

  if (isLoading) {
    return (
      <div className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm h-64 flex items-center justify-center">
        <span className="text-gray-500">Loading leaderboard...</span>
      </div>
    );
  }

  // Sort by WVI score descending and grab top 5
  const topWards = [...(wards || [])]
    .sort((a: any, b: any) => b.wvi_score - a.wvi_score)
    .slice(0, 5);

  return (
    <div className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
      <h3 className="text-sm font-bold text-gray-700 mb-3 border-b pb-2">Most Vulnerable Wards (Top 5)</h3>
      <div className="space-y-3 mt-4">
        {topWards.map((ward, index) => (
          <div key={ward.id} className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className={`text-xs font-bold w-5 h-5 flex items-center justify-center rounded-full ${index === 0 ? 'bg-red-100 text-red-700' : index < 3 ? 'bg-orange-100 text-orange-700' : 'bg-gray-100 text-gray-600'}`}>
                {index + 1}
              </span>
              <span className="text-sm font-medium text-gray-800">{ward.ward_name}</span>
            </div>
            <div className="text-right">
              <div className="text-sm font-semibold text-gray-900">{ward.wvi_score.toFixed(3)}</div>
              <div className="text-[10px] text-gray-500 uppercase tracking-wider">WVI Score</div>
            </div>
          </div>
        ))}
        {topWards.length === 0 && (
          <div className="text-sm text-gray-500">No ward data available.</div>
        )}
      </div>
    </div>
  );
};
