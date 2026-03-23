"""Section 1.1 — Rational numbers."""

from __future__ import annotations

import random
from fractions import Fraction

from app.question_generators.base import (
    BaseQuestionGenerator,
    GeneratedQuestionData,
    ValidationResult,
)


def _kfrac(a: int, b: int) -> str:
    return f"\\(\\frac{{{a}}}{{{b}}}\\)"


class ClassifyNumberGenerator(BaseQuestionGenerator):
    generator_key = "classify_number"

    _SETS = ["N", "W", "Z", "Q"]

    def generate(self, difficulty: int) -> GeneratedQuestionData:
        # Pick a number type scenario
        kind = random.choice(["natural", "whole_non_natural", "int_neg", "rational_non_int"])
        if kind == "natural":
            n = random.randint(1, 20)
            num, correct = n, "N"
            qhtml = f"Which set does \\( {n} \\) belong to <strong>first</strong> (most specific usual classification in NCERT)?"
        elif kind == "whole_non_natural":
            num, correct = 0, "W"
            qhtml = "Which set does \\( 0 \\) belong to among these choices?"
        elif kind == "int_neg":
            num = -random.randint(1, 15)
            correct = "Z"
            qhtml = f"Which set does \\( {num} \\) belong to?"
        else:
            a, b = random.randint(1, 5), random.randint(2, 7)
            if a >= b:
                a, b = b, a + 1
            num = f"{a}/{b}"
            correct = "Q"
            qhtml = f"Which set does \\(\\frac{{{a}}}{{{b}}}\\) belong to?"

        options = list(self._SETS)
        random.shuffle(options)
        misconceptions = {
            "N": "Almost! Remember \\(0\\) is whole but not natural, and fractions live in \\(\\mathbb{Q}\\).",
            "W": "Common mix-up: whole numbers include \\(0\\), naturals start at \\(1\\).",
            "Z": "Here's the trick: integers are whole positives, negatives, and zero — fractions need \\(\\mathbb{Q}\\).",
            "Q": "Nice catch — rationals can be written as \\(p/q\\) with integers \\(q \\neq 0\\).",
        }
        return GeneratedQuestionData(
            question_html=qhtml,
            correct_answer=correct,
            options=options,
            params={"number_repr": str(num), "correct_set": correct},
            misconception_map={k: misconceptions[k] for k in options if k != correct},
        )

    def validate(self, params: dict, user_answer: str) -> ValidationResult:
        correct = params["correct_set"]
        ua = user_answer.strip().upper()
        is_ok = ua == correct
        misconception_map = {
            "N": "Almost! Remember \\(0\\) is whole but not natural, and fractions live in \\(\\mathbb{Q}\\).",
            "W": "Common mix-up: whole numbers include \\(0\\), naturals start at \\(1\\).",
            "Z": "Here's the trick: integers are whole positives, negatives, and zero — fractions need \\(\\mathbb{Q}\\).",
            "Q": "Nice rethink — rationals can be written as \\(p/q\\) with \\(q \\neq 0\\).",
        }
        if is_ok:
            return ValidationResult(True, correct, None, None)
        mc = ua if ua in misconception_map else "unknown"
        exp = misconception_map.get(ua, "Let's look at the definition again — you've got this.")
        return ValidationResult(False, correct, mc, exp)

    def get_hints(self, params: dict) -> list[str]:
        return [
            "Think: can it be written as a fraction with integer numerator and denominator?",
            "Naturals: counting numbers. Wholes: include 0. Integers: include negatives.",
            f"The intended answer for this card is \\(\\mathbf{{{params['correct_set']}}}\\) — check which definition fits best.",
        ]


class FindRationalsBetweenGenerator(BaseQuestionGenerator):
    generator_key = "find_rationals_between"

    def generate(self, difficulty: int) -> GeneratedQuestionData:
        a, c = random.randint(1, 4), random.randint(5, 9)
        b, d = random.randint(2, 6), random.randint(2, 6)
        left = Fraction(a, b)
        right = Fraction(c, d)
        if left >= right:
            left, right = right, left
        mid = (left + right) / 2
        ans = f"{mid.numerator}/{mid.denominator}"
        qhtml = (
            f"Give <strong>one</strong> rational number strictly between {_kfrac(left.numerator, left.denominator)} "
            f"and {_kfrac(right.numerator, right.denominator)}. Write it as a fraction \\(p/q\\) in lowest terms."
        )
        return GeneratedQuestionData(
            question_html=qhtml,
            correct_answer=ans,
            options=None,
            params={
                "left": [left.numerator, left.denominator],
                "right": [right.numerator, right.denominator],
                "mid": ans,
            },
        )

    def validate(self, params: dict, user_answer: str) -> ValidationResult:
        mid = params["mid"]
        ua = user_answer.strip().replace(" ", "")
        ok = self.symbolic_equal(ua, mid) or ua == mid
        return ValidationResult(ok, f"\\({mid}\\)", None if ok else "not_between", None if ok else "Almost! Try averaging the two fractions after writing them with a common denominator.")

    def get_hints(self, params: dict) -> list[str]:
        return [
            "Average the two endpoints: \\(\\frac{a}{b}\\) and \\(\\frac{c}{d}\\) → add and divide by 2.",
            "Same denominator makes comparison easier.",
            f"A concrete answer that works here is \\({params['mid']}\\).",
        ]


class TrueFalseNumberTypesGenerator(BaseQuestionGenerator):
    generator_key = "true_false_number_types"

    STATEMENTS = [
        ("Every natural number is a whole number.", True),
        ("Every whole number is a natural number.", False),
        ("Every integer is a rational number.", True),
        ("Every rational number is an integer.", False),
    ]

    def generate(self, difficulty: int) -> GeneratedQuestionData:
        stmt, ok = random.choice(self.STATEMENTS)
        qhtml = f"True or false? {stmt}"
        return GeneratedQuestionData(
            question_html=qhtml,
            correct_answer="true" if ok else "false",
            options=["true", "false"],
            params={"statement": stmt, "correct_bool": ok},
            misconception_map={
                "wrong_tf": "Common mix-up: check whether **every** example works, especially edge cases like \\(0\\).",
            },
        )

    def validate(self, params: dict, user_answer: str) -> ValidationResult:
        ca = "true" if params["correct_bool"] else "false"
        ua = user_answer.strip().lower()
        is_ok = ua == ca
        return ValidationResult(
            is_ok,
            ca,
            None if is_ok else "wrong_tf",
            None if is_ok else "Almost! Try one concrete example — edge cases like \\(0\\) often decide it.",
        )

    def get_hints(self, params: dict) -> list[str]:
        return [
            "Try examples: \\(0\\), \\(1\\), a fraction like \\(\\frac12\\).",
            "If even one counterexample exists, a 'for every' statement is false.",
            "Compare definitions of \\(\\mathbb{N}\\), \\(\\mathbb{W}\\), \\(\\mathbb{Z}\\), \\(\\mathbb{Q}\\).",
        ]


class DragClassifyNumbersGenerator(BaseQuestionGenerator):
    generator_key = "drag_classify_numbers"

    def generate(self, difficulty: int) -> GeneratedQuestionData:
        mapping = {
            "3": "N",
            "0": "W",
            "-2": "Z",
            "1/2": "Q",
            "sqrt(2)": "R",
        }
        nums = list(mapping.keys())
        random.shuffle(nums)
        qhtml = (
            "Drag each number into the correct bag: "
            "\\(N, W, Z, Q, R\\). Use JSON like "
            '`{"3":"N",...}` with keys exactly as: '
            + ", ".join(nums)
            + "."
        )
        options = {"bags": ["N", "W", "Z", "Q", "R"], "items": nums}
        import json

        correct = json.dumps(mapping, sort_keys=True)
        return GeneratedQuestionData(
            question_html=qhtml,
            correct_answer=correct,
            options=options,
            params={"mapping": mapping},
        )

    def validate(self, params: dict, user_answer: str) -> ValidationResult:
        import json

        expected = params["mapping"]
        try:
            submitted = json.loads(user_answer)
        except json.JSONDecodeError:
            return ValidationResult(
                False,
                json.dumps(expected, sort_keys=True),
                "bad_format",
                "Almost! Send your answer as JSON mapping item → set label.",
            )
        ok = submitted == expected
        return ValidationResult(
            ok,
            json.dumps(expected, sort_keys=True),
            None if ok else "misclassified",
            None
            if ok
            else "Common mix-up: \\(\\sqrt{2}\\) is not rational; \\(0\\) is whole but not natural.",
        )

    def get_hints(self, params: dict) -> list[str]:
        return [
            "Start with fractions: if it is \\(p/q\\) with integers, it is rational.",
            "\\(0\\) is a whole number; natural numbers usually start at \\(1\\).",
            "Irrationals like \\(\\sqrt{2}\\) are real but not rational — use bag R or a separate irrational slot if provided.",
        ]
