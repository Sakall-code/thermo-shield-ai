from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Ward, HourlyForecast
from app.services import health_model_service

router = APIRouter()

@router.get("/heatmap")
async def get_risk_heatmap(db: AsyncSession = Depends(get_db)):
    """Returns the latest risk level and WVI for all wards to plot on a map."""
    result = await db.execute(select(Ward))
    wards = result.scalars().all()
    
    heatmap_data = []
    for w in wards:
        # Get earliest future forecast for this ward (or fallback to latest)
        forecast_res = await db.execute(
            select(HourlyForecast)
            .where(HourlyForecast.ward_id == w.id)
            .order_by(HourlyForecast.forecast_ts.asc())
            .limit(1)
        )
        hf = forecast_res.scalars().first()
        current_risk = hf.risk_level if hf else "UNKNOWN"
        
        heatmap_data.append({
            "ward_id": w.id,
            "ward_name": w.ward_name,
            "wvi_score": w.wvi_score,
            "risk_level": current_risk,
            "centroid": {"lat": w.centroid_lat, "lon": w.centroid_lon}
        })
        
    return heatmap_data

@router.get("/surges")
async def get_risk_surges(db: AsyncSession = Depends(get_db)):
    """Predicts hospital/ER surges based on 5-day heat index series."""
    result = await db.execute(select(Ward))
    wards = result.scalars().all()
    
    surges = []
    for w in wards:
        forecast_res = await db.execute(
            select(HourlyForecast.heat_index)
            .where(HourlyForecast.ward_id == w.id)
            .order_by(HourlyForecast.forecast_ts.asc())
        )
        wbgt_series = forecast_res.scalars().all()
        
        if not wbgt_series:
            continue
            
        prediction = health_model_service.mock_surge_prediction(
            wbgt_series_5day=wbgt_series, 
            wvi_score=w.wvi_score
        )
        
        surges.append({
            "ward_id": w.id,
            "ward_name": w.ward_name,
            "wvi_score": w.wvi_score,
            "projected_excess_deaths": prediction.projected_excess_deaths,
            "projected_er_surge_percent": prediction.projected_er_surge_percent,
            "trigger_red_alert": prediction.trigger_red_alert
        })
        
    return surges
