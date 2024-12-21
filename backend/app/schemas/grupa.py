from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, Annotated

from schemas.klijent import Klijent
from schemas.termin import Termin

class GrupaBase(BaseModel):
    naziv: Annotated[str, Field(max_length=50)]
    opis: Annotated[Optional[str], Field(max_length=200)] = None
    klijenti_id: list[int]

    @field_validator("klijenti_id")
    @classmethod
    def validate_klijenti_id(cls, value):
        if len(value) < 2:
            raise ValueError("Grupa mora imati makar dva klijenta.")
        
        if len(set(value)) != len(value):
            raise ValueError("Lista klijenti_id ne smije sadržavati duplikate.")

        return value

class GrupaCreate(GrupaBase):
    pass

class GrupaUpdateFull(GrupaBase):
    pass

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
    termini: Optional[list[Termin]] = None

    model_config = ConfigDict(from_attributes=True)