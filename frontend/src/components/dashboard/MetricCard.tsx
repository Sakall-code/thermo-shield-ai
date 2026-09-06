import React from 'react';

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  isAlert?: boolean;
}

export const MetricCard: React.FC<MetricCardProps> = ({ title, value, subtitle, isAlert = false }) => {
  return (
    <div className={`p-4 rounded-lg border shadow-sm flex flex-col ${isAlert ? 'bg-red-50 border-red-200' : 'bg-white border-gray-200'}`}>
      <span className="text-sm font-medium text-gray-500 mb-1">{title}</span>
      <span className={`text-2xl font-bold ${isAlert ? 'text-red-700' : 'text-gray-900'}`}>
        {value}
      </span>
      {subtitle && (
        <span className={`text-xs mt-2 ${isAlert ? 'text-red-600 font-semibold' : 'text-gray-400'}`}>
          {subtitle}
        </span>
      )}
    </div>
  );
};
