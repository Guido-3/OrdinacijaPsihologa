from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from exceptions import DbnotFoundException, KlijentAlreadyExistsException
from schemas.klijent import Klijent, KlijentCreate, KlijentUpdatePartial
import crud.klijent as klijent
from database import get_db

router = APIRouter(prefix="/klijent")

@router.get("/{klijent_id}", response_model=Klijent)
def get_klijent(klijent_id: int, db: Session = Depends(get_db)):
    try:
        return klijent.get_klijent(db, klijent_id)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Klijent sa ID-jem '{klijent_id}' nije pronađen.")

@router.get("", response_model=list[Klijent])
def list_klijenti(ime: Optional[str] = None, prezime: Optional[str] = None, username: Optional[str] = None, db: Session = Depends(get_db)):
    return klijent.list_klijenti(db, ime, prezime, username)

@router.post("", response_model=Klijent)
def create_klijent(klijent_data: KlijentCreate, db: Session = Depends(get_db)):
    try:
        return klijent.create_klijent(db, klijent_data)
    except KlijentAlreadyExistsException:
        raise HTTPException(status_code=400, detail=f"Klijent sa korisničkim imenom '{klijent_data.username}' već postoji.")

@router.patch("/{klijent_id}", response_model=Klijent)
def update_klijent(klijent_id: int, klijent_data: KlijentUpdatePartial, db: Session = Depends(get_db)):
    try:
        return klijent.update_klijent(db, klijent_id, klijent_data)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Klijent sa ID-jem '{klijent_id}' nije pronađen.")

@router.delete("/{klijent_id}", response_model=None)
def delete_klijent(klijent_id: int, db: Session = Depends(get_db)):
    try:
        klijent.delete_klijent(db, klijent_id)
        return {"message": f"Klijent sa ID-jem '{klijent_id}' je uspešno obrisan."}
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Klijent sa ID-jem '{klijent_id}' nije pronađen.")
