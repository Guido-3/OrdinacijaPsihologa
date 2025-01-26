from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import select, and_, or_
from app.models.termin import Termin
from app.models.klijent import Klijent
from app.models.grupa import Grupa
from app.models.tip_termina import TipTermina
import app.schemas.termin as terminSchemas
# from app.schemas.shared import TerminCreate, TerminUpdateFull, TerminUpdatePartial, FilterTermin
from app.exceptions import DbnotFoundException
from datetime import datetime, timezone

def is_time_slot_taken(db: Session, termin_id: int, datum_vrijeme: datetime) -> bool:
    """
    Proverava da li je vremenski slot zauzet i da li je unutar radnog vremena.
    Termini mogu biti zakazani samo na pune sate između 8:00 i 16:00.
    """
    # Provera da li je vreme zakazivanja na puni sat
    if datum_vrijeme.minute != 0 or datum_vrijeme.second != 0:
        raise ValueError("Termin može biti zakazan samo na pune sate (npr. 10:00, 11:00).")
    
    # Provera da li je vreme zakazivanja unutar radnog vremena
    if datum_vrijeme.hour < 8 or datum_vrijeme.hour >= 16:
        raise ValueError("Termin mora biti unutar radnog vremena (od 8:00 do 16:00).")
    
    # Provera da li je vremenski slot već zauzet (osim za trenutni termin koji se ažurira)
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

    result = db.execute(
        select(Termin)
        .where(Termin.id == termin_id)
        .options(
            selectinload(Termin.klijent),
            selectinload(Termin.grupa),
            selectinload(Termin.tip_termina)
        )
    )

    termin = result.scalars().first()

    if not termin:
        raise DbnotFoundException(f"Termin sa ID-jem{termin_id} nije pronadjen")
    
    return termin

from datetime import datetime

def list_termini(db: Session, filters: terminSchemas.FilterTermin = terminSchemas.FilterTermin()) -> list[Termin]:
    """
    Dohvata samo buduće termine ili filtrira prema prosleđenim parametrima.
    """
    query = select(Termin).options(
        joinedload(Termin.klijent),
        joinedload(Termin.grupa),
        joinedload(Termin.tip_termina)
    )

    # Dodavanje filtera
    conditions = []
    now = datetime.now(timezone.utc) # 👈 Dobijamo trenutni datum i vreme

    conditions.append(Termin.datum_vrijeme >= now)  # 👈 Prikazujemo samo buduće termine

    if filters.status:
        conditions.append(Termin.status == filters.status)
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

from sqlalchemy import or_

def list_svi_termini(db: Session, klijent_id: int) -> list[Termin]:
    """
    Vraća sve buduće termine za određenog klijenta, uključujući:
    - Individualne termine (gdje je klijent direktno zakazan)
    - Grupne termine (gdje klijent pripada grupi koja ima termin)
    """
    sada = datetime.now(timezone.utc)

    query = select(Termin).options(
        joinedload(Termin.klijent),
        joinedload(Termin.grupa),
        joinedload(Termin.tip_termina)
    ).where(
        and_(
            Termin.datum_vrijeme >= sada,  # 📌 Samo budući termini
            or_(
                Termin.klijent_id == klijent_id,  # 📌 Individualni termini
                Termin.grupa_id.in_(  # 📌 Grupni termini
                    select(Grupa.id).where(Grupa.klijenti.any(id=klijent_id))
                )
            )
        )
    )

    return db.execute(query).scalars().all()

def list_svi_termini_za_klijenta(db: Session, klijent_id: int) -> list[Termin]:
    """
    Vraća sve buduće termine za određenog klijenta:
    - Individualne termine (gdje je klijent direktno zakazan).
    - Grupne termine (gdje klijent pripada grupi koja ima termin).
    """
    sada = datetime.now(timezone.utc)

    query = select(Termin).options(
        joinedload(Termin.klijent),
        joinedload(Termin.grupa),
        joinedload(Termin.tip_termina)
    ).where(
        and_(
            Termin.datum_vrijeme >= sada,  
            or_(
                Termin.klijent_id == klijent_id,  
                Termin.grupa_id.in_(  
                    select(Grupa.id).where(Grupa.klijenti.any(id=klijent_id))
                )
            )
        )
    )

    return db.execute(query).scalars().all()

def list_termini_za_grupu(db: Session, grupa_id: int) -> list[Termin]:
    """
    Vraća sve buduće termine za određenu grupu.
    """
    sada = datetime.now(timezone.utc)

    query = select(Termin).options(
        joinedload(Termin.tip_termina)
    ).where(
        and_(
            Termin.datum_vrijeme >= sada,
            Termin.grupa_id == grupa_id  # 📌 Filtriramo samo termine za datu grupu
        )
    )

    return db.execute(query).scalars().all()

def create_termin(db: Session, termin_data: terminSchemas.TerminCreate) -> Termin:
    """
    Kreira novi termin nakon validacije da li vremenski slot ispunjava uslove.
    """
    # Validacija zauzetog vremena
    if is_time_slot_taken(db, None, termin_data.datum_vrijeme):
        raise ValueError(f"Termin u datom vremenskom slotu ({termin_data.datum_vrijeme}) je već zauzet.")

    # Validacija tipa termina
    tip_termina = db.get(TipTermina, termin_data.tip_termina_id)
    if not tip_termina:
        raise DbnotFoundException(f"Tip termina sa ID-jem '{termin_data.tip_termina_id}' nije pronađen.")
    
    # Validacija klijenta ili grupe
    if termin_data.klijent_id:
        klijent = db.get(Klijent, termin_data.klijent_id)
        if not klijent:
            raise DbnotFoundException(f"Klijent sa ID-jem '{termin_data.klijent_id}' nije pronađen.")
    elif termin_data.grupa_id:
        grupa = db.get(Grupa, termin_data.grupa_id)
        if not grupa:
            raise DbnotFoundException(f"Grupa sa ID-jem '{termin_data.grupa_id}' nije pronađena.")
    else:
        raise ValueError("Termin mora imati ili klijenta ili grupu, ali ne oba.")

    # Kreiranje termina
    new_termin = Termin(**termin_data.model_dump())
    db.add(new_termin)
    db.commit()
    db.refresh(new_termin)
    return new_termin

def update_termin_full(db: Session, termin_id: int, termin_data: terminSchemas.TerminUpdateFull) -> Termin:
    """
    Ažurira sve atribute postojećeg termina nakon validacije.
    """
    # Dohvatanje termina po ID-ju
    termin = get_termin(db, termin_id)

    # Validacija zauzetog vremena
    if is_time_slot_taken(db, termin_id, termin_data.datum_vrijeme):
        raise ValueError(f"Termin u datom vremenskom slotu ({termin_data.datum_vrijeme}) je već zauzet.")

    # Validacija tipa termina
    tip_termina = db.get(TipTermina, termin_data.tip_termina_id)
    if not tip_termina:
        raise DbnotFoundException(f"Tip termina sa ID-jem '{termin_data.tip_termina_id}' nije pronađen.")
    termin.tip_termina = tip_termina

    # Validacija klijenta ili grupe
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

    # Ažuriranje ostalih atributa
    termin.status = termin_data.status
    termin.datum_vrijeme = termin_data.datum_vrijeme
    termin.nacin_izvodjenja = termin_data.nacin_izvodjenja

    # Komitovanje promena
    db.commit()
    db.refresh(termin)
    return termin

def update_termin_partially(db: Session, termin_id: int, termin_data: terminSchemas.TerminUpdatePartial) -> Termin:
    """
    Ažurira određene atribute termina nakon validacije.
    """
    # Dohvatanje termina po ID-ju
    termin = get_termin(db, termin_id)

    # Validacija zauzetog vremena (samo ako se menja datum_vrijeme)
    if termin_data.datum_vrijeme and is_time_slot_taken(db, termin_id, termin_data.datum_vrijeme):
        raise ValueError(f"Termin u datom vremenskom slotu ({termin_data.datum_vrijeme}) je već zauzet.")

    # Validacija atributa
    if termin_data.tip_termina_id is not None:
        tip_termina = db.get(TipTermina, termin_data.tip_termina_id)
        if not tip_termina:
            raise DbnotFoundException(f"Tip termina sa ID-jem '{termin_data.tip_termina_id}' nije pronađen.")
        termin.tip_termina = tip_termina

    if termin_data.klijent_id is not None:
        klijent = db.get(Klijent, termin_data.klijent_id)
        if not klijent:
            raise DbnotFoundException(f"Klijent sa ID-jem '{termin_data.klijent_id}' nije pronađen.")
        termin.klijent = klijent
        termin.grupa = None  # Osigurati da grupa bude prazna
    elif termin_data.grupa_id is not None:
        grupa = db.get(Grupa, termin_data.grupa_id)
        if not grupa:
            raise DbnotFoundException(f"Grupa sa ID-jem '{termin_data.grupa_id}' nije pronađena.")
        termin.grupa = grupa
        termin.klijent = None  # Osigurati da klijent bude prazan

    # Proveri konflikt klijenta i grupe (samo ako se oba ažuriraju u istom zahtevu)
    if termin.klijent is not None and termin.grupa is not None:
        raise ValueError("Termin mora imati ili samo klijenta ili samo grupu klijenata.")

    # Ažuriranje preostalih atributa
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
