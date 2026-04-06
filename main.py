from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

from db.database import get_db, engine
from models.models import Base

import crud.crud as crud
import schemas.schemas as schemas
from hooks.hooks import exception_handlers


def create_tables():
    Base.metadata.create_all(bind=engine)


app = FastAPI(title="Horse Racing Management System")


# -------------------- EXCEPTION HANDLERS --------------------

for exception, handler in exception_handlers.items():
    app.add_exception_handler(exception, handler)


# -------------------- STARTUP --------------------

@app.on_event("startup")
def on_startup():
    create_tables()


# -------------------- ROOT --------------------

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в систему управления скачками!"}


# -------------------- OWNERS --------------------

@app.post("/owners/", response_model=schemas.Owner)
def create_owner(owner: schemas.OwnerCreate, db: Session = Depends(get_db)):
    return crud.create_owner(db, owner)


@app.get("/owners/", response_model=List[schemas.Owner])
def get_owners(db: Session = Depends(get_db)):
    return crud.get_owners(db)


@app.get("/owners/{owner_id}", response_model=schemas.Owner)
def get_owner(owner_id: int, db: Session = Depends(get_db)):
    return crud.get_owner(db, owner_id)


@app.delete("/owners/{owner_id}", response_model=schemas.Owner)
def delete_owner(owner_id: int, db: Session = Depends(get_db)):
    return crud.delete_owner(db, owner_id)


# -------------------- HORSES --------------------

@app.post("/horses/", response_model=schemas.Horse)
def create_horse(horse: schemas.HorseCreate, db: Session = Depends(get_db)):
    return crud.create_horse(db, horse)


@app.get("/horses/", response_model=List[schemas.Horse])
def get_horses(db: Session = Depends(get_db)):
    return crud.get_horses(db)


@app.get("/horses/{horse_id}", response_model=schemas.Horse)
def get_horse(horse_id: int, db: Session = Depends(get_db)):
    return crud.get_horse(db, horse_id)


@app.delete("/horses/{horse_id}", response_model=schemas.Horse)
def delete_horse(horse_id: int, db: Session = Depends(get_db)):
    return crud.delete_horse(db, horse_id)


@app.get("/horses/{horse_id}/races", response_model=schemas.HorseRaces)
def get_horse_races(horse_id: int, db: Session = Depends(get_db)):
    return crud.get_horse_races(db, horse_id)


# -------------------- JOCKEYS --------------------

@app.post("/jockeys/", response_model=schemas.Jockey)
def create_jockey(jockey: schemas.JockeyCreate, db: Session = Depends(get_db)):
    return crud.create_jockey(db, jockey)


@app.get("/jockeys/", response_model=List[schemas.Jockey])
def get_jockeys(db: Session = Depends(get_db)):
    return crud.get_jockeys(db)


@app.get("/jockeys/{jockey_id}", response_model=schemas.Jockey)
def get_jockey(jockey_id: int, db: Session = Depends(get_db)):
    return crud.get_jockey(db, jockey_id)


@app.delete("/jockeys/{jockey_id}", response_model=schemas.Jockey)
def delete_jockey(jockey_id: int, db: Session = Depends(get_db)):
    return crud.delete_jockey(db, jockey_id)


@app.get("/jockeys/{jockey_id}/races", response_model=schemas.JockeyRaces)
def get_jockey_races(jockey_id: int, db: Session = Depends(get_db)):
    return crud.get_jockey_races(db, jockey_id)


# -------------------- RACES --------------------

@app.post("/races/", response_model=schemas.RaceWithResults)
def create_race(race: schemas.RaceCreate, db: Session = Depends(get_db)):
    return crud.create_race(db, race)


@app.get("/races/", response_model=List[schemas.RaceBase])
def get_races(db: Session = Depends(get_db)):
    return crud.get_races(db)


@app.get("/races/{race_id}", response_model=schemas.RaceWithResults)
def get_race(race_id: int, db: Session = Depends(get_db)):
    return crud.get_race(db, race_id)


@app.delete("/races/{race_id}", response_model=schemas.RaceBase)
def delete_race(race_id: int, db: Session = Depends(get_db)):
    return crud.delete_race(db, race_id)


# -------------------- RACE RESULTS --------------------

@app.post("/races/{race_id}/results", response_model=schemas.RaceResult)
def add_race_result(
    race_id: int,
    result: schemas.RaceResultCreate,
    db: Session = Depends(get_db)
):
    return crud.add_race_result(db, race_id, result)


@app.get("/results/", response_model=List[schemas.RaceResult])
def get_all_results(db: Session = Depends(get_db)):
    return crud.get_races_results(db)


@app.get("/races/{race_id}/results", response_model=List[schemas.RaceResult])
def get_race_results(race_id: int, db: Session = Depends(get_db)):
    return crud.get_race_results(db, race_id)


@app.delete("/results/{result_id}", response_model=schemas.RaceResult)
def delete_race_result(result_id: int, db: Session = Depends(get_db)):
    return crud.delete_race_results(db, result_id)


# -------------------- RUN --------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
