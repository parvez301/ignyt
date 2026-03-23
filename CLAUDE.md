# Ignyt — Project Instructions

## What is Ignyt?

A gamified learning web app that turns textbook chapters into interactive quests. Starting with Class 9 NCERT Maths Chapter 1 (Number Systems). Extensible to any chapter, grade, or subject.

- **Spec:** `docs/SPEC.md` — the single source of truth for architecture, schema, APIs, and game rules
- **GitHub:** github.com/parvez301/ignyt
- **Target users:** 9th class students who find maths hard — the app must be encouraging, never intimidating

## Tech Stack

- **Frontend:** React 18 + Vite + TypeScript + Tailwind CSS + KaTeX + Framer Motion + Zustand
- **Backend:** FastAPI (Python 3.12) + SQLAlchemy 2.0 + Alembic + SymPy
- **Database:** PostgreSQL 16
- **Containers:** Podman + podman-compose (NOT Docker)
- **Formatter:** `ruff` for Python, `eslint` for frontend

## IMPORTANT: Running Scripts and Database Operations

**ALWAYS use the container** for:
- Running Python scripts, migrations, seed scripts
- Database queries and operations

```bash
# Run scripts inside container
podman exec -it ignyt-api python -m app.seed.chapter1

# Run alembic migrations
podman exec -it ignyt-api alembic upgrade head

# Run Python code inside container
podman exec -it ignyt-api python -c "your code here"

# Sync code changes to container (volume-mounted, usually auto-syncs)
# If not syncing, restart: podman-compose restart api
```

**Why?** The local machine cannot connect to the PostgreSQL container network directly on macOS. The container has proper network access and environment variables configured.

## Container Setup

```bash
# Start everything
podman-compose up -d

# Check status
podman ps

# View logs
podman logs -f ignyt-api
podman logs -f ignyt-frontend

# Stop everything
podman-compose down

# Rebuild after dependency changes
podman-compose up -d --build
```

**Ports (chosen to avoid ShipRate conflicts):**
- PostgreSQL: `localhost:5433` (container internal: 5432)
- API: `localhost:8001` (container internal: 8000)
- Frontend: `localhost:5173`

## Testing

### Backend Tests

```bash
# Run all tests inside container
podman exec -it ignyt-api pytest

# Run specific test file
podman exec -it ignyt-api pytest tests/test_question_engine.py -v

# Run with coverage
podman exec -it ignyt-api pytest --cov=app --cov-report=term-missing

# Run a specific test
podman exec -it ignyt-api pytest tests/test_auth.py::test_signup -v
```

**What to test:**
- **Question engine (critical):** Every generator must have tests verifying: generation produces valid output, sympy validation accepts correct answers in multiple formats, wrong answers are rejected, hints return 3 items, misconception keys map correctly
- **Auth:** Signup, login, JWT validation, profile update
- **Progress state machine:** Test every valid transition and verify invalid transitions are rejected (e.g., can't skip from `learn` to `master`)
- **XP service:** Verify XP is awarded correctly AND `users.total_xp` stays in sync with `xp_ledger` sum
- **Star computation:** Verify stars are always computed server-side from score, never trusted from client

### Frontend Tests

```bash
# Run from frontend directory (or inside container)
podman exec -it ignyt-frontend npm test

# Run with UI
podman exec -it ignyt-frontend npm run test:ui
```

**What to test:**
- KaTeX rendering doesn't break on edge cases (fractions, nested surds, exponents)
- Theme toggle persists correctly
- Question flow: generate → answer → feedback → next question
- Practice session state management (questionStore)

### Manual Testing Checklist

Before considering any feature complete:
- [ ] Works in both light and dark theme
- [ ] Math renders correctly with KaTeX (fractions, surds, exponents)
- [ ] Incorrect answers show misconception-specific feedback (not just "Wrong")
- [ ] XP updates on leaderboard after answering
- [ ] Streak counter updates correctly
- [ ] Stars display correctly on chapter map after completing practice/master
- [ ] Section unlocks when previous section is completed

## Code Style & Conventions

### Python (Backend)
- Use `ruff` for formatting (run via `uvx ruff format` or inside container)
- Type hints on all function signatures
- Pydantic schemas for all API request/response models
- SQLAlchemy models use declarative base
- Services contain business logic, routers are thin (just parse request → call service → return response)
- Always use transactions when updating XP (xp_ledger + users.total_xp together)

### TypeScript (Frontend)
- Functional components only
- Zustand for state management (authStore, progressStore, questionStore, themeStore)
- Use `client.ts` API wrapper for all backend calls (handles JWT automatically)
- KaTeX rendering via shared utility (`utils/katex.ts`)
- Tailwind for styling — use CSS variables for theme colors, `dark:` variant for theme switching

### Naming Conventions
- **Files:** snake_case for Python, PascalCase for React components, camelCase for hooks/utils
- **DB tables:** snake_case plural (e.g., `question_templates`, `user_progress`)
- **API routes:** kebab-case (e.g., `/daily-challenge`, `/worked-examples`)
- **Variables:** descriptive names always (no single-letter vars except loop counters)

## Architecture Rules

1. **Questions are generated server-side.** The `generated_questions` table stores params and correct answers. The client NEVER receives `params_json` — only rendered `question_html` and `generated_question_id`. This prevents cheating.

2. **Stars are computed server-side.** The `POST /topics/{id}/complete-phase` endpoint accepts `{phase, score}` only. Stars are calculated from the score using the rules in SPEC.md. Never trust star values from the client.

3. **XP is always transactional.** When awarding XP: insert into `xp_ledger` AND update `users.total_xp` in the same transaction. The leaderboard reads `users.total_xp` directly.

4. **Topic progress follows a strict state machine:** `locked → learn → practice → master → completed`. See `docs/SPEC.md` "Topic Progress State Machine" section for full transition rules. Invalid transitions must be rejected with 400 errors.

5. **Tone is encouraging.** Wrong answer feedback uses phrases like "Almost!", "Common mix-up", "Here's the trick". Never "Wrong!", "Incorrect!", or "Failed".

## Database

- **Container name:** `ignyt-postgres`
- **Database:** `ignyt_db`
- **User:** `ignyt_user`
- **Password:** `ignyt_password`
- **Internal host:** `postgres` (from within podman network)
- **External port:** `5433` (from host machine, if needed)

```bash
# Connect to DB from inside container
podman exec -it ignyt-postgres psql -U ignyt_user -d ignyt_db

# Run a query
podman exec -it ignyt-postgres psql -U ignyt_user -d ignyt_db -c "SELECT count(*) FROM users;"
```

## Phased Delivery

The project is built in 4 phases. See `docs/SPEC.md` for full details.

- **Phase 1 (current):** Foundation — scaffolding, auth, content model, question engine, core UI, basic gamification
- **Phase 2:** Engagement — daily challenges, spaced repetition, animations, inventory
- **Phase 3:** Interactive widgets — number line, long division animator, square root spiral
- **Phase 4:** Competition — head-to-head, unlockables, analytics

**Do NOT build Phase 2+ features during Phase 1.** Do NOT create Phase 2+ database tables in the initial migration. Each phase gets its own Alembic migration.

## Common Tasks

```bash
# Create a new Alembic migration
podman exec -it ignyt-api alembic revision --autogenerate -m "description"

# Seed Chapter 1 data
podman exec -it ignyt-api python -m app.seed.chapter1

# Add a new Python dependency
# 1. Add to requirements.txt
# 2. Rebuild: podman-compose up -d --build api

# Add a new frontend dependency
# 1. podman exec -it ignyt-frontend npm install <package>
# 2. Or add to package.json and rebuild: podman-compose up -d --build frontend

# Format Python code
podman exec -it ignyt-api ruff format .
podman exec -it ignyt-api ruff check --fix .

# Format frontend code
podman exec -it ignyt-frontend npx eslint . --fix
```
