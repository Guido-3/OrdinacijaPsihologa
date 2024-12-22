from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, and_
from models.termin import Termin
from models.klijent import Klijent
from models.grupa import Grupa
from schemas.termin import FilterTermin, TerminCreate, TerminUpdatePartial
from exceptions import DbnotFoundException


def get_termin(db: Session, termin_id: int) -> Termin:
    """
    Dohvata termin po ID-u.
    Ako termin ne postoji, baca izuzetak.
    """
    termin = db.get(Termin, termin_id)
    if not termin:
        raise DbnotFoundException(f"Termin sa ID-jem '{termin_id}' nije pronađen.")
    return termin


def list_termini(db: Session, filters: FilterTermin = FilterTermin()) -> list[Termin]:
    """
    Dohvata sve termine ili filtrira prema prosleđenim parametrima
    (status, datum, klijent, grupa, ime i prezime klijenta, naziv grupe).
    """
    query = select(Termin).options(
        joinedload(Termin.klijent),
        joinedload(Termin.grupa)
    )

    # Dodavanje filtera
    conditions = []
    if filters.status:
        conditions.append(Termin.status == filters.status)
    if filters.datum_vrijeme:
        conditions.append(Termin.datum_vrijeme == filters.datum_vrijeme)
    if filters.klijent_id:
        conditions.append(Termin.klijent_id == filters.klijent_id)
    if filters.grupa_id:
        conditions.append(Termin.grupa_id == filters.grupa_id)
    if filters.klijent_ime:
        conditions.append(Klijent.ime.ilike(f"%{filters.klijent_ime}%"))
    if filters.klijent_prezime:
        conditions.append(Klijent.prezime.ilike(f"%{filters.klijent_prezime}%"))
    if filters.naziv_grupe:
        conditions.append(Grupa.naziv.ilike(f"%{filters.naziv_grupe}%"))

    if conditions:
        query = query.where(and_(*conditions))

    return db.execute(query).scalars().all()


def create_termin(db: Session, termin_data: TerminCreate) -> Termin:
    """
    Kreira novi termin.
    """
    new_termin = Termin(**termin_data.model_dump())
    db.add(new_termin)
    db.commit()
    db.refresh(new_termin)
    return new_termin


def update_termin(db: Session, termin_id: int, termin_data: TerminUpdatePartial) -> Termin:
    """
    Ažurira postojeći termin.
    Ako termin ne postoji, baca izuzetak.
    """
    termin = get_termin(db, termin_id)

    update_data = termin_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(termin, key, value)

    db.commit()
    db.refresh(termin)
    return termin


def delete_termin(db: Session, termin_id: int) -> None:
    """
    Briše termin iz baze podataka.
    Ako termin ne postoji, baca izuzetak.
    """
    termin = get_termin(db, termin_id)
    db.delete(termin)
    db.commit()
