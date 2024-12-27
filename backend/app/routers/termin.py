from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.termin import Termin, TerminCreate, TerminUpdatePartial, FilterTermin, TerminUpdateFull
import app.crud.termin as termin
from app.database import get_db
from app.exceptions import DbnotFoundException

router = APIRouter(prefix="/termin", tags=["Termin"])

@router.get("/{termin_id}", response_model=Termin)
def get_termin(termin_id: int, db: Session = Depends(get_db)):
    try:
        return termin.get_termin(db, termin_id)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Termin sa ID-jem '{termin_id}' nije pronađen.")

@router.get("", response_model=List[Termin])
def list_termini(
    filters: FilterTermin = Depends(),
    db: Session = Depends(get_db)
):

    return termin.list_termini(db, filters)

@router.post("", response_model=Termin)
def create_termin(termin_data: TerminCreate, db: Session = Depends(get_db)):
    try:
        return termin.create_termin(db, termin_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{termin_id}", response_model=Termin)
def update_termin_full(termin_id: int, termin_data: TerminUpdateFull, db: Session = Depends(get_db)):
    try:
        return termin.update_termin_full(db, termin_id, termin_data)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Termin sa ID-jem '{termin_id}' nije pronađen.")

@router.patch("/{termin_id}", response_model=Termin)
def update_termin_partially(
    termin_id: int,
    termin_data: TerminUpdatePartial,
    db: Session = Depends(get_db)
):
    try:
        return termin.update_termin_partially(db, termin_id, termin_data)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Termin sa ID-jem '{termin_id}' nije pronađen.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{termin_id}", response_model=None)
def delete_termin(termin_id: int, db: Session = Depends(get_db)):
    try:
        termin.delete_termin(db, termin_id)
        return {"message": f"Termin sa ID-jem '{termin_id}' je uspešno obrisan."}
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Termin sa ID-jem '{termin_id}' nije pronađen.")
