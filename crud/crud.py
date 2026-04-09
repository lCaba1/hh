from sqlalchemy.orm import Session
from models.models import Owner, Horse, Jockey, Race, RaceResult

from schemas.schemas import (
    OwnerCreate,
    HorseCreate,
    JockeyCreate,
    RaceCreate,
    RaceResultCreate
)

from exceptions.exceptions import (
    OwnerNotFoundException, OwnerHasHorsesException,
    HorseNotFoundException, HorseHasResultsException,
    JockeyNotFoundException, JockeyHasResultsException,
    RaceNotFoundException, RaceHasResultsException,
    RaceResultNotFoundException, HorseAlreadyInRaceException, JockeyAlreadyInRaceException
)


# -------------------- OWNER --------------------

def create_owner(db: Session, owner: OwnerCreate):
    db_owner = Owner(**owner.model_dump())
    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    return db_owner


def get_owners(db: Session):
    return db.query(Owner).all()


def get_owner(db: Session, owner_id: int):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    #if not owner:
    #    raise OwnerNotFoundException(f"Владелец с ID {owner_id} не найден")
    return owner


def delete_owner(db: Session, owner_id: int):
    owner = get_owner(db, owner_id)

    # нельзя удалить если есть лошади
    if owner.horses:
        raise OwnerHasHorsesException("У владельца есть лошади")

    db.delete(owner)
    db.commit()
    return owner


# -------------------- HORSE --------------------

def create_horse(db: Session, horse: HorseCreate):
    owner = get_owner(db, horse.owner_id)
    db_horse = Horse(**horse.model_dump())
    db.add(db_horse)
    db.commit()
    db.refresh(db_horse)
    return db_horse


def get_horses(db: Session):
    return db.query(Horse).all()


def get_horse(db: Session, horse_id: int):
    horse = db.query(Horse).filter(Horse.id == horse_id).first()
    if not horse:
        raise HorseNotFoundException(f"Лошадь с ID {horse_id} не найдена")
    return horse


def delete_horse(db: Session, horse_id: int):
    horse = get_horse(db, horse_id)

    if horse.race_results:
        raise HorseHasResultsException("Нельзя удалить лошадь, участвовавшую в состязаниях")

    db.delete(horse)
    db.commit()
    return horse


def get_horse_races(db: Session, horse_id: int):
    horse = get_horse(db, horse_id)

    results = db.query(RaceResult).filter(
        RaceResult.horse_id == horse_id
    ).all()

    races = [r.race for r in results]

    return {
        "horse_id": horse.id,
        "horse_name": horse.name,
        "races": races
    }


# -------------------- JOCKEY --------------------

def create_jockey(db: Session, jockey: JockeyCreate):
    existing = db.query(Jockey).filter(Jockey.name == jockey.name).first()
    db_jockey = Jockey(**jockey.model_dump())
    db.add(db_jockey)
    db.commit()
    db.refresh(db_jockey)
    return db_jockey


def get_jockeys(db: Session):
    return db.query(Jockey).all()


def get_jockey(db: Session, jockey_id: int):
    jockey = db.query(Jockey).filter(Jockey.id == jockey_id).first()
    if not jockey:
        raise JockeyNotFoundException(f"Жокей с ID {jockey_id} не найден")
    return jockey


def delete_jockey(db: Session, jockey_id: int):
    jockey = get_jockey(db, jockey_id)

    if jockey.race_results:
        raise JockeyHasResultsException("Нельзя удалить жокея, участвовавшего в состязаниях")

    db.delete(jockey)
    db.commit()
    return jockey


def get_jockey_races(db: Session, jockey_id: int):
    jockey = get_jockey(db, jockey_id)

    results = db.query(RaceResult).filter(
        RaceResult.jockey_id == jockey_id
    ).all()

    races = [r.race for r in results]

    return {
        "jockey_id": jockey.id,
        "jockey_name": jockey.name,
        "races": races
    }


# -------------------- RACE --------------------

def create_race(db: Session, race: RaceCreate):
    existing = db.query(Race).filter(
        Race.date == race.date,
        Race.time == race.time,
        Race.hippodrome == race.hippodrome
    ).first()

    db_race = Race(**race.model_dump())
    db.add(db_race)
    db.commit()
    db.refresh(db_race)
    return db_race


def get_races(db: Session):
    return db.query(Race).all()


def get_race(db: Session, race_id: int):
    race = db.query(Race).filter(Race.id == race_id).first()
    if not race:
        raise RaceNotFoundException(f"Состязание с ID {race_id} не найдено")
    return race


def delete_race(db: Session, race_id: int):
    race = get_race(db, race_id)

    if race.results:
        raise RaceHasResultsException("Нельзя удалить состязание с результатами")

    db.delete(race)
    db.commit()
    return race



# -------------------- RACE RESULT --------------------

def add_race_result(db: Session, race_id: int, result: RaceResultCreate):
    race = get_race(db, race_id)

    horse = get_horse(db, result.horse_id)
    jockey = get_jockey(db, result.jockey_id)

    # проверка уникальности лошади в гонке
    existing = db.query(RaceResult).filter(
        RaceResult.race_id == race_id,
        RaceResult.horse_id == result.horse_id
    ).first()

    if existing:
        raise HorseAlreadyInRaceException("Результат для этой лошади уже добавлен")

    # проверка уникальности жокея
    jockey_exists = db.query(RaceResult).filter(
        RaceResult.race_id == race_id,
        RaceResult.jockey_id == result.jockey_id
    ).first()

    if jockey_exists:
        raise JockeyAlreadyInRaceException("Результат для этого жокея уже добавлен")

    db_result = RaceResult(
        race_id=race_id,
        **result.model_dump()
    )

    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result


def get_races_results(db: Session):
    return db.query(RaceResult).all()


def get_race_results(db: Session, race_id: int):
    race = get_race(db, race_id)
    return race.results


def delete_race_results(db: Session, result_id: int):
    result = db.query(RaceResult).filter(RaceResult.id == result_id).first()
    if not result:
        raise RaceResultNotFoundException(
            f"Результат с ID {result_id} не найден"
        )

    db.delete(result)
    db.commit()
    return result
