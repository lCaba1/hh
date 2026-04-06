from pydantic import BaseModel
from typing import List, Optional
from datetime import date, time


class OwnerBase(BaseModel):
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None


class OwnerCreate(OwnerBase):
    pass


class Owner(OwnerBase):
    id: int

    class Config:
        from_attributes = True


class HorseBase(BaseModel):
    name: str
    gender: Optional[str] = None
    age: Optional[int] = None


class HorseCreate(HorseBase):
    owner_id: int


class Horse(HorseBase):
    id: int
    owner: Optional[Owner]

    class Config:
        from_attributes = True


class JockeyBase(BaseModel):
    name: str
    address: Optional[str] = None
    age: Optional[int] = None
    rating: Optional[float] = None


class JockeyCreate(JockeyBase):
    pass


class Jockey(JockeyBase):
    id: int

    class Config:
        from_attributes = True


class RaceBase(BaseModel):
    date: date
    time: time
    hippodrome: str
    name: Optional[str] = None


# список состязаний лошади
class HorseRaces(BaseModel):
    horse_id: int
    horse_name: str
    races: List[RaceBase]


# список состязаний жокея
class JockeyRaces(BaseModel):
    jockey_id: int
    jockey_name: str
    races: List[RaceBase]


class RaceCreate(RaceBase):
    pass


class RaceResultBase(BaseModel):
    horse_id: int
    jockey_id: int
    place: int
    finish_time: float


class RaceResultCreate(RaceResultBase):
    pass


class RaceResult(RaceResultBase):
    id: int
    horse: Optional[Horse]
    jockey: Optional[Jockey]

    class Config:
        from_attributes = True



class RaceWithResults(RaceBase):
    id: int
    results: List[RaceResult]

    class Config:
        from_attributes = True
