import uuid
from datetime import datetime

from pydantic import BaseModel


class SubjectOut(BaseModel):
    id: uuid.UUID
    name: str
    icon: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class GradeOut(BaseModel):
    id: uuid.UUID
    subject_id: uuid.UUID
    name: str
    level: int
    created_at: datetime

    model_config = {"from_attributes": True}


class SectionBrief(BaseModel):
    id: uuid.UUID
    name: str
    section_number: str | None
    order: int


class ChapterDetail(BaseModel):
    id: uuid.UUID
    grade_id: uuid.UUID
    name: str
    description: str | None
    order: int
    icon: str | None
    sections: list[SectionBrief]


class ChapterMapSection(BaseModel):
    id: uuid.UUID
    name: str
    section_number: str | None
    order: int
    status: str
    stars_earned: int
    stars_possible: int


class ChapterMapOut(BaseModel):
    chapter_id: uuid.UUID
    sections: list[ChapterMapSection]


class TopicOut(BaseModel):
    id: uuid.UUID
    section_id: uuid.UUID
    name: str
    difficulty: int
    order: int

    model_config = {"from_attributes": True}


class ConceptCardOut(BaseModel):
    id: uuid.UUID
    title: str
    content_html: str
    order: int


class WorkedExampleOut(BaseModel):
    id: uuid.UUID
    title: str
    steps_json: list
    order: int
    completed: bool = False


class LearnBundle(BaseModel):
    concept_cards: list[ConceptCardOut]
    worked_examples: list[WorkedExampleOut]
    real_world_hook: str | None
