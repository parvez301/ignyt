import uuid
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.models import (
    Chapter,
    Section,
    Topic,
    UserMilestone,
    UserProgress,
    UserSectionProgress,
    UserWorkedExample,
    WorkedExample,
)
from app.services import badge_service, xp_service
from app.utils.math_score import stars_for_phase


def _topic_prev_in_section(db: Session, topic: Topic) -> Topic | None:
    return (
        db.query(Topic)
        .filter(Topic.section_id == topic.section_id, Topic.order < topic.order)
        .order_by(Topic.order.desc())
        .first()
    )


def ensure_user_bootstrap(db: Session, user_id: uuid.UUID) -> None:
    """Create progress rows for all topics/sections; unlock first section."""
    chapter = db.query(Chapter).order_by(Chapter.order).first()
    if not chapter:
        return
    sections = db.query(Section).filter(Section.chapter_id == chapter.id).order_by(Section.order).all()
    if not sections:
        return
    min_order = min(s.order for s in sections)
    for sec in sections:
        usp = (
            db.query(UserSectionProgress)
            .filter(UserSectionProgress.user_id == user_id, UserSectionProgress.section_id == sec.id)
            .first()
        )
        if usp is None:
            status = "in_progress" if sec.order == min_order else "locked"
            unlocked_at = datetime.now(UTC) if sec.order == min_order else None
            usp = UserSectionProgress(
                id=uuid.uuid4(),
                user_id=user_id,
                section_id=sec.id,
                status=status,
                stars_earned=0,
                stars_possible=0,
                unlocked_at=unlocked_at,
            )
            db.add(usp)
        topics = db.query(Topic).filter(Topic.section_id == sec.id).order_by(Topic.order).all()
        for top in topics:
            up = (
                db.query(UserProgress)
                .filter(UserProgress.user_id == user_id, UserProgress.topic_id == top.id)
                .first()
            )
            if up is None:
                phase = "locked"
                if sec.order == min_order and _topic_prev_in_section(db, top) is None:
                    phase = "learn"
                up = UserProgress(
                    id=uuid.uuid4(),
                    user_id=user_id,
                    topic_id=top.id,
                    phase=phase,
                    stars=0,
                    best_score=0,
                    attempts=0,
                )
                db.add(up)
    db.flush()


def refresh_unlocks(db: Session, user_id: uuid.UUID) -> None:
    """Propagate unlocks after progress changes."""
    chapter = db.query(Chapter).order_by(Chapter.order).first()
    if not chapter:
        return
    sections = db.query(Section).filter(Section.chapter_id == chapter.id).order_by(Section.order).all()
    for i, sec in enumerate(sections):
        usp = (
            db.query(UserSectionProgress)
            .filter(UserSectionProgress.user_id == user_id, UserSectionProgress.section_id == sec.id)
            .first()
        )
        if usp is None:
            continue
        if i > 0:
            prev = sections[i - 1]
            prev_usp = (
                db.query(UserSectionProgress)
                .filter(
                    UserSectionProgress.user_id == user_id,
                    UserSectionProgress.section_id == prev.id,
                )
                .first()
            )
            if prev_usp and prev_usp.status == "completed" and usp.status == "locked":
                usp.status = "in_progress"
                usp.unlocked_at = datetime.now(UTC)
        topics = db.query(Topic).filter(Topic.section_id == sec.id).order_by(Topic.order).all()
        for top in topics:
            up = (
                db.query(UserProgress)
                .filter(UserProgress.user_id == user_id, UserProgress.topic_id == top.id)
                .first()
            )
            if up is None:
                continue
            prev_topic = _topic_prev_in_section(db, top)
            if prev_topic:
                pup = (
                    db.query(UserProgress)
                    .filter(UserProgress.user_id == user_id, UserProgress.topic_id == prev_topic.id)
                    .first()
                )
                if pup and pup.phase == "completed" and up.phase == "locked":
                    up.phase = "learn"
            elif usp.status in ("in_progress", "completed") and up.phase == "locked":
                up.phase = "learn"
        n_topics = len(topics)
        usp.stars_possible = 3 * n_topics if n_topics else 0
        progresses = (
            db.query(UserProgress)
            .filter(UserProgress.user_id == user_id, UserProgress.topic_id.in_([t.id for t in topics]))
            .all()
        )
        by_tid = {p.topic_id: p for p in progresses}
        usp.stars_earned = sum((by_tid.get(t.id).stars or 0) for t in topics if by_tid.get(t.id))
        all_done = bool(topics) and all(
            by_tid.get(t.id) and by_tid[t.id].phase == "completed" for t in topics
        )
        if all_done:
            usp.status = "completed"
    db.flush()


def complete_phase(
    db: Session,
    user_id: uuid.UUID,
    topic_id: uuid.UUID,
    phase: str,
    score: int | None,
) -> dict:
    ensure_user_bootstrap(db, user_id)
    refresh_unlocks(db, user_id)
    up = (
        db.query(UserProgress)
        .filter(UserProgress.user_id == user_id, UserProgress.topic_id == topic_id)
        .first()
    )
    if up is None:
        raise ValueError("Topic progress not found")
    topic = db.get(Topic, topic_id)
    if topic is None:
        raise ValueError("Topic not found")

    xp_earned = 0
    earned_badges: list[uuid.UUID] = []

    if phase == "learn":
        if up.phase != "learn":
            raise ValueError("Invalid transition for learn phase")
        wes = db.query(WorkedExample).filter(WorkedExample.topic_id == topic_id).all()
        for we in wes:
            uwe = (
                db.query(UserWorkedExample)
                .filter(
                    UserWorkedExample.user_id == user_id,
                    UserWorkedExample.worked_example_id == we.id,
                )
                .first()
            )
            if uwe is None or not uwe.completed:
                raise ValueError("Complete all worked examples first")
        up.phase = "practice"
        xp_earned = 20
        xp_service.award_xp(db, user_id=user_id, amount=xp_earned, source="learn_complete", topic_id=topic_id)
        up.attempts = (up.attempts or 0) + 1
    elif phase == "practice":
        if score is None:
            raise ValueError("score required")
        if score < 50:
            raise ValueError("Practice requires score >= 50")
        phase_stars = stars_for_phase("practice", score)
        up.stars = max(up.stars or 0, phase_stars)
        up.best_score = max(up.best_score or 0, score)
        if up.phase == "completed":
            xp_earned = 0
        elif up.phase == "practice":
            up.phase = "master"
            xp_earned = 30
            xp_service.award_xp(
                db, user_id=user_id, amount=xp_earned, source="practice_complete", topic_id=topic_id
            )
        else:
            raise ValueError("Invalid transition for practice phase")
        up.attempts = (up.attempts or 0) + 1
    elif phase == "master":
        if score is None:
            raise ValueError("score required")
        if score < 50:
            raise ValueError("Master requires score >= 50")
        phase_stars = stars_for_phase("master", score)
        up.stars = max(up.stars or 0, phase_stars)
        up.best_score = max(up.best_score or 0, score)
        if up.phase == "completed":
            xp_earned = 0
        elif up.phase == "master":
            up.phase = "completed"
            xp_earned = 40
            xp_service.award_xp(
                db, user_id=user_id, amount=xp_earned, source="master_complete", topic_id=topic_id
            )
        else:
            raise ValueError("Invalid transition for master phase")
        up.attempts = (up.attempts or 0) + 1
    else:
        raise ValueError("Unsupported phase")

    sec = db.get(Section, topic.section_id)
    if sec:
        badge_service.recalc_section_completion(db, user_id, sec.id)
        earned_badges = badge_service.check_section_complete_badges(db, user_id)

    refresh_unlocks(db, user_id)
    db.flush()

    milestones: list[dict] = []
    if up.stars and up.stars >= 1:
        m = UserMilestone(
            id=uuid.uuid4(),
            user_id=user_id,
            milestone_type="first_star",
            milestone_value=str(topic_id),
            seen=False,
        )
        db.add(m)
        milestones.append({"id": str(m.id), "type": "first_star"})

    return {
        "new_phase": up.phase,
        "stars": up.stars,
        "xp_earned": xp_earned,
        "badges_earned": [str(b) for b in earned_badges],
        "milestones": milestones,
    }
