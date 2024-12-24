from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from models.grupa import Grupa
from models.klijent import Klijent
from schemas.grupa import GrupaCreate, GrupaUpdatePartial
from exceptions import DbnotFoundException
from typing import Optional


def get_grupa(db: Session, grupa_id: int) -> Grupa:
    """
    Dohvata grupu po ID-u.
    """
    grupa = db.get(Grupa, grupa_id)
    if not grupa:
        raise DbnotFoundException(f"Grupa sa ID-jem '{grupa_id}' nije pronađena.")
    return grupa

# def list_grupe(
#     db: Session,
#     naziv: Optional[str] = None,
#     klijent_ime: Optional[str] = None,
#     klijent_prezime: Optional[str] = None
# ) -> list[Grupa]:
#     """
#     Dohvata sve grupe ili filtrira po nazivu, imenu i prezimenu klijenata.
#     """
#     query = select(Grupa).distinct()

#     if naziv:
#         query = query.where(Grupa.naziv.ilike(f"%{naziv}%"))

#     if klijent_ime or klijent_prezime:
#         query = query.join(Grupa.klijenti)
#         if klijent_ime:
#             query = query.where(Klijent.ime.ilike(f"%{klijent_ime}%"))
#         if klijent_prezime:
#             query = query.where(Klijent.prezime.ilike(f"%{klijent_prezime}%"))

#     return db.scalars(query).all()

# mozda je ovaj kod bolji
def list_grupe(
    db: Session,
    naziv: Optional[str] = None,
    klijent_ime: Optional[str] = None,
    klijent_prezime: Optional[str] = None
) -> list[Grupa]:
    query = select(Grupa).options(joinedload(Grupa.klijenti))

    if naziv:
        query = query.where(Grupa.naziv.ilike(f"%{naziv}%"))

    if klijent_ime or klijent_prezime:
        query = query.join(Grupa.klijenti)
        if klijent_ime:
            query = query.where(Klijent.ime.ilike(f"%{klijent_ime}%"))
        if klijent_prezime:
            query = query.where(Klijent.prezime.ilike(f"%{klijent_prezime}%"))

    result = db.execute(query).scalars().all()
    return result



def create_grupa(db: Session, grupa_data: GrupaCreate) -> Grupa:
    """
    Kreira novu grupu samo ako svi navedeni klijenti postoje.
    """
    klijenti = db.query(Klijent).filter(Klijent.id.in_(grupa_data.klijenti_id)).all()
    if len(klijenti) != len(grupa_data.klijenti_id):
        missing_ids = set(grupa_data.klijenti_id) - {klijent.id for klijent in klijenti}
        raise ValueError(f"Klijenti sa ID-evima {missing_ids} ne postoje.")

    new_grupa = Grupa(naziv=grupa_data.naziv, opis=grupa_data.opis, klijenti=klijenti)

    db.add(new_grupa)
    db.commit()
    db.refresh(new_grupa)
    return new_grupa


def update_grupa(db: Session, grupa_id: int, grupa_data: GrupaUpdatePartial) -> Grupa:
    """
    Ažurira postojeću grupu samo ako svi navedeni klijenti postoje.
    """
    # Provjera da li grupa postoji
    grupa = get_grupa(db, grupa_id)

    if grupa_data.naziv is not None:
        grupa.naziv = grupa_data.naziv

    if grupa_data.opis is not None:
        grupa.opis = grupa_data.opis

    if grupa_data.klijenti_id is not None:
        klijenti = db.query(Klijent).filter(Klijent.id.in_(grupa_data.klijenti_id)).all()
        if len(klijenti) != len(grupa_data.klijenti_id):
            missing_ids = set(grupa_data.klijenti_id) - {klijent.id for klijent in klijenti}
            raise ValueError(f"Klijenti sa ID-evima {missing_ids} ne postoje.")
        grupa.klijenti = klijenti

    db.commit()
    db.refresh(grupa)
    return grupa


def delete_grupa(db: Session, grupa_id: int) -> None:
    """
    Briše grupu iz baze podataka.
    """
    # Provjera da li grupa postoji
    grupa = get_grupa(db, grupa_id)
    db.delete(grupa)
    db.commit()
