from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.crud.auth import create_user, verify_password, create_access_token
from app.dependencies import get_db, require_admin
from app.models import User
from app.schemas import TokenSchema, UserOut, UserCreate

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenSchema, status_code=HTTP_200_OK)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    q = await db.execute(select(User).where(User.username == form_data.username))
    user = q.scalars().first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(user.username)
    return TokenSchema(access_token=token)


@router.post("/users", response_model=UserOut, status_code=HTTP_201_CREATED)
async def admin_create_user(
        payload: UserCreate,
        db: AsyncSession = Depends(require_admin)
):
    user = await create_user(payload, db)
    return user
