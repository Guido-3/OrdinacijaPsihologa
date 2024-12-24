from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from exceptions import DbnotFoundException, TipTerminaAlreadyExistsException
from schemas.tip_termina import TipTermina, TipTerminaCreate, TipTerminaUpdatePartial, FilterTip
import crud.tip_termina as tip_termina
from database import get_db

router = APIRouter(prefix="/tip_termina")

@router.get("/{tip_id}", response_model=TipTermina)
def get_tip_termina(tip_id: int, db: Session = Depends(get_db)):
    try:
        return tip_termina.get_tip_termina(db, tip_id)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Tip termina sa ID-jem '{tip_id}' nije pronadjen u bazi podataka")
    
@router.get("", response_model=list[TipTermina])
def list_tipovi_termina(filters: FilterTip = Depends(), db: Session = Depends(get_db)):
    return tip_termina.list_tipovi_termina(db, filters)

@router.post("", response_model=TipTermina)
def create_tip_termina(tip_data: TipTerminaCreate, db: Session = Depends(get_db)):
    try:
        return tip_termina.create_tip_termina(db, tip_data)
    except TipTerminaAlreadyExistsException:
        raise HTTPException(status_code=400, detail=f"Tip termina sa nazivom '{tip_data.naziv}' vec postoji u bazi podataka")
    
@router.patch("/{tip_id}", response_model=TipTermina)
def update_tip_termina_partially(tip_id: int, tip_data: TipTerminaUpdatePartial, db: Session = Depends(get_db)):
    try:
        return tip_termina.update_tip_termina(db, tip_id, tip_data)
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Tip termina sa ID-jem '{tip_id}' nije pronadjen u bazi podataka")
    
@router.delete("/{tip_id}")
def delete_tip_termina(tip_id: int, db: Session = Depends(get_db)):
    try:
        tip_termina.delete_tip_termina(db, tip_id)
        return {"message": f"Tip termina sa ID-jem '{tip_id}' je uspešno obrisan."}
    except DbnotFoundException:
        raise HTTPException(status_code=404, detail=f"Tip termina sa ID-jem '{tip_id}' nije pronadjen u bazi podataka")