from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import app.schemas.termin as terminSchemas
import app.crud.termin as termin
from app.database import get_db
from app.exceptions import DbnotFoundException

router = APIRouter(prefix="/termin", tags=["Termin"])

@router.get("/svi_termini", response_model=List[terminSchemas.Termin])
def list_svi_termini_za_klijenta(
    klijent_id: int,  
    db: Session = Depends(get_db)
):
    """
    Dohvata sve buduće termine za određenog klijenta:
    - Individualne termine (gdje je klijent direktno zakazan).
    - Grupne termine (gdje klijent pripada grupi koja ima termin).
    """
    return termin.list_svi_termini_za_klijenta(db, klijent_id)

@router.get("/grupa/{grupa_id}", response_model=List[terminSchemas.Termin])
def list_termini_za_grupu(grupa_id: int, db: Session = Depends(get_db)):
    """
    Dohvata sve buduće termine za određenu grupu.
    """
    return termin.list_termini_za_grupu(db, grupa_id)

@router.get("/{termin_id}", response_model=terminSchemas.Termin)
def get_termin(termin_id: int, db: Session = Depends(get_db)):
    try:
        termin_obj = termin.get_termin(db, termin_id)
        print("DOhvaceni termin: ", termin_obj) 
        return termin_obj
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Termin sa ID-jem '{termin_id}' nije pronađen.")

# @router.get("", response_model=List[terminSchemas.Termin])
# def list_termini(
#     klijent_id: Optional[int] = None,  # 👈 Omogućavamo filtriranje po klijentovom ID-u
#     db: Session = Depends(get_db)
# ):
#     filters = terminSchemas.FilterTermin(klijent_id=klijent_id)
#     return termin.list_termini(db, filters)

@router.get("", response_model=List[terminSchemas.Termin])
def list_svi_termini(
    klijent_id: Optional[int] = None,  # 📌 Ispravan query parametar
    db: Session = Depends(get_db)
):
    """
    Dohvata sve buduće termine (individualne + grupne) za datog klijenta.
    """
    if klijent_id is None:
        raise HTTPException(status_code=400, detail="Klijent ID je obavezan.")

    return termin.list_svi_termini(db, klijent_id)

@router.post("", response_model=terminSchemas.Termin)
def create_termin(termin_data: terminSchemas.TerminCreate, db: Session = Depends(get_db)):
    try:
        return termin.create_termin(db, termin_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{termin_id}", response_model=terminSchemas.Termin)
def update_termin_full(termin_id: int, termin_data: terminSchemas.TerminUpdateFull, db: Session = Depends(get_db)):
    try:
        return termin.update_termin_full(db, termin_id, termin_data)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Termin sa ID-jem '{termin_id}' nije pronađen.")

@router.patch("/{termin_id}", response_model=terminSchemas.Termin)
def update_termin_partially(
    termin_id: int,
    termin_data: terminSchemas.TerminUpdatePartial,
    db: Session = Depends(get_db)
):
    try:
        print("router funkcija se poziva")
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
