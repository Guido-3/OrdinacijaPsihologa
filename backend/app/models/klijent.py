from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Date
from datetime import date

from association_tables import klijent_grupa
from database import Base

class Klijent(Base):
    __tablename__ = "klijenti"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ime: Mapped[str] = mapped_column(String, nullable=False)
    prezime: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    datum_rodjenja: Mapped[date] = mapped_column(Date, nullable=False)
    broj_telefona: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    fotografija: Mapped[str] = mapped_column(String, nullable=True)

    termini: Mapped[list["Termin"]] = relationship(secondary="klijent_grupa", back_populates="klijent")