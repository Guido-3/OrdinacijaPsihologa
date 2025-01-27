from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from app.models.grupa import Grupa
from app.models.klijent import Klijent
import app.schemas.grupa as grupaSchemas
# from app.schemas.shared import GrupaCreate, GrupaUpdateFull, GrupaUpdatePartial
from app.exceptions import DbnotFoundException
from typing import Optional


def get_grupa(db: Session, grupa_id: int) -> Grupa:
    """
    Dohvata grupu po ID-u.
    """
    grupa = db.get(Grupa, grupa_id)
    if not grupa:
        raise DbnotFoundException(f"Grupa sa ID-jem '{grupa_id}' nije pronađena.")
    return grupa

def list_grupe(
    db: Session,
    naziv: Optional[str] = None,
    klijent_ime: Optional[str] = None,
    klijent_prezime: Optional[str] = None,
    klijent_id: Optional[int] = None
) -> list[Grupa]:
    """
    Dohvata sve grupe ili filtrira po nazivu, imenu/prezimenu klijenata i klijent ID-u.
    """
    query = select(Grupa).options(joinedload(Grupa.klijenti)).distinct()

    if naziv:
        query = query.where(Grupa.naziv.ilike(f"%{naziv}%"))

    if klijent_id or klijent_ime or klijent_prezime:
        query = query.join(Grupa.klijenti)

        if klijent_id:
            query = query.where(Klijent.id == klijent_id)

        if klijent_ime:
            query = query.where(Klijent.ime.ilike(f"%{klijent_ime}%"))

        if klijent_prezime:
            query = query.where(Klijent.prezime.ilike(f"%{klijent_prezime}%"))

    return db.execute(query).unique().scalars().all()

# mozda je ovaj kod bolji
# def list_grupe(
#     db: Session,
#     naziv: Optional[str] = None,
#     klijent_ime: Optional[str] = None,
#     klijent_prezime: Optional[str] = None
# ) -> list[Grupa]:
#     query = select(Grupa).options(joinedload(Grupa.klijenti))

#     if naziv:
#         query = query.where(Grupa.naziv.ilike(f"%{naziv}%"))

#     if klijent_ime or klijent_prezime:
#         query = query.join(Grupa.klijenti)
#         if klijent_ime:
#             query = query.where(Klijent.ime.ilike(f"%{klijent_ime}%"))
#         if klijent_prezime:
#             query = query.where(Klijent.prezime.ilike(f"%{klijent_prezime}%"))

#     result = db.execute(query).scalars().all()
#     return result

def create_grupa(db: Session, grupa_data: grupaSchemas.GrupaCreate) -> Grupa:
    """
    Kreira novu grupu na osnovu unetih username-ova klijenata.
    """
    # Dohvatanje klijenata po username-u
    klijenti = db.query(Klijent).filter(Klijent.username.in_(grupa_data.klijenti_usernames)).all()

    # Provera da li svi uneti korisnici postoje
    if len(klijenti) != len(grupa_data.klijenti_usernames):
        found_usernames = {klijent.username for klijent in klijenti}
        missing_usernames = set(grupa_data.klijenti_usernames) - found_usernames
        raise ValueError(f"Korisnici sa username-ovima {missing_usernames} ne postoje.")

    # Kreiranje grupe
    new_grupa = Grupa(naziv=grupa_data.naziv, opis=grupa_data.opis, klijenti=klijenti)
    db.add(new_grupa)
    db.commit()
    db.refresh(new_grupa)

    return new_grupa

def update_grupa_full(db: Session, grupa_id: int, grupa_data: grupaSchemas.GrupaUpdateFull) -> Grupa:
    """
    Ažurira sve atribute postojeće grupe na osnovu prosleđenih podataka.
    """
    # Dohvatanje grupe po ID-ju
    grupa = get_grupa(db, grupa_id)

    # Ažuriranje atributa
    grupa.naziv = grupa_data.naziv
    grupa.opis = grupa_data.opis

    # Validacija i ažuriranje klijenata
    klijenti = db.query(Klijent).filter(Klijent.id.in_(grupa_data.klijenti_id)).all()
    if len(klijenti) != len(grupa_data.klijenti_id):
        missing_ids = set(grupa_data.klijenti_id) - {klijent.id for klijent in klijenti}
        raise ValueError(f"Klijenti sa ID-evima {missing_ids} ne postoje.")
    grupa.klijenti = klijenti

    # Komitovanje promena
    db.commit()
    db.refresh(grupa)
    return grupa

def update_grupa_partially(db: Session, grupa_id: int, grupa_data: grupaSchemas.GrupaUpdatePartial) -> Grupa:
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
