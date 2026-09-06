import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { MapContainer } from './components/map/MapContainer';
import { MetricCard } from './components/dashboard/MetricCard';
import { SurgeChart } from './components/dashboard/SurgeChart';
import { WardLeaderboard } from './components/dashboard/WardLeaderboard';
import { riskApi } from './api/riskApi';
import { useWardData } from './hooks/useWardData';

function App() {
  const [selectedWardId, setSelectedWardId] = useState<string | null>(null);
  
  const { data: surges } = useQuery({ queryKey: ['surges'], queryFn: riskApi.getSurges });
  const { data: wards } = useWardData();
  
  // Compute city-wide metrics for the top cards
  const maxSurge = surges?.length 
    ? Math.max(...surges.map((s: any) => s.projected_er_surge_percent)) 
    : 0;
  
  const hasRedAlert = surges?.some((s: any) => s.trigger_red_alert);
  
  // Use the first ward as a fallback for the chart if none selected
  const chartWardId = selectedWardId || wards?.[0]?.id || null;

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900 tracking-tight">ThermoShield <span className="text-blue-600">AI</span></h1>
          <nav className="flex space-x-4">
            <span className="text-sm font-medium text-gray-500">Ahmedabad Pilot</span>
          </nav>
        </div>
      </header>
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 flex flex-col">
        <div className="mb-6">
          <h2 className="text-xl font-semibold text-gray-800">Live Heat Risk Dashboard</h2>
          <p className="text-gray-600 text-sm mt-1">Interactive microclimate risks, peak projections, and hospital surge warnings.</p>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1">
          {/* Left Column: Map */}
          <div className="lg:col-span-2 flex flex-col min-h-[600px]">
            <MapContainer onWardSelect={setSelectedWardId} />
          </div>
          
          {/* Right Column: Dashboard Metrics */}
          <div className="space-y-6 flex flex-col">
            <div className="grid grid-cols-2 gap-4">
              <MetricCard 
                title="Max Proj. ER Surge" 
                value={`${maxSurge.toFixed(1)}%`} 
                isAlert={hasRedAlert}
                subtitle={hasRedAlert ? "Critical Level Reached" : "Normal Capacity"}
              />
              <MetricCard 
                title="Active Alerts" 
                value={hasRedAlert ? "RED" : "None"} 
                isAlert={hasRedAlert}
              />
            </div>
            
            <SurgeChart wardId={chartWardId} />
            <WardLeaderboard />
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
