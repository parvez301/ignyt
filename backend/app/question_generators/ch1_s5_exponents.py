"""Section 1.5 — Laws of exponents."""

from __future__ import annotations

import random

from app.question_generators.base import (
    BaseQuestionGenerator,
    GeneratedQuestionData,
    ValidationResult,
)


class EvaluateFractionalExponentGenerator(BaseQuestionGenerator):
    generator_key = "evaluate_fractional_exponent"

    def generate(self, difficulty: int) -> GeneratedQuestionData:
        base = random.choice([4, 8, 16, 27, 64])
        if base == 64:
            exp = "1/2"
            val = 8
        elif base == 27:
            exp = "1/3"
            val = 3
        elif base == 16:
            exp = "1/2"
            val = 4
        elif base == 8:
            exp = "1/3"
            val = 2
        else:
            exp = "1/2"
            val = 2
        qhtml = f"Evaluate \\({base}^{{{exp}}}\\)."
        ans = str(val)
        return GeneratedQuestionData(
            question_html=qhtml,
            correct_answer=ans,
            options=None,
            params={"base": base, "exp": exp, "answer": ans},
        )

    def validate(self, params: dict, user_answer: str) -> ValidationResult:
        ca = params["answer"]
        ok = self.symbolic_equal(user_answer, ca) or self.normalize_numeric_answer(user_answer) == ca
        return ValidationResult(
            ok,
            ca,
            None if ok else "frac_exp",
            None if ok else "Here's the trick: \\(a^{1/n}\\) is the \\(n\\)th root of \\(a\\).",
        )

    def get_hints(self, params: dict) -> list[str]:
        return [
            "Fractional exponent \\(1/n\\) means nth root.",
            "Find a number whose nth power returns the base.",
            f"For this base {params['base']}, think perfect powers.",
        ]


class SimplifyExponentExpressionGenerator(BaseQuestionGenerator):
    generator_key = "simplify_exponent_expression"

    def generate(self, difficulty: int) -> GeneratedQuestionData:
        # 2^(2/3)*2^(1/3)=2^1=2
        qhtml = "Simplify \\(2^{2/3} \\cdot 2^{1/3}\\)."
        ans = "2"
        return GeneratedQuestionData(
            question_html=qhtml,
            correct_answer=ans,
            options=None,
            params={"answer": ans},
        )

    def validate(self, params: dict, user_answer: str) -> ValidationResult:
        ca = params["answer"]
        ok = self.symbolic_equal(user_answer, ca)
        return ValidationResult(
            ok,
            ca,
            None if ok else "exp_law",
            None if ok else "Almost! When bases match, **add** the exponents.",
        )

    def get_hints(self, params: dict) -> list[str]:
        return [
            "Use \\(a^m \\cdot a^n = a^{m+n}\\).",
            "Add \\(\\frac{2}{3}+\\frac{1}{3}\\).",
            "The result is an integer power of 2.",
        ]


class ApplyExponentLawGenerator(BaseQuestionGenerator):
    generator_key = "apply_exponent_law"

    LABELS = {
        "power_of_product": "(ab)^n = a^n b^n",
        "product_of_powers": "a^m * a^n = a^(m+n)",
        "power_of_power": "(a^m)^n = a^(mn)",
        "quotient_rule": "a^m / a^n = a^(m-n)",
    }

    def generate(self, difficulty: int) -> GeneratedQuestionData:
        qhtml = "Which exponent law matches \\((ab)^n = a^n b^n\\)? Pick the **name** of the law."
        correct = "power_of_product"
        options = list(self.LABELS.keys())
        random.shuffle(options)
        display_opts = [self.LABELS[k] for k in options]
        return GeneratedQuestionData(
            question_html=qhtml,
            correct_answer=correct,
            options=display_opts,
            params={"correct_key": correct, "option_keys": options},
        )

    def validate(self, params: dict, user_answer: str) -> ValidationResult:
        ca = params["correct_key"]
        ua = user_answer.strip()
        rev = {v: k for k, v in self.LABELS.items()}
        ua_key = rev.get(ua, ua)
        ok = ua_key == ca
        return ValidationResult(
            ok,
            self.LABELS[ca],
            None if ok else ua_key,
            None
            if ok
            else "Almost! A product inside parentheses raised to a power splits across factors.",
        )

    def get_hints(self, params: dict) -> list[str]:
        return [
            "Check whether exponents distribute across multiplication inside parentheses.",
            "Contrast with adding exponents when bases match.",
            "The rule is \\((ab)^n = a^n b^n\\).",
        ]
