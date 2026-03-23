"""Seed NCERT Class 9 Maths Chapter 1 — Number Systems."""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import (
    Badge,
    Chapter,
    ConceptCard,
    Grade,
    ItemType,
    QuestionTemplate,
    RealWorldAnchor,
    Section,
    Subject,
    Topic,
    WorkedExample,
)

NS = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")


def uid(name: str) -> uuid.UUID:
    # Keep the original deterministic ID namespace stable so existing
    # seeded data doesn't get duplicated under a new UUID scheme.
    return uuid.uuid5(NS, "ignyt.ch1." + name)


def join_html(*parts: str) -> str:
    return " ".join(parts)


def _template(
    topic_id: uuid.UUID,
    type_: str,
    generator_key: str,
    difficulty: int,
    hints: list[str],
    misconceptions: dict | None = None,
) -> QuestionTemplate:
    return QuestionTemplate(
        id=uuid.uuid4(),
        topic_id=topic_id,
        type=type_,
        generator_key=generator_key,
        difficulty=difficulty,
        misconceptions_json=misconceptions,
        hints_json=hints,
        template_metadata=None,
    )


def seed_chapter1(db: Session) -> None:
    subject_id = uid("subject.math")
    grade_id = uid("grade.9")
    chapter_id = uid("chapter1")

    subject = db.get(Subject, subject_id) or Subject(id=subject_id, name="Mathematics", icon="calculator")
    grade = db.get(Grade, grade_id) or Grade(id=grade_id, subject_id=subject.id, name="Class 9", level=9)
    chapter = (
        db.get(Chapter, chapter_id)
        or Chapter(
            id=chapter_id,
            grade_id=grade.id,
            name="Number Systems",
            description="Rational, irrational, decimals, surds, exponents",
            order=1,
            icon="hash",
        )
    )

    # Add only if missing; re-runs should not duplicate.
    if db.get(Subject, subject_id) is None:
        db.add(subject)
    if db.get(Grade, grade_id) is None:
        db.add(grade)
    if db.get(Chapter, chapter_id) is None:
        db.add(chapter)

    hooks = [
        (
            uid("section.1.1"),
            "Every time you count your change — 1, 2, 3 rupees — you're using natural numbers. But what about splitting a pizza? That's where rationals come in.",
        ),
        (
            uid("section.1.2"),
            "Your phone screen is 6.1 inches diagonally. But the diagonal of a 1x1 inch square is \\(\\sqrt{2}\\) inches. You literally hold irrational numbers in your hand every day.",
        ),
        (
            uid("section.1.3"),
            "When you split 100 rupees equally among 3 friends, each gets 33.333... forever. That repeating pattern isn't a glitch — it's mathematics telling you 100 and 3 don't divide evenly.",
        ),
        (
            uid("section.1.4"),
            "Engineers building bridges need to calculate exact diagonal lengths like \\(\\sqrt{2}+\\sqrt{3}\\). They rationalise these expressions so designs stay exact and safe.",
        ),
        (
            uid("section.1.5"),
            "Computer storage: KB, MB, GB, TB — each step uses powers of 2. Understanding exponents is how you make sense of '128 GB' and beyond.",
        ),
    ]

    sections_spec: list[tuple[str, str, int, list[tuple[str, int, list[tuple]]]]] = [
        (
            "1.1 — Rational Numbers",
            "1.1",
            1,
            [
                (
                    "Classify numbers into N, W, Z, Q sets",
                    1,
                    [
                        ("classify_number", "mcq"),
                        ("drag_classify_numbers", "drag_drop"),
                        ("true_false_number_types", "true_false"),
                    ],
                ),
                (
                    "Find rational numbers between two given rationals",
                    2,
                    [("find_rationals_between", "fill_in")],
                ),
                (
                    "True/false statements about number types",
                    3,
                    [("true_false_number_types", "true_false")],
                ),
            ],
        ),
        (
            "1.2 — Irrational Numbers",
            "1.2",
            2,
            [
                (
                    "Identify rational vs irrational numbers",
                    1,
                    [("classify_rational_irrational", "mcq")],
                ),
                (
                    "Recognize perfect squares vs non-perfect squares under roots",
                    2,
                    [("identify_irrationals_in_set", "mcq")],
                ),
                (
                    "Properties of irrational numbers (true/false)",
                    3,
                    [("true_false_irrationals", "true_false")],
                ),
            ],
        ),
        (
            "1.3 — Decimal Expansions",
            "1.3",
            3,
            [
                (
                    "Terminating vs recurring decimals from fractions",
                    1,
                    [("decimal_expansion_type", "mcq")],
                ),
                (
                    "Decimal expansion by division",
                    2,
                    [("convert_fraction_to_decimal", "fill_in")],
                ),
                (
                    "Recurring decimal to p/q",
                    3,
                    [("convert_recurring_to_fraction", "fill_in")],
                ),
                (
                    "Predict decimal patterns (e.g. multiples of 1/7)",
                    4,
                    [("predict_decimal_pattern", "fill_in")],
                ),
            ],
        ),
        (
            "1.4 — Operations on Real Numbers",
            "1.4",
            4,
            [
                (
                    "Add and subtract surd expressions",
                    1,
                    [("add_subtract_surds", "fill_in")],
                ),
                (
                    "Multiply surd expressions",
                    2,
                    [("simplify_surd_expression", "fill_in")],
                ),
                (
                    "Use identities (a+√b)(a-√b)",
                    3,
                    [("simplify_surd_expression", "fill_in")],
                ),
                (
                    "Rationalise the denominator",
                    4,
                    [("rationalise_denominator", "fill_in"), ("classify_after_operation", "mcq")],
                ),
            ],
        ),
        (
            "1.5 — Laws of Exponents",
            "1.5",
            5,
            [
                (
                    "Evaluate numbers with fractional exponents",
                    1,
                    [("evaluate_fractional_exponent", "fill_in")],
                ),
                (
                    "Simplify using exponent laws",
                    2,
                    [("simplify_exponent_expression", "fill_in")],
                ),
                (
                    "Choose and apply the right exponent law",
                    3,
                    [("apply_exponent_law", "mcq")],
                ),
            ],
        ),
    ]

    db.add(subject)
    db.add(grade)
    db.add(chapter)

    section_rows: dict[str, Section] = {}
    topic_by_key: dict[str, Topic] = {}
    topic_qtypes_by_key: dict[str, list[str]] = {}
    pending_templates: list[QuestionTemplate] = []

    for sec_name, sec_num, sec_order, topics in sections_spec:
        sid = uid(f"section.{sec_num}")
        sec = db.get(Section, sid) or Section(
            id=sid,
            chapter_id=chapter.id,
            name=sec_name,
            section_number=sec_num,
            order=sec_order,
        )
        if db.get(Section, sid) is None:
            db.add(sec)
        section_rows[sec_num] = sec
        for tname, torder, gens in topics:
            topic_key = f"{sec_num}.{torder}"
            tid = uid(f"topic.{sec_num}.{torder}")
            top = db.get(Topic, tid) or Topic(
                id=tid,
                section_id=sid,
                name=tname,
                difficulty=min(3, 1 + (torder % 3)),
                order=torder,
            )
            if db.get(Topic, tid) is None:
                db.add(top)
            topic_by_key[topic_key] = top
            topic_qtypes_by_key[topic_key] = [qtype for _gkey, qtype in gens]
            hint_pack = [
                "Start with the definition — what family of numbers are we in?",
                "Try a small example or rewrite the expression.",
                "Compare with a known fact from the concept cards.",
            ]
            for gkey, qtype in gens:
                # Ensure templates exist once per topic/generator/type.
                existing_tpl = (
                    db.query(QuestionTemplate)
                    .filter(QuestionTemplate.topic_id == top.id)
                    .filter(QuestionTemplate.generator_key == gkey)
                    .filter(QuestionTemplate.type == qtype)
                    .first()
                )
                if existing_tpl is None:
                    pending_templates.append(_template(top.id, qtype, gkey, 2, hint_pack))

    # Flush parent rows (subject/grade/chapter/sections/topics/templates) before inserting
    # dependents like concept_cards and worked_examples. This avoids FK ordering issues
    # during the final flush/commit in Postgres.
    db.flush()

    # Add templates only after topics are flushed, so FK constraints are satisfiable.
    for tpl in pending_templates:
        db.add(tpl)
    db.flush()

    for sid, text in hooks:
        existing_anchor = db.query(RealWorldAnchor).filter(RealWorldAnchor.section_id == sid).first()
        if existing_anchor is None:
            db.add(RealWorldAnchor(id=uuid.uuid4(), section_id=sid, hook_text=text))

    # Concept cards + worked examples (sample per topic)
    def add_card(topic_key: str, title: str, html: str, order: int) -> None:
        top = topic_by_key[topic_key]
        existing = (
            db.query(ConceptCard)
            .filter(ConceptCard.topic_id == top.id)
            .filter(ConceptCard.order == order)
            .first()
        )
        if existing is None:
            db.add(
                ConceptCard(
                    id=uuid.uuid4(),
                    topic_id=top.id,
                    title=title,
                    content_html=html,
                    order=order,
                )
            )
        else:
            # Keep seed idempotent but also allow seed *updates* when content changes.
            existing.title = title
            existing.content_html = html
            existing.order = order

    def add_we(topic_key: str, title: str, steps: list[dict], order: int) -> None:
        top = topic_by_key[topic_key]
        existing = (
            db.query(WorkedExample)
            .filter(WorkedExample.topic_id == top.id)
            .filter(WorkedExample.order == order)
            .first()
        )
        if existing is None:
            db.add(
                WorkedExample(
                    id=uuid.uuid4(),
                    topic_id=top.id,
                    title=title,
                    steps_json=steps,
                    order=order,
                )
            )
        else:
            existing.title = title
            existing.steps_json = steps
            existing.order = order

    # NCERT-aligned (but condensed) learning content.
    # This seed updates existing cards/examples in-place (by (topic_id, order)).
    concepts_by_topic: dict[str, list[tuple[str, str]]] = {
        "1.1.1": [
            (
                "Number sets: N, W, Z, Q",
                "<p>You meet different collections of numbers on the number line.</p>"
                "<p><strong>Natural numbers</strong> are \\(1,2,3,\\dots\\) and we denote the set by \\(\\mathbb{N}\\).</p>"
                "<p><strong>Whole numbers</strong> include zero: \\(\\mathbb{W} = \\{0,1,2,3,\\dots\\}\\).</p>"
                "<p><strong>Integers</strong> include negatives: \\(\\mathbb{Z} = \\{..., -2,-1,0,1,2,...\\}\\).</p>"
                "<p><strong>Rational numbers</strong> are numbers of the form \\(\\frac{p}{q}\\) where \\(p,q\\) are integers and \\(q\\neq 0\\). We denote them by \\(\\mathbb{Q}\\).</p>"
                "<p>These sets are nested: \\(\\mathbb{N} \\subset \\mathbb{W} \\subset \\mathbb{Z} \\subset \\mathbb{Q}\\).</p>"
                "<p>New symbol note: \\(\\subset\\) means “is a subset of / is contained in”.</p>"
                "<p>So \\(\\mathbb{N} \\subset \\mathbb{W}\\) means every natural number is also a whole number.</p>",
            ),
            (
                "Quick classification rules",
                "<ul>"
                "<li>If a number is an integer and \\(\\ge 1\\), it belongs to \\(\\mathbb{N}\\) (natural).</li>"
                "<li>If a number is an integer and \\(\\ge 0\\), it belongs to \\(\\mathbb{W}\\) (whole).</li>"
                "<li>If a number is an integer (positive, negative, or zero), it belongs to \\(\\mathbb{Z}\\) (integer).</li>"
                "<li>If a number can be written as \\(\\frac{p}{q}\\) with \\(q\\neq 0\\), it belongs to \\(\\mathbb{Q}\\) (rational). Every integer is also rational because \\(a=\\frac{a}{1}\\).</li>"
                "</ul>"
                "<p><strong>Common mix-up:</strong> \\(0\\) is whole but <strong>not</strong> natural (natural numbers start from 1).</p>",
            ),
        ],
        "1.1.2": [
            (
                "Infinitely many rationals between two rationals",
                "<p>Take two distinct rational numbers \\(\\frac{a}{b}\\) and \\(\\frac{c}{d}\\) with \\(\\frac{a}{b} \\lt \\frac{c}{d}\\).</p>"
                "<p>Their <strong>average</strong> is</p>"
                "<p>\\(\\displaystyle \\frac{\\frac{a}{b}+\\frac{c}{d}}{2}\\).</p>"
                "<p>Because the average of two rationals is rational, it gives a rational number strictly between them.</p>"
                "<p>Since you can keep averaging again and again, you get infinitely many rationals between the same two rationals.</p>",
            ),
            (
                "A simple method (average/halving)",
                "<p>Procedure:</p>"
                "<ul>"
                "<li>Write both numbers with a common denominator if needed.</li>"
                "<li>Add them and divide by 2 to get a middle rational.</li>"
                "<li>Repeat between the original lower number and the middle number (or between middle and upper).</li>"
                "</ul>"
                "<p>Each repetition creates a new rational that still lies between the two endpoints.</p>",
            ),
        ],
        "1.1.3": [
            (
                "Reasoning with number sets (True/False)",
                "<p>When you judge a statement about \\(\\mathbb{N},\\mathbb{W},\\mathbb{Z},\\mathbb{Q}\\), translate it into a <em>definition check</em>.</p>"
                "<ul>"
                "<li>Natural numbers start at \\(1\\). So any statement claiming \\(0\\in\\mathbb{N}\\) is false.</li>"
                "<li>Every natural number is a whole number, so \\(\\mathbb{N} \\subset \\mathbb{W}\\).</li>"
                "<li>Integers are all whole numbers plus negatives, so \\(\\mathbb{W} \\subset \\mathbb{Z}\\).</li>"
                "<li>Rationals are numbers of the form \\(\\frac{p}{q}\\) with \\(q\\neq 0\\). Every integer is rational because \\(a=\\frac{a}{1}\\), but not every rational is an integer.</li>"
                "</ul>"
                "<p>So you can often disprove a statement by finding a single counterexample.</p>",
            )
        ],
        "1.2.1": [
            (
                "Rational vs irrational (and why \\(\\sqrt{n}\\) matters)",
                "<p>A real number is either <strong>rational</strong> or <strong>irrational</strong>.</p>"
                "<p><strong>Rational:</strong> it can be written as \\(\\frac{p}{q}\\) where \\(p,q\\) are integers and \\(q\\neq 0\\).</p>"
                "<p><strong>Irrational:</strong> it cannot be written in that form.</p>"
                "<p>In particular, for square roots: \\(\\sqrt{n}\\) is <strong>rational</strong> exactly when \\(n\\) is a perfect square (for example, \\(\\sqrt{9}=3\\)); otherwise \\(\\sqrt{n}\\) is irrational (for example, \\(\\sqrt{2}\\)).</p>",
            ),
            (
                "Square-root test",
                "<p>To classify \\(\\sqrt{n}\\):</p>"
                "<ul>"
                "<li>Factor \\(n\\) and look for a perfect-square factor.</li>"
                "<li>If the radical simplifies completely (e.g., \\(\\sqrt{8}=2\\sqrt{2}\\)), then check the remaining radical.</li>"
                "<li>If the remaining part is not a perfect square, the number is irrational.</li>"
                "</ul>"
                "<p>This is the key idea used in many classification questions.</p>",
            ),
        ],
        "1.2.2": [
            (
                "Spotting irrationals in a set",
                "<p>To identify irrational numbers among candidates:</p>"
                "<ul>"
                "<li>Any number that can be written as \\(\\frac{p}{q}\\) with \\(q\\neq 0\\) is rational.</li>"
                "<li>For square roots, check whether the under-root number is a perfect square.</li>"
                "<li>Decimals that terminate or repeat are rational; non-terminating non-repeating decimals are irrational (in the school context).</li>"
                "</ul>"
                "<p>So you can classify each element one by one and select all irrationals.</p>",
            ),
            (
                "Perfect-square checklist",
                "<p>Common quick checks:</p>"
                "<ul>"
                "<li>\\(\\sqrt{49}=7\\) (perfect square) → rational.</li>"
                "<li>\\(\\sqrt{10}\\) is not a perfect square → irrational.</li>"
                "<li>\\(\\sqrt{2}\\) is irrational.</li>"
                "</ul>",
            ),
        ],
        "1.2.3": [
            (
                "True/False about irrationals",
                "<p>Use the defining property: irrationals cannot be written as \\(\\frac{p}{q}\\) with \\(q\\neq 0\\).</p>"
                "<ul>"
                "<li>Statements about \\(\\sqrt{n}\\) usually reduce to whether \\(n\\) is a perfect square.</li>"
                "<li>Remember: \\(\\sqrt{9}=3\\) is rational, even though a square root is involved.</li>"
                "<li>Numbers like \\(\\pi\\) and \\(\\sqrt{2}\\) are irrational.</li>"
                "</ul>"
                "<p>So if you can rewrite the expression and it becomes an integer or a fraction, the statement is likely false.</p>",
            )
        ],
        "1.3.1": [
            (
                "Terminating vs recurring decimals",
                "<p>NCERT's key idea: for any rational number \\(\\frac{p}{q}\\) (with \\(q\\neq 0\\)), decimal expansion has only two possibilities:</p>"
                "<ul>"
                "<li><strong>Terminating</strong> (ends after a finite number of steps), or</li>"
                "<li><strong>Non-terminating recurring</strong> (a repeating block of digits).</li>"
                "</ul>"
                "<p>Examples from the chapter pattern: \\(\\frac{7}{8}=0.875\\) terminates, while \\(\\frac{10}{3}=3.333\\dots\\) and \\(\\frac{1}{7}=0.142857142857\\dots\\) are recurring.</p>"
                "<p>For fractions in lowest terms, decimal terminates iff denominator has no prime factors except \\(2\\) and \\(5\\).</p>",
            ),
            (
                "Quick decision from the denominator",
                "<p>Steps:</p>"
                "<ul>"
                "<li>Reduce \\(\\frac{p}{q}\\) to lowest terms.</li>"
                "<li>Factor \\(q\\).</li>"
                "<li>If \\(q\\) has only prime factors \\(2\\) and \\(5\\), the decimal terminates; else it is recurring.</li>"
                "</ul>",
            ),
            (
                "Why remainder repetition gives recurring decimals",
                "<p>During long division, every remainder is between \\(0\\) and \\(q-1\\).</p>"
                "<p>So only finitely many remainder values are possible. If remainder never becomes \\(0\\), some remainder must repeat.</p>"
                "<p>Once a remainder repeats, the quotient digits repeat from that point, giving a recurring decimal block.</p>",
            ),
        ],
        "1.3.2": [
            (
                "Convert a fraction to a decimal",
                "<p>To convert \\(\\frac{p}{q}\\) to a decimal, do division. Track the remainder:</p>"
                "<ul>"
                "<li>If the remainder becomes \\(0\\), you get a terminating decimal.</li>"
                "<li>If remainders start repeating, you get a recurring decimal.</li>"
                "</ul>"
                "<p>In both cases, the decimal expansion is still describing a rational number.</p>",
            ),
            (
                "Remainder pattern (what you watch for)",
                "<p>During long division:</p>"
                "<ul>"
                "<li>Remainders determine what digits come next.</li>"
                "<li>Once a remainder repeats, the digits repeat too.</li>"
                "</ul>"
                "<p>This is why some fractions produce decimals like \\(0.5\\) while others produce repeating blocks like \\(0.142857\\).</p>",
            ),
            (
                "Worked check: \\(\\frac{10}{3},\\ \\frac{7}{8},\\ \\frac{1}{7}\\)",
                "<ul>"
                "<li>\\(\\frac{10}{3}=3.333\\dots\\) because remainder repeats as 1.</li>"
                "<li>\\(\\frac{7}{8}=0.875\\) because remainder becomes 0.</li>"
                "<li>\\(\\frac{1}{7}=0.142857142857\\dots\\) because remainder cycle repeats (3,2,6,4,5,1,...).</li>"
                "</ul>",
            ),
        ],
        "1.3.3": [
            (
                "Convert recurring decimals to fractions",
                "<p>For recurring decimals, NCERT's core method is algebraic elimination of the repeating block.</p>"
                "<p>Suppose \\(x = 0.\\overline{ab}\\), where the 2-digit block \\(ab\\) repeats forever.</p>"
                "<p>Multiply by \\(10^2\\): \\(100x = ab.\\overline{ab}\\).</p>"
                "<p>Now subtract \\(x\\) from \\(100x\\):</p>"
                "<p>\\(100x - x = ab.\\overline{ab} - 0.\\overline{ab}\\Rightarrow 99x = ab\\).</p>"
                "<p>So \\(x = \\frac{ab}{99}\\), and then reduce to lowest terms.</p>"
                "<p>This guarantees the result is rational, matching the theorem that recurring decimals are rational numbers.</p>",
            ),
            (
                "Two common patterns",
                "<ul>"
                "<li><strong>1-digit repeating:</strong> e.g., \\(0.\\overline{3}=\\frac{1}{3}\\).</li>"
                "<li><strong>multi-digit repeating:</strong> e.g., \\(0.\\overline{12}\\) becomes \\(\\frac{12}{99}=\\frac{4}{33}\\).</li>"
                "</ul>"
                "<p>Always reduce to lowest terms at the end and verify by reconverting to decimal mentally.</p>"
                "<p>If your reduced fraction gives back the same repeating pattern, your algebra is consistent.</p>",
            ),
            (
                "Mixed recurring form (non-repeating + repeating)",
                "<p>For a number like \\(x=0.1\\overline{6}\\): multiply once to move non-repeating part, then again to align repeating block.</p>"
                "<p>Example method: \\(10x=1.\\overline{6}\\), \\(100x=16.\\overline{6}\\), subtract to eliminate recurring part.</p>"
                "<p>This gives a linear equation in \\(x\\), so you get a rational fraction finally.</p>",
            ),
            (
                "Worked NCERT-style conversion",
                "<p>Take \\(x = 0.\\overline{27}\\).</p>"
                "<p>Then \\(100x = 27.\\overline{27}\\).</p>"
                "<p>Subtract: \\(100x - x = 27\\Rightarrow 99x = 27\\Rightarrow x = \\frac{27}{99} = \\frac{3}{11}\\).</p>"
                "<p>So \\(0.\\overline{27}=\\frac{3}{11}\\).</p>"
                "<p>This step sequence is the exact template students should reuse for any recurring block.</p>",
            ),
        ],
        "1.3.4": [
            (
                "Predict decimal patterns (remainder shifting)",
                "<p>For a fixed divisor \\(q\\), the sequence of remainders during division repeats. That means the block of digits in the quotient repeats in a predictable way.</p>"
                "<p>For example, for \\(\\frac{1}{7}\\) the repeating block is:</p>"
                "<p>\\(0.\\overline{142857}\\).</p>"
                "<p>Then \\(\\frac{4}{7}\\) uses the same digits but the cycle is shifted:</p>"
                "<p>\\(\\frac{4}{7}=0.\\overline{571428}\\).</p>",
            ),
            (
                "Cycle memory trick for sevenths",
                "<p>Remember one cycle: \\(142857\\).</p>"
                "<p>Multiples of \\(\\frac{1}{7}\\) rotate the same 6-digit cycle:</p>"
                "<ul>"
                "<li>\\(\\frac{2}{7}=0.\\overline{285714}\\)</li>"
                "<li>\\(\\frac{3}{7}=0.\\overline{428571}\\)</li>"
                "<li>\\(\\frac{4}{7}=0.\\overline{571428}\\)</li>"
                "</ul>"
                "<p>So prediction is just identifying the right shift.</p>",
            ),
        ],
        "1.4.1": [
            (
                "Add and subtract surds (like radicals combine)",
                "<p>Surds are irrational expressions involving roots, like \\(\\sqrt{2},\\ \\sqrt{3}\\), etc.</p>"
                "<p>When adding/subtracting, only <strong>like surds</strong> combine.</p>"
                "<p>Like surds have the same radical part, for example:</p>"
                "<p>\\(2\\sqrt{3}+5\\sqrt{3}-\\sqrt{3}=(2+5-1)\\sqrt{3}=6\\sqrt{3}\\).</p>",
            ),
            (
                "Step-by-step approach",
                "<ul>"
                "<li>Rewrite each term so radicals match (simplify if needed).</li>"
                "<li>Combine coefficients for the identical radical.</li>"
                "<li>Leave unlike surds as separate terms.</li>"
                "</ul>",
            ),
            (
                "Common mistake to avoid",
                "<p>You cannot combine unlike surds by adding inside radicals.</p>"
                "<p>So \\(\\sqrt{2}+\\sqrt{3}\\neq\\sqrt{5}\\).</p>"
                "<p>Only terms with the same radical part combine, e.g. \\(3\\sqrt{5}-2\\sqrt{5}=\\sqrt{5}\\).</p>",
            ),
        ],
        "1.4.2": [
            (
                "Multiply surds (and divide) using root laws",
                "<p>Use the basic root rules:</p>"
                "<ul>"
                "<li>\\(\\sqrt{a}\\cdot\\sqrt{b}=\\sqrt{ab}\\)</li>"
                "<li>\\(\\frac{\\sqrt{a}}{\\sqrt{b}}=\\sqrt{\\frac{a}{b}}\\)</li>"
                "</ul>"
                "<p>Then simplify the resulting square root.</p>",
            ),
            (
                "Watch for perfect squares",
                "<p>After multiplying/dividing, check whether the number inside the root becomes a perfect square. If yes, the surd becomes rational (an integer).</p>"
                "<p>For instance, \\(\\sqrt{8}\\cdot\\sqrt{2}=\\sqrt{16}=4\\).</p>",
            ),
            (
                "NCERT-style simplification flow",
                "<p>First simplify each surd if possible: e.g., \\(\\sqrt{12}=2\\sqrt{3}\\).</p>"
                "<p>Then apply multiplication/division rule. This avoids large numbers inside roots and reduces errors.</p>"
                "<p>Finally, check if the answer can be made surd-free or further simplified.</p>",
            ),
        ],
        "1.4.3": [
            (
                "Use identities to simplify expressions",
                "<p>A very useful identity is the product of a conjugate pair:</p>"
                "<p>\\(\\left(a+\\sqrt{b}\\right)\\left(a-\\sqrt{b}\\right)=a^2-b\\).</p>"
                "<p>It works because cross terms cancel and you’re left with a simple expression.</p>",
            ),
            (
                "Why conjugates matter",
                "<p>Conjugates have same first term and opposite sign between terms.</p>"
                "<p>When multiplied, the middle terms cancel: \\((x+y)(x-y)=x^2-y^2\\).</p>"
                "<p>This trick appears repeatedly in rationalisation and surd simplification.</p>",
            ),
        ],
        "1.4.4": [
            (
                "Rationalise the denominator",
                "<p>Rationalising means rewriting an expression so the denominator no longer contains a surd like \\(\\sqrt{b}\\).</p>"
                "<p>For expressions such as:</p>"
                "<p>\\(\\frac{1}{a+\\sqrt{b}}\\),</p>"
                "<p>multiply numerator and denominator by the conjugate \\(a-\\sqrt{b}\\).</p>"
                "<p>This makes the denominator:</p>"
                "<p>\\((a+\\sqrt{b})(a-\\sqrt{b})=a^2-b\\),</p>"
                "<p>which is rational.</p>",
            ),
            (
                "Worked outline: \\(\\frac{1}{2+\\sqrt{3}}\\)",
                "<ul>"
                "<li>Multiply by conjugate: \\(\\frac{1}{2+\\sqrt3}\\cdot\\frac{2-\\sqrt3}{2-\\sqrt3}\\).</li>"
                "<li>Denominator: \\((2+\\sqrt3)(2-\\sqrt3)=4-3=1\\).</li>"
                "<li>Result: \\(2-\\sqrt3\\).</li>"
                "</ul>"
                "<p>This is the standard NCERT pattern for rationalisation questions.</p>",
            ),
        ],
        "1.5.1": [
            (
                "Fractional exponents = roots",
                "<p>If you see a fractional exponent, rewrite it as a root.</p>"
                "<p>For example:</p>"
                "<p>\\(a^{\\frac{m}{n}}=\\sqrt[n]{a^m}\\).</p>"
                "<p>So</p>"
                "<p>\\(64^{\\frac{1}{2}}=\\sqrt[2]{64}=8\\).</p>",
            ),
            (
                "Turn it into a root, then evaluate",
                "<ul>"
                "<li>Identify the base \\(a\\), numerator \\(m\\), and denominator \\(n\\).</li>"
                "<li>Compute \\(a^m\\) first (if it’s not too large).</li>"
                "<li>Take the \\(n\\)th root.</li>"
                "</ul>",
            ),
        ],
        "1.5.2": [
            (
                "Exponent laws (cheat sheet)",
                "<p>These laws help you simplify powers quickly:</p>"
                "<ul>"
                "<li>\\(a^m\\cdot a^n=a^{m+n}\\)</li>"
                "<li>\\(a^m\\div a^n=a^{m-n}\\)</li>"
                "<li>\\((a^m)^n=a^{mn}\\)</li>"
                "<li>\\((ab)^n=a^n b^n\\)</li>"
                "<li>\\(\\frac{a^n}{b^n}=\\left(\\frac{a}{b}\\right)^n\\)</li>"
                "</ul>",
            ),
            (
                "Simplify in small moves",
                "<p>Best practice:</p>"
                "<ul>"
                "<li>Simplify inside parentheses first.</li>"
                "<li>Combine like bases using addition/subtraction of exponents.</li>"
                "<li>Apply one law at a time; avoid “jumping steps”.</li>"
                "</ul>",
            ),
        ],
        "1.5.3": [
            (
                "Apply the right exponent law",
                "<p>Each exponent-expression matches a specific law.</p>"
                "<p>Before choosing, compare the pattern:</p>"
                "<ul>"
                "<li>If you see the same base multiplied → add exponents.</li>"
                "<li>If you see a power of a power → multiply exponents.</li>"
                "<li>If you see \\((ab)^n\\) → distribute exponent to both factors.</li>"
                "</ul>",
            )
        ],
    }

    worked_examples_by_topic: dict[str, list[tuple[str, list[dict]]]] = {
        "1.1.1": [
            (
                "Classify numbers into N, W, Z, Q",
                [
                    {"step": 1, "content": "Check the type: is it an integer or of the form p/q?", "explanation": "If it can be written as p/q with q ≠ 0, it is rational (in Q)."},
                    {"step": 2, "content": "Classify by sign and zero: 0 is whole but not natural; negatives are not whole/natural.", "explanation": "Natural numbers start at 1, so 0 is not in N."},
                    {"step": 3, "content": "Pick the best sets.", "explanation": "Example: -3 is in Z and in Q, but not in N or W."},
                ],
            ),
            (
                "Example classification set",
                [
                    {"step": 1, "content": "Rewrite the fraction (if any) and check \\(q\\neq 0\\).", "explanation": "For \\(\\frac{5}{2}\\), we have integers \\(p=5\\), \\(q=2\\neq 0\\), so it’s rational."},
                    {"step": 2, "content": "Check whether it is an integer.", "explanation": "Since \\(\\frac{5}{2}\\) is not an integer, it cannot be in \\(\\mathbb{Z}\\) as a whole-number/integer."},
                    {"step": 3, "content": "State the set(s) for the number.", "explanation": "Result: \\(\\frac{5}{2}\\in\\mathbb{Q}\\) (and not in \\(\\mathbb{N}\\), \\(\\mathbb{W}\\), \\(\\mathbb{Z}\\))."},
                ],
            ),
        ],
        "1.1.2": [
            (
                "Find a rational between \\(\\frac{1}{3}\\) and \\(\\frac{1}{2}\\)",
                [
                    {"step": 1, "content": "Write both numbers with a common denominator.", "explanation": "\\(\\frac{1}{3}=\\frac{2}{6}\\) and \\(\\frac{1}{2}=\\frac{3}{6}\\)."},
                    {"step": 2, "content": "Take the average: \\(\\frac{\\frac{1}{3}+\\frac{1}{2}}{2}=\\frac{\\frac{2}{6}+\\frac{3}{6}}{2}\\).", "explanation": "Average keeps you strictly between two distinct rationals."},
                    {"step": 3, "content": "Simplify: \\(\\frac{\\frac{5}{6}}{2}=\\frac{5}{12}\\).", "explanation": "So \\(\\frac{1}{3} \\lt \\frac{5}{12} \\lt \\frac{1}{2}\\)."},
                ],
            ),
            (
                "Find another one between \\(\\frac{1}{3}\\) and \\(\\frac{5}{12}\\)",
                [
                    {"step": 1, "content": "Average again: \\(\\frac{\\frac{1}{3}+\\frac{5}{12}}{2}\\).", "explanation": "Using averaging gives another rational strictly between."},
                    {"step": 2, "content": "Compute: \\(\\frac{\\frac{4}{12}+\\frac{5}{12}}{2}=\\frac{\\frac{9}{12}}{2}=\\frac{3}{8}\\).", "explanation": "Keep fractions in simplest form at the end."},
                    {"step": 3, "content": "Conclude ordering.", "explanation": "\\(\\frac{1}{3} \\lt \\frac{3}{8} \\lt \\frac{5}{12}\\)."},
                ],
            ),
        ],
        "1.1.3": [
            (
                "True/False: “\\(0\\) is a natural number.”",
                [
                    {"step": 1, "content": "Recall definition of natural numbers.", "explanation": "\\(\\mathbb{N}=\\{1,2,3,\\dots\\}\\), so it starts at 1."},
                    {"step": 2, "content": "Check the statement against the definition.", "explanation": "Since \\(0\\notin\\{1,2,3,\\dots\\}\\), the statement is false."},
                    {"step": 3, "content": "Give correct classification for \\(0\\).", "explanation": "\\(0\\in\\mathbb{W}\\) but \\(0\\notin\\mathbb{N}\\)."},
                ],
            ),
            (
                "True/False: “Every integer is rational.”",
                [
                    {"step": 1, "content": "Use the rational form \\(\\frac{p}{q}\\) with \\(q\\neq 0\\).", "explanation": "Any integer \\(a\\) can be written as \\(\\frac{a}{1}\\)."},
                    {"step": 2, "content": "Check the condition on \\(q\\).", "explanation": "Here \\(q=1\\neq 0\\), so it is valid."},
                    {"step": 3, "content": "Conclude.", "explanation": "So every integer lies in \\(\\mathbb{Q}\\)."},
                ],
            ),
        ],
        "1.2.1": [
            (
                "Decide: is \\(\\sqrt{8}\\) rational?",
                [
                    {"step": 1, "content": "Simplify \\(\\sqrt{8}\\) using factorization.", "explanation": "\\(8=4\\cdot 2\\), so \\(\\sqrt{8}=\\sqrt{4\\cdot 2}=2\\sqrt{2}\\)."},
                    {"step": 2, "content": "Now check the remaining radical \\(\\sqrt{2}\\).", "explanation": "2 is not a perfect square, so \\(\\sqrt{2}\\) is irrational."},
                    {"step": 3, "content": "Conclude the classification.", "explanation": "Since \\(2\\sqrt{2}\\) is irrational, \\(\\sqrt{8}\\) is irrational."},
                ],
            )
        ],
        "1.2.2": [
            (
                "Choose the irrational numbers in the set",
                [
                    {"step": 1, "content": "For each element that looks like \\(\\sqrt{n}\\), check whether \\(n\\) is a perfect square.", "explanation": "If yes, the root becomes an integer (rational); if not, it stays irrational."},
                    {"step": 2, "content": "Use decimal knowledge for numbers given as decimals.", "explanation": "Terminating or repeating decimals are rational; non-terminating non-repeating are irrational."},
                    {"step": 3, "content": "Select all items that are irrational.", "explanation": "Example picks: \\(\\sqrt{10}\\) is irrational, but \\(\\sqrt{49}=7\\) is rational."},
                ],
            )
        ],
        "1.2.3": [
            (
                "True/False: “\\(\\sqrt{9}\\) is irrational.”",
                [
                    {"step": 1, "content": "Use the perfect-square test.", "explanation": "Since \\(9\\) is a perfect square, \\(\\sqrt{9}=3\\)."},
                    {"step": 2, "content": "Classify \\(3\\).", "explanation": "3 is an integer, so it is rational (\\(3=\\frac{3}{1}\\))."},
                    {"step": 3, "content": "Decide True/False.", "explanation": "The statement is false because \\(\\sqrt{9}\\) is rational."},
                ],
            ),
            (
                "True/False: “\\(\\sqrt{2}\\) is rational.”",
                [
                    {"step": 1, "content": "Check whether 2 is a perfect square.", "explanation": "2 is not a perfect square."},
                    {"step": 2, "content": "Conclude about \\(\\sqrt{2}\\).", "explanation": "\\(\\sqrt{2}\\) cannot be written as \\(\\frac{p}{q}\\) so it is irrational."},
                    {"step": 3, "content": "Decide True/False.", "explanation": "The statement is false."},
                ],
            ),
        ],
        "1.3.1": [
            (
                "Decide: is \\(\\frac{7}{8}\\) terminating or recurring?",
                [
                    {"step": 1, "content": "Factor the denominator: \\(8=2^3\\).", "explanation": "Only prime factor is 2, so the decimal will terminate."},
                    {"step": 2, "content": "Check the rule: denominator has only 2 and 5.", "explanation": "Since there is no prime factor other than 2, termination happens."},
                    {"step": 3, "content": "Conclude.", "explanation": "\\(\\frac{7}{8}\\) has a terminating decimal expansion."},
                ],
            )
        ],
        "1.3.2": [
            (
                "Convert \\(\\frac{3}{8}\\) to a decimal",
                [
                    {"step": 1, "content": "Do division: \\(3\\div 8\\).", "explanation": "Long division generates digits one by one."},
                    {"step": 2, "content": "Track remainders until it becomes 0.", "explanation": "If remainder becomes 0, the decimal stops (terminating)."},
                    {"step": 3, "content": "Write the terminating decimal.", "explanation": "For example, \\(\\frac{3}{8}=0.375\\)."},
                ],
            ),
            (
                "Convert another fraction (focus on stopping vs repeating)",
                [
                    {"step": 1, "content": "Choose a fraction like \\(\\frac{5}{12}\\).", "explanation": "Now examine the remainders during division."},
                    {"step": 2, "content": "If remainders repeat, the decimal repeats.", "explanation": "Repeated remainder means a repeated block of digits."},
                    {"step": 3, "content": "Write the recurring decimal format.", "explanation": "Non-terminating recurring decimals arise when other primes appear in denominator."},
                ],
            ),
        ],
        "1.3.3": [
            (
                "Convert \\(0.\\overline{3}\\) to a fraction",
                [
                    {"step": 1, "content": "Let \\(x=0.\\overline{3}\\).", "explanation": "So \\(x=0.3333\\dots\\)."},
                    {"step": 2, "content": "Multiply by 10: \\(10x=3.3333\\dots\\).", "explanation": "The repeating part aligns."},
                    {"step": 3, "content": "Subtract: \\(10x-x=3\\Rightarrow 9x=3\\Rightarrow x=\\frac{1}{3}\\).", "explanation": "Therefore \\(0.\\overline{3}=\\frac{1}{3}\\)."},
                ],
            ),
            (
                "Convert \\(0.\\overline{12}\\) to a fraction",
                [
                    {"step": 1, "content": "Let \\(x=0.\\overline{12}\\).", "explanation": "So digits 12 repeat forever."},
                    {"step": 2, "content": "Multiply by 100: \\(100x=12.\\overline{12}\\).", "explanation": "Two-digit repeat → multiply by \\(10^2\\)."},
                    {"step": 3, "content": "Subtract: \\(100x-x=12\\Rightarrow 99x=12\\Rightarrow x=\\frac{12}{99}=\\frac{4}{33}\\).", "explanation": "Reduce to lowest terms."},
                ],
            ),
        ],
        "1.3.4": [
            (
                "Predict digits for \\(\\frac{4}{7}\\) using the cycle of \\(\\frac{1}{7}\\)",
                [
                    {"step": 1, "content": "Write the repeating block for \\(\\frac{1}{7}\\): \\(0.\\overline{142857}\\).", "explanation": "This block comes from repeating remainders in long division."},
                    {"step": 2, "content": "Find how multiplication by 4 shifts the cycle.", "explanation": "The same digits appear but starting at the shifted remainder."},
                    {"step": 3, "content": "So \\(\\frac{4}{7}=0.\\overline{571428}\\).", "explanation": "Now you can read the first digits after the decimal."},
                ],
            ),
            (
                "Another check (same pattern, different start)",
                [
                    {"step": 1, "content": "Remember: the repeating block length is tied to the divisor.", "explanation": "For \\(1/7\\), the repeating block has length 6."},
                    {"step": 2, "content": "Predict digits by cycling through the block.", "explanation": "Move forward in the block according to the numerator."},
                    {"step": 3, "content": "Write the repeating decimal using the bar.", "explanation": "This matches what long division would produce."},
                ],
            ),
        ],
        "1.4.1": [
            (
                "Add/subtract like surds: \\(2\\sqrt{3}+5\\sqrt{3}-\\sqrt{3}\\)",
                [
                    {"step": 1, "content": "Check that radicals match (like surds).", "explanation": "Here every term has \\(\\sqrt{3}\\)."},
                    {"step": 2, "content": "Add coefficients: \\((2+5-1)\\sqrt{3}\\).", "explanation": "Only coefficients change; \\(\\sqrt{3}\\) stays."},
                    {"step": 3, "content": "Simplify to get \\(6\\sqrt{3}\\).", "explanation": "That is the final simplified surd expression."},
                ],
            ),
            (
                "Another like-surds example",
                [
                    {"step": 1, "content": "Simplify any square factors inside radicals first.", "explanation": "For example, \\(\\sqrt{12}=2\\sqrt{3}\\) before combining."},
                    {"step": 2, "content": "Combine like surds.", "explanation": "After simplification, group terms with the same radical."},
                    {"step": 3, "content": "Write the simplified result.", "explanation": "Keep unlike surds as separate terms."},
                ],
            ),
        ],
        "1.4.2": [
            (
                "Multiply surds: \\(\\sqrt{8}\\cdot\\sqrt{2}\\)",
                [
                    {"step": 1, "content": "Use \\(\\sqrt{a}\\cdot\\sqrt{b}=\\sqrt{ab}\\).", "explanation": "So \\(\\sqrt{8}\\cdot\\sqrt{2}=\\sqrt{16}\\)."},
                    {"step": 2, "content": "Simplify the square root.", "explanation": "\\(\\sqrt{16}=4\\)."},
                    {"step": 3, "content": "Conclude the value (rational).", "explanation": "Because it becomes an integer, the result is rational."},
                ],
            ),
            (
                "Divide surds: \\(\\frac{\\sqrt{12}}{\\sqrt{3}}\\)",
                [
                    {"step": 1, "content": "Use \\(\\frac{\\sqrt{a}}{\\sqrt{b}}=\\sqrt{\\frac{a}{b}}\\).", "explanation": "So \\(\\frac{\\sqrt{12}}{\\sqrt{3}}=\\sqrt{4}\\)."},
                    {"step": 2, "content": "Simplify inside the root.", "explanation": "Here \\(\\frac{12}{3}=4\\)."},
                    {"step": 3, "content": "Compute: \\(\\sqrt{4}=2\\).", "explanation": "Again, perfect squares give rational results."},
                ],
            ),
        ],
        "1.4.3": [
            (
                "Use identity: \\(\\left(a+\\sqrt{b}\\right)\\left(a-\\sqrt{b}\\right)=a^2-b\\)",
                [
                    {"step": 1, "content": "Recognize the pattern (conjugates).", "explanation": "The expression is exactly \\((a+\\sqrt{b})(a-\\sqrt{b})\\)."},
                    {"step": 2, "content": "Apply the identity directly.", "explanation": "Cross terms cancel, leaving \\(a^2-b\\)."},
                    {"step": 3, "content": "Simplify if needed.", "explanation": "The result is rational (no square root in the final form)."},
                ],
            ),
            (
                "Identity application with numbers",
                [
                    {"step": 1, "content": "Substitute \\(a\\) and \\(b\\).", "explanation": "Example: take \\(a=5\\), \\(b=3\\)."},
                    {"step": 2, "content": "Compute \\(a^2-b\\).", "explanation": "\\(25-3=22\\)."},
                    {"step": 3, "content": "Write the simplified value.", "explanation": "\\(\\left(5+\\sqrt{3}\\right)\\left(5-\\sqrt{3}\\right)=22\\)."},
                ],
            ),
        ],
        "1.4.4": [
            (
                "Rationalise: \\(\\frac{1}{a+\\sqrt{b}}\\)",
                [
                    {"step": 1, "content": "Multiply top and bottom by the conjugate \\(a-\\sqrt{b}\\).", "explanation": "This removes the surd from the denominator."},
                    {"step": 2, "content": "Use the identity: \\((a+\\sqrt{b})(a-\\sqrt{b})=a^2-b\\).", "explanation": "Denominator becomes rational."},
                    {"step": 3, "content": "Simplify the fraction.", "explanation": "Final form has no surd in the denominator."},
                ],
            ),
            (
                "Classify after operation (rational vs irrational)",
                [
                    {"step": 1, "content": "Rationalisation makes the denominator rational.", "explanation": "But the <em>whole value</em> may still involve \\(\\sqrt{b}\\) in the numerator."},
                    {"step": 2, "content": "Check whether the simplified expression contains \\(\\sqrt{n}\\) as an essential part.", "explanation": "If it can be reduced to a rational number, it’s rational; otherwise it remains irrational."},
                    {"step": 3, "content": "State the classification.", "explanation": "This matches the idea of \\(\\sqrt{n}\\) being rational only for perfect squares."},
                ],
            ),
        ],
        "1.5.1": [
            (
                "Evaluate: \\(64^{\\frac{1}{2}}\\)",
                [
                    {"step": 1, "content": "Rewrite the fractional exponent as a root.", "explanation": "\\(64^{\\frac{1}{2}}=\\sqrt[2]{64}\\)."},
                    {"step": 2, "content": "Compute the root.", "explanation": "\\(\\sqrt{64}=8\\)."},
                    {"step": 3, "content": "Write the final answer.", "explanation": "So \\(64^{\\frac{1}{2}}=8\\)."},
                ],
            ),
            (
                "Another fractional exponent evaluation",
                [
                    {"step": 1, "content": "Example idea: \\(a^{\\frac{m}{n}}\\Rightarrow \\sqrt[n]{a^m}\\).", "explanation": "Always convert to a root expression first."},
                    {"step": 2, "content": "Compute \\(a^m\\) then take the \\(n\\)th root.", "explanation": "Simplify powers before rooting to avoid mistakes."},
                    {"step": 3, "content": "Conclude.", "explanation": "Check if the root is exact (perfect squares/cubes)."},
                ],
            ),
        ],
        "1.5.2": [
            (
                "Simplify using exponent laws: \\(2^\\frac{2}{3}\\cdot 2^\\frac{1}{3}\\)",
                [
                    {"step": 1, "content": "Same base multiplication → add exponents.", "explanation": "Rule: \\(a^m\\cdot a^n=a^{m+n}\\)."},
                    {"step": 2, "content": "Compute the sum: \\(\\frac{2}{3}+\\frac{1}{3}=1\\).", "explanation": "So the product becomes \\(2^1\\)."},
                    {"step": 3, "content": "Final answer: \\(2\\).", "explanation": "Write the simplest power form or integer value."},
                ],
            ),
            (
                "Combine powers carefully",
                [
                    {"step": 1, "content": "Spot which law is applicable (multiply/divide/power of power).", "explanation": "Avoid combining exponents in the wrong situation."},
                    {"step": 2, "content": "Re-check arithmetic in exponents.", "explanation": "Fractions in exponents require careful addition/subtraction."},
                    {"step": 3, "content": "Simplify the final expression.", "explanation": "You usually end with a simpler surd-free rational or a simpler power."},
                ],
            ),
        ],
        "1.5.3": [
            (
                "Choose the exponent law",
                [
                    {"step": 1, "content": "Identify the pattern in \\((ab)^n\\).", "explanation": "It looks like a product inside the bracket, raised to a power."},
                    {"step": 2, "content": "Match to the correct rule.", "explanation": "Rule: \\((ab)^n=a^n b^n\\)."},
                    {"step": 3, "content": "Pick the name of the law.", "explanation": "This is exactly the multiplication law for exponents."},
                ],
            )
        ],
    }

    def topic_sort_key(key: str) -> tuple[int, int, int]:
        a, b, c = key.split(".")
        return int(a), int(b), int(c)

    for topic_key in sorted(topic_by_key.keys(), key=topic_sort_key):
        top = topic_by_key[topic_key]
        qtypes = topic_qtypes_by_key.get(topic_key, [])

        # Deeper learn phase:
        # - 4 concept cards for first topic in section (foundational),
        # - 3 concept cards for all other topics.
        # - 3 worked examples for every topic.
        concept_target = 4 if top.order == 1 else 3
        example_target = 3

        # Concepts
        concept_cards = concepts_by_topic.get(topic_key, [])
        for idx, (c_title, c_html) in enumerate(concept_cards[:concept_target], start=1):
            add_card(topic_key, c_title, c_html, idx)

        # If something is missing, fill with section-specific authored cards.
        for idx in range(len(concept_cards) + 1, concept_target + 1):
            section_prefix = ".".join(topic_key.split(".")[:2])
            if section_prefix == "1.1":
                if idx == 2:
                    fallback_title = f"{top.name} — Mini Checkpoint"
                    fallback_html = (
                        "<p><strong>Try quickly:</strong> Classify \\(-1, 0, \\frac{9}{4}\\) into \\(\\mathbb{N},\\mathbb{W},\\mathbb{Z},\\mathbb{Q}\\).</p>"
                        "<ul>"
                        "<li>\\(-1\\): integer and rational, not whole/natural.</li>"
                        "<li>\\(0\\): whole, integer, rational; not natural.</li>"
                        "<li>\\(\\frac{9}{4}\\): rational only.</li>"
                        "</ul>"
                        "<p>Reason with definitions, not memory tricks.</p>"
                    )
                elif idx == 3:
                    fallback_title = f"{top.name} — Misconception Notes"
                    fallback_html = (
                        "<ul>"
                        "<li>\\(0\\in\\mathbb{W}\\) but \\(0\\notin\\mathbb{N}\\) in NCERT convention.</li>"
                        "<li>Every integer is rational because \\(a=\\frac{a}{1}\\).</li>"
                        "<li>Between any two distinct rationals, infinitely many rationals exist.</li>"
                        "</ul>"
                        "<p>Check each statement with a direct counterexample if unsure.</p>"
                    )
                else:
                    fallback_title = f"{top.name} — Exam Ready Steps"
                    fallback_html = (
                        "<ol>"
                        "<li>Write the set-definition/the rule first.</li>"
                        "<li>Perform classification or ordering line by line.</li>"
                        "<li>End with clear notation (for example, \\(\\in\\), \\(\\notin\\), \\(\\subset\\)).</li>"
                        "</ol>"
                        "<p>Correct notation is part of full marks.</p>"
                    )
            elif section_prefix == "1.2":
                if idx == 2:
                    fallback_title = f"{top.name} — Mini Checkpoint"
                    fallback_html = (
                        "<p>Classify: \\(\\sqrt{16},\\ \\sqrt{12},\\ \\pi,\\ -\\frac{7}{5}\\).</p>"
                        "<ul>"
                        "<li>\\(\\sqrt{16}=4\\): rational.</li>"
                        "<li>\\(\\sqrt{12}=2\\sqrt3\\): irrational.</li>"
                        "<li>\\(\\pi\\): irrational.</li>"
                        "<li>\\(-\\frac{7}{5}\\): rational.</li>"
                        "</ul>"
                    )
                elif idx == 3:
                    fallback_title = f"{top.name} — Misconception Notes"
                    fallback_html = (
                        "<ul>"
                        "<li>Not all square roots are irrational (perfect-square roots are rational).</li>"
                        "<li>A non-terminating repeating decimal is rational, not irrational.</li>"
                        "<li>Every real number belongs to exactly one: rational or irrational.</li>"
                        "</ul>"
                    )
                else:
                    fallback_title = f"{top.name} — Exam Ready Steps"
                    fallback_html = (
                        "<ol>"
                        "<li>Use perfect-square test for radicals.</li>"
                        "<li>Use fraction form \\(\\frac{p}{q}\\) test for rationals.</li>"
                        "<li>State the final class with one supporting line.</li>"
                        "</ol>"
                    )
            elif section_prefix == "1.3":
                if idx == 2:
                    fallback_title = f"{top.name} — Mini Checkpoint"
                    fallback_html = (
                        "<p>Decide decimal type of \\(\\frac{9}{20},\\ \\frac{7}{12},\\ \\frac{13}{25}\\).</p>"
                        "<ul>"
                        "<li>If denominator in simplest form has only 2s and 5s, decimal terminates.</li>"
                        "<li>Otherwise, it is non-terminating recurring.</li>"
                        "</ul>"
                    )
                elif idx == 3:
                    fallback_title = f"{top.name} — Misconception Notes"
                    fallback_html = (
                        "<ul>"
                        "<li>Reduce fraction first before checking denominator factors.</li>"
                        "<li>Remainder 0 means terminating decimal.</li>"
                        "<li>Repeating remainder means recurring block starts.</li>"
                        "</ul>"
                    )
                else:
                    fallback_title = f"{top.name} — Exam Ready Steps"
                    fallback_html = (
                        "<ol>"
                        "<li>Simplify fraction.</li>"
                        "<li>Prime-factorize denominator.</li>"
                        "<li>Conclude decimal type and write one reason.</li>"
                        "</ol>"
                    )
            elif section_prefix == "1.4":
                if idx == 2:
                    fallback_title = f"{top.name} — Mini Checkpoint"
                    fallback_html = (
                        "<p>Simplify and classify:</p>"
                        "<ul>"
                        "<li>\\(5\\sqrt2-3\\sqrt2\\)</li>"
                        "<li>\\((3+\\sqrt5)(3-\\sqrt5)\\)</li>"
                        "<li>\\(\\frac{1}{2+\\sqrt3}\\) (rationalise)</li>"
                        "</ul>"
                    )
                elif idx == 3:
                    fallback_title = f"{top.name} — Misconception Notes"
                    fallback_html = (
                        "<ul>"
                        "<li>Like surds combine; unlike surds do not.</li>"
                        "<li>Use conjugate for rationalisation of binomial surd denominators.</li>"
                        "<li>Do not write \\(\\sqrt a + \\sqrt b = \\sqrt{a+b}\\).</li>"
                        "</ul>"
                    )
                else:
                    fallback_title = f"{top.name} — Exam Ready Steps"
                    fallback_html = (
                        "<ol>"
                        "<li>First identify operation type (addition/product/rationalisation).</li>"
                        "<li>Apply the matching surd identity.</li>"
                        "<li>Simplify to standard form and conclude.</li>"
                        "</ol>"
                    )
            else:
                if idx == 2:
                    fallback_title = f"{top.name} — Mini Checkpoint"
                    fallback_html = (
                        "<p>Evaluate: \\(32^{1/5},\\ 81^{1/2},\\ 8^{2/3}\\), then simplify one exponent-law expression.</p>"
                        "<p>Rewrite fractional exponents as roots before computing.</p>"
                    )
                elif idx == 3:
                    fallback_title = f"{top.name} — Misconception Notes"
                    fallback_html = (
                        "<ul>"
                        "<li>Keep the same base rule separate from power-of-a-power rule.</li>"
                        "<li>Negative exponent means reciprocal, not negative value.</li>"
                        "<li>Distribute exponent correctly in \\((ab)^n\\).</li>"
                        "</ul>"
                    )
                else:
                    fallback_title = f"{top.name} — Exam Ready Steps"
                    fallback_html = (
                        "<ol>"
                        "<li>Choose the exponent law by pattern.</li>"
                        "<li>Apply one law at a time.</li>"
                        "<li>Write final answer in simplest exact form.</li>"
                        "</ol>"
                    )
            add_card(
                topic_key,
                fallback_title,
                fallback_html,
                idx,
            )

        # Worked examples
        worked_cards = worked_examples_by_topic.get(topic_key, [])
        for idx, (w_title, w_steps) in enumerate(worked_cards[:example_target], start=1):
            add_we(topic_key, w_title, w_steps, idx)

        for idx in range(len(worked_cards) + 1, example_target + 1):
            if idx == 3:
                section_prefix = ".".join(topic_key.split(".")[:2])
                if section_prefix == "1.1":
                    steps = [
                        {"step": 1, "content": "Classify this set: \\(-5,\\ 0,\\ \\frac{7}{3},\\ 12\\).", "explanation": "Check each number against N, W, Z, Q definitions."},
                        {"step": 2, "content": "Find one rational between \\(\\frac{2}{5}\\) and \\(\\frac{3}{5}\\).", "explanation": "Use averaging: \\(\\frac{\\frac25+\\frac35}{2}=\\frac12\\)."},
                        {"step": 3, "content": "Explain why 0 is not natural but is whole.", "explanation": "Natural starts at 1 in NCERT convention; whole includes 0."},
                        {"step": 4, "content": "Write final classification neatly.", "explanation": "Present each number with the correct set(s)."},
                    ]
                elif section_prefix == "1.2":
                    steps = [
                        {"step": 1, "content": "Decide: \\(\\sqrt{18},\\ \\sqrt{49},\\ \\pi,\\ 0.125\\) — rational or irrational?", "explanation": "Use perfect-square test and decimal form logic."},
                        {"step": 2, "content": "Simplify where needed (e.g., \\(\\sqrt{18}=3\\sqrt{2}\\)).", "explanation": "Simplification helps reveal irrational parts."},
                        {"step": 3, "content": "Mark common trap: square root does not always mean irrational.", "explanation": "\\(\\sqrt{49}=7\\) is rational because 49 is a perfect square."},
                        {"step": 4, "content": "State final set membership.", "explanation": "Each number must be either rational or irrational (in R)."},
                    ]
                elif section_prefix == "1.3":
                    steps = [
                        {"step": 1, "content": "Check decimal type for \\(\\frac{21}{40}\\), \\(\\frac{11}{15}\\), and \\(\\frac{13}{125}\\).", "explanation": "Reduce and inspect denominator prime factors (2,5 only or not)."},
                        {"step": 2, "content": "Convert \\(0.\\overline{27}\\) to fraction.", "explanation": "Let \\(x=0.\\overline{27}\\), then \\(100x-x=27\\Rightarrow x=\\frac{27}{99}=\\frac{3}{11}\\)."},
                        {"step": 3, "content": "Predict first 3 digits of \\(\\frac{5}{7}\\) using the cycle of \\(\\frac{1}{7}\\).", "explanation": "Use the repeating block \\(142857\\) and shift appropriately."},
                        {"step": 4, "content": "Write one line explaining remainder repetition.", "explanation": "Repeated remainder forces repeated quotient digits."},
                    ]
                elif section_prefix == "1.4":
                    steps = [
                        {"step": 1, "content": "Simplify \\(3\\sqrt5 + 2\\sqrt5 - \\sqrt5\\).", "explanation": "Like surds combine by coefficients."},
                        {"step": 2, "content": "Simplify \\((4+\\sqrt3)(4-\\sqrt3)\\).", "explanation": "Use conjugate identity: \\(a^2-b\\)."},
                        {"step": 3, "content": "Rationalise \\(\\frac{1}{3+\\sqrt2}\\).", "explanation": "Multiply by conjugate \\(3-\\sqrt2\\)."},
                        {"step": 4, "content": "Explain one mistake to avoid.", "explanation": "Do not combine unlike surds as \\(\\sqrt a + \\sqrt b = \\sqrt{a+b}\\)."},
                    ]
                else:
                    steps = [
                        {"step": 1, "content": "Evaluate \\(27^{1/3}\\) and \\(16^{1/2}\\).", "explanation": "Fractional exponents map to roots."},
                        {"step": 2, "content": "Simplify \\(2^{2/3}\\cdot 2^{1/3}\\).", "explanation": "Same base multiplication adds exponents."},
                        {"step": 3, "content": "Pick the law for \\((ab)^n\\).", "explanation": "Distribution law over multiplication."},
                        {"step": 4, "content": "Write final answers and law names.", "explanation": "Clear presentation helps in exams."},
                    ]
            else:
                steps = [
                    {
                        "step": 1,
                        "content": "Read the question and mark what is being asked.",
                        "explanation": "Students often lose marks by solving the wrong target. Start by identifying whether you need classification, decimal conversion, simplification, or proof-style reasoning.",
                    },
                    {
                        "step": 2,
                        "content": "Rewrite the expression into a standard form.",
                        "explanation": "Convert to fraction form, apply denominator factoring, or simplify roots so the main rule becomes obvious.",
                    },
                    {
                        "step": 3,
                        "content": "Apply the main rule carefully.",
                        "explanation": "Use one theorem/law at a time and keep intermediate results visible.",
                    },
                    {
                        "step": 4,
                        "content": "Simplify and present final answer cleanly.",
                        "explanation": "Reduce fractions, combine like terms, and remove unnecessary complexity.",
                    },
                    {
                        "step": 5,
                        "content": "Sanity-check your answer.",
                        "explanation": "Verify type and behavior (e.g., if denominator has primes other than 2/5, decimal should not terminate).",
                    },
                ]
            add_we(
                topic_key,
                f"{top.name} — NCERT Style Drill {idx}" if idx == 3 else f"{top.name} — Practice Example {idx}",
                steps,
                idx,
            )

    badges_spec = [
        ("Number Explorer", "Complete Section 1.1", {"type": "section_complete", "section_id": str(uid("section.1.1"))}),
        ("Irrational Detective", "Complete Section 1.2", {"type": "section_complete", "section_id": str(uid("section.1.2"))}),
        ("Decimal Master", "Complete Section 1.3", {"type": "section_complete", "section_id": str(uid("section.1.3"))}),
        ("Surd Slayer", "Complete Section 1.4", {"type": "section_complete", "section_id": str(uid("section.1.4"))}),
        ("Exponent Emperor", "Complete Section 1.5", {"type": "section_complete", "section_id": str(uid("section.1.5"))}),
    ]
    for name, desc, crit in badges_spec:
        existing = db.query(Badge).filter(Badge.name == name).first()
        if existing is None:
            db.add(Badge(id=uuid.uuid4(), name=name, description=desc, icon="star", criteria_json=crit))

    items = [
        ("streak_freeze", "Skip a streak break for one day", "snow", 50),
        ("hint_reveal", "Auto-reveal hint 1", "bulb", 20),
        ("skip_question", "Skip one question", "forward", 30),
        ("2x_xp", "Double XP for next 5 questions", "bolt", 100),
    ]
    for name, desc, icon, cost in items:
        existing = db.query(ItemType).filter(ItemType.name == name).first()
        if existing is None:
            db.add(ItemType(id=uuid.uuid4(), name=name, description=desc, icon=icon, cost_xp=cost))

    db.commit()


def main() -> None:
    db = SessionLocal()
    try:
        seed_chapter1(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
