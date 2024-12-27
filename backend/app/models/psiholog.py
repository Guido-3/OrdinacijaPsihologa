from datetime import date
from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Psiholog(Base):
    __tablename__ = "psiholozi"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ime: Mapped[str] = mapped_column(String, nullable=False)
    prezime: Mapped[str] = mapped_column(String, nullable=False)
    datum_rodjenja: Mapped[date] = mapped_column(Date, nullable=False)
    broj_telefona: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    fotografija: Mapped[str] = mapped_column(String, nullable=True)

    termini: Mapped[list["Termin"]] = relationship(back_populates="psiholog")