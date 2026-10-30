import pytest

pytestmark = pytest.mark.db


def test_db_requests(super_admin, db_helper, created_user_db):
    assert created_user_db == db_helper.get_user_by_id(created_user_db.id)
    assert db_helper.user_exists_by_email("api1@gmail.com")