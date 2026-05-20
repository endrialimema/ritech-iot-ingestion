from fastapi import APIRouter
from app.services.stats_service import get_stats, get_recent

router = APIRouter()


@router.get("/")
async def stats():
    return await get_stats()


@router.get("/recent")
async def recent(limit: int = 20):
    return await get_recent(limit)
