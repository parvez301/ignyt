import uuid
from datetime import date, datetime

from pydantic import BaseModel


class LeaderboardUser(BaseModel):
    rank: int
    user_id: uuid.UUID
    display_name: str
    avatar: str
    total_xp: int
    level: int


class BadgeOut(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    icon: str | None
    earned_at: datetime | None = None


class StreakOut(BaseModel):
    current_streak: int
    longest_streak: int
    last_active_date: date | None


class MilestoneOut(BaseModel):
    id: uuid.UUID
    milestone_type: str
    milestone_value: str | None
    seen: bool
    created_at: datetime


class InventoryItemOut(BaseModel):
    item_type_id: uuid.UUID
    name: str
    quantity: int
    cost_xp: int


class BuyBody(BaseModel):
    item_type_id: uuid.UUID


class BuyResponse(BaseModel):
    success: bool
    new_xp_total: int
    item_quantity: int


class UseItemBody(BaseModel):
    item_type_id: uuid.UUID
    context: str | None = None


class UseItemResponse(BaseModel):
    success: bool
    remaining_quantity: int
