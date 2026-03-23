import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Chapter, Section, Streak, Topic, User, UserProgress, UserSectionProgress
from app.schemas.progress import CompletePhaseBody, CompletePhaseResponse, MeProgressOut
from app.services import progress_service

router = APIRouter(prefix="/users/me", tags=["progress"])


@router.get("/progress", response_model=MeProgressOut)
def my_progress(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> MeProgressOut:
    progress_service.ensure_user_bootstrap(db, user.id)
    progress_service.refresh_unlocks(db, user.id)
    db.commit()
    streak = db.query(Streak).filter(Streak.user_id == user.id).first()
    total_stars = (
        db.query(func.coalesce(func.sum(UserProgress.stars), 0))
        .filter(UserProgress.user_id == user.id)
        .scalar()
    )
    return MeProgressOut(
        total_xp=user.total_xp or 0,
        level=user.level or 1,
        streak_current=streak.current_streak if streak else 0,
        streak_longest=streak.longest_streak if streak else 0,
        total_stars=int(total_stars or 0),
    )


@router.get("/progress/chapter/{chapter_id}")
def chapter_progress(
    chapter_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    ch = db.get(Chapter, chapter_id)
    if not ch:
        raise HTTPException(status_code=404, detail="Chapter not found")
    progress_service.ensure_user_bootstrap(db, user.id)
    sections = db.query(Section).filter(Section.chapter_id == chapter_id).order_by(Section.order).all()
    out: list[dict] = []
    for sec in sections:
        topics = db.query(Topic).filter(Topic.section_id == sec.id).order_by(Topic.order).all()
        topic_rows: list[dict] = []
        for t in topics:
            up = (
                db.query(UserProgress)
                .filter(UserProgress.user_id == user.id, UserProgress.topic_id == t.id)
                .first()
            )
            topic_rows.append(
                {
                    "topic_id": str(t.id),
                    "name": t.name,
                    "phase": up.phase if up else "locked",
                    "stars": up.stars if up else 0,
                    "best_score": up.best_score if up else 0,
                }
            )
        usp = (
            db.query(UserSectionProgress)
            .filter(UserSectionProgress.user_id == user.id, UserSectionProgress.section_id == sec.id)
            .first()
        )
        out.append(
            {
                "section_id": str(sec.id),
                "name": sec.name,
                "section_number": sec.section_number,
                "status": usp.status if usp else "locked",
                "stars_earned": usp.stars_earned if usp else 0,
                "stars_possible": usp.stars_possible if usp else 0,
                "topics": topic_rows,
            }
        )
    return {"chapter_id": str(chapter_id), "chapter_name": ch.name, "sections": out}


router_topics = APIRouter()


@router_topics.post("/topics/{topic_id}/complete-phase", response_model=CompletePhaseResponse)
def complete_phase_route(
    topic_id: uuid.UUID,
    body: CompletePhaseBody,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> CompletePhaseResponse:
    try:
        result = progress_service.complete_phase(db, user.id, topic_id, body.phase, body.score)
        db.commit()
        return CompletePhaseResponse.model_validate(result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
