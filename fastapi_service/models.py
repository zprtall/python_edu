from pydantic import BaseModel
import datetime


class Struct(BaseModel):
    number_of_tooth: int
    hight: float
    name: str
    created_at: datetime.date
    birth_date: datetime.date
