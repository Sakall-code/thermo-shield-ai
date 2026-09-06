import React from 'react';
import { Source, Layer } from 'react-map-gl/maplibre';
import type { FeatureCollection } from 'geojson';

interface ChoroplethLayerProps {
  data: FeatureCollection | null;
}

export const ChoroplethLayer: React.FC<ChoroplethLayerProps> = ({ data }) => {
  if (!data) return null;

  return (
    <Source id="wards-source" type="geojson" data={data}>
      {/* Fill layer driven by the 'color' property in the GeoJSON */}
      <Layer
        id="wards-fill"
        type="fill"
        paint={{
          'fill-color': ['get', 'color'],
          'fill-opacity': 0.6,
        }}
      />
      {/* Outline layer for ward boundaries */}
      <Layer
        id="wards-outline"
        type="line"
        paint={{
          'line-color': '#ffffff',
          'line-width': 1.5,
        }}
      />
    </Source>
  );
};
