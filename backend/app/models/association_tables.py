from sqlalchemy import Table, Column, Integer, ForeignKey
from database import Base

klijent_grupa = Table(
    "klijent_grupa", 
    Base.metadata,
    Column("klijent_id", Integer, ForeignKey("klijenti.id"), primary_key=True),
    Column("grupa_id", Integer, ForeignKey("grupe.id"), primary_key=True)
)