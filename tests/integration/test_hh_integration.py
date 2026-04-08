import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database import Base
from models.models import Owner, Horse, Jockey, Race
from schemas.schemas import OwnerCreate, HorseCreate, JockeyCreate, RaceCreate, RaceResultCreate
from crud.crud import (
    create_owner, get_owner, get_owners,
    create_horse, get_horse, get_horses,
    create_jockey, get_jockey, get_jockeys,
    create_race, get_race, get_races,
    add_race_result, get_race_results, get_races_results, delete_race_results
)


@pytest.fixture
def db_session():
    DATABASE_URL = "sqlite:///:memory:"

    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
        engine.dispose()


class TestOwnerIntegration:
    def test_create_and_get_owner(self, db_session):
        owner_data = OwnerCreate(
            name="Stable Owner",
            address="123 Racetrack Blvd",
            phone="+1234567890"
        )

        created_owner = create_owner(db_session, owner_data)
        retrieved_owner = get_owner(db_session, created_owner.id)

        assert retrieved_owner is not None
        assert retrieved_owner.name == "Stable Owner"
        assert retrieved_owner.phone == "+1234567890"

    def test_get_all_owners(self, db_session):
        owner1 = OwnerCreate(name="Owner One", address="Address 1", phone="+1111111111")
        owner2 = OwnerCreate(name="Owner Two", address="Address 2", phone="+2222222222")

        create_owner(db_session, owner1)
        create_owner(db_session, owner2)

        all_owners = get_owners(db_session)

        assert len(all_owners) == 2
        owner_names = [owner.name for owner in all_owners]
        assert "Owner One" in owner_names
        assert "Owner Two" in owner_names


class TestHorseIntegration:
    def test_create_and_get_horse(self, db_session):
        owner = create_owner(db_session, OwnerCreate(
            name="Stable Owner",
            address="123 Racetrack Blvd",
            phone="+1234567890"
        ))

        horse_data = HorseCreate(
            name="Thunder",
            gender="male",
            age=6,
            owner_id=owner.id
        )

        created_horse = create_horse(db_session, horse_data)
        retrieved_horse = get_horse(db_session, created_horse.id)

        assert retrieved_horse is not None
        assert retrieved_horse.name == "Thunder"
        assert retrieved_horse.owner_id == owner.id

    def test_get_all_horses(self, db_session):
        owner = create_owner(db_session, OwnerCreate(
            name="Stable Owner",
            address="123 Racetrack Blvd",
            phone="+1234567890"
        ))

        horse1 = HorseCreate(name="Thunder", gender="male", age=6, owner_id=owner.id)
        horse2 = HorseCreate(name="Lightning", gender="female", age=5, owner_id=owner.id)

        create_horse(db_session, horse1)
        create_horse(db_session, horse2)

        all_horses = get_horses(db_session)

        assert len(all_horses) == 2
        horse_names = [horse.name for horse in all_horses]
        assert "Thunder" in horse_names
        assert "Lightning" in horse_names


class TestJockeyIntegration:
    def test_create_and_get_jockey(self, db_session):
        jockey_data = JockeyCreate(
            name="Alex Rider",
            address="456 Track Road",
            age=28,
            rating=9.1
        )

        created_jockey = create_jockey(db_session, jockey_data)
        retrieved_jockey = get_jockey(db_session, created_jockey.id)

        assert retrieved_jockey is not None
        assert retrieved_jockey.name == "Alex Rider"
        assert retrieved_jockey.rating == 9.1

    def test_get_all_jockeys(self, db_session):
        jockey1 = JockeyCreate(name="Alex Rider", address="456 Track Road", age=28, rating=9.1)
        jockey2 = JockeyCreate(name="Max Speed", address="789 Arena Ave", age=32, rating=8.3)

        create_jockey(db_session, jockey1)
        create_jockey(db_session, jockey2)

        all_jockeys = get_jockeys(db_session)

        assert len(all_jockeys) == 2
        jockey_names = [jockey.name for jockey in all_jockeys]
        assert "Alex Rider" in jockey_names
        assert "Max Speed" in jockey_names


class TestRaceIntegration:
    def test_create_and_get_race(self, db_session):
        race_data = RaceCreate(
            date="2026-05-01",
            time="15:30:00",
            hippodrome="Central Racetrack",
            name="Spring Cup"
        )

        created_race = create_race(db_session, race_data)
        retrieved_race = get_race(db_session, created_race.id)

        assert retrieved_race is not None
        assert retrieved_race.hippodrome == "Central Racetrack"
        assert retrieved_race.name == "Spring Cup"

    def test_get_all_races(self, db_session):
        race1 = RaceCreate(date="2026-05-01", time="15:30:00", hippodrome="Central Racetrack", name="Spring Cup")
        race2 = RaceCreate(date="2026-06-01", time="16:00:00", hippodrome="East Track", name="Summer Stakes")

        create_race(db_session, race1)
        create_race(db_session, race2)

        all_races = get_races(db_session)

        assert len(all_races) == 2
        race_names = [race.name for race in all_races]
        assert "Spring Cup" in race_names
        assert "Summer Stakes" in race_names


class TestRaceResultIntegration:
    def test_add_and_get_race_result(self, db_session):
        owner = create_owner(db_session, OwnerCreate(name="Stable Owner", address="123 Racetrack Blvd", phone="+1234567890"))
        horse = create_horse(db_session, HorseCreate(name="Thunder", gender="male", age=6, owner_id=owner.id))
        jockey = create_jockey(db_session, JockeyCreate(name="Alex Rider", address="456 Track Road", age=28, rating=9.1))
        race = create_race(db_session, RaceCreate(date="2026-05-01", time="15:30:00", hippodrome="Central Racetrack", name="Spring Cup"))

        result_data = RaceResultCreate(horse_id=horse.id, jockey_id=jockey.id, place=1, finish_time=72.35)
        created_result = add_race_result(db_session, race.id, result_data)

        assert created_result is not None
        assert created_result.place == 1
        assert created_result.horse_id == horse.id

    def test_get_race_results(self, db_session):
        owner = create_owner(db_session, OwnerCreate(name="Stable Owner", address="123 Racetrack Blvd", phone="+1234567890"))
        horse = create_horse(db_session, HorseCreate(name="Thunder", gender="male", age=6, owner_id=owner.id))
        jockey = create_jockey(db_session, JockeyCreate(name="Alex Rider", address="456 Track Road", age=28, rating=9.1))
        race = create_race(db_session, RaceCreate(date="2026-05-01", time="15:30:00", hippodrome="Central Racetrack", name="Spring Cup"))

        result_data = RaceResultCreate(horse_id=horse.id, jockey_id=jockey.id, place=1, finish_time=72.35)
        add_race_result(db_session, race.id, result_data)

        results = get_race_results(db_session, race.id)

        assert len(results) == 1
        assert results[0].horse_id == horse.id
        assert results[0].jockey_id == jockey.id

    def test_delete_race_result(self, db_session):
        owner = create_owner(db_session, OwnerCreate(name="Stable Owner", address="123 Racetrack Blvd", phone="+1234567890"))
        horse = create_horse(db_session, HorseCreate(name="Thunder", gender="male", age=6, owner_id=owner.id))
        jockey = create_jockey(db_session, JockeyCreate(name="Alex Rider", address="456 Track Road", age=28, rating=9.1))
        race = create_race(db_session, RaceCreate(date="2026-05-01", time="15:30:00", hippodrome="Central Racetrack", name="Spring Cup"))

        result_data = RaceResultCreate(horse_id=horse.id, jockey_id=jockey.id, place=1, finish_time=72.35)
        created_result = add_race_result(db_session, race.id, result_data)

        deleted_result = delete_race_results(db_session, created_result.id)

        assert deleted_result.id == created_result.id
        remaining_results = get_race_results(db_session, race.id)
        assert len(remaining_results) == 0

    def test_get_all_results(self, db_session):
        owner = create_owner(db_session, OwnerCreate(name="Stable Owner", address="123 Racetrack Blvd", phone="+1234567890"))
        horse = create_horse(db_session, HorseCreate(name="Thunder", gender="male", age=6, owner_id=owner.id))
        jockey = create_jockey(db_session, JockeyCreate(name="Alex Rider", address="456 Track Road", age=28, rating=9.1))
        race = create_race(db_session, RaceCreate(date="2026-05-01", time="15:30:00", hippodrome="Central Racetrack", name="Spring Cup"))

        result_data = RaceResultCreate(horse_id=horse.id, jockey_id=jockey.id, place=1, finish_time=72.35)
        add_race_result(db_session, race.id, result_data)

        all_results = get_races_results(db_session)

        assert len(all_results) == 1
        assert all_results[0].horse_id == horse.id
