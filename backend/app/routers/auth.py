from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.limiter import limiter
from app.models import User
from app.schemas.auth import LoginRequest, PatchMeRequest, SignupRequest, TokenResponse, UserPublic
from app.services import auth_service
from app.utils.security import create_access_token, verify_password

router = APIRouter()


def user_public(u: User) -> UserPublic:
    return UserPublic.model_validate(u)


@router.post("/signup", response_model=TokenResponse)
@limiter.limit("5/minute")
def signup(request: Request, body: SignupRequest, db: Session = Depends(get_db)) -> TokenResponse:
    if db.query(User).filter(User.username == body.username).first():
        raise HTTPException(status_code=400, detail="Username taken")
    if db.query(User).filter(User.email == body.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = auth_service.create_user(
        db,
        username=body.username,
        email=str(body.email),
        password=body.password,
        display_name=body.display_name,
    )
    db.commit()
    token = create_access_token(user.username)
    return TokenResponse(token=token, user=user_public(user))


@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
def login(request: Request, body: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    user = db.query(User).filter(User.username == body.username).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user.username)
    return TokenResponse(token=token, user=user_public(user))


@router.get("/me", response_model=UserPublic)
def me(user: User = Depends(get_current_user)) -> UserPublic:
    return user_public(user)


@router.patch("/me", response_model=UserPublic)
def patch_me(
    body: PatchMeRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserPublic:
    if body.display_name is not None:
        user.display_name = body.display_name
    if body.avatar is not None:
        user.avatar = body.avatar
    if body.theme is not None:
        user.theme = body.theme
    db.commit()
    db.refresh(user)
    return user_public(user)
