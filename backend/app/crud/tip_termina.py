from sqlalchemy.orm import Session
from sqlalchemy import and_, select
from models.tip_termina import TipTermina
from schemas.tip_termina import TipTerminaCreate, TipTerminaUpdatePartial
from exceptions import DbnotFoundException, DbAlreadyExistsException
from typing import Optional
from models.tip_termina import TipTermina
from schemas.tip_termina import FilterTip


def get_tip_termina(db: Session, tip_id: int) -> TipTermina:
    """
    Dohvata tip termina po ID-u.
    """
    tip = db.get(TipTermina, tip_id)
    if not tip:
        raise DbnotFoundException(f"Tip termina sa ID-jem '{tip_id}' nije pronađen.")
    return tip

def list_tipovi_termina(db: Session, filters: Optional[FilterTip] = None) -> list[TipTermina]:
    """
    Dohvata sve tipove termina ili filtrira prema prosleđenim parametrima (id i naziv).
    Ako nema pronađenih termina, vraća praznu listu.
    """
    if filters is None:
        filters = FilterTip()

    query = select(TipTermina)

    # Dodavanje filtera
    conditions = []
    if filters.id:
        conditions.append(TipTermina.id == filters.id)
    if filters.naziv:
        conditions.append(TipTermina.naziv.ilike(f"%{filters.naziv}%"))

    # Primjena uslova
    if conditions:
        query = query.where(and_(*conditions))

    # Izvršavanje upita
    rezultati = db.execute(query).scalars().all()

    return rezultati


def create_tip_termina(db: Session, tip_data: TipTerminaCreate) -> TipTermina:
    """
    Kreira novi tip termina u bazi podataka.
    """
    # Provjera da li postoji tip termina sa istim nazivom
    existing_tip = db.query(TipTermina).filter(TipTermina.naziv == tip_data.naziv).first()
    if existing_tip:
        raise DbAlreadyExistsException(f"Tip termina sa nazivom '{tip_data.naziv}' već postoji.")

    new_tip = TipTermina(**tip_data.model_dump())
    db.add(new_tip)
    db.commit()
    db.refresh(new_tip)
    return new_tip


def update_tip_termina(db: Session, tip_id: int, tip_data: TipTerminaUpdatePartial) -> TipTermina:
    """
    Ažurira postojeći tip termina.
    """
    tip = get_tip_termina(db, tip_id)

    update_data = tip_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(tip, key, value)

    db.commit()
    db.refresh(tip)
    return tip


def delete_tip_termina(db: Session, tip_id: int) -> None:
    """
    Briše tip termina iz baze podataka.
    """
    tip = get_tip_termina(db, tip_id)
    db.delete(tip)
    db.commit()
