from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Annotated, Optional
from datetime import date


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

class KlijentUpdateFull(KlijentBase):
    hashed_password: Annotated[str, Field(min_length=8, max_length=100)]

class KlijentUpdatePartial(KlijentBase):
    ime: Annotated[Optional[str], Field(max_length=100)] = None
    prezime: Annotated[Optional[str], Field(max_length=100)] = None
    username: Annotated[Optional[str], Field(max_length=100)] = None
    hashed_password: Annotated[Optional[str], Field(min_length=8, max_length=100)] = None
    email: Optional[EmailStr] = None
    broj_telefona: Annotated[Optional[str], Field(min_length=9, max_length=30)] = None
    datum_rodjenja: Optional[date] = None
    fotografija: Optional[str] = None

class Klijent(KlijentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)