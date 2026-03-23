from app.question_generators.base import (
    BaseQuestionGenerator,
    GeneratedQuestionData,
    ValidationResult,
)
from app.question_generators.ch1_s1_rationals import (
    ClassifyNumberGenerator,
    DragClassifyNumbersGenerator,
    FindRationalsBetweenGenerator,
    TrueFalseNumberTypesGenerator,
)
from app.question_generators.ch1_s2_irrationals import (
    ClassifyRationalIrrationalGenerator,
    IdentifyIrrationalsInSetGenerator,
    TrueFalseIrrationalsGenerator,
)
from app.question_generators.ch1_s3_decimals import (
    ConvertFractionToDecimalGenerator,
    ConvertRecurringToFractionGenerator,
    DecimalExpansionTypeGenerator,
    PredictDecimalPatternGenerator,
)
from app.question_generators.ch1_s4_operations import (
    AddSubtractSurdsGenerator,
    ClassifyAfterOperationGenerator,
    RationaliseDenominatorGenerator,
    SimplifySurdExpressionGenerator,
)
from app.question_generators.ch1_s5_exponents import (
    ApplyExponentLawGenerator,
    EvaluateFractionalExponentGenerator,
    SimplifyExponentExpressionGenerator,
)

ALL_GENERATORS: list[type[BaseQuestionGenerator]] = [
    ClassifyNumberGenerator,
    FindRationalsBetweenGenerator,
    TrueFalseNumberTypesGenerator,
    DragClassifyNumbersGenerator,
    ClassifyRationalIrrationalGenerator,
    IdentifyIrrationalsInSetGenerator,
    TrueFalseIrrationalsGenerator,
    DecimalExpansionTypeGenerator,
    ConvertFractionToDecimalGenerator,
    ConvertRecurringToFractionGenerator,
    PredictDecimalPatternGenerator,
    SimplifySurdExpressionGenerator,
    RationaliseDenominatorGenerator,
    ClassifyAfterOperationGenerator,
    AddSubtractSurdsGenerator,
    EvaluateFractionalExponentGenerator,
    SimplifyExponentExpressionGenerator,
    ApplyExponentLawGenerator,
]

GENERATOR_REGISTRY: dict[str, type[BaseQuestionGenerator]] = {
    cls.generator_key: cls for cls in ALL_GENERATORS
}


def get_generator(key: str) -> type[BaseQuestionGenerator] | None:
    return GENERATOR_REGISTRY.get(key)


__all__ = [
    "ALL_GENERATORS",
    "GENERATOR_REGISTRY",
    "BaseQuestionGenerator",
    "GeneratedQuestionData",
    "ValidationResult",
    "get_generator",
]
