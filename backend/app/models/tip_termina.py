from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from database import Base


class TipTermina(Base):
    __tablename__ = "tipovi_termina"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    naziv: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    opis: Mapped[str] = mapped_column(String, nullable=False)


    termini: Mapped[list["Termin"]] = relationship(back_populates="tip_termina")