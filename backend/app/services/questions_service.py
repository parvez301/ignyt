import random
import uuid
from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from app.models import GeneratedQuestion, QuestionAttempt, QuestionTemplate
from app.question_generators import get_generator
from app.services import streak_service, xp_service


class QuestionExpiredError(Exception):
    pass


def _hints_used_from_params(params: dict) -> int:
    return int(params.get("_hints_used", 0) or 0)


def _set_hints_used(params: dict, n: int) -> dict:
    out = dict(params)
    out["_hints_used"] = n
    return out


def generate_questions_for_topic(
    db: Session,
    user_id: uuid.UUID,
    topic_id: uuid.UUID,
    phase: str,
    count: int,
) -> list[dict]:
    templates = (
        db.query(QuestionTemplate).filter(QuestionTemplate.topic_id == topic_id).all()
    )
    if not templates:
        return []
    out: list[dict] = []
    expires_at = datetime.now(UTC) + timedelta(hours=1)
    for _ in range(min(count, 20)):
        tmpl = random.choice(templates)
        gen_cls = get_generator(tmpl.generator_key)
        if gen_cls is None:
            continue
        gen = gen_cls()
        data = gen.generate(tmpl.difficulty)
        params = dict(data.params)
        params.pop("_hints_used", None)
        gq = GeneratedQuestion(
            id=uuid.uuid4(),
            user_id=user_id,
            question_template_id=tmpl.id,
            params_json=params,
            correct_answer=data.correct_answer,
            question_html=data.question_html,
            options_json=data.options,
            phase=phase,
            answered=False,
            expires_at=expires_at,
        )
        db.add(gq)
        db.flush()
        item = {
            "generated_question_id": str(gq.id),
            "type": tmpl.type,
            "question_html": data.question_html,
        }
        if data.options is not None:
            item["options"] = data.options
        out.append(item)
    db.flush()
    return out


def get_hint_text(
    db: Session,
    user_id: uuid.UUID,
    generated_question_id: uuid.UUID,
    hint_number: int,
) -> str:
    if hint_number not in (1, 2, 3):
        raise ValueError("hint_number must be 1, 2, or 3")
    gq = db.get(GeneratedQuestion, generated_question_id)
    if gq is None or gq.user_id != user_id:
        raise LookupError("Question not found")
    if datetime.now(UTC) > gq.expires_at:
        raise QuestionExpiredError
    tmpl = db.get(QuestionTemplate, gq.question_template_id)
    if tmpl is None:
        raise LookupError("Template missing")
    gen_cls = get_generator(tmpl.generator_key)
    hints: list[str] = []
    if gen_cls:
        hints = gen_cls().get_hints(gq.params_json) or []
    if len(hints) < 3:
        base = tmpl.hints_json if isinstance(tmpl.hints_json, list) else []
        while len(hints) < 3 and len(base) > len(hints):
            hints.append(base[len(hints)])
    while len(hints) < 3:
        hints.append("Take a breath — break the problem into a smaller step.")
    idx = hint_number - 1
    new_params = _set_hints_used(gq.params_json, max(_hints_used_from_params(gq.params_json), hint_number))
    gq.params_json = new_params
    db.flush()
    return hints[idx]


def check_answer(
    db: Session,
    user_id: uuid.UUID,
    generated_question_id: uuid.UUID,
    user_answer: str,
    time_taken_seconds: int | None = None,
) -> dict:
    gq = db.get(GeneratedQuestion, generated_question_id)
    if gq is None or gq.user_id != user_id:
        raise LookupError("Question not found")
    if datetime.now(UTC) > gq.expires_at:
        raise QuestionExpiredError
    if gq.answered:
        raise ValueError("Already answered")

    tmpl = db.get(QuestionTemplate, gq.question_template_id)
    if tmpl is None:
        raise LookupError("Template missing")
    gen_cls = get_generator(tmpl.generator_key)
    if gen_cls is None:
        raise ValueError("Unknown generator")

    result = gen_cls().validate(gq.params_json, user_answer)
    hints_used = _hints_used_from_params(gq.params_json)

    attempt = QuestionAttempt(
        id=uuid.uuid4(),
        user_id=user_id,
        question_template_id=tmpl.id,
        generated_question_id=generated_question_id,
        params_json=gq.params_json,
        user_answer=user_answer,
        correct_answer=gq.correct_answer,
        is_correct=result.is_correct,
        misconception_key=result.misconception_key,
        hints_used=hints_used,
        time_taken_seconds=time_taken_seconds,
    )
    db.add(attempt)

    xp_earned = 0
    if result.is_correct:
        base_xp = {"practice": 10, "master": 20, "daily_challenge": 15, "review": 5}
        xp_earned += base_xp.get(gq.phase, 10)
        if hints_used == 0:
            xp_earned += 5
        prev_streak = streak_service.consecutive_correct_count(db, user_id)
        if prev_streak >= 2:
            xp_earned += 10
        streak_service.touch_activity_on_correct_answer(db, user_id)
        xp_service.award_xp(
            db,
            user_id=user_id,
            amount=xp_earned,
            source="question",
            topic_id=tmpl.topic_id,
        )

    gq.answered = True
    db.flush()

    misconception_explanation = result.misconception_explanation
    if not result.is_correct and tmpl.misconceptions_json and result.misconception_key:
        mj = tmpl.misconceptions_json
        if isinstance(mj, dict) and result.misconception_key in mj:
            misconception_explanation = str(mj[result.misconception_key])

    return {
        "is_correct": result.is_correct,
        "correct_answer_html": result.correct_answer_html,
        "misconception_explanation": misconception_explanation,
        "xp_earned": xp_earned,
        "hints_used": hints_used,
    }
