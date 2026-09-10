from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.database import get_db
from app.models import User
from app.auth.schemas import UserCreate, UserLogin, Token
from app.auth.utils import verify_password, get_password_hash, create_access_token
from app.schemas import APIResponse
from app.services.notification_service import NotificationService

router = APIRouter()

@router.post("/register", response_model=APIResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).where(User.email == user_data.email.lower()))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="An account with this email already exists")
    if len(user_data.password) < 8:
        raise HTTPException(status_code=422, detail="Password must contain at least 8 characters")
    user = User(email=user_data.email.lower(), full_name=user_data.full_name, role=user_data.role, hashed_password=get_password_hash(user_data.password))
    db.add(user)
    await db.flush()
    token = create_access_token({"sub": str(user.user_id), "email": user.email, "role": user.role})
    await NotificationService().send_registration_email(user.email, user.full_name)
    return APIResponse(data=Token(access_token=token), message="Registration successful")

@router.post("/login", response_model=APIResponse)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == credentials.email.lower()))
    user = result.scalar_one_or_none()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.user_id), "email": user.email, "role": user.role})
    return APIResponse(data=Token(access_token=token), message="Login successful")
