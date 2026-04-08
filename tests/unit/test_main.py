import pytest
from sqlalchemy.orm import Session
import crud.crud as crud
from exceptions.exceptions import OwnerNotFoundException

class TestCRUD:
    def test_get_owner_not_found(self, db_session: Session):
        with pytest.raises(OwnerNotFoundException):
            crud.get_owner(db_session, 999)
