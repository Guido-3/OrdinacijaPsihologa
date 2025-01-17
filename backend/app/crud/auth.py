from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import timedelta
from app.models.klijent import Klijent
from app.schemas.auth import LoginSchema
from app.core.security import verify_password, create_access_token

def authenticate_user(login_data: LoginSchema, db: Session):
    user = db.query(Klijent).filter(Klijent.username == login_data.username).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Neispravno korisničko ime ili lozinka.")

    # ✅ Generišemo token sa ID-jem korisnika
    access_token = create_access_token({
        "id": user.id,  # ✅ Sada pravilno dodajemo ID korisnika u token
        "username": user.username
    }, expires_delta=timedelta(minutes=60))

    return {"access_token": access_token, "token_type": "bearer"}
