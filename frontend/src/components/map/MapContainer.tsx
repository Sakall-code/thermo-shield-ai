import React, { useState, useEffect } from 'react';
import Map, { Popup } from 'react-map-gl/maplibre';
import * as maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import { useQuery } from '@tanstack/react-query';
import type { FeatureCollection } from 'geojson';

import { useWardData } from '../../hooks/useWardData';
import { wardsApi } from '../../api/wardsApi';
import { riskApi } from '../../api/riskApi';
import { getRiskColor } from '../../utils/colorScales';
import { ChoroplethLayer } from './ChoroplethLayer';
import { WardPopupContent } from './WardPopup';

interface MapContainerProps {
  onWardSelect?: (wardId: string | null) => void;
}

export const MapContainer: React.FC<MapContainerProps> = ({ onWardSelect }) => {
  // Fetch ward metadata and risk heatmap
  const { data: wards } = useWardData();
  const { data: heatmap } = useQuery({ queryKey: ['heatmap'], queryFn: riskApi.getHeatmap });

  const [geoJson, setGeoJson] = useState<FeatureCollection | null>(null);
  
  // State for handling clicks & popups
  const [clickedWard, setClickedWard] = useState<{ id: string; name: string; lng: number; lat: number } | null>(null);

  // Assemble the GeoJSON FeatureCollection once wards and heatmap are loaded
  useEffect(() => {
    if (wards && heatmap) {
      // Fetch geometry for each ward in parallel
      Promise.all(wards.map((w: any) => wardsApi.getWardGeometry(w.id)))
        .then((geoms) => {
          const features = wards.map((w: any, index: number) => {
            const riskInfo = heatmap.find((h: any) => h.ward_id === w.id);
            const riskLevel = riskInfo?.risk_level || 'NORMAL';
            
            return {
              type: 'Feature',
              properties: {
                ward_id: w.id,
                ward_name: w.ward_name,
                risk_level: riskLevel,
                color: getRiskColor(riskLevel),
              },
              geometry: geoms[index],
            };
          });

          setGeoJson({ type: 'FeatureCollection', features });
        })
        .catch(err => console.error("Error building GeoJSON:", err));
    }
  }, [wards, heatmap]);

  const onClick = (event: any) => {
    const feature = event.features?.[0];
    if (feature && feature.properties.ward_id) {
      setClickedWard({
        id: feature.properties.ward_id,
        name: feature.properties.ward_name,
        lng: event.lngLat.lng,
        lat: event.lngLat.lat,
      });
      onWardSelect?.(feature.properties.ward_id);
    } else {
      setClickedWard(null);
      onWardSelect?.(null);
    }
  };

  return (
    <div className="w-full h-[600px] rounded-lg overflow-hidden shadow-lg border border-gray-200">
      <Map
        mapLib={maplibregl}
        initialViewState={{
          longitude: 72.58, // Ahmedabad longitude
          latitude: 23.02,  // Ahmedabad latitude
          zoom: 11.5,
        }}
        style={{ width: '100%', height: '100%' }}
        mapStyle="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
        interactiveLayerIds={['wards-fill']}
        onClick={onClick}
        cursor="pointer"
      >
        <ChoroplethLayer data={geoJson} />

        {clickedWard && (
          <Popup
            longitude={clickedWard.lng}
            latitude={clickedWard.lat}
            anchor="bottom"
            onClose={() => setClickedWard(null)}
            closeOnClick={false}
            className="z-50"
          >
            <WardPopupContent wardId={clickedWard.id} wardName={clickedWard.name} />
          </Popup>
        )}
      </Map>
    </div>
  );
};
