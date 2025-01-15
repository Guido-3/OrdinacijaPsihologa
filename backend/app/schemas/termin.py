from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Annotated, Optional, ForwardRef
from datetime import datetime
# from app.schemas.grupa import Grupa
# from app.schemas.klijent import Klijent
# from app.schemas.tip_termina import TipTermina

# Grupa = ForwardRef("Grupa")
# Klijent = ForwardRef("Klijent")
# TipTermina = ForwardRef("TipTermina")

class TerminBase(BaseModel):
    status: Annotated[str, Field(enum=["zakazan", "blokiran"])]
    datum_vrijeme: datetime
    nacin_izvodjenja: Optional[Annotated[str, Field(enum=["uzivo", "online"])]] = None
    tip_termina_id: int
    klijent_id: Optional[int] = None
    grupa_id: Optional[int] = None
    psiholog_id: int = 1
    
    model_config = ConfigDict(validate_assignment=True)

class TerminCreate(TerminBase):
    @model_validator(mode="before")
    @classmethod
    def validate_klijent_or_grupa(cls, values):
        if not isinstance(values, dict):
            values = vars(values)

        klijent_id = values.get("klijent_id")
        grupa_id = values.get("grupa_id")

        if not klijent_id and not grupa_id:
            raise ValueError("Termin mora imati ili samo klijenta ili samo grupu klijenata.")
        if klijent_id and grupa_id:
            raise ValueError("Termin mora imati ili samo klijenta ili samo grupu klijenata.")
        
        return values

class TerminUpdateFull(TerminBase):
    @model_validator(mode="before")
    @classmethod
    def validate_klijent_or_grupa(cls, values):
        if not isinstance(values, dict):
            values = vars(values)

        klijent_id = values.get("klijent_id")
        grupa_id = values.get("grupa_id")

        if not klijent_id and not grupa_id:
            raise ValueError("Termin mora imati ili samo klijenta ili samo grupu klijenata.")
        if klijent_id and grupa_id:
            raise ValueError("Termin mora imati ili samo klijenta ili samo grupu klijenata.")
        
        return values

class TerminUpdatePartial(TerminBase):
    status: Optional[Annotated[str, Field(enum=["zakazan", "blokiran"])]] = None
    datum_vrijeme: Optional[datetime] = None
    nacin_izvodjenja: Optional[Annotated[str, Field(enum=["uzivo", "online"])]] = None
    tip_termina_id: Optional[int] = None
    klijent_id: Optional[int] = None
    grupa_id: Optional[int] = None

    @model_validator(mode="before")
    @classmethod
    def validate_optional_klijent_or_grupa(cls, values):
        klijent_id = values.get("klijent_id")
        grupa_id = values.get("grupa_id")

        if klijent_id and grupa_id:
            raise ValueError("Termin ne moze imati i klijenta i grupu, samo jedno od to dvoje.")
        
        return values
    
class Termin(TerminBase):
    id: int
    # klijent: Optional[Klijent] = None
    # grupa: Optional[Grupa] = None
    # tip_termina: TipTermina

    model_config = ConfigDict(from_attributes=True)

class FilterTermin(BaseModel):
    status: Optional[str] = None
    datum_vrijeme: Optional[datetime] = None
    klijent_id: Optional[int] = None
    grupa_id: Optional[int] = None
    klijent_ime: Optional[str] = None  # Filtriranje po imenu klijenta
    klijent_prezime: Optional[str] = None  # Filtriranje po prezimenu klijenta
    naziv_grupe: Optional[str] = None  # Filtriranje po nazivu grupe

    class Config:
        model_config = ConfigDict(from_attributes=True)

# from app.schemas.grupa import Grupa
# from app.schemas.klijent import Klijent
# from app.schemas.tip_termina import TipTermina

# Termin.model_rebuild()