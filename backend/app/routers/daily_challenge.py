from fastapi import APIRouter, Depends, HTTPException

from app.deps import get_current_user
from app.models import User

router = APIRouter(prefix="/daily-challenge", tags=["daily_challenge"])


@router.get("")
def get_daily(_: User = Depends(get_current_user)) -> dict:
    raise HTTPException(status_code=501, detail="Daily challenge is Phase 2")


@router.post("/submit")
def submit(_: User = Depends(get_current_user)) -> dict:
    raise HTTPException(status_code=501, detail="Daily challenge is Phase 2")


@router.get("/leaderboard")
def dc_leaderboard(_: User = Depends(get_current_user)) -> dict:
    raise HTTPException(status_code=501, detail="Daily challenge is Phase 2")
