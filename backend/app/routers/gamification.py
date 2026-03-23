import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Badge, ItemType, Streak, User, UserBadge, UserInventory, UserMilestone
from app.schemas.common import PaginatedResponse
from app.schemas.gamification import (
    BadgeOut,
    BuyBody,
    BuyResponse,
    InventoryItemOut,
    LeaderboardUser,
    MilestoneOut,
    StreakOut,
    UseItemBody,
    UseItemResponse,
)
from app.services import xp_service

router = APIRouter()


@router.get("/leaderboard", response_model=PaginatedResponse[LeaderboardUser])
def leaderboard(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> PaginatedResponse[LeaderboardUser]:
    q = db.query(User).order_by(User.total_xp.desc())
    total = q.count()
    rows = q.offset((page - 1) * per_page).limit(per_page).all()
    items = [
        LeaderboardUser(
            rank=(page - 1) * per_page + i + 1,
            user_id=u.id,
            display_name=u.display_name,
            avatar=u.avatar or "default",
            total_xp=u.total_xp or 0,
            level=u.level or 1,
        )
        for i, u in enumerate(rows)
    ]
    return PaginatedResponse(items=items, total=total, page=page, per_page=per_page)


@router.get("/users/me/badges", response_model=list[BadgeOut])
def my_badges(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[BadgeOut]:
    rows = (
        db.query(Badge, UserBadge)
        .join(UserBadge, UserBadge.badge_id == Badge.id)
        .filter(UserBadge.user_id == user.id)
        .all()
    )
    out: list[BadgeOut] = []
    for b, ub in rows:
        out.append(
            BadgeOut(
                id=b.id,
                name=b.name,
                description=b.description,
                icon=b.icon,
                earned_at=ub.earned_at,
            )
        )
    return out


@router.get("/users/me/streak", response_model=StreakOut)
def my_streak(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> StreakOut:
    s = db.query(Streak).filter(Streak.user_id == user.id).first()
    if not s:
        return StreakOut(current_streak=0, longest_streak=0, last_active_date=None)
    return StreakOut(
        current_streak=s.current_streak or 0,
        longest_streak=s.longest_streak or 0,
        last_active_date=s.last_active_date,
    )


@router.get("/users/me/milestones", response_model=list[MilestoneOut])
def milestones(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[MilestoneOut]:
    rows = (
        db.query(UserMilestone)
        .filter(UserMilestone.user_id == user.id, UserMilestone.seen.is_(False))
        .order_by(UserMilestone.created_at.desc())
        .all()
    )
    return [
        MilestoneOut(
            id=m.id,
            milestone_type=m.milestone_type,
            milestone_value=m.milestone_value,
            seen=m.seen or False,
            created_at=m.created_at,
        )
        for m in rows
    ]


@router.post("/users/me/milestones/{milestone_id}/seen")
def mark_milestone_seen(
    milestone_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    m = db.get(UserMilestone, milestone_id)
    if not m or m.user_id != user.id:
        raise HTTPException(status_code=404, detail="Milestone not found")
    m.seen = True
    db.commit()
    return {"ok": True}


@router.get("/users/me/inventory", response_model=list[InventoryItemOut])
def inventory(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[InventoryItemOut]:
    rows = (
        db.query(UserInventory, ItemType)
        .join(ItemType, ItemType.id == UserInventory.item_type_id)
        .filter(UserInventory.user_id == user.id)
        .all()
    )
    return [
        InventoryItemOut(
            item_type_id=it.id,
            name=it.name,
            quantity=inv.quantity or 0,
            cost_xp=it.cost_xp,
        )
        for inv, it in rows
    ]


@router.post("/users/me/inventory/buy", response_model=BuyResponse)
def buy_item(
    body: BuyBody,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> BuyResponse:
    it = db.get(ItemType, body.item_type_id)
    if not it:
        raise HTTPException(status_code=404, detail="Item not found")
    cost = it.cost_xp
    if (user.total_xp or 0) < cost:
        raise HTTPException(status_code=400, detail="Insufficient XP")
    xp_service.award_xp(db, user_id=user.id, amount=-cost, source="shop_purchase")
    inv = (
        db.query(UserInventory)
        .filter(UserInventory.user_id == user.id, UserInventory.item_type_id == it.id)
        .first()
    )
    if inv is None:
        inv = UserInventory(
            id=uuid.uuid4(),
            user_id=user.id,
            item_type_id=it.id,
            quantity=1,
        )
        db.add(inv)
    else:
        inv.quantity = (inv.quantity or 0) + 1
    db.commit()
    db.refresh(user)
    db.refresh(inv)
    return BuyResponse(success=True, new_xp_total=user.total_xp or 0, item_quantity=inv.quantity or 0)


@router.post("/users/me/inventory/use", response_model=UseItemResponse)
def use_item(
    body: UseItemBody,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> UseItemResponse:
    inv = (
        db.query(UserInventory)
        .filter(UserInventory.user_id == user.id, UserInventory.item_type_id == body.item_type_id)
        .first()
    )
    if not inv or (inv.quantity or 0) < 1:
        raise HTTPException(status_code=400, detail="No items to use")
    inv.quantity = (inv.quantity or 0) - 1
    from app.models import ItemUsageLog

    db.add(
        ItemUsageLog(
            id=uuid.uuid4(),
            user_id=user.id,
            item_type_id=body.item_type_id,
            context=body.context,
        )
    )
    db.commit()
    db.refresh(inv)
    return UseItemResponse(success=True, remaining_quantity=inv.quantity or 0)
