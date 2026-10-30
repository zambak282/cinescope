from typing import Any, Iterator

import allure
import pytest
import requests
from playwright.sync_api import Playwright, Page, expect
from sqlalchemy.orm import Session

from clients.api_manager import ApiManager
from common.tools import Tools
from constants.roles import Roles
from data.movie_data import build_movie_payload
from data.user_data import build_register_user_payload
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper
from entities.user import User
from pages.film_page import CinescopeFilmPage
from pages.login_page import CinescopeLoginPage
from pages.register_page import CinescopeRegisterPage
from resources.user_creds import SuperAdminCreds
from utils.data_generator import DataGenerator


DEFAULT_UI_TIMEOUT = 30000 # 30 sec


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
def created_user_db(db_helper):
    user_data = DataGenerator.generate_user_data()
    created_user = db_helper.create_user(user_data)
    yield created_user
    if db_helper.get_user_by_id(created_user.id):
        db_helper.delete_user(created_user)


@pytest.fixture(scope="session")
def browser(playwright: Playwright):
    browser = playwright.firefox.launch(headless=False) # False - для вывода браузера
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context(ignore_https_errors=True)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    context.set_default_timeout(DEFAULT_UI_TIMEOUT)
    yield context
    log_name = f"trace_{Tools.get_timestamp()}.zip"
    trace_path = Tools.files_dir('playwright_trace', log_name)
    context.tracing.stop(path=trace_path)
    context.close()


@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def register_page(page: Page) -> CinescopeRegisterPage:
    register_page = CinescopeRegisterPage(page)
    register_page.open()
    return register_page


@pytest.fixture(scope="function")
def login_page(page: Page) -> CinescopeLoginPage:
    login_page = CinescopeLoginPage(page)
    login_page.open()
    return login_page


@pytest.fixture(scope="function")
def film_page(page: Page) -> CinescopeFilmPage:
    return CinescopeFilmPage(page)


@pytest.fixture(scope="function")
def logged_in_user(common_user, login_page, page):
    with allure.step(f"Логин пользователя с email: {common_user.email}"):
        login_page.login(common_user.email, common_user.password)
        page.wait_for_load_state("networkidle")
        expect(page.get_by_role("button", name="Профиль")).to_be_visible(timeout=10000)
    return common_user