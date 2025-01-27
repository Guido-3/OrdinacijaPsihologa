from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.exceptions import DbnotFoundException
import app.schemas.grupa as grupaSchemas
import app.crud.grupa as grupa
from app.database import get_db

router = APIRouter(prefix="/grupa", tags=["Grupa"])

@router.get("/{grupa_id}", response_model=grupaSchemas.Grupa)
def get_grupa(grupa_id: int, db: Session = Depends(get_db)):
    try:
        return grupa.get_grupa(db, grupa_id)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Grupa sa ID-jem '{grupa_id}' nije pronađena.")

@router.get("", response_model=list[grupaSchemas.Grupa])
def list_grupe(
    naziv: Optional[str] = None,
    klijent_ime: Optional[str] = None,
    klijent_prezime: Optional[str] = None,
    klijent_id: Optional[int] = None,  # ✅ Dodajemo klijent_id kao parametar
    db: Session = Depends(get_db)
):
    return grupa.list_grupe(db, naziv, klijent_ime, klijent_prezime, klijent_id)

@router.post("", response_model=grupaSchemas.Grupa)
def create_grupa(grupa_data: grupaSchemas.GrupaCreate, db: Session = Depends(get_db)):
    """
    Kreira grupu na osnovu unetih username-ova.
    """
    try:
        return grupa.create_grupa(db, grupa_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{grupa_id}", response_model=grupaSchemas.Grupa)
def update_grupa_full(grupa_id: int, grupa_data: grupaSchemas.GrupaUpdateFull, db: Session = Depends(get_db)):
    try:
        return grupa.update_grupa_full(db, grupa_id, grupa_data)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Grupa sa ID-jem '{grupa_id}' nije pronađena.")

@router.patch("/{grupa_id}", response_model=grupaSchemas.Grupa)
def update_grupa_partially(grupa_id: int, grupa_data: grupaSchemas.GrupaUpdatePartial, db: Session = Depends(get_db)):
    try:
        return grupa.update_grupa_partially(db, grupa_id, grupa_data)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Grupa sa ID-jem '{grupa_id}' nije pronađena.")

@router.delete("/{grupa_id}", response_model=None)
def delete_grupa(grupa_id: int, db: Session = Depends(get_db)):
    try:
        grupa.delete_grupa(db, grupa_id)
        return {"message": f"Grupa sa ID-jem '{grupa_id}' je uspešno obrisana."}
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Grupa sa ID-jem '{grupa_id}' nije pronađena.")
