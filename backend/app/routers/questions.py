import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Topic, User
from app.schemas.question import (
    CheckAnswerBody,
    CheckAnswerResponse,
    GeneratedQuestionItem,
    GenerateQuestionsBody,
    HintBody,
    HintResponse,
)
from app.services import questions_service
from app.services.questions_service import QuestionExpiredError

router = APIRouter()


@router.post("/topics/{topic_id}/questions", response_model=list[GeneratedQuestionItem])
def generate_questions(
    topic_id: uuid.UUID,
    body: GenerateQuestionsBody,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> list[GeneratedQuestionItem]:
    topic = db.get(Topic, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    items = questions_service.generate_questions_for_topic(
        db, user.id, topic_id, body.phase, body.count
    )
    db.commit()
    return [GeneratedQuestionItem.model_validate(i) for i in items]


@router.post("/questions/{generated_question_id}/check", response_model=CheckAnswerResponse)
def check_question(
    generated_question_id: uuid.UUID,
    body: CheckAnswerBody,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> CheckAnswerResponse:
    try:
        result = questions_service.check_answer(db, user.id, generated_question_id, body.user_answer)
        db.commit()
        return CheckAnswerResponse.model_validate(result)
    except LookupError:
        raise HTTPException(status_code=404, detail="Question not found")
    except QuestionExpiredError:
        raise HTTPException(status_code=410, detail="Question expired")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/questions/{generated_question_id}/hint", response_model=HintResponse)
def hint(
    generated_question_id: uuid.UUID,
    body: HintBody,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> HintResponse:
    try:
        text = questions_service.get_hint_text(db, user.id, generated_question_id, body.hint_number)
        db.commit()
        return HintResponse(hint_text=text)
    except LookupError:
        raise HTTPException(status_code=404, detail="Question not found")
    except QuestionExpiredError:
        raise HTTPException(status_code=410, detail="Question expired")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
