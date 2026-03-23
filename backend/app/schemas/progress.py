from pydantic import BaseModel, Field


class CompletePhaseBody(BaseModel):
    phase: str = Field(pattern="^(learn|practice|master)$")
    score: int | None = Field(default=None, ge=0, le=100)


class CompletePhaseResponse(BaseModel):
    new_phase: str
    stars: int
    xp_earned: int
    badges_earned: list[str]
    milestones: list[dict]


class MeProgressOut(BaseModel):
    total_xp: int
    level: int
    streak_current: int
    streak_longest: int
    total_stars: int


class ChapterProgressBreakdown(BaseModel):
    chapter_id: str
    chapter_name: str
    sections: list[dict]
