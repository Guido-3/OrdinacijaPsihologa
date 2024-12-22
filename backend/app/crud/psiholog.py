from sqlalchemy.orm import Session
from models.psiholog import Psiholog
from schemas.psiholog import PsihologUpdatePartial
from exceptions import DbnotFoundException


def get_psiholog(db: Session) -> Psiholog:
    """
    Dohvata psihologa iz baze podataka.
    """
    psiholog = db.query(Psiholog).first()
    if not psiholog:
        raise DbnotFoundException("Psiholog nije pronađen u bazi podataka.")
    return psiholog


def update_psiholog(db: Session, psiholog_data: PsihologUpdatePartial) -> Psiholog:
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
