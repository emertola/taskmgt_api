from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services import user_service


router = APIRouter(
  prefix="/users",
  tags=["users"],
)

@router.post("/register", response_model=UserResponse, status_code=201, responses={400: {"description": "Email already registered"}})
def register_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
  created_user = user_service.create_user(db, user)
  if created_user is None:
    raise HTTPException(status_code=400, detail="Email already registered")
  return created_user

@router.post("/login", response_model=UserResponse, responses={401: {"description": "Invalid email or password"}})
def login_user(credentials: UserLogin, db: Annotated[Session, Depends(get_db)]):
  user = user_service.authenticate_user(db, credentials.email, credentials.password)
  if user is None:
    raise HTTPException(status_code=401, detail="Invalid email or password")
  return user