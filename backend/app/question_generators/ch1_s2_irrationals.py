"""Section 1.2 — Irrational numbers."""

from __future__ import annotations

import json
import random

from app.question_generators.base import (
    BaseQuestionGenerator,
    GeneratedQuestionData,
    ValidationResult,
)


class ClassifyRationalIrrationalGenerator(BaseQuestionGenerator):
    generator_key = "classify_rational_irrational"

    def generate(self, difficulty: int) -> GeneratedQuestionData:
        if random.random() < 0.5:
            n = random.choice([2, 3, 5, 7, 8])
            label = "irrational"
            qhtml = f"Is \\(\\sqrt{{{n}}}\\) rational or irrational? (Assume standard real roots.)"
        else:
            n = random.choice([4, 9, 16, 25])
            label = "rational"
            qhtml = f"Is \\(\\sqrt{{{n}}}\\) rational or irrational?"
        options = ["rational", "irrational"]
        random.shuffle(options)
        misconceptions = {
            "rational": "Almost! If it is not a perfect square, \\(\\sqrt{n}\\) is irrational.",
            "irrational": "Common mix-up: perfect squares give **rational** roots.",
        }
        return GeneratedQuestionData(
            question_html=qhtml,
            correct_answer=label,
            options=options,
            params={"n": n, "label": label},
            misconception_map=misconceptions,
        )

    def validate(self, params: dict, user_answer: str) -> ValidationResult:
        ca = params["label"]
        ua = user_answer.strip().lower()
        ok = ua == ca
        mm = {
            "rational": "Almost! If it is not a perfect square, \\(\\sqrt{n}\\) is irrational.",
            "irrational": "Common mix-up: perfect squares give rational roots.",
        }
        return ValidationResult(
            ok,
            ca,
            None if ok else ua,
            None if ok else mm.get(ua, "Here's the trick: check whether \\(n\\) is a perfect square."),
        )

    def get_hints(self, params: dict) -> list[str]:
        n = params["n"]
        return [
            "Is \\(n\\) a perfect square? If yes, the root is rational.",
            "If not, the square root is irrational (for non-square positive integers).",
            f"For this problem, \\(n={n}\\).",
        ]


class IdentifyIrrationalsInSetGenerator(BaseQuestionGenerator):
    generator_key = "identify_irrationals_in_set"

    def generate(self, difficulty: int) -> GeneratedQuestionData:
        items = [
            ("2", "rational"),
            ("\\sqrt{2}", "irrational"),
            ("\\frac{3}{4}", "rational"),
            ("\\pi", "irrational"),
        ]
        random.shuffle(items)
        irr = [t[0] for t in items if t[1] == "irrational"]
        qhtml = "Select **all** irrational numbers: " + ", ".join(f"\\({t[0]}\\)" for t in items)
        correct_payload = json.dumps(sorted(irr))
        return GeneratedQuestionData(
            question_html=qhtml,
            correct_answer=correct_payload,
            options=[t[0] for t in items],
            params={"items": items, "irrationals": irr},
        )

    def validate(self, params: dict, user_answer: str) -> ValidationResult:
        irr = sorted(params["irrationals"])
        try:
            parsed = json.loads(user_answer)
            if not isinstance(parsed, list):
                raise ValueError
            ua = sorted(parsed)
        except (json.JSONDecodeError, ValueError, TypeError):
            return ValidationResult(
                False,
                str(irr),
                "format",
                "Almost! Send a JSON array of the selected expressions as strings.",
            )
        ok = ua == irr
        return ValidationResult(
            ok,
            ", ".join(irr),
            None if ok else "missed_or_extra",
            None
            if ok
            else "Common mix-up: \\(\\pi\\) and \\(\\sqrt{2}\\) are irrational; fractions and integers are rational.",
        )

    def get_hints(self, params: dict) -> list[str]:
        return [
            "Irrationals cannot be written as \\(p/q\\) with integers \\(q\\neq 0\\).",
            "Famous irrationals: \\(\\sqrt{2}\\), \\(\\pi\\).",
            "Fractions and terminating/repeating decimals are rational.",
        ]


class TrueFalseIrrationalsGenerator(BaseQuestionGenerator):
    generator_key = "true_false_irrationals"

    PAIRS = [
        ("The sum of two irrationals is always irrational.", False),
        ("There are infinitely many irrational numbers between any two rationals.", True),
    ]

    def generate(self, difficulty: int) -> GeneratedQuestionData:
        stmt, ok = random.choice(self.PAIRS)
        return GeneratedQuestionData(
            question_html=f"True or false? {stmt}",
            correct_answer="true" if ok else "false",
            options=["true", "false"],
            params={"statement": stmt, "correct_bool": ok},
        )

    def validate(self, params: dict, user_answer: str) -> ValidationResult:
        ca = "true" if params["correct_bool"] else "false"
        ua = user_answer.strip().lower()
        ok = ua == ca
        return ValidationResult(
            ok,
            ca,
            None if ok else "wrong_tf",
            None
            if ok
            else "Almost! Try a concrete example — sometimes rationals hide inside sums of irrationals.",
        )

    def get_hints(self, params: dict) -> list[str]:
        return [
            "Try simple examples like \\(\\sqrt{2}\\) and \\(-\\sqrt{2}\\).",
            "Density of rationals/irrationals on the number line is a good intuition.",
            "If you find one counterexample, a universal 'always' claim is false.",
        ]
