from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.schemas.auth import LoginSchema, Token
from app.crud.auth import authenticate_user

router = APIRouter(prefix="/auth", tags=["Auth"])

# Prijava korisnika
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    login_data = LoginSchema(username=form_data.username, password=form_data.password)
    return authenticate_user(login_data, db)
