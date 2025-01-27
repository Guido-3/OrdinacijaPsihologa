from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.exceptions import DbnotFoundException, KlijentAlreadyExistsException
import app.schemas.klijent as klijentSchemas
import app.crud.klijent as klijent
from app.database import get_db

router = APIRouter(prefix="/klijent", tags=["Klijent"])

@router.get("/{klijent_id}", response_model=klijentSchemas.Klijent)
def get_klijent(klijent_id: int, db: Session = Depends(get_db)):
    try:
        return klijent.get_klijent(db, klijent_id)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Klijent sa ID-jem '{klijent_id}' nije pronađen.")

@router.get("", response_model=list[klijentSchemas.Klijent])
def list_klijenti(ime: Optional[str] = None, prezime: Optional[str] = None, username: Optional[str] = None, db: Session = Depends(get_db)):
    return klijent.list_klijenti(db, ime, prezime, username)

@router.post("", response_model=klijentSchemas.Klijent)
def create_klijent(klijent_data: klijentSchemas.KlijentCreate, db: Session = Depends(get_db)):
    try:
        return klijent.create_klijent(db, klijent_data)
    except KlijentAlreadyExistsException:
        raise HTTPException(status_code=400, detail=f"Korisnik sa ovim email-om, korisničkim imenom ili brojem telefona već postoji.")

@router.put("/{klijent_id}", response_model=klijentSchemas.Klijent)
def update_klijent_full(klijent_id: int, klijent_data: klijentSchemas.KlijentUpdateFull, db: Session = Depends(get_db)):
    try:
        return klijent.update_klijent_full(db, klijent_id, klijent_data)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Klijent sa ID-jem '{klijent_id}' nije pronađen.")

@router.patch("/{klijent_id}", response_model=klijentSchemas.Klijent)
def update_klijent_partially(klijent_id: int, klijent_data: klijentSchemas.KlijentUpdatePartial, db: Session = Depends(get_db)):
    try:
        return klijent.update_klijent_partially(db, klijent_id, klijent_data)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Klijent sa ID-jem '{klijent_id}' nije pronađen.")

@router.delete("/{klijent_id}", response_model=None)
def delete_klijent(klijent_id: int, db: Session = Depends(get_db)):
    try:
        klijent.delete_klijent(db, klijent_id)
        return {"message": f"Klijent sa ID-jem '{klijent_id}' je uspešno obrisan."}
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Klijent sa ID-jem '{klijent_id}' nije pronađen.")
