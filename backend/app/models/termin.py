from datetime import datetime
from sqlalchemy import String, DateTime, Integer, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Termin(Base):
    __tablename__ = "termini"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[str] = mapped_column(Enum("zakazan", "blokiran", name="status_enum"), nullable=False)
    datum_vrijeme: Mapped[datetime] = mapped_column(DateTime, nullable=False, unique=True)
    nacin_izvodjenja: Mapped[str] = mapped_column(Enum("uzivo", "online", name="nacin_izvodjenja_status"), nullable=True)
    # MOZE I OVAKO - POGLEDAJ DO KRAJA LINIJU:
    # nacin_izvodjenja: Mapped[str] = mapped_column(Enum("uzivo", "online", "blokiran", name="nacin_izvodjenja_status"), nullable=False)
    napomena: Mapped[str] = mapped_column(String, nullable=True)
    
    psiholog_id: Mapped[int] = mapped_column(Integer, ForeignKey("psiholozi.id"), nullable=False)
    psiholog: Mapped["Psiholog"] = relationship(back_populates="termini")

    klijent_id: Mapped[int] = mapped_column(Integer, ForeignKey("klijenti.id"), nullable=True)
    klijent: Mapped["Klijent"] = relationship(back_populates="termini")

    grupa_id: Mapped[int] = mapped_column(Integer, ForeignKey("grupe.id"), nullable=True)
    grupa: Mapped["Grupa"] = relationship(back_populates="termini")

    tip_termina_id: Mapped[int] = mapped_column(Integer, ForeignKey("tipovi_termina.id"), nullable=False)
    tip_termina: Mapped["TipTermina"] = relationship(back_populates="termini")