from pydantic import BaseModel, Field


class GenerateQuestionsBody(BaseModel):
    phase: str = Field(pattern="^(practice|master|review|daily_challenge)$")
    count: int = Field(ge=1, le=20)


class GeneratedQuestionItem(BaseModel):
    generated_question_id: str
    type: str
    question_html: str
    options: list | dict | None = None


class CheckAnswerBody(BaseModel):
    user_answer: str


class CheckAnswerResponse(BaseModel):
    is_correct: bool
    correct_answer_html: str
    misconception_explanation: str | None = None
    xp_earned: int
    hints_used: int


class HintBody(BaseModel):
    hint_number: int = Field(ge=1, le=3)


class HintResponse(BaseModel):
    hint_text: str
