from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from exceptions import DbnotFoundException
from schemas.psiholog import Psiholog, PsihologUpdatePartial
import crud.psiholog as psiholog


from database import get_db

router = APIRouter(prefix="/psiholog")

@router.get("", response_model=Psiholog)
def get_psiholog(db: Session = Depends(get_db)):
    try:
        return psiholog.get_psiholog(db)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail="Psiholog nije pronadjen u bazi podataka.")
    
@router.patch("", response_model=Psiholog)
def update_psiholog_partially(psiholog_data: PsihologUpdatePartial, db: Session = Depends(get_db)):
    try:
        return psiholog.update_psiholog_partially(db, psiholog_data)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail="Psiholog nije pronadjen u bazi podataka.")