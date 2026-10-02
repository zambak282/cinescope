import pytest
import requests

from clients.api_manager import ApiManager
from data.movies.movie_data import build_movie_payload
from utils.data_generator import generate_random_password, generate_random_email, generate_random_name


SUPER_ADMIN_EMAIL = "api1@gmail.com"
SUPER_ADMIN_PASSWORD = "asdqwe123Q"


# SESSIONS
@pytest.fixture(scope="session")
def session_factory():
    sessions: list[requests.Session] = []
    def _make() -> requests.Session:
        s = requests.Session()
        sessions.append(s)
        return s

    yield _make

    for s in sessions:
        s.close()


# MANAGERS
@pytest.fixture(scope="function")
def api_manager(session_factory):
    return ApiManager(session=session_factory())

@pytest.fixture(scope="session")
def super_admin_api_manager(session_factory):
    api = ApiManager(session=session_factory())
    api.auth_api.authenticate((SUPER_ADMIN_EMAIL, SUPER_ADMIN_PASSWORD))
    return api

#pytest.fixture(scope="session")
#def admin_api_manager(session_factory):
#    return ApiManager(session=session_factory())

@pytest.fixture(scope="function")
def user_api_manager(session_factory, registered_user):
    api = ApiManager(session=session_factory())
    api.auth_api.authenticate((registered_user["email"], registered_user["password"]))
    return api

@pytest.fixture(scope="function")
def unauthorized_api_manager(session_factory):
    return ApiManager(session=session_factory())


# USER
@pytest.fixture(scope="function")
def test_user_data():
    password = generate_random_password()
    return {
        "email": generate_random_email(),
        "fullName": generate_random_name(),
        "password": password,
        "passwordRepeat": password,
        "roles": ["USER"]
    }


@pytest.fixture(scope="function")
def registered_user(session_factory, test_user_data, super_admin_api_manager):
    api = ApiManager(session=session_factory())
    response = api.auth_api.register_user(test_user_data)
    assert response.status_code == 201, response.text
    test_user_data["id"] = response.json()["id"]

    yield test_user_data

    super_admin_api_manager.user_api.delete_user(test_user_data["id"])


# FILM
@pytest.fixture(scope="function")
def created_movie(super_admin_api_manager):
    payload = build_movie_payload()
    response = super_admin_api_manager.movies_api.create_movie(payload)
    assert response.status_code == 201, response.text
    movie = response.json()

    yield movie

    super_admin_api_manager.movies_api.delete_movie(movie["id"])