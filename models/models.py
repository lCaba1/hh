from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey, Date, Time
from sqlalchemy.orm import relationship
from db.database import Base


class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String)
    phone = Column(String)

    horses = relationship("Horse", back_populates="owner")


class Horse(Base):
    __tablename__ = "horses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # кличка
    gender = Column(String)  # пол
    age = Column(Integer)

    owner_id = Column(Integer, ForeignKey("owners.id"))

    owner = relationship("Owner", back_populates="horses")
    race_results = relationship("RaceResult", back_populates="horse")


class Jockey(Base):
    __tablename__ = "jockeys"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String)
    age = Column(Integer)
    rating = Column(Float)

    race_results = relationship("RaceResult", back_populates="jockey")


class Race(Base):
    __tablename__ = "races"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    hippodrome = Column(String, nullable=False)  # место проведения
    name = Column(String)  # название состязания (может быть null)

    results = relationship("RaceResult", back_populates="race")


class RaceResult(Base):
    __tablename__ = "race_results"

    id = Column(Integer, primary_key=True, index=True)

    race_id = Column(Integer, ForeignKey("races.id"))
    horse_id = Column(Integer, ForeignKey("horses.id"))
    jockey_id = Column(Integer, ForeignKey("jockeys.id"))

    place = Column(Integer)  # занятое место
    finish_time = Column(Float)  # время в секундах (можно хранить как float)

    race = relationship("Race", back_populates="results")
    horse = relationship("Horse", back_populates="race_results")
    jockey = relationship("Jockey", back_populates="race_results")

