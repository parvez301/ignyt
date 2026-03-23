"""Section 1.4 — Operations on real numbers / surds."""

from __future__ import annotations

import random

from sympy import sympify

from app.question_generators.base import (
    BaseQuestionGenerator,
    GeneratedQuestionData,
    ValidationResult,
)


class SimplifySurdExpressionGenerator(BaseQuestionGenerator):
    generator_key = "simplify_surd_expression"

    def generate(self, difficulty: int) -> GeneratedQuestionData:
        a, b = random.randint(1, 3), random.choice([2, 3, 5])
        c, d = random.randint(1, 3), random.choice([2, 3, 5])
        expr = f"({a}+sqrt({b}))*({c}+sqrt({d}))"
        expanded = sympify(f"({a}+sqrt({b}))*({c}+sqrt({d}))").simplify()
        ans = str(expanded).replace("**", "^").replace("*", "")
        # sympy uses sqrt(2) style
        ans = str(expanded)
        qhtml = f"Simplify \\(({a}+\\sqrt{{{b}}})({c}+\\sqrt{{{d}}})\\). Use `sqrt(n)` in your answer if needed."
        return GeneratedQuestionData(
            question_html=qhtml,
            correct_answer=ans,
            options=None,
            params={"expr": expr, "answer": ans},
        )

    def validate(self, params: dict, user_answer: str) -> ValidationResult:
        ca = params["answer"]
        ok = self.symbolic_equal(user_answer, ca)
        return ValidationResult(
            ok,
            f"\\({ca}\\)",
            None if ok else "surd_expand",
            None if ok else "Almost! Expand with distributive property and use \\(\\sqrt{a}\\sqrt{b}=\\sqrt{ab}\\) when helpful.",
        )

    def get_hints(self, params: dict) -> list[str]:
        return [
            "Use FOIL / distributive multiplication.",
            "Combine like surd terms at the end.",
            "Watch for \\(\\sqrt{m}\\sqrt{n}=\\sqrt{mn}\\).",
        ]


class RationaliseDenominatorGenerator(BaseQuestionGenerator):
    generator_key = "rationalise_denominator"

    def generate(self, difficulty: int) -> GeneratedQuestionData:
        a = random.randint(1, 4)
        b = random.choice([2, 3, 5, 7])
        # 1/(a+sqrt(b)) * (a-sqrt(b))/(a-sqrt(b))
        from sympy import simplify as s

        val = s(1 / sympify(f"{a}+sqrt({b})"))
        ans = str(val)
        qhtml = f"Rationalise the denominator: \\(\\frac{{1}}{{{a}+\\sqrt{{{b}}}}}\\). Use `sqrt(n)` in your answer."
        return GeneratedQuestionData(
            question_html=qhtml,
            correct_answer=ans,
            options=None,
            params={"a": a, "b": b, "answer": ans},
        )

    def validate(self, params: dict, user_answer: str) -> ValidationResult:
        ca = params["answer"]
        ok = self.symbolic_equal(user_answer, ca)
        return ValidationResult(
            ok,
            f"\\({ca}\\)",
            None if ok else "rationalise",
            None if ok else "Here's the trick: multiply top and bottom by the conjugate \\(a-\\sqrt{b}\\).",
        )

    def get_hints(self, params: dict) -> list[str]:
        return [
            "Multiply numerator and denominator by the conjugate.",
            "Denominator becomes a difference of squares: \\(a^2-b\\).",
            "Simplify the resulting fraction.",
        ]


class ClassifyAfterOperationGenerator(BaseQuestionGenerator):
    generator_key = "classify_after_operation"

    def generate(self, difficulty: int) -> GeneratedQuestionData:
        # sqrt(2)+sqrt(3) irrational
        qhtml = "Is \\(\\sqrt{2}+\\sqrt{3}\\) rational or irrational?"
        ans = "irrational"
        options = ["rational", "irrational"]
        random.shuffle(options)
        return GeneratedQuestionData(
            question_html=qhtml,
            correct_answer=ans,
            options=options,
            params={"answer": ans},
        )

    def validate(self, params: dict, user_answer: str) -> ValidationResult:
        ca = params["answer"]
        ua = user_answer.strip().lower()
        ok = ua == ca
        return ValidationResult(
            ok,
            ca,
            None if ok else "classify_op",
            None
            if ok
            else "Almost! A sum of two irrationals can be rational or irrational — this classic one stays irrational.",
        )

    def get_hints(self, params: dict) -> list[str]:
        return [
            "Assume it is rational and try squaring both sides — look for a contradiction.",
            "If it were rational, \\((\\sqrt2+\\sqrt3)^2\\) would be rational too — what happens?",
            "The standard proof shows \\(\\sqrt2+\\sqrt3\\) is irrational.",
        ]


class AddSubtractSurdsGenerator(BaseQuestionGenerator):
    generator_key = "add_subtract_surds"

    def generate(self, difficulty: int) -> GeneratedQuestionData:
        # 2√3 + 5√3 - √3 = 6√3
        r = 3
        qhtml = f"Simplify \\(2\\sqrt{{{r}}} + 5\\sqrt{{{r}}} - \\sqrt{{{r}}}\\)."
        ans = f"6*sqrt({r})"
        return GeneratedQuestionData(
            question_html=qhtml,
            correct_answer=ans,
            options=None,
            params={"r": r, "answer": ans},
        )

    def validate(self, params: dict, user_answer: str) -> ValidationResult:
        ca = params["answer"]
        ok = self.symbolic_equal(user_answer, ca)
        return ValidationResult(
            ok,
            f"\\(6\\sqrt{{{params['r']}}}\\)",
            None if ok else "combine_surds",
            None if ok else "Common mix-up: combine like surds — treat \\(\\sqrt{n}\\) like a variable token.",
        )

    def get_hints(self, params: dict) -> list[str]:
        r = params["r"]
        return [
            "Factor out \\(\\sqrt{" + str(r) + "}\\) like a common variable.",
            "Add the coefficients: \\(2+5-1\\).",
            "You should get a single surd term.",
        ]
