from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.database import get_db
from app.models import Ward

router = APIRouter()

@router.get("")
@router.get("/")
async def get_wards(db: AsyncSession = Depends(get_db)):
    """Returns basic details for all pilot wards."""
    result = await db.execute(select(Ward))
    wards = result.scalars().all()
    return [
        {
            "id": w.id,
            "ward_name": w.ward_name,
            "population": w.population,
            "wvi_score": w.wvi_score,
            "mean_ndvi": w.mean_ndvi,
            "mean_ndbi": w.mean_ndbi,
            "centroid": {"lat": w.centroid_lat, "lon": w.centroid_lon}
        }
        for w in wards
    ]

@router.get("/{id}/geometry")
async def get_ward_geometry(id: str, db: AsyncSession = Depends(get_db)):
    """Returns the GeoJSON MultiPolygon for a specific ward."""
    result = await db.execute(select(Ward).where(Ward.id == id))
    ward = result.scalars().first()
    if not ward:
        raise HTTPException(status_code=404, detail="Ward not found")
    return json.loads(ward.geom_geojson)
