import uuid

from sqlalchemy.orm import Session

from app.models import User, XPLedger
from app.utils.level import level_from_xp


def award_xp(
    db: Session,
    *,
    user_id: uuid.UUID,
    amount: int,
    source: str,
    topic_id: uuid.UUID | None = None,
) -> int:
    """Insert xp_ledger row and update users.total_xp in the same transaction. Returns new total_xp."""
    ledger = XPLedger(
        id=uuid.uuid4(),
        user_id=user_id,
        amount=amount,
        source=source,
        topic_id=topic_id,
    )
    db.add(ledger)
    user = db.get(User, user_id)
    if user is None:
        raise ValueError("User not found")
    user.total_xp = (user.total_xp or 0) + amount
    user.level = level_from_xp(user.total_xp)
    db.flush()
    return user.total_xp
