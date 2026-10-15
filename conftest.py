from typing import Any, Iterator

import pytest
import requests
from sqlalchemy.orm import Session

from clients.api_manager import ApiManager
from constants.roles import Roles
from data.movie_data import build_movie_payload
from data.user_data import build_register_user_payload
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper
from entities.user import User
from resources.user_creds import SuperAdminCreds
from utils.data_generator import DataGenerator


# ACTORS
@pytest.fixture
def user_session():
    """
    Фабрика изолированных сессий
    :return: сессию пользователя ApiManager(session)
    """
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture
def super_admin(user_session):
    """
    сессия пользователя с правами SUPER_ADMIN
    :param user_session:
    :return:
    """
    new_session = user_session()

    super_admin = User(
        email=SuperAdminCreds.EMAIL,
        password=SuperAdminCreds.PASSWORD,
        roles=[Roles.SUPER_ADMIN.value],
        api=new_session,
    )

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture
def admin(user_session, super_admin, admin_data):
    new_session = user_session()

    response_data = super_admin.api.auth_api.create_user(admin_data).json()

    admin = User(
        user_id=response_data["id"],
        email=admin_data["email"],
        password=admin_data["password"],
        roles=admin_data["roles"],
        api=new_session,
    )

    admin.api.auth_api.authenticate(admin.creds)

    yield admin

    super_admin.api.user_api.delete_user(admin.id)


@pytest.fixture
def common_user(user_session, super_admin, common_user_data):
    new_session = user_session()

    response_data = super_admin.api.user_api.create_user(common_user_data).json()

    common_user = User(
        user_id=response_data["id"],
        email=common_user_data["email"],
        password=common_user_data["password"],
        roles=common_user_data["roles"],
        api=new_session,
    )

    common_user.api.auth_api.authenticate(common_user.creds)

    yield common_user

    super_admin.api.user_api.delete_user(common_user.id)


@pytest.fixture
def unauthorized_user(user_session):
    new_session = user_session()

    unauthorized_user = User(
        email=None,
        password=None,
        roles=[],
        api=new_session,
    )

    return unauthorized_user


@pytest.fixture(scope="function")
def admin_data() -> dict[str, Any]:
    return build_register_user_payload(
        verified = True,
        banned = False,
        roles = [Roles.ADMIN.value],
    )


@pytest.fixture(scope="function")
def common_user_data() -> dict[str, Any]:
    return build_register_user_payload(
        verified=True,
        banned=False,
        roles=[Roles.USER.value],
    )


@pytest.fixture(scope="function")
def generated_user_data() -> dict[str, Any]:
    return build_register_user_payload()


# FILM
@pytest.fixture(scope="function")
def created_movie(super_admin):
    payload = build_movie_payload()
    response = super_admin.api.movies_api.create_movie(payload)
    assert response.status_code == 201, response.text
    movie = response.json()

    yield movie

    super_admin.api.movies_api.delete_movie(movie["id"])


@pytest.fixture(scope="module")
def db_session() -> Iterator[Session]:
    db_session = get_db_session()
    yield db_session
    db_session.close()

@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture(scope="function")
def created_user(db_helper):
    user = db_helper.create_user(DataGenerator.generate_user_data())
    yield user
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)