from datetime import date

from sqlalchemy.orm import Session

from app.models import QuestionAttempt, Streak


def touch_activity_on_correct_answer(db: Session, user_id) -> None:
    """Increment daily streak when user answers correctly today (calendar day)."""
    streak = db.query(Streak).filter(Streak.user_id == user_id).first()
    if streak is None:
        streak = Streak(user_id=user_id, current_streak=0, longest_streak=0)
        db.add(streak)
        db.flush()
    today = date.today()
    if streak.last_active_date == today:
        return
    if streak.last_active_date is None:
        streak.current_streak = 1
    else:
        gap = (today - streak.last_active_date).days
        if gap == 1:
            streak.current_streak = (streak.current_streak or 0) + 1
        else:
            streak.current_streak = 1
    streak.last_active_date = today
    streak.longest_streak = max(streak.longest_streak or 0, streak.current_streak or 0)


def consecutive_correct_count(db: Session, user_id, limit: int = 5) -> int:
    attempts = (
        db.query(QuestionAttempt)
        .filter(QuestionAttempt.user_id == user_id)
        .order_by(QuestionAttempt.created_at.desc())
        .limit(limit)
        .all()
    )
    c = 0
    for a in attempts:
        if a.is_correct:
            c += 1
        else:
            break
    return c
