from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
import logging

from app.database import get_db
from app.models import AlertLog

logger = logging.getLogger(__name__)
router = APIRouter()

class AlertTriggerRequest(BaseModel):
    ward_id: str
    alert_level: str
    headline: str
    description: str

@router.post("/trigger")
async def trigger_alert(req: AlertTriggerRequest, db: AsyncSession = Depends(get_db)):
    """Triggers an alert. Prototype marks as LOG_ONLY instead of Twilio/Telegram."""
    logger.info(f"LOG_ONLY: Triggering {req.alert_level} alert for {req.ward_id}. Not calling Twilio/Telegram.")
    
    alert = AlertLog(
        ward_id=req.ward_id,
        alert_level=req.alert_level,
        headline=req.headline,
        description=req.description,
        issued_at=datetime.now(timezone.utc),
        expires_at=datetime.now(timezone.utc) + timedelta(days=2),
        acknowledged=False
    )
    
    db.add(alert)
    await db.commit()
    await db.refresh(alert)
    
    return {"status": "success", "alert_id": alert.id, "message": "Alert triggered (LOG_ONLY)"}

@router.get("/history")
async def get_alerts_history(db: AsyncSession = Depends(get_db)):
    """Returns recent alert logs."""
    result = await db.execute(select(AlertLog).order_by(AlertLog.issued_at.desc()).limit(50))
    alerts = result.scalars().all()
    return alerts
