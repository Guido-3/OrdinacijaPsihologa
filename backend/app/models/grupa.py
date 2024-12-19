from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String

from association_tables import klijent_grupa
from database import Base

class Grupa(Base):
    __tablename__ = "grupe"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    naziv: Mapped[str] = mapped_column(String, nullable=True)
    opis: Mapped[str] = mapped_column(String, nullable=True)

    termini: Mapped[list["Termin"]] = relationship(secondary="klijent_grupa", back_populates="grupa")