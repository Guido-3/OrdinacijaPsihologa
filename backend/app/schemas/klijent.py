from pydantic import BaseModel, Field, ConfigDict, EmailStr, field_validator
from typing import Annotated, Optional, ForwardRef
from datetime import date
# from app.schemas.grupa import Grupa
# from app.schemas.termin import Termin

# Grupa = ForwardRef("Grupa")
# Termin = ForwardRef("Termin")

# import app.schemas.grupa as grupa
# import app.schemas.termin as termin

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
    # grupe: Optional[list[Grupa]] = None
    # termini: Optional[list[Termin]] = None

    model_config = ConfigDict(from_attributes=True)

# from app.schemas.grupa import Grupa
# from app.schemas.termin import Termin

# Klijent.model_rebuild()