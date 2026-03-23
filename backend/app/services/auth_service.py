import uuid

from sqlalchemy.orm import Session

from app.models import Streak, User
from app.services import progress_service
from app.utils.security import hash_password


def create_user(
    db: Session,
    *,
    username: str,
    email: str,
    password: str,
    display_name: str,
) -> User:
    user = User(
        id=uuid.uuid4(),
        username=username,
        email=email,
        display_name=display_name,
        password_hash=hash_password(password),
        avatar="default",
        theme="dark",
        total_xp=0,
        level=1,
    )
    db.add(user)
    db.flush()
    db.add(Streak(user_id=user.id, current_streak=0, longest_streak=0))
    db.flush()
    progress_service.ensure_user_bootstrap(db, user.id)
    progress_service.refresh_unlocks(db, user.id)
    db.flush()
    return user
