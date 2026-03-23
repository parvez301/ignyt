import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.models import Badge, Topic, UserBadge, UserProgress, UserSectionProgress


def award_badge_if_new(db: Session, user_id: uuid.UUID, badge_id: uuid.UUID) -> bool:
    exists = (
        db.query(UserBadge)
        .filter(UserBadge.user_id == user_id, UserBadge.badge_id == badge_id)
        .first()
    )
    if exists:
        return False
    db.add(UserBadge(user_id=user_id, badge_id=badge_id))
    return True


def check_section_complete_badges(db: Session, user_id: uuid.UUID) -> list[uuid.UUID]:
    earned: list[uuid.UUID] = []
    for badge in db.query(Badge).all():
        crit: dict[str, Any] = badge.criteria_json or {}
        if crit.get("type") != "section_complete":
            continue
        sid_raw = crit.get("section_id")
        if not sid_raw:
            continue
        try:
            suid = uuid.UUID(str(sid_raw))
        except ValueError:
            continue
        usp = (
            db.query(UserSectionProgress)
            .filter(UserSectionProgress.user_id == user_id, UserSectionProgress.section_id == suid)
            .first()
        )
        if usp and usp.status == "completed":
            if award_badge_if_new(db, user_id, badge.id):
                earned.append(badge.id)
    return earned


def recalc_section_completion(db: Session, user_id: uuid.UUID, section_id: uuid.UUID) -> None:
    topic_rows = (
        db.query(Topic).filter(Topic.section_id == section_id).order_by(Topic.order).all()
    )
    if not topic_rows:
        return
    topic_ids = [t.id for t in topic_rows]
    progresses = (
        db.query(UserProgress)
        .filter(UserProgress.user_id == user_id, UserProgress.topic_id.in_(topic_ids))
        .all()
    )
    by_topic = {p.topic_id: p for p in progresses}
    all_completed = all(
        by_topic.get(tid) is not None and by_topic[tid].phase == "completed" for tid in topic_ids
    )
    usp = (
        db.query(UserSectionProgress)
        .filter(UserSectionProgress.user_id == user_id, UserSectionProgress.section_id == section_id)
        .first()
    )
    if usp is None:
        return
    stars_earned = sum((by_topic[tid].stars or 0) for tid in topic_ids if by_topic.get(tid))
    stars_possible = 3 * len(topic_ids)
    usp.stars_earned = stars_earned
    usp.stars_possible = stars_possible
    if all_completed:
        usp.status = "completed"
    db.flush()
