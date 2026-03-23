# Ignyt — Gamified Learning Platform

## Vision
A gamified learning web app that turns textbook chapters into interactive quests. Starting with Class 9 NCERT Maths Chapter 1 (Number Systems), designed to be extensible to any chapter, grade, or subject.

Target audience: 9th class students who find maths hard and need encouragement, not intimidation.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite + TypeScript |
| Styling | Tailwind CSS (light + dark theme) |
| Math rendering | KaTeX |
| Animations | Framer Motion |
| Interactive widgets | Canvas/SVG |
| Backend | FastAPI (Python 3.12) |
| Database | PostgreSQL 16 |
| ORM | SQLAlchemy 2.0 + Alembic |
| Math validation | SymPy |
| Auth | JWT (python-jose + passlib) |
| Containers | Podman + podman-compose |
| Repo | Monorepo at ~/projects/personal/ignyt/ |
| GitHub | github.com/parvez301/ignyt |

## Project Structure

```
ignyt/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/           # Button, Card, Modal, ThemeToggle
│   │   │   ├── auth/             # LoginForm, SignupForm
│   │   │   ├── dashboard/        # HomeDashboard, StreakCounter, XPBar
│   │   │   ├── chapter-map/      # QuestPath, SectionNode
│   │   │   ├── learn/            # ConceptCard, WorkedExample, RealWorldHook
│   │   │   ├── practice/         # QuestionScreen, MCQ, FillIn, DragDrop, TrueFalse
│   │   │   ├── feedback/         # CorrectAnswer, WrongAnswer, MisconceptionExplain
│   │   │   ├── leaderboard/      # LeaderboardTable, DailyChallenge
│   │   │   └── profile/          # UserProfile, BadgeGrid, StatsOverview
│   │   ├── pages/
│   │   │   ├── LoginPage.tsx
│   │   │   ├── SignupPage.tsx
│   │   │   ├── HomePage.tsx
│   │   │   ├── ChapterMapPage.tsx
│   │   │   ├── LearnPage.tsx
│   │   │   ├── PracticePage.tsx
│   │   │   ├── MasterPage.tsx
│   │   │   ├── ResultsPage.tsx
│   │   │   ├── LeaderboardPage.tsx
│   │   │   ├── DailyChallengePage.tsx
│   │   │   ├── ReviewPage.tsx
│   │   │   └── ProfilePage.tsx
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useProgress.ts
│   │   │   ├── useQuestions.ts
│   │   │   └── useTheme.ts
│   │   ├── api/
│   │   │   └── client.ts          # Axios/fetch wrapper with JWT interceptor
│   │   ├── stores/
│   │   │   ├── authStore.ts       # Zustand
│   │   │   ├── progressStore.ts
│   │   │   ├── questionStore.ts   # Current practice session state (question index, answers, timer)
│   │   │   └── themeStore.ts
│   │   ├── types/
│   │   │   └── index.ts           # Shared TypeScript interfaces
│   │   ├── theme/
│   │   │   └── tokens.ts          # CSS variable definitions for light/dark
│   │   ├── utils/
│   │   │   └── katex.ts           # KaTeX rendering helpers
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── router.tsx             # React Router v6
│   ├── index.html
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── main.py                # FastAPI app, CORS, lifespan
│   │   ├── config.py              # Settings from env vars
│   │   ├── database.py            # SQLAlchemy engine + session
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py            # User, Streak
│   │   │   ├── content.py         # Subject, Grade, Chapter, Section, Topic
│   │   │   ├── learning.py        # ConceptCard, WorkedExample, RealWorldAnchor
│   │   │   ├── question.py        # QuestionTemplate, QuestionAttempt, GeneratedQuestion
│   │   │   ├── progress.py        # UserProgress, UserSectionProgress, UserWorkedExample
│   │   │   ├── gamification.py    # XPLedger, Badge, UserBadge, UserMilestone
│   │   │   ├── inventory.py       # ItemType, UserInventory, ItemUsageLog
│   │   │   ├── challenge.py       # DailyChallenge, DailyChallengeAttempt
│   │   │   ├── review.py          # ReviewQueue
│   │   │   └── feedback.py        # Feedback, Tip
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── content.py
│   │   │   ├── question.py
│   │   │   ├── progress.py
│   │   │   └── gamification.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py            # POST /auth/signup, /auth/login; GET /auth/me; PATCH /auth/me
│   │   │   ├── content.py         # GET /subjects, /chapters, /sections, /topics
│   │   │   ├── learn.py           # GET /topics/{id}/learn (concept cards + worked examples)
│   │   │   ├── questions.py       # POST /topics/{id}/questions, POST /questions/{id}/check
│   │   │   ├── progress.py        # GET /users/me/progress, chapter map state
│   │   │   ├── gamification.py    # GET /leaderboard, /users/me/badges, /users/me/streak, inventory
│   │   │   ├── daily_challenge.py # GET /daily-challenge, POST /daily-challenge/submit
│   │   │   └── review.py          # GET /review/due, POST /review/submit
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── question_engine.py # Generate, validate (sympy), hints
│   │   │   ├── progress_service.py
│   │   │   ├── xp_service.py      # XP calculation, level-up logic
│   │   │   ├── badge_service.py   # Check and award badges
│   │   │   ├── streak_service.py
│   │   │   ├── review_service.py  # SM-2 spaced repetition algorithm
│   │   │   └── challenge_service.py
│   │   ├── question_generators/
│   │   │   ├── __init__.py
│   │   │   ├── base.py            # Abstract base generator
│   │   │   ├── ch1_s1_rationals.py        # Section 1.1 generators
│   │   │   ├── ch1_s2_irrationals.py      # Section 1.2 generators
│   │   │   ├── ch1_s3_decimals.py         # Section 1.3 generators
│   │   │   ├── ch1_s4_operations.py       # Section 1.4 generators
│   │   │   └── ch1_s5_exponents.py        # Section 1.5 generators
│   │   └── seed/
│   │       ├── __init__.py
│   │       └── chapter1.py        # Seed all Chapter 1 content
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   └── alembic.ini
│   ├── tests/
│   │   ├── test_question_engine.py
│   │   ├── test_auth.py
│   │   └── test_progress.py
│   ├── requirements.txt
│   └── pyproject.toml
├── podman-compose.yml
├── Containerfile.frontend
├── Containerfile.backend
├── .env.example
├── .gitignore
└── README.md
```

## API Conventions

- **Pagination:** All list endpoints use `?page=1&per_page=20` query params. Response includes `{items: [...], total: N, page: N, per_page: N}`.
- **Error responses:** `{detail: "Error message"}` with appropriate HTTP status codes (400, 401, 403, 404, 422).
- **Auth:** All endpoints except `/api/auth/signup` and `/api/auth/login` require `Authorization: Bearer <JWT>` header.
- **Rate limiting:** Auth endpoints limited to 5 requests/minute per IP (use slowapi). Other endpoints: 60 requests/minute per user.

## Database Schema

### Core Content (extensible to any subject)

```sql
CREATE TABLE subjects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    icon VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE grades (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subject_id UUID NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,        -- "Class 9"
    level INTEGER NOT NULL,            -- 9
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE chapters (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    grade_id UUID NOT NULL REFERENCES grades(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,        -- "Number Systems"
    description TEXT,
    "order" INTEGER NOT NULL,          -- 1
    icon VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE sections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chapter_id UUID NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,        -- "Rational Numbers"
    section_number VARCHAR(10),        -- "1.1"
    "order" INTEGER NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE topics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    section_id UUID NOT NULL REFERENCES sections(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,        -- "Find rationals between two numbers"
    difficulty INTEGER NOT NULL CHECK (difficulty BETWEEN 1 AND 3),
    "order" INTEGER NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE topic_prerequisites (
    topic_id UUID REFERENCES topics(id) ON DELETE CASCADE,
    prerequisite_topic_id UUID REFERENCES topics(id) ON DELETE CASCADE,
    PRIMARY KEY (topic_id, prerequisite_topic_id)
);
```

### Learning Content

```sql
CREATE TABLE concept_cards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    content_html TEXT NOT NULL,         -- KaTeX-ready HTML
    "order" INTEGER NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE worked_examples (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    steps_json JSONB NOT NULL,         -- [{step: 1, content: "...", explanation: "..."}]
    "order" INTEGER NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- One hook per section (not per topic). The /topics/{id}/learn endpoint
-- joins up to the parent section to fetch the real_world_anchor.
CREATE TABLE real_world_anchors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    section_id UUID NOT NULL REFERENCES sections(id) ON DELETE CASCADE,
    hook_text TEXT NOT NULL,
    media_url VARCHAR(500),
    created_at TIMESTAMPTZ DEFAULT now()
);
```

### Question Engine

```sql
CREATE TABLE question_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,         -- mcq | fill_in | drag_drop | true_false | number_line | step_solver | long_division
    generator_key VARCHAR(100) NOT NULL, -- maps to Python generator function
    difficulty INTEGER NOT NULL CHECK (difficulty BETWEEN 1 AND 3),
    misconceptions_json JSONB,         -- nullable: not all questions trigger misconceptions
    hints_json JSONB NOT NULL,         -- always required: ["Think about...", "Try calculating...", "23 is not..."]
    template_metadata JSONB,           -- extra config per question type
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Server-side storage of generated question instances.
-- Prevents client from inspecting params_json to derive answers.
-- Questions expire after 1 hour (cleaned up by periodic task).
CREATE TABLE generated_questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    question_template_id UUID NOT NULL REFERENCES question_templates(id) ON DELETE CASCADE,
    params_json JSONB NOT NULL,        -- randomized params (server-side only, never sent to client)
    correct_answer TEXT NOT NULL,       -- pre-computed correct answer
    question_html TEXT NOT NULL,        -- rendered question text (sent to client)
    options_json JSONB,                -- MCQ options (sent to client)
    phase VARCHAR(20) NOT NULL,        -- practice | master | review | daily_challenge
    answered BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL    -- auto-cleanup after 1 hour
);
```

### Users & Auth

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(100) NOT NULL,
    avatar VARCHAR(100) DEFAULT 'default',
    password_hash VARCHAR(255) NOT NULL,
    theme VARCHAR(10) DEFAULT 'dark' CHECK (theme IN ('light', 'dark')),
    total_xp INTEGER DEFAULT 0,        -- denormalized, updated transactionally with xp_ledger
    level INTEGER DEFAULT 1,           -- computed from total_xp thresholds
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE streaks (
    user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    last_active_date DATE,
    updated_at TIMESTAMPTZ DEFAULT now()
);
```

### Progress Tracking

```sql
CREATE TABLE user_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    topic_id UUID NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    phase VARCHAR(20) NOT NULL DEFAULT 'locked'
        CHECK (phase IN ('locked', 'learn', 'practice', 'master', 'completed')),
    stars INTEGER DEFAULT 0 CHECK (stars BETWEEN 0 AND 3),
    best_score INTEGER DEFAULT 0,
    attempts INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE (user_id, topic_id)
);

CREATE TABLE user_section_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    section_id UUID NOT NULL REFERENCES sections(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'locked'
        CHECK (status IN ('locked', 'in_progress', 'completed')),
    stars_earned INTEGER DEFAULT 0,
    stars_possible INTEGER DEFAULT 0,
    unlocked_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE (user_id, section_id)
);

CREATE TABLE user_worked_examples (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    worked_example_id UUID NOT NULL REFERENCES worked_examples(id) ON DELETE CASCADE,
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMPTZ,
    UNIQUE (user_id, worked_example_id)
);

CREATE TABLE question_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    question_template_id UUID NOT NULL REFERENCES question_templates(id) ON DELETE CASCADE,
    generated_question_id UUID REFERENCES generated_questions(id),
    params_json JSONB,                 -- copy of the randomized params used
    user_answer TEXT,
    correct_answer TEXT,
    is_correct BOOLEAN NOT NULL,
    misconception_key VARCHAR(100),    -- which misconception they hit (if wrong)
    hints_used INTEGER DEFAULT 0,
    time_taken_seconds INTEGER,
    created_at TIMESTAMPTZ DEFAULT now()
);
```

### Gamification

```sql
CREATE TABLE xp_ledger (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    amount INTEGER NOT NULL,
    source VARCHAR(50) NOT NULL,       -- question | daily_challenge | streak_bonus | badge | login
    topic_id UUID REFERENCES topics(id),  -- nullable: not all XP sources are topic-specific
    created_at TIMESTAMPTZ DEFAULT now()
);
-- When inserting into xp_ledger, ALWAYS also UPDATE users SET total_xp = total_xp + amount
-- in the same transaction. This keeps the denormalized total_xp in sync.

CREATE TABLE badges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon VARCHAR(100),
    criteria_json JSONB NOT NULL       -- {"type": "section_complete", "section_id": "..."}
);

CREATE TABLE user_badges (
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    badge_id UUID NOT NULL REFERENCES badges(id) ON DELETE CASCADE,
    earned_at TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (user_id, badge_id)
);

CREATE TABLE user_milestones (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    milestone_type VARCHAR(50) NOT NULL,  -- first_star | section_complete | streak_7 | xp_100
    milestone_value VARCHAR(200),
    seen BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT now()
);
```

### Inventory & Rewards

```sql
CREATE TABLE item_types (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(50) NOT NULL,         -- streak_freeze | hint_reveal | skip_question | 2x_xp
    description TEXT,
    icon VARCHAR(100),
    cost_xp INTEGER NOT NULL
);

CREATE TABLE user_inventory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    item_type_id UUID NOT NULL REFERENCES item_types(id) ON DELETE CASCADE,
    quantity INTEGER DEFAULT 0,
    updated_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE (user_id, item_type_id)
);

CREATE TABLE item_usage_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    item_type_id UUID NOT NULL REFERENCES item_types(id) ON DELETE CASCADE,
    context VARCHAR(200),
    used_at TIMESTAMPTZ DEFAULT now()
);
```

### Challenges & Competition

Note: `challenges` and `challenge_responses` (head-to-head) are Phase 4. Do NOT create these tables in the initial migration. Only create `daily_challenges` and `daily_challenge_attempts` (Phase 2).

```sql
-- Phase 2 tables:
CREATE TABLE daily_challenges (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    challenge_date DATE UNIQUE NOT NULL,
    questions_json JSONB NOT NULL,      -- [{template_id, params_json}]
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE daily_challenge_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    challenge_id UUID NOT NULL REFERENCES daily_challenges(id) ON DELETE CASCADE,
    score INTEGER NOT NULL,
    time_taken_seconds INTEGER,
    completed_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE (user_id, challenge_id)
);

-- Phase 4 tables (do NOT create in initial migration):
-- challenges (challenger_id, opponent_id, topic_id, status, questions_json, ...)
-- challenge_responses (challenge_id, user_id, score, time_taken_seconds, ...)
```

### Spaced Repetition

```sql
CREATE TABLE review_queue (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    question_template_id UUID NOT NULL REFERENCES question_templates(id) ON DELETE CASCADE,
    last_params_json JSONB,
    next_review_at DATE NOT NULL,
    interval_days INTEGER DEFAULT 1,
    ease_factor FLOAT DEFAULT 2.5,
    review_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    UNIQUE (user_id, question_template_id)
);
```

### Engagement

```sql
CREATE TABLE tips (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    topic_id UUID REFERENCES topics(id),
    display_after_event VARCHAR(50)     -- on_login | after_wrong_answer | after_streak_break
);

CREATE TABLE feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    topic_id UUID REFERENCES topics(id),
    question_template_id UUID REFERENCES question_templates(id),
    message TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Phase 4: learning_sessions table (do NOT create in initial migration)
-- learning_sessions (user_id, started_at, ended_at, topics_covered, questions_answered, xp_earned)
```

### Indexes

```sql
-- Content ordering
CREATE INDEX idx_chapters_grade_order ON chapters(grade_id, "order");
CREATE INDEX idx_sections_chapter_order ON sections(chapter_id, "order");
CREATE INDEX idx_topics_section_order ON topics(section_id, "order");
CREATE INDEX idx_concept_cards_topic_order ON concept_cards(topic_id, "order");
CREATE INDEX idx_worked_examples_topic_order ON worked_examples(topic_id, "order");

-- User progress queries
CREATE INDEX idx_user_progress_user ON user_progress(user_id);
CREATE INDEX idx_user_section_progress_user ON user_section_progress(user_id);

-- Question tracking
CREATE INDEX idx_question_attempts_user_created ON question_attempts(user_id, created_at);
CREATE INDEX idx_question_attempts_template ON question_attempts(question_template_id);
CREATE INDEX idx_generated_questions_user ON generated_questions(user_id, expires_at);
CREATE INDEX idx_generated_questions_expiry ON generated_questions(expires_at) WHERE answered = FALSE;

-- Gamification
CREATE INDEX idx_xp_ledger_user_created ON xp_ledger(user_id, created_at);

-- Spaced repetition
CREATE INDEX idx_review_queue_user_next ON review_queue(user_id, next_review_at);

-- Leaderboard (uses users.total_xp directly, no aggregation needed)
CREATE INDEX idx_users_total_xp ON users(total_xp DESC);

-- Daily challenges
CREATE INDEX idx_daily_challenge_attempts_challenge_score ON daily_challenge_attempts(challenge_id, score DESC);
```

## Topic Progress State Machine

Each topic has a phase that progresses through a strict state machine:

```
locked → learn → practice → master → completed
```

### Transition Rules

| Current Phase | Next Phase | Trigger | Preconditions |
|---------------|------------|---------|---------------|
| `locked` | `learn` | Auto-unlock | Topic's section is unlocked (see Section Unlock below) AND all prerequisite topics are `completed` |
| `learn` | `practice` | `POST /topics/{id}/complete-phase {phase: "learn"}` | All worked examples for this topic are marked completed |
| `practice` | `master` | `POST /topics/{id}/complete-phase {phase: "practice", score: N}` | Score >= 50% (at least attempted all questions) |
| `master` | `completed` | `POST /topics/{id}/complete-phase {phase: "master", score: N}` | Score >= 50% |
| `completed` | `completed` | Re-attempt practice or master | Stars and best_score update if improved; phase stays `completed` |

### Star Computation (server-side only — never trust client)

Stars are computed by the server from `phase` and `score`:
- **1 star:** Complete practice phase with any score
- **2 stars:** Score >= 80% in practice
- **3 stars:** Score >= 90% in master phase

Stars accumulate (max of previous and new): if a student gets 2 stars in practice and later 3 stars in master, they keep 3 stars.

### Section Unlock Rules

| Section Status | Trigger |
|---------------|---------|
| First section (1.1) | Auto-unlocked on signup |
| Subsequent sections | Previous section status = `completed` (all topics in previous section are `completed`) |
| Section becomes `in_progress` | When first topic in section transitions from `locked` to `learn` |
| Section becomes `completed` | When all topics in section are `completed` |

### Side Effects on Phase Transition

When a phase completes, the `progress_service` must:
1. Update `user_progress.phase`, `.stars`, `.best_score`, `.attempts`
2. Recalculate `user_section_progress.stars_earned` (sum of topic stars)
3. Check if section is now complete → unlock next section's topics
4. Award XP via `xp_service` (which updates both `xp_ledger` AND `users.total_xp`)
5. Check badge criteria via `badge_service`
6. Create `user_milestones` entries for any new milestones (celebration triggers)
7. If answer was wrong, optionally add to `review_queue` for spaced repetition (Phase 2)

## API Endpoints

### Auth
```
POST /api/auth/signup          → {username, email, password, display_name} → {token, user}
POST /api/auth/login           → {username, password} → {token, user}
GET  /api/auth/me              → user profile (requires JWT)
PATCH /api/auth/me             → update display_name, avatar, theme
```

### Content
```
GET  /api/subjects                      → list all subjects
GET  /api/subjects/{id}/grades          → list grades for subject
GET  /api/grades/{id}/chapters          → list chapters for grade
GET  /api/chapters/{id}                 → chapter detail + sections
GET  /api/chapters/{id}/map             → chapter map with user progress per section
GET  /api/sections/{id}/topics          → list topics in section
GET  /api/topics/{id}/learn             → concept cards + worked examples + real-world hook
                                          (joins to parent section for real_world_anchor)
POST /api/topics/{id}/worked-examples/{we_id}/complete → mark worked example as done
```

### Questions
```
POST /api/topics/{id}/questions         → generate a set of questions for practice/master
     body: {phase: "practice"|"master", count: 5}
     returns: [{generated_question_id, type, question_html, options?}]
     NOTE: params_json is stored server-side in generated_questions table.
           The client only receives generated_question_id + rendered content.
           This prevents cheating by inspecting params.

POST /api/questions/{generated_question_id}/check → validate an answer
     body: {user_answer}
     returns: {is_correct, correct_answer_html, misconception_explanation?, xp_earned, hints_used}
     NOTE: Server looks up correct_answer from generated_questions table,
           validates using sympy, computes XP server-side, records attempt.

POST /api/questions/{generated_question_id}/hint → get next progressive hint
     body: {hint_number: 1|2|3}
     returns: {hint_text}
     NOTE: Hints come from the generator's get_hints() method (parameterized),
           falling back to question_templates.hints_json if generator doesn't override.
```

### Progress
```
GET  /api/users/me/progress             → overall stats: total_xp, level, streak, total_stars
GET  /api/users/me/progress/chapter/{id} → per-chapter progress breakdown
POST /api/topics/{id}/complete-phase    → mark learn/practice/master as done
     body: {phase, score}
     NOTE: Stars are computed SERVER-SIDE from phase + score (see State Machine).
           Do NOT send stars from client.
     returns: {new_phase, stars, xp_earned, badges_earned[], milestones[]}
```

### Gamification
```
GET  /api/leaderboard                   → top users by total_xp (paginated via ?page=&per_page=)
     NOTE: Uses users.total_xp column directly, no aggregation needed.
GET  /api/users/me/badges               → earned badges
GET  /api/users/me/streak               → streak info
GET  /api/users/me/milestones           → unseen milestones (for celebration animations)
POST /api/users/me/milestones/{id}/seen → mark milestone as seen
GET  /api/users/me/inventory            → items owned
POST /api/users/me/inventory/buy        → buy an item with XP
     body: {item_type_id}
     returns: {success, new_xp_total, item_quantity}
     NOTE: Deducts cost_xp from users.total_xp (fails if insufficient).
           Inserts negative entry into xp_ledger with source="shop_purchase".
POST /api/users/me/inventory/use        → use an item (streak_freeze, etc.)
     body: {item_type_id, context?}
     returns: {success, remaining_quantity}
```

### Daily Challenge (Phase 2)
```
GET  /api/daily-challenge               → today's challenge (5 questions)
POST /api/daily-challenge/submit        → submit answers
     body: {answers: [{question_index, answer}], time_taken_seconds}
     returns: {score, rank, xp_earned}
GET  /api/daily-challenge/leaderboard   → today's rankings
```

### Review / Spaced Repetition (Phase 2)
```
GET  /api/review/due                    → questions due for review today
POST /api/review/submit                 → submit review answer
     body: {review_id, answer, quality: 0-5}  (quality = SM-2 self-rating)
     returns: {is_correct, next_review_date}
GET  /api/review/stats                  → review queue size, upcoming reviews
```

## Question Engine Design

### Generator Architecture

Each question type has a Python generator class:

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from sympy import simplify, sympify, SympifyError

@dataclass
class GeneratedQuestion:
    question_html: str           # KaTeX-ready question text
    correct_answer: str          # Canonical answer for validation
    options: list[str] | None    # MCQ options (None for fill-in)
    params: dict                 # Randomized params (stored server-side)
    misconception_map: dict      # {wrong_option: "explanation"} for MCQs

@dataclass
class ValidationResult:
    is_correct: bool
    correct_answer_html: str     # Human-readable correct answer
    misconception_key: str | None
    misconception_explanation: str | None

class BaseQuestionGenerator(ABC):
    @abstractmethod
    def generate(self, difficulty: int) -> GeneratedQuestion:
        """Generate a question with randomized parameters."""
        pass

    @abstractmethod
    def validate(self, params: dict, user_answer: str) -> ValidationResult:
        """Validate answer using sympy for symbolic comparison."""
        pass

    def get_hints(self, params: dict) -> list[str]:
        """Return 3 progressive hints. Override for parameterized hints.
        Falls back to static hints_json from question_template if not overridden."""
        return []

    @staticmethod
    def symbolic_equal(user_answer: str, correct_answer: str) -> bool:
        """Compare two math expressions symbolically using sympy."""
        try:
            user_expr = sympify(user_answer)
            correct_expr = sympify(correct_answer)
            return simplify(user_expr - correct_expr) == 0
        except (SympifyError, ValueError, TypeError):
            return False
```

### Chapter 1 Question Generators

**Section 1.1 — Rational Numbers:**
- `classify_number`: Given a number, classify as N/W/Z/Q — MCQ
- `find_rationals_between`: Find n rational numbers between a/b and c/d — fill_in
- `true_false_number_types`: "Every natural number is a whole number" — true_false with reasoning
- `drag_classify_numbers`: Sort a set of numbers into N/W/Z/Q/R bags — drag_drop (Phase 2)

**Section 1.2 — Irrational Numbers:**
- `classify_rational_irrational`: Is this number rational or irrational? — MCQ
- `identify_irrationals_in_set`: Pick all irrationals from a list — MCQ (multi-select)
- `true_false_irrationals`: True/false statements about irrational numbers — true_false

**Section 1.3 — Decimal Expansions:**
- `decimal_expansion_type`: What type of decimal does p/q produce? — MCQ
- `convert_fraction_to_decimal`: Find the decimal expansion of p/q — fill_in
- `convert_recurring_to_fraction`: Express 0.abab... as p/q — fill_in (sympy validated)
- `predict_decimal_pattern`: Predict decimal of 4/7 knowing 1/7 — fill_in

**Section 1.4 — Operations on Real Numbers:**
- `simplify_surd_expression`: Simplify (a+√b)(c+√d) — fill_in (sympy validated)
- `rationalise_denominator`: Rationalise 1/(a+√b) — fill_in (sympy validated)
- `classify_after_operation`: Is (√a + √b) rational or irrational? — MCQ
- `add_subtract_surds`: Simplify 2√3 + 5√3 - √3 — fill_in

**Section 1.5 — Laws of Exponents:**
- `evaluate_fractional_exponent`: Find 64^(1/2) — fill_in
- `simplify_exponent_expression`: Simplify 2^(2/3) * 2^(1/3) — fill_in (sympy validated)
- `apply_exponent_law`: Which law applies? — MCQ

## UI/UX Design

### Theme System

CSS variables switch between light and dark via Tailwind's `dark:` variant:

```
--bg-primary:      dark #0f172a  |  light #f8fafc
--bg-card:         dark #1e293b  |  light #ffffff
--bg-surface:      dark #334155  |  light #e2e8f0
--text-primary:    dark #f1f5f9  |  light #0f172a
--text-secondary:  dark #94a3b8  |  light #64748b
--brand:           #6366f1 (both)
--success:         #22c55e (both)
--warning:         #f59e0b (both)
--danger:          #ef4444 (both)
```

Toggle via sun/moon icon in top bar. Preference stored in `users.theme` column and synced via `PATCH /api/auth/me`.

### Key Screens

1. **Home Dashboard** — greeting, streak counter, XP bar, continue learning card, daily challenge card, review due count, mini leaderboard
2. **Chapter Map** — vertical quest path, sections as nodes (locked/in-progress/completed with stars), current section glows
3. **Learn Phase** — real-world hook at top, concept cards (bite-sized, KaTeX rendered), worked examples with step-by-step reveal and "Why?" buttons
4. **Practice Phase** — progress bar (Q3 of 5), question card with KaTeX math, answer input (MCQ grid / fill-in), hint button with count, skip button, XP preview
5. **Master Phase** — same as practice but harder variants + countdown timer
6. **Results Screen** — score, stars earned (with animation), XP gained, streaks updated, "Next Section" or "Review Mistakes"
7. **Wrong Answer Feedback** — encouraging tone ("Almost!"), misconception-specific explanation with key insight box, "Got it! Next question" button
8. **Leaderboard** — ranked list with avatars, XP, streaks
9. **Daily Challenge** — 5 questions, 5-minute timer, submit for score + ranking (Phase 2)
10. **Review Queue** — spaced repetition questions due today (Phase 2)
11. **Profile** — stats, badges earned, streak history, inventory

### Design Principles
- Desktop-first layout (1200px max-width, centered)
- One question at a time — no scrolling during practice
- Big, clear action buttons
- Encouraging tone throughout — "Almost!" not "Wrong!"
- Celebration animations on milestones (Framer Motion confetti/particles)
- KaTeX for all math rendering (fractions, surds, exponents)
- No lives/hearts — mistakes redirect, never punish

## Gamification Rules

### XP System
| Action | XP |
|--------|-----|
| Correct answer (practice) | +10 |
| Correct answer (master) | +20 |
| Correct answer (daily challenge) | +15 |
| Correct answer (review) | +5 |
| No hints used bonus | +5 |
| First try bonus | +5 |
| Streak bonus (3 correct in a row) | +10 |
| Complete Learn phase | +20 |
| Complete section (3 stars) | +50 |
| Daily login | +5 |

### Level Thresholds
| Level | XP Required |
|-------|------------|
| 1 | 0 |
| 2 | 100 |
| 3 | 250 |
| 4 | 500 |
| 5 | 1000 |
| 6 | 2000 |
| 7 | 3500 |
| 8 | 5500 |
| 9 | 8000 |
| 10 | 12000 |

### Stars
- 1 star: Complete practice phase (any score)
- 2 stars: Score >= 80% in practice
- 3 stars: Score >= 90% in master phase

### Streak
- Increments each calendar day they answer at least 1 question
- Streak freeze item prevents streak break for 1 day
- Streak milestones: 3, 7, 14, 30, 60, 100 days → badges

### Badges (Chapter 1)
| Badge | Criteria |
|-------|----------|
| Number Explorer | Complete Section 1.1 |
| Irrational Detective | Complete Section 1.2 |
| Decimal Master | Complete Section 1.3 |
| Surd Slayer | Complete Section 1.4 |
| Exponent Emperor | Complete Section 1.5 |
| Chapter Champion | Complete all 5 sections |
| Perfect Chapter | 3 stars on all sections |
| Speed Demon | Complete a master phase in under 2 minutes |
| Streak Starter | 3-day streak |
| Week Warrior | 7-day streak |
| Hint-Free Hero | Complete a practice without using hints |
| Daily Challenger | Complete 5 daily challenges |

## Container Setup (Podman)

### podman-compose.yml
```yaml
version: "3.8"

services:
  postgres:
    image: postgres:16-alpine
    container_name: ignyt-postgres
    environment:
      POSTGRES_DB: ignyt_db
      POSTGRES_USER: ignyt_user
      POSTGRES_PASSWORD: ignyt_password
    volumes:
      - ignyt-postgres-data:/var/lib/postgresql/data
    ports:
      - "5433:5432"    # 5433 to avoid conflict with ShipRate's 5432
    networks:
      - ignyt-network

  api:
    build:
      context: .
      dockerfile: Containerfile.backend
    container_name: ignyt-api
    environment:
      DATABASE_URL: postgresql://ignyt_user:ignyt_password@postgres:5432/ignyt_db
      JWT_SECRET: change-me-in-production
      CORS_ORIGINS: http://localhost:5173
    volumes:
      - ./backend:/app
    ports:
      - "8001:8000"    # 8001 to avoid conflict with ShipRate's 8000
    depends_on:
      - postgres
    networks:
      - ignyt-network
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: .
      dockerfile: Containerfile.frontend
    container_name: ignyt-frontend
    volumes:
      - ./frontend:/app
      - /app/node_modules
    ports:
      - "5173:5173"
    depends_on:
      - api
    networks:
      - ignyt-network
    command: npm run dev -- --host 0.0.0.0

volumes:
  ignyt-postgres-data:

networks:
  ignyt-network:
    driver: bridge
```

### Containerfile.backend
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### Containerfile.frontend
```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY frontend/package.json frontend/package-lock.json ./
RUN npm install

COPY frontend/ .

EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

## Seed Data — Chapter 1: Number Systems

The seed script (`backend/app/seed/chapter1.py`) populates:

### Subject & Grade
- Subject: Mathematics (icon: "calculator")
- Grade: Class 9 (level: 9)

### Chapter
- Chapter 1: Number Systems

### Sections (5)
1. **1.1 — Rational Numbers** (3 topics)
2. **1.2 — Irrational Numbers** (3 topics)
3. **1.3 — Decimal Expansions** (4 topics)
4. **1.4 — Operations on Real Numbers** (4 topics)
5. **1.5 — Laws of Exponents** (3 topics)

### Topics (17 total)

**Section 1.1:**
1. Classify numbers into N, W, Z, Q sets
2. Find rational numbers between two given rationals
3. True/false statements about number types

**Section 1.2:**
1. Identify rational vs irrational numbers
2. Recognize perfect squares vs non-perfect squares under root
3. Properties of irrational numbers (true/false)

**Section 1.3:**
1. Determine if a fraction gives terminating or recurring decimal
2. Find decimal expansion by long division
3. Convert recurring decimal to p/q form
4. Predict decimal patterns using remainder analysis

**Section 1.4:**
1. Add and subtract expressions with surds
2. Multiply and divide surd expressions
3. Simplify using identities: (a+root(b))(a-root(b)) = a^2-b
4. Rationalise the denominator

**Section 1.5:**
1. Evaluate numbers with fractional exponents
2. Simplify expressions using exponent laws
3. Apply multiple exponent laws in combination

### Real-World Hooks (per section)
1. S1.1: "Every time you count your change — 1, 2, 3 rupees — you're using natural numbers. But what about splitting a pizza? That's where rationals come in."
2. S1.2: "Your phone screen is 6.1 inches diagonally. But the diagonal of a 1x1 inch square is root(2) inches. You literally hold irrational numbers in your hand every day."
3. S1.3: "When you split 100 rupees equally among 3 friends, each gets 33.333... forever. That repeating pattern isn't a glitch — it's mathematics telling you 100 and 3 don't divide evenly."
4. S1.4: "Engineers building bridges need to calculate exact diagonal lengths like root(2) + root(3). They can't just approximate — lives depend on rationalising these expressions correctly."
5. S1.5: "Computer storage: KB, MB, GB, TB — each is 2^10 times the last. Understanding exponents is how you understand why your phone says '128 GB' instead of '128,000 MB'."

### Concept Cards, Worked Examples, Question Templates
Each topic gets:
- 1-3 concept cards (bite-sized explanations with KaTeX)
- 1-2 worked examples (matching NCERT Examples 1-20)
- 2-4 question templates (parameterized generators)
- 3 hints per template (progressive: nudge -> approach -> walkthrough)
- Misconception mappings for wrong answers

### Badges (12)
See Gamification Rules section above.

### Item Types
- Streak Freeze (cost: 50 XP)
- Hint Reveal (cost: 20 XP) — auto-reveals hint 1
- Skip Question (cost: 30 XP)
- 2x XP Boost (cost: 100 XP) — doubles XP for next 5 questions

## Phased Delivery

### Phase 1 — Foundation (build first, all in initial migration)
1. Project scaffolding (monorepo, podman-compose, Containerfiles, .env)
2. Database schema + Alembic migration (Phase 1 tables only — see notes on each table)
3. Auth system (signup, login, JWT, GET /me, PATCH /me)
4. Content model API (CRUD for subjects -> topics)
5. Question engine with sympy validation (5 generator files, ~17 generators)
6. Seed script for Chapter 1 (all sections, topics, concept cards, worked examples, hooks, templates, badges)
7. Frontend scaffolding (Vite, React Router, Tailwind, KaTeX, Zustand stores, theme system)
8. Auth pages (login, signup)
9. Home dashboard
10. Chapter map (quest path)
11. Learn phase (concept cards + worked examples with step reveals)
12. Practice phase (MCQ + fill-in question types)
13. Master phase (harder + timed)
14. Results screen with stars + XP
15. Wrong answer feedback with misconception explanations
16. Basic gamification: XP ledger, stars, streak counter, level display
17. Leaderboard page
18. Profile page with badges
19. Light/dark theme toggle

### Phase 2 — Engagement (after user feedback)
- Daily challenges (create daily_challenges + daily_challenge_attempts tables)
- Spaced repetition review queue (SM-2 algorithm)
- Celebration animations (Framer Motion confetti)
- Inventory system (buy + use items)
- Drag-and-drop question type
- True/false with reasoning question type

### Phase 3 — Interactive Widgets
- Interactive number line explorer (zoom between rationals)
- Long division animator
- Square root spiral builder
- Step-by-step solver question type
- Number classification drag-into-bags widget

### Phase 4 — Competition & Analytics
- Head-to-head challenges (create challenges + challenge_responses tables)
- Unlockable avatars and themes (create unlockables + user_unlockables tables)
- Prerequisite graph with adaptive routing
- Learning session analytics (create learning_sessions table)
- Feedback system
