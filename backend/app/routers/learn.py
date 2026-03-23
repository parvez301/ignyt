import uuid
from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import ConceptCard, RealWorldAnchor, Topic, User, UserWorkedExample, WorkedExample
from app.schemas.content import ConceptCardOut, LearnBundle, WorkedExampleOut

router = APIRouter()


@router.get("/topics/{topic_id}/learn", response_model=LearnBundle)
def get_learn(
    topic_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> LearnBundle:
    topic = db.get(Topic, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    cards = (
        db.query(ConceptCard)
        .filter(ConceptCard.topic_id == topic_id)
        .order_by(ConceptCard.order)
        .all()
    )
    examples = (
        db.query(WorkedExample)
        .filter(WorkedExample.topic_id == topic_id)
        .order_by(WorkedExample.order)
        .all()
    )
    completed_rows = (
        db.query(UserWorkedExample)
        .filter(
            UserWorkedExample.user_id == user.id,
            UserWorkedExample.worked_example_id.in_([w.id for w in examples] or []),
        )
        .all()
    )
    completed_by_we = {row.worked_example_id: bool(row.completed) for row in completed_rows}
    hook_row = (
        db.query(RealWorldAnchor)
        .filter(RealWorldAnchor.section_id == topic.section_id)
        .first()
    )
    return LearnBundle(
        concept_cards=[
            ConceptCardOut(id=c.id, title=c.title, content_html=c.content_html, order=c.order)
            for c in cards
        ],
        worked_examples=[
            WorkedExampleOut(
                id=w.id,
                title=w.title,
                steps_json=w.steps_json,
                order=w.order,
                completed=completed_by_we.get(w.id, False),
            )
            for w in examples
        ],
        real_world_hook=hook_row.hook_text if hook_row else None,
    )


@router.post("/topics/{topic_id}/worked-examples/{we_id}/complete")
def complete_worked_example(
    topic_id: uuid.UUID,
    we_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    we = db.get(WorkedExample, we_id)
    if not we or we.topic_id != topic_id:
        raise HTTPException(status_code=404, detail="Worked example not found")
    row = (
        db.query(UserWorkedExample)
        .filter(
            UserWorkedExample.user_id == user.id,
            UserWorkedExample.worked_example_id == we_id,
        )
        .first()
    )
    if row is None:
        row = UserWorkedExample(
            id=uuid.uuid4(),
            user_id=user.id,
            worked_example_id=we_id,
            completed=True,
            completed_at=datetime.now(UTC),
        )
        db.add(row)
    else:
        row.completed = True
        row.completed_at = datetime.now(UTC)
    db.commit()
    return {"ok": True}
