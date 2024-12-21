from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Annotated, Optional
from datetime import date

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