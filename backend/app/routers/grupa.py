from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from exceptions import DbnotFoundException
from schemas.grupa import Grupa, GrupaCreate, GrupaUpdatePartial
import crud.grupa as grupa
from database import get_db

router = APIRouter(prefix="/grupa")

@router.get("/{grupa_id}", response_model=Grupa)
def get_grupa(grupa_id: int, db: Session = Depends(get_db)):
    try:
        return grupa.get_grupa(db, grupa_id)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Grupa sa ID-jem '{grupa_id}' nije pronađena.")

@router.get("", response_model=list[Grupa])
def list_grupe(
    naziv: Optional[str] = None,
    klijent_ime: Optional[str] = None,
    klijent_prezime: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return grupa.list_grupe(db, naziv, klijent_ime, klijent_prezime)

@router.post("", response_model=Grupa)
def create_grupa(grupa_data: GrupaCreate, db: Session = Depends(get_db)):
    try:
        return grupa.create_grupa(db, grupa_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{grupa_id}", response_model=Grupa)
def update_grupa(grupa_id: int, grupa_data: GrupaUpdatePartial, db: Session = Depends(get_db)):
    try:
        return grupa.update_grupa(db, grupa_id, grupa_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Grupa sa ID-jem '{grupa_id}' nije pronađena.")

@router.delete("/{grupa_id}", response_model=None)
def delete_grupa(grupa_id: int, db: Session = Depends(get_db)):
    try:
        grupa.delete_grupa(db, grupa_id)
        return {"message": f"Grupa sa ID-jem '{grupa_id}' je uspešno obrisana."}
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Grupa sa ID-jem '{grupa_id}' nije pronađena.")
