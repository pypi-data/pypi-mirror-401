from pydantic import  Field
from typing import List, Optional

from .base_dto import BaseDTO

class PowerStatsHistoryEntryDTO(BaseDTO):
    value: float = Field(..., alias="value")
    timestamp: str = Field(..., alias="timestamp")

class PowerStatsDTO(BaseDTO):
    history: Optional[List[PowerStatsHistoryEntryDTO]] = Field(default=None, alias="history")
    average_kw: Optional[float] = Field(default=None, alias="averageKw")
    max_kw: Optional[float] = Field(default=None, alias="maxKw")
