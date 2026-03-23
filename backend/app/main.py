from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.config import get_settings
from app.limiter import limiter
from app.routers import (
    auth,
    content,
    daily_challenge,
    gamification,
    learn,
    progress,
    questions,
    review,
)

settings = get_settings()
origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]

app = FastAPI(title="Ignyt API", version="0.1.0")
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request, exc):  # type: ignore[no-untyped-def]
    from fastapi.responses import JSONResponse

    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(content.router, prefix="/api", tags=["content"])
app.include_router(learn.router, prefix="/api", tags=["learn"])
app.include_router(questions.router, prefix="/api", tags=["questions"])
app.include_router(progress.router, prefix="/api", tags=["progress"])
app.include_router(progress.router_topics, prefix="/api", tags=["progress"])
app.include_router(gamification.router, prefix="/api", tags=["gamification"])
app.include_router(daily_challenge.router, prefix="/api", tags=["daily_challenge"])
app.include_router(review.router, prefix="/api", tags=["review"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
