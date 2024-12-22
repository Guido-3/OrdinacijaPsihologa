from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, Optional

from schemas.termin import Termin

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
    termini: Optional[list[Termin]] = None
    model_config = ConfigDict(from_attributes=True)

class FilterTip(BaseModel):
    id: Optional[int] = None
    naziv: Optional[str] = None

    class Config:
        orm_mode = True