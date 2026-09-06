from fastapi import APIRouter

router = APIRouter()

@router.get("/healthz")
async def healthz():
    """Simple API health check."""
    return {"status": "ok"}
