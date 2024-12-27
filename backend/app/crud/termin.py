from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, and_
from app.models.termin import Termin
from app.models.klijent import Klijent
from app.models.grupa import Grupa
from app.models.tip_termina import TipTermina
from app.schemas.termin import FilterTermin, TerminCreate, TerminUpdatePartial, TerminUpdateFull
from app.exceptions import DbnotFoundException
from datetime import datetime

def is_time_slot_taken(db: Session, termin_id: int, datum_vrijeme: datetime) -> bool:
    """
    Proverava da li već postoji termin u datom vremenskom slotu,
    isključujući trenutni termin koji se ažurira.
    """
    query = select(Termin).where(
        Termin.datum_vrijeme == datum_vrijeme,
        Termin.id != termin_id
    )
    existing_termin = db.execute(query).scalars().first()
    return existing_termin is not None


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


def update_termin_full(db: Session, termin_id: int, termin_data: TerminUpdateFull) -> Termin:
    """
    Ažurira sve atribute postojećeg termina na osnovu prosleđenih podataka.
    Proverava da li je novo vreme termina već zauzeto.
    """
    # Dohvatanje termina po ID-ju
    termin = get_termin(db, termin_id)

    # Validacija zauzetog vremena
    if is_time_slot_taken(db, termin_id, termin_data.datum_vrijeme):
        raise ValueError(f"Termin u datom vremenskom slotu ({termin_data.datum_vrijeme}) je već zauzet.")

    # Ažuriranje osnovnih atributa
    termin.status = termin_data.status
    termin.datum_vrijeme = termin_data.datum_vrijeme
    termin.nacin_izvodjenja = termin_data.nacin_izvodjenja

    # Validacija i ažuriranje tipa termina
    tip_termina = db.get(TipTermina, termin_data.tip_termina_id)
    if not tip_termina:
        raise DbnotFoundException(f"Tip termina sa ID-jem '{termin_data.tip_termina_id}' nije pronađen.")
    termin.tip_termina = tip_termina

    # Validacija i ažuriranje klijenta ili grupe
    if termin_data.klijent_id:
        klijent = db.get(Klijent, termin_data.klijent_id)
        if not klijent:
            raise DbnotFoundException(f"Klijent sa ID-jem '{termin_data.klijent_id}' nije pronađen.")
        termin.klijent = klijent
        termin.grupa = None  # Osigurati da grupa bude prazna
    elif termin_data.grupa_id:
        grupa = db.get(Grupa, termin_data.grupa_id)
        if not grupa:
            raise DbnotFoundException(f"Grupa sa ID-jem '{termin_data.grupa_id}' nije pronađena.")
        termin.grupa = grupa
        termin.klijent = None  # Osigurati da klijent bude prazan
    else:
        raise ValueError("Termin mora imati ili klijenta ili grupu, ali ne oba.")

    # Komitovanje promena
    db.commit()
    db.refresh(termin)
    return termin


def update_termin_partially(db: Session, termin_id: int, termin_data: TerminUpdatePartial) -> Termin:
    """
    Ažurira određene atribute termina na osnovu prosleđenih podataka.
    Proverava da li je novo vreme termina već zauzeto.
    """
    # Dohvatanje termina po ID-ju
    termin = get_termin(db, termin_id)

    # Validacija zauzetog vremena (samo ako se menja datum_vrijeme)
    if termin_data.datum_vrijeme and is_time_slot_taken(db, termin_id, termin_data.datum_vrijeme):
        raise ValueError(f"Termin u datom vremenskom slotu ({termin_data.datum_vrijeme}) je već zauzet.")

    # Ažuriranje atributa na osnovu prosleđenih vrednosti
    update_data = termin_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(termin, key, value)

    # Komitovanje promena
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
