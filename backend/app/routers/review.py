from fastapi import APIRouter, Depends, HTTPException

from app.deps import get_current_user
from app.models import User

router = APIRouter(prefix="/review", tags=["review"])


@router.get("/due")
def due(_: User = Depends(get_current_user)) -> dict:
    raise HTTPException(status_code=501, detail="Review queue is Phase 2")


@router.post("/submit")
def submit(_: User = Depends(get_current_user)) -> dict:
    raise HTTPException(status_code=501, detail="Review queue is Phase 2")


@router.get("/stats")
def stats(_: User = Depends(get_current_user)) -> dict:
    return {"due_count": 0, "upcoming": []}
