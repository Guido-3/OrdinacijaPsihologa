from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.klijent import Klijent
import app.schemas.klijent as klijentSchemas
# from app.schemas.shared import KlijentCreate, KlijentUpdateFull, KlijentUpdatePartial
from app.exceptions import DbnotFoundException, KlijentAlreadyExistsException
from app.core.security import hash_password



def get_klijent(db: Session, klijent_id: int) -> Klijent:
    klijent = db.get(Klijent, klijent_id)
    if not klijent:
        raise DbnotFoundException(f"Klijent sa ID-jem '{klijent_id}' nije pronađen.")
    return klijent

def list_klijenti(
    db: Session,
    ime: Optional[str] = None,
    prezime: Optional[str] = None,
    username: Optional[str] = None
) -> List[Klijent]:
    """
    Vraća listu klijenata sa opcionalnim filtriranjem po imenu, prezimenu ili korisničkom imenu.
    """
    query = select(Klijent)

    if ime:
        query = query.where(Klijent.ime.ilike(f"%{ime}%"))
    if prezime:
        query = query.where(Klijent.prezime.ilike(f"%{prezime}%"))
    if username:
        query = query.where(Klijent.username.ilike(f"%{username}%"))

    return db.execute(query).scalars().all()


def create_klijent(db: Session, klijent_data: klijentSchemas.KlijentCreate) -> Klijent:
    """
    Kreira novog klijenta u bazi podataka, ali provjerava da li već postoji klijent sa istim korisničkim imenom, email-om ili brojem telefona.
    """
    existing_klijent = db.query(Klijent).filter(
        (Klijent.username == klijent_data.username) |
        (Klijent.email == klijent_data.email) |
        (Klijent.broj_telefona == klijent_data.broj_telefona)
    ).first()

    if existing_klijent:
        raise KlijentAlreadyExistsException("Korisnik sa ovim email-om, korisničkim imenom ili brojem telefona već postoji.")

    new_klijent = Klijent(
        ime=klijent_data.ime,
        prezime=klijent_data.prezime,
        username=klijent_data.username,
        email=klijent_data.email,
        datum_rodjenja=klijent_data.datum_rodjenja,
        broj_telefona=klijent_data.broj_telefona,
        hashed_password=hash_password(klijent_data.hashed_password),
        fotografija=klijent_data.fotografija,
    )
    db.add(new_klijent)
    db.commit()
    db.refresh(new_klijent)
    return new_klijent

def update_klijent_partially(db: Session, klijent_id: int, klijent_data: klijentSchemas.KlijentUpdatePartial) -> Klijent:
    klijent = get_klijent(db, klijent_id)

    # Provera da li korisničko ime već postoji kod drugog klijenta
    existing_klijent = db.execute(
        select(Klijent).where(Klijent.username == klijent_data.username, Klijent.id != klijent_id)).scalars().first()
    if existing_klijent:
        raise KlijentAlreadyExistsException(f"Klijent sa korisničkim imenom '{klijent_data.username}' već postoji.")

    update_data = klijent_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(klijent, key, value)

    db.commit()
    db.refresh(klijent)
    return klijent

def delete_klijent(db: Session, klijent_id: int) -> None:
    """
    Briše klijenta iz baze podataka, ali prvo provjerava da li klijent postoji.
    """
    klijent = get_klijent(db, klijent_id)
    db.delete(klijent)
    db.commit()
