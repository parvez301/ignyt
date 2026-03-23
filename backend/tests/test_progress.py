import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Topic, User, UserProgress
from app.seed.chapter1 import seed_chapter1, uid
from app.services import progress_service, xp_service
from app.utils.math_score import score_percent, stars_for_phase
from app.utils.security import hash_password


def test_score_percent_half_up() -> None:
    assert score_percent(1, 2) == 50
    assert score_percent(2, 3) == 67  # 66.666... rounds half-up to 67
    assert score_percent(5, 6) == 83  # 83.333... -> 83


def test_stars_for_phase_rules() -> None:
    assert stars_for_phase("practice", 50) == 1
    assert stars_for_phase("practice", 80) == 2
    assert stars_for_phase("master", 89) == 2
    assert stars_for_phase("master", 90) == 3


def test_complete_phase_rejects_low_practice_score(client: TestClient, db_session: Session) -> None:
    seed_chapter1(db_session)
    user = User(
        id=uuid.uuid4(),
        username="proguser",
        email="proguser@example.com",
        display_name="P",
        password_hash=hash_password("pw"),
    )
    db_session.add(user)
    db_session.commit()
    from app.models import Streak

    db_session.add(Streak(user_id=user.id, current_streak=0, longest_streak=0))
    db_session.commit()
    progress_service.ensure_user_bootstrap(db_session, user.id)
    db_session.commit()

    topic = db_session.query(Topic).filter(Topic.id == uid("topic.1.1.1")).first()
    assert topic
    up = (
        db_session.query(UserProgress)
        .filter(UserProgress.user_id == user.id, UserProgress.topic_id == topic.id)
        .first()
    )
    assert up
    up.phase = "practice"
    db_session.commit()

    from app.utils.security import create_access_token

    token = create_access_token(user.username)
    r = client.post(
        f"/api/topics/{topic.id}/complete-phase",
        headers={"Authorization": f"Bearer {token}"},
        json={"phase": "practice", "score": 40},
    )
    assert r.status_code == 400


def test_xp_transaction_updates_total(db_session: Session) -> None:
    seed_chapter1(db_session)
    user = User(
        id=uuid.uuid4(),
        username="xpuser",
        email="xpuser@example.com",
        display_name="X",
        password_hash=hash_password("pw"),
        total_xp=0,
        level=1,
    )
    db_session.add(user)
    db_session.commit()
    xp_service.award_xp(db_session, user_id=user.id, amount=25, source="question")
    db_session.commit()
    db_session.refresh(user)
    assert user.total_xp == 25
    assert user.level >= 1
