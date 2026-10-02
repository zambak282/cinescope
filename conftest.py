import pytest
import requests

from clients.api_manager import ApiManager
from clients.auth_api import AuthApi
from clients.user_api import UserApi
from utils.data_generator import generate_random_password, generate_random_email, generate_random_name


@pytest.fixture(scope="session")
def session():
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    return ApiManager(session=session)

@pytest.fixture(scope="session")
def unauthorized_api_manager(session):
    return ApiManager(session=session)

@pytest.fixture(scope="function")
def test_user():
    password = generate_random_password()
    return {
        "email": generate_random_email(),
        "fullName": generate_random_name(),
        "password": password,
        "passwordRepeat": password,
        "roles": ["USER"]
    }

@pytest.fixture(scope="function")
def registered_user(api_manager, test_user):
    response = api_manager.auth_api.register_user(test_user).json()
    test_user["id"] = response["id"]
    return test_user