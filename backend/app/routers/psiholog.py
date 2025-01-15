from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.exceptions import DbnotFoundException, DatabaseError
from app.schemas.psiholog import Psiholog, PsihologUpdatePartial, PsihologUpdateFull, PsihologCreate
import app.crud.psiholog as psiholog
from app.database import get_db

router = APIRouter(prefix="/psiholog", tags=["Psiholog"])

@router.get("", response_model=Psiholog)
def get_psiholog(db: Session = Depends(get_db)):
    try:
        return psiholog.get_psiholog(db)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail="Psiholog nije pronadjen u bazi podataka.")

@router.post("", response_model=Psiholog)
def create_psiholog(psiholog_data: PsihologCreate, db: Session = Depends(get_db)):
    try:
        return psiholog.create_psiholog(db, psiholog_data)
    except DatabaseError:
        raise HTTPException(status_code=500, detail="Greska pri kreiranju psihologa.")

    
@router.put("", response_model=Psiholog)
def update_psiholog_full(psiholog_data: PsihologUpdateFull, db: Session = Depends(get_db)):
    try:
        return psiholog.update_psiholog_full(db, psiholog_data)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail="Psiholog nije pronadjen u bazi podataka.")
    
@router.patch("", response_model=Psiholog)
def update_psiholog_partially(psiholog_data: PsihologUpdatePartial, db: Session = Depends(get_db)):
    try:
        return psiholog.update_psiholog_partially(db, psiholog_data)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail="Psiholog nije pronadjen u bazi podataka.")