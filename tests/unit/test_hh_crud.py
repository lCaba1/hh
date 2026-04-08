import pytest
from unittest.mock import Mock, create_autospec
from sqlalchemy.orm import Session
from models.models import Owner, Horse, Jockey, Race, RaceResult
from schemas.schemas import OwnerCreate, HorseCreate, JockeyCreate, RaceCreate, RaceResultCreate
from exceptions.exceptions import (
    OwnerNotFoundException,
    OwnerHasHorsesException,
    HorseNotFoundException,
    HorseHasResultsException,
    JockeyNotFoundException,
    JockeyHasResultsException,
    RaceNotFoundException,
    RaceHasResultsException,
    RaceResultNotFoundException,
    HorseAlreadyInRaceException
)
from crud.crud import (
    get_owner, get_owners, create_owner, delete_owner,
    get_horse, get_horses, create_horse, delete_horse,
    get_jockey, get_jockeys, create_jockey, delete_jockey,
    create_race, get_races, get_race, delete_race,
    add_race_result, get_races_results, get_race_results, delete_race_results
)


class TestOwnerCRUD:
    def test_get_owner_found(self):
        mock_db = create_autospec(Session)
        mock_owner = Mock(spec=Owner)
        mock_db.query.return_value.filter.return_value.first.return_value = mock_owner

        result = get_owner(mock_db, 1)

        assert result == mock_owner
        mock_db.query.assert_called_once_with(Owner)

    def test_get_owner_not_found(self):
        mock_db = create_autospec(Session)
        mock_db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(OwnerNotFoundException):
            get_owner(mock_db, 999)

    def test_get_owners(self):
        mock_db = create_autospec(Session)
        mock_owners = [Mock(spec=Owner), Mock(spec=Owner)]
        mock_db.query.return_value.all.return_value = mock_owners

        result = get_owners(mock_db)

        assert result == mock_owners
        mock_db.query.assert_called_once_with(Owner)

    def test_delete_owner_success(self):
        mock_db = create_autospec(Session)
        mock_owner = Mock(spec=Owner)
        mock_owner.horses = []

        with pytest.MonkeyPatch().context() as m:
            m.setattr('crud.crud.get_owner', lambda db, owner_id: mock_owner)

            result = delete_owner(mock_db, 1)

            assert result == mock_owner
            mock_db.delete.assert_called_once_with(mock_owner)
            mock_db.commit.assert_called_once()

    def test_delete_owner_not_found(self):
        mock_db = create_autospec(Session)

        with pytest.MonkeyPatch().context() as m:
            def mock_get_owner_fail(db, owner_id):
                raise OwnerNotFoundException(f"Владелец с ID {owner_id} не найден")

            m.setattr('crud.crud.get_owner', mock_get_owner_fail)

            with pytest.raises(OwnerNotFoundException):
                delete_owner(mock_db, 999)


class TestHorseCRUD:
    def test_create_horse_owner_not_found(self):
        mock_db = create_autospec(Session)
        horse_data = HorseCreate(
            name="Test Horse",
            gender="female",
            age=5,
            owner_id=999
        )

        mock_db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(OwnerNotFoundException):
            create_horse(mock_db, horse_data)

    def test_get_horse_found(self):
        mock_db = create_autospec(Session)
        mock_horse = Mock(spec=Horse)
        mock_db.query.return_value.filter.return_value.first.return_value = mock_horse

        result = get_horse(mock_db, 1)

        assert result == mock_horse
        mock_db.query.assert_called_once_with(Horse)

    def test_get_horses(self):
        mock_db = create_autospec(Session)
        mock_horses = [Mock(spec=Horse), Mock(spec=Horse)]
        mock_db.query.return_value.all.return_value = mock_horses

        result = get_horses(mock_db)

        assert result == mock_horses
        mock_db.query.assert_called_once_with(Horse)

    def test_delete_horse_success(self):
        mock_db = create_autospec(Session)
        mock_horse = Mock(spec=Horse)
        mock_horse.race_results = []

        with pytest.MonkeyPatch().context() as m:
            m.setattr('crud.crud.get_horse', lambda db, horse_id: mock_horse)

            result = delete_horse(mock_db, 1)

            assert result == mock_horse
            mock_db.delete.assert_called_once_with(mock_horse)
            mock_db.commit.assert_called_once()


class TestJockeyCRUD:
    def test_create_jockey(self):
        mock_db = create_autospec(Session)
        jockey_data = JockeyCreate(
            name="Test Jockey",
            address="Test Address",
            age=30,
            rating=7.5
        )

        result = create_jockey(mock_db, jockey_data)

        assert result is not None
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

    def test_get_jockeys(self):
        mock_db = create_autospec(Session)
        mock_jockeys = [Mock(spec=Jockey), Mock(spec=Jockey)]
        mock_db.query.return_value.all.return_value = mock_jockeys

        result = get_jockeys(mock_db)

        assert result == mock_jockeys
        mock_db.query.assert_called_once_with(Jockey)

    def test_get_jockey_not_found(self):
        mock_db = create_autospec(Session)
        mock_db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(JockeyNotFoundException):
            get_jockey(mock_db, 999)


class TestRaceCRUD:
    def test_create_race(self):
        mock_db = create_autospec(Session)
        race_data = RaceCreate(
            date="2026-05-01",
            time="15:30:00",
            hippodrome="Central Racetrack",
            name="Spring Cup"
        )

        result = create_race(mock_db, race_data)

        assert result is not None
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

    def test_get_race_not_found(self):
        mock_db = create_autospec(Session)
        mock_db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(RaceNotFoundException):
            get_race(mock_db, 999)

    def test_get_races(self):
        mock_db = create_autospec(Session)
        mock_races = [Mock(spec=Race), Mock(spec=Race)]
        mock_db.query.return_value.all.return_value = mock_races

        result = get_races(mock_db)

        assert result == mock_races
        mock_db.query.assert_called_once_with(Race)

    def test_delete_race_success(self):
        mock_db = create_autospec(Session)
        mock_race = Mock(spec=Race)
        mock_race.results = []

        with pytest.MonkeyPatch().context() as m:
            m.setattr('crud.crud.get_race', lambda db, race_id: mock_race)

            result = delete_race(mock_db, 1)

            assert result == mock_race
            mock_db.delete.assert_called_once_with(mock_race)
            mock_db.commit.assert_called_once()


class TestRaceResultCRUD:
    def test_add_race_result_duplicate_horse(self):
        mock_db = create_autospec(Session)
        result_data = RaceResultCreate(
            horse_id=1,
            jockey_id=1,
            place=1,
            finish_time=72.35
        )

        mock_db.query.return_value.filter.return_value.first.side_effect = [
            Mock(spec=Race),
            Mock(spec=Horse),
            Mock(spec=Jockey),
            Mock(spec=RaceResult)
        ]

        with pytest.raises(HorseAlreadyInRaceException):
            add_race_result(mock_db, 1, result_data)

    def test_delete_race_results_not_found(self):
        mock_db = create_autospec(Session)
        mock_db.query.return_value.filter.return_value.first.return_value = None

        with pytest.raises(RaceResultNotFoundException):
            delete_race_results(mock_db, 999)
