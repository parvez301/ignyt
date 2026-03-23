from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from sympy import simplify, sympify
from sympy.core.sympify import SympifyError


@dataclass
class GeneratedQuestionData:
    question_html: str
    correct_answer: str
    options: list[str] | dict | None
    params: dict
    misconception_map: dict[str, str] = field(default_factory=dict)


@dataclass
class ValidationResult:
    is_correct: bool
    correct_answer_html: str
    misconception_key: str | None
    misconception_explanation: str | None


class BaseQuestionGenerator(ABC):
    generator_key: str = ""

    @abstractmethod
    def generate(self, difficulty: int) -> GeneratedQuestionData:
        pass

    @abstractmethod
    def validate(self, params: dict, user_answer: str) -> ValidationResult:
        pass

    def get_hints(self, params: dict) -> list[str]:
        return []

    @staticmethod
    def symbolic_equal(user_answer: str, correct_answer: str) -> bool:
        try:
            user_expr = sympify(user_answer.strip())
            correct_expr = sympify(correct_answer.strip())
            return simplify(user_expr - correct_expr) == 0
        except (SympifyError, ValueError, TypeError, AttributeError):
            return False

    @staticmethod
    def normalize_numeric_answer(s: str) -> str:
        return s.strip().replace(" ", "")
