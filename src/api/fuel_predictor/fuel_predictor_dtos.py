from pydantic import BaseModel, Field
from enum import Enum

class BeaufortEnum(str, Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'

class TripData(BaseModel):
    Date: str
    Latitude_degree: float
    Longitude_degree: float
    Beaufort: BeaufortEnum
    Speed: float = Field(..., alias='Speed(Ground)')
    Revolution: float = Field(..., alias='M/E REVOLUTION')
