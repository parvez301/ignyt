"""Section 1.3 — Decimal expansions."""

from __future__ import annotations

import random
from fractions import Fraction

from app.question_generators.base import (
    BaseQuestionGenerator,
    GeneratedQuestionData,
    ValidationResult,
)


class DecimalExpansionTypeGenerator(BaseQuestionGenerator):
    generator_key = "decimal_expansion_type"

    def generate(self, difficulty: int) -> GeneratedQuestionData:
        # terminating vs recurring
        if random.random() < 0.5:
            p, q = 3, 8  # 0.375 terminating
            ans = "terminating"
        else:
            p, q = 1, 3
            ans = "recurring"
        qhtml = f"What kind of decimal expansion does \\(\\frac{{{p}}}{{{q}}}\\) have?"
        options = ["terminating", "recurring"]
        random.shuffle(options)
        return GeneratedQuestionData(
            question_html=qhtml,
            correct_answer=ans,
            options=options,
            params={"p": p, "q": q, "answer": ans},
        )

    def validate(self, params: dict, user_answer: str) -> ValidationResult:
        ca = params["answer"]
        ua = user_answer.strip().lower()
        ok = ua == ca
        return ValidationResult(
            ok,
            ca,
            None if ok else "decimal_type",
            None
            if ok
            else "Here's the trick: after fully simplifying, if the denominator (in lowest terms) has only factors 2 and 5, the decimal terminates.",
        )

    def get_hints(self, params: dict) -> list[str]:
        return [
            "Write the fraction in lowest terms and factor the denominator.",
            "Only factors 2 and 5 → terminating; any other prime → recurring.",
            f"For \\(\\frac{{{params['p']}}}{{{params['q']}}}\\), factor {params['q']}.",
        ]


class ConvertFractionToDecimalGenerator(BaseQuestionGenerator):
    generator_key = "convert_fraction_to_decimal"

    def generate(self, difficulty: int) -> GeneratedQuestionData:
        p, q = random.choice([(1, 4), (3, 8), (2, 5), (1, 8)])
        val = float(Fraction(p, q))
        ans = str(val).rstrip("0").rstrip(".") if "." in str(val) else str(val)
        if ans.endswith("."):
            ans = ans[:-1]
        qhtml = f"Express \\(\\frac{{{p}}}{{{q}}}\\) as a decimal."
        return GeneratedQuestionData(
            question_html=qhtml,
            correct_answer=ans,
            options=None,
            params={"p": p, "q": q, "answer": ans},
        )

    def validate(self, params: dict, user_answer: str) -> ValidationResult:
        ca = params["answer"]
        ua = self.normalize_numeric_answer(user_answer)
        ok = self.symbolic_equal(ua, ca) or ua == ca
        return ValidationResult(
            ok,
            ca,
            None if ok else "conversion",
            None if ok else "Almost! Divide numerator by denominator carefully.",
        )

    def get_hints(self, params: dict) -> list[str]:
        return [
            "Perform long division or convert denominator to a power of 10 if possible.",
            "Try multiplying top and bottom to get 10, 100, 1000...",
            f"The exact value here is {params['answer']}.",
        ]


class ConvertRecurringToFractionGenerator(BaseQuestionGenerator):
    generator_key = "convert_recurring_to_fraction"

    def generate(self, difficulty: int) -> GeneratedQuestionData:
        # 0.(12) = 12/99 = 4/33
        num = random.choice([12, 45, 36])
        den = 99
        f = Fraction(num, den)
        ans = f"{f.numerator}/{f.denominator}"
        qhtml = f"Write \\(0.\\overline{{{num:02d}}}\\) as a fraction \\(p/q\\) in lowest terms."
        return GeneratedQuestionData(
            question_html=qhtml,
            correct_answer=ans,
            options=None,
            params={"rep": num, "answer": ans},
        )

    def validate(self, params: dict, user_answer: str) -> ValidationResult:
        ca = params["answer"]
        ua = user_answer.strip().replace(" ", "")
        ok = self.symbolic_equal(ua, ca) or ua == ca
        return ValidationResult(
            ok,
            f"\\({ca}\\)",
            None if ok else "recurring_convert",
            None if ok else "Common mix-up: use \\(x=0.\\overline{ab}\\), multiply by \\(10^n\\), subtract, solve.",
        )

    def get_hints(self, params: dict) -> list[str]:
        return [
            "Let \\(x\\) be the repeating decimal, multiply by \\(10^n\\) where \\(n\\) is period length.",
            "Subtract to eliminate the repeating tail.",
            "Reduce the fraction at the end.",
        ]


class PredictDecimalPatternGenerator(BaseQuestionGenerator):
    generator_key = "predict_decimal_pattern"

    def generate(self, difficulty: int) -> GeneratedQuestionData:
        # 4/7 = 0.571428571... → first two digits after decimal: 57
        ans = "57"
        qhtml = (
            "The decimal expansion of \\(1/7\\) repeats \\(0.\\overline{142857}\\). "
            "What are the **first two digits after the decimal point** of \\(4/7\\)?"
        )
        return GeneratedQuestionData(
            question_html=qhtml,
            correct_answer=ans,
            options=None,
            params={"answer": ans},
        )

    def validate(self, params: dict, user_answer: str) -> ValidationResult:
        ca = params["answer"]
        ua = self.normalize_numeric_answer(user_answer)
        ok = ua == ca
        return ValidationResult(
            ok,
            ca,
            None if ok else "pattern",
            None if ok else "Almost! The same 6-digit cycle rotates — shift the starting point for \\(4/7\\).",
        )

    def get_hints(self, params: dict) -> list[str]:
        return [
            "Multiplying the fraction shifts where the repeating cycle starts.",
            "Write a few digits of \\(4/7\\) by long division or scaling \\(1/7\\).",
            "The repeating block length for \\(1/7\\) is 6.",
        ]
