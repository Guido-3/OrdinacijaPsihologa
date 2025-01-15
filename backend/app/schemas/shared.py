from pydantic import BaseModel, Field, ConfigDict, EmailStr, model_validator, field_validator
from typing import Annotated, Optional
from datetime import date
from datetime import datetime

class PsihologBase(BaseModel):
    ime: str
    prezime: str
    username: str
    email: EmailStr
    broj_telefona: Annotated[str, Field(min_length=9, max_length=30)]
    datum_rodjenja: date
    fotografija: Optional[str] = None

class PsihologCreate(PsihologBase):
    hashed_password: Annotated[str, Field(min_length=8, max_length=100)]

class PsihologUpdateFull(PsihologBase):
    hashed_password: Annotated[str, Field(min_length=8, max_length=100)]

class PsihologUpdatePartial(PsihologBase):
    ime: Optional[str] = None
    prezime: Optional[str] = None
    username: Optional[str] = None
    hashed_password: Annotated[Optional[str], Field(min_length=8, max_length=100)] = None
    email: Optional[EmailStr] = None
    broj_telefona: Annotated[Optional[str], Field(min_length=9, max_length=30)] = None
    datum_rodjenja: Optional[date] = None
    fotografija: Optional[str] = None

class Psiholog(PsihologBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class TipTerminaBase(BaseModel):
    naziv: Annotated[str, Field(min_length=3, max_length=50)]
    opis: Annotated[str, Field(min_length=10, max_length=1000)]

class TipTerminaCreate(TipTerminaBase):
    pass

class TipTerminaUpdateFull(TipTerminaBase):
    pass

class TipTerminaUpdatePartial(TipTerminaBase):
    naziv: Annotated[Optional[str], Field(min_length=3, max_length=50)] = None
    opis: Annotated[Optional[str], Field(min_length=10, max_length=1000)] = None

class TipTermina(TipTerminaBase):
    id: int
    termini: Optional[list["Termin"]] = None
    model_config = ConfigDict(from_attributes=True)

TipTermina.model_rebuild()

class FilterTip(BaseModel):
    id: Optional[int] = None
    naziv: Optional[str] = None

    class Config:
        model_config = ConfigDict(from_attributes=True)


# Zasebna funkcija za validaciju lozinke
def validate_password_complexity(value: str) -> str:
    if not any(char.isdigit() for char in value):
        raise ValueError("Lozinka mora sadržati barem jedan broj.")
    if not any(char.isupper() for char in value):
        raise ValueError("Lozinka mora sadržati barem jedno veliko slovo.")
    if not any(char.islower() for char in value):
        raise ValueError("Lozinka mora sadržati barem jedno malo slovo.")
    if not any(char in "!@#$%^&*()_+-=[]{}|;':,./<>?" for char in value):
        raise ValueError("Lozinka mora sadržati barem jedan specijalan znak.")
    return value

class KlijentBase(BaseModel):
    ime: Annotated[str, Field(max_length=100)]
    prezime: Annotated[str, Field(max_length=100)]
    username: Annotated[str, Field(max_length=100)]
    email: EmailStr
    broj_telefona: Annotated[str, Field(min_length=9, max_length=30)]
    datum_rodjenja: date
    fotografija: Optional[str] = None

class KlijentCreate(KlijentBase):
    hashed_password: Annotated[str, Field(min_length=8, max_length=100)]

    @field_validator("hashed_password")
    @classmethod
    def validate_password(cls, value):
        return validate_password_complexity(value)

class KlijentUpdateFull(KlijentBase):
    hashed_password: Annotated[str, Field(min_length=8, max_length=100)]

    @field_validator("hashed_password")
    @classmethod
    def validate_password(cls, value):
        return validate_password_complexity(value)
    
class KlijentUpdatePartial(KlijentBase):
    ime: Annotated[Optional[str], Field(max_length=100)] = None
    prezime: Annotated[Optional[str], Field(max_length=100)] = None
    username: Annotated[Optional[str], Field(max_length=100)] = None
    hashed_password: Annotated[Optional[str], Field(min_length=8, max_length=100)] = None
    email: Optional[EmailStr] = None
    broj_telefona: Annotated[Optional[str], Field(min_length=9, max_length=30)] = None
    datum_rodjenja: Optional[date] = None
    fotografija: Optional[str] = None

    @field_validator("hashed_password")
    @classmethod
    def validate_password(cls, value):
        if value is not None:
            return validate_password_complexity(value)
        return value

class Klijent(KlijentBase):
    id: int
    grupe: Optional[list["Grupa"]] = None
    termini: Optional[list["Termin"]] = None

    model_config = ConfigDict(from_attributes=True)

Klijent.model_rebuild()

class GrupaBase(BaseModel):
    naziv: Annotated[str, Field(max_length=50)]
    opis: Annotated[Optional[str], Field(max_length=200)] = None

class GrupaCreate(GrupaBase):
    klijenti_id: list[int]

    @field_validator("klijenti_id")
    @classmethod
    def validate_klijenti_id(cls, value):
        if len(value) < 2:
            raise ValueError("Grupa mora imati makar dva klijenta.")
        
        if len(set(value)) != len(value):
            raise ValueError("Lista klijenti_id ne smije sadržavati duplikate.")

        return value

class GrupaUpdateFull(GrupaBase):
    klijenti_id: list[int]

    @field_validator("klijenti_id")
    @classmethod
    def validate_klijenti_id(cls, value):
        if len(value) < 2:
            raise ValueError("Grupa mora imati makar dva klijenta.")
        
        if len(set(value)) != len(value):
            raise ValueError("Lista klijenti_id ne smije sadržavati duplikate.")

        return value

class GrupaUpdatePartial(GrupaBase):
    naziv: Annotated[Optional[str], Field(max_length=50)] = None
    klijenti_id: Optional[list[int]] = None

    @field_validator("klijenti_id", mode="before")
    @classmethod
    def validate_optional_klijenti_id(cls, value):
        if value is None:
            return value
        
        if len(value) < 2:
            raise ValueError("Grupa mora imati makar dva klijenta")
        
        if len(set(value)) != len(value):
            raise ValueError("Lista klijenti_id ne smije sadržavati duplikate.")

        return value
    
class Grupa(GrupaBase):
    id: int
    klijenti: list[Klijent]
    termini: Optional[list["Termin"]] = None

    model_config = ConfigDict(from_attributes=True)

Grupa.model_rebuild()

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
    klijent: Optional[Klijent] = None
    grupa: Optional[Grupa] = None
    tip_termina: TipTermina

    model_config = ConfigDict(from_attributes=True)

Termin.model_rebuild()

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
