from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.psiholog import Psiholog
from app.schemas.psiholog import PsihologUpdateFull, PsihologUpdatePartial, PsihologCreate
# from app.schemas.shared import PsihologCreate, PsihologUpdateFull, PsihologUpdatePartial
from app.exceptions import DbnotFoundException


def get_psiholog(db: Session) -> Psiholog:
    """
    Dohvata psihologa iz baze podataka.
    """
    psiholog = db.execute(select(Psiholog)).scalars().first()
    # psiholog = db.query(Psiholog).first() // ovo moze ali je bolji noviji pristup - barem chat tako kaze
    if not psiholog:
        raise DbnotFoundException("Psiholog nije pronađen u bazi podataka.")
    return psiholog

def create_psiholog(db: Session, psiholog_data: PsihologCreate) -> Psiholog:
    new_psiholog = Psiholog(**psiholog_data.model_dump())

    db.add(new_psiholog)
    db.commit()
    db.refresh(new_psiholog)  
    return new_psiholog

def update_psiholog_full(db: Session, psiholog_data: PsihologUpdateFull) -> Psiholog:
    psiholog = get_psiholog(db)

    update_data = psiholog_data.model_dump()

    for key, value in update_data.items():
        setattr(psiholog, key, value)

    db.commit()
    db.refresh(psiholog)
    return psiholog

def update_psiholog_partially(db: Session, psiholog_data: PsihologUpdatePartial) -> Psiholog:
    """
    Ažurira podatke psihologa.
    """
    psiholog = get_psiholog(db)

    update_data = psiholog_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(psiholog, key, value)

    db.commit()
    db.refresh(psiholog)
    return psiholog
