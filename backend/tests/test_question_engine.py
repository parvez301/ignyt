"""Question generators: output validity, sympy validation, hints, misconceptions."""

import json

import pytest

from app.question_generators import ALL_GENERATORS, GENERATOR_REGISTRY


@pytest.mark.parametrize("cls", ALL_GENERATORS)
def test_generator_produces_valid_output(cls) -> None:
    gen = cls()
    for difficulty in (1, 2, 3):
        data = gen.generate(difficulty)
        assert data.question_html
        assert data.correct_answer is not None and str(data.correct_answer).strip() != ""
        assert isinstance(data.params, dict)


@pytest.mark.parametrize("key", sorted(GENERATOR_REGISTRY.keys()))
def test_validate_correct_and_wrong(key: str) -> None:
    cls = GENERATOR_REGISTRY[key]
    gen = cls()
    data = gen.generate(2)
    ok = gen.validate(data.params, str(data.correct_answer))
    assert ok.is_correct

    bad = gen.validate(data.params, "__definitely_not_the_answer__")
    assert not bad.is_correct


@pytest.mark.parametrize("key", sorted(GENERATOR_REGISTRY.keys()))
def test_hints_length_three(key: str) -> None:
    cls = GENERATOR_REGISTRY[key]
    gen = cls()
    data = gen.generate(2)
    hints = gen.get_hints(data.params)
    assert len(hints) == 3
    assert all(isinstance(h, str) and h.strip() for h in hints)


@pytest.mark.parametrize("key", sorted(GENERATOR_REGISTRY.keys()))
def test_misconception_keys_when_wrong(key: str) -> None:
    cls = GENERATOR_REGISTRY[key]
    gen = cls()
    data = gen.generate(2)
    bad = gen.validate(data.params, "__wrong__")
    if data.misconception_map:
        assert bad.misconception_key is not None
    # identify_irrationals expects JSON list
    if key == "identify_irrationals_in_set":
        bad2 = gen.validate(data.params, json.dumps([]))
        assert not bad2.is_correct
