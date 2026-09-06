import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';
import { useForecast } from '../../hooks/useForecast';

interface SurgeChartProps {
  wardId: string | null;
}

export const SurgeChart: React.FC<SurgeChartProps> = ({ wardId }) => {
  const { data, isLoading } = useForecast(wardId, 5);

  if (isLoading) {
    return (
      <div className="h-64 bg-white border border-gray-200 rounded-lg shadow-sm flex items-center justify-center">
        <span className="text-gray-500">Loading forecast...</span>
      </div>
    );
  }

  if (!data?.forecast || data.forecast.length === 0) {
    return (
      <div className="h-64 bg-white border border-gray-200 rounded-lg shadow-sm flex items-center justify-center">
        <span className="text-gray-500">Select a ward on the map or wait for data.</span>
      </div>
    );
  }

  // Format data for Recharts (e.g., extracting a readable hour/day)
  const chartData = data.forecast.map((row: any) => {
    const d = new Date(row.forecast_ts);
    return {
      time: `${d.getMonth() + 1}/${d.getDate()} ${d.getHours()}:00`,
      wbgt: row.wbgt,
      utci: row.utci,
    };
  });

  return (
    <div className="bg-white p-4 rounded-lg border border-gray-200 shadow-sm flex flex-col h-72">
      <h3 className="text-sm font-bold text-gray-700 mb-4">5-Day Heat Trend</h3>
      <div className="flex-1 min-h-0">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e5e7eb" />
            <XAxis 
              dataKey="time" 
              tick={{ fontSize: 10, fill: '#6b7280' }} 
              tickMargin={10}
              minTickGap={30}
            />
            <YAxis 
              domain={['dataMin - 2', 'dataMax + 2']} 
              tick={{ fontSize: 11, fill: '#6b7280' }} 
              axisLine={false}
              tickLine={false}
            />
            <Tooltip 
              contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
              labelStyle={{ fontWeight: 'bold', color: '#374151' }}
            />
            <Legend wrapperStyle={{ fontSize: '12px' }} />
            <Line 
              type="monotone" 
              dataKey="wbgt" 
              name="WBGT (°C)" 
              stroke="#f97316" 
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 4 }}
            />
            <Line 
              type="monotone" 
              dataKey="utci" 
              name="UTCI (°C)" 
              stroke="#ef4444" 
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
