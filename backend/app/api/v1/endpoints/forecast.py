from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.models import Ward, HourlyForecast
from app.services import weather_service, downscaling_service, biomet_service

router = APIRouter()

@router.get("/{ward_id}")
async def get_ward_forecast(ward_id: str, days: int = 5, db: AsyncSession = Depends(get_db)):
    """
    Fetches upstream weather forecast, downscales it to the ward microclimate,
    computes biometeorological WBGT/UTCI metrics, stores them, and returns them.
    """
    # 1. Fetch Ward
    result = await db.execute(select(Ward).where(Ward.id == ward_id))
    ward = result.scalars().first()
    if not ward:
        raise HTTPException(status_code=404, detail="Ward not found")
        
    # 2. Fetch raw regional forecast
    raw_rows = await weather_service.get_forecast(
        lat=ward.centroid_lat, 
        lon=ward.centroid_lon, 
        forecast_days=days
    )
    
    forecasts_to_insert = []
    response_data = []
    
    # 3. Process, Downscale, and Calculate Biomet
    for r in raw_rows:
        t_ward = downscaling_service.apply_downscaling(
            t_regional=r.temperature_c, 
            ndvi=ward.mean_ndvi, 
            ndbi=ward.mean_ndbi
        )
        
        biomet = biomet_service.compute_wbgt_utci(
            t_air=t_ward,
            rh=r.humidity_pct,
            wind_speed=r.wind_speed_kmh,
            solar_radiation=r.solar_radiation_wm2,
            wind_is_kmh=True
        )
        
        hf = HourlyForecast(
            ward_id=ward.id,
            forecast_ts=r.timestamp,
            temperature_c=t_ward,
            humidity_pct=r.humidity_pct,
            wind_speed_kmh=r.wind_speed_kmh,
            heat_index=biomet.wbgt,
            risk_level=biomet.risk_level
        )
        forecasts_to_insert.append(hf)
        
        response_data.append({
            "forecast_ts": r.timestamp,
            "temperature_c": t_ward,
            "humidity_pct": r.humidity_pct,
            "wind_speed_kmh": r.wind_speed_kmh,
            "wbgt": biomet.wbgt,
            "utci": biomet.utci,
            "risk_level": biomet.risk_level
        })
        
    # 4. Store in DB (Overwrite old forecast for prototyping simplicity)
    await db.execute(delete(HourlyForecast).where(HourlyForecast.ward_id == ward_id))
    db.add_all(forecasts_to_insert)
    await db.commit()
    
    return {"ward_id": ward_id, "forecast": response_data}
