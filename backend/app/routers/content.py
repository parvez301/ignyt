import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import (
    Chapter,
    Grade,
    Section,
    Subject,
    Topic,
    User,
    UserSectionProgress,
)
from app.schemas.common import PaginatedResponse
from app.schemas.content import (
    ChapterDetail,
    ChapterMapOut,
    ChapterMapSection,
    GradeOut,
    SectionBrief,
    SubjectOut,
    TopicOut,
)
from app.services import progress_service

router = APIRouter()


@router.get("/subjects", response_model=PaginatedResponse[SubjectOut])
def list_subjects(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> PaginatedResponse[SubjectOut]:
    q = db.query(Subject).order_by(Subject.name)
    total = q.count()
    items = q.offset((page - 1) * per_page).limit(per_page).all()
    return PaginatedResponse(
        items=[SubjectOut.model_validate(i) for i in items],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get("/subjects/{subject_id}/grades", response_model=PaginatedResponse[GradeOut])
def list_grades(
    subject_id: uuid.UUID,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> PaginatedResponse[GradeOut]:
    q = db.query(Grade).filter(Grade.subject_id == subject_id).order_by(Grade.level)
    total = q.count()
    items = q.offset((page - 1) * per_page).limit(per_page).all()
    return PaginatedResponse(
        items=[GradeOut.model_validate(i) for i in items],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get("/grades/{grade_id}/chapters", response_model=PaginatedResponse[dict])
def list_chapters(
    grade_id: uuid.UUID,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> PaginatedResponse[dict]:
    q = db.query(Chapter).filter(Chapter.grade_id == grade_id).order_by(Chapter.order)
    total = q.count()
    items = q.offset((page - 1) * per_page).limit(per_page).all()
    return PaginatedResponse(
        items=[
            {
                "id": str(c.id),
                "name": c.name,
                "description": c.description,
                "order": c.order,
                "icon": c.icon,
            }
            for c in items
        ],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get("/chapters/{chapter_id}", response_model=ChapterDetail)
def chapter_detail(
    chapter_id: uuid.UUID,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> ChapterDetail:
    ch = db.get(Chapter, chapter_id)
    if not ch:
        raise HTTPException(status_code=404, detail="Chapter not found")
    sections = db.query(Section).filter(Section.chapter_id == chapter_id).order_by(Section.order).all()
    return ChapterDetail(
        id=ch.id,
        grade_id=ch.grade_id,
        name=ch.name,
        description=ch.description,
        order=ch.order,
        icon=ch.icon,
        sections=[
            SectionBrief(id=s.id, name=s.name, section_number=s.section_number, order=s.order)
            for s in sections
        ],
    )


@router.get("/chapters/{chapter_id}/map", response_model=ChapterMapOut)
def chapter_map(
    chapter_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ChapterMapOut:
    ch = db.get(Chapter, chapter_id)
    if not ch:
        raise HTTPException(status_code=404, detail="Chapter not found")
    progress_service.ensure_user_bootstrap(db, user.id)
    progress_service.refresh_unlocks(db, user.id)
    db.commit()
    sections = db.query(Section).filter(Section.chapter_id == chapter_id).order_by(Section.order).all()
    out_sections: list[ChapterMapSection] = []
    for s in sections:
        usp = (
            db.query(UserSectionProgress)
            .filter(UserSectionProgress.user_id == user.id, UserSectionProgress.section_id == s.id)
            .first()
        )
        out_sections.append(
            ChapterMapSection(
                id=s.id,
                name=s.name,
                section_number=s.section_number,
                order=s.order,
                status=usp.status if usp else "locked",
                stars_earned=usp.stars_earned if usp else 0,
                stars_possible=usp.stars_possible if usp else 0,
            )
        )
    return ChapterMapOut(chapter_id=chapter_id, sections=out_sections)


@router.get("/sections/{section_id}/topics", response_model=PaginatedResponse[TopicOut])
def list_topics(
    section_id: uuid.UUID,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> PaginatedResponse[TopicOut]:
    q = db.query(Topic).filter(Topic.section_id == section_id).order_by(Topic.order)
    total = q.count()
    items = q.offset((page - 1) * per_page).limit(per_page).all()
    return PaginatedResponse(
        items=[TopicOut.model_validate(i) for i in items],
        total=total,
        page=page,
        per_page=per_page,
    )
