import time

import allure
import pytest
from playwright.sync_api import expect

from resources.user_creds import SuperAdminCreds


pytestmark = pytest.mark.ui


@allure.epic("Тестирование UI")
@allure.feature("Логин")
class TestLogin:
    @allure.title("Успешный логин пользователя")
    def test_login(self, created_user, login_page, page):
        login_page.login(created_user.email, created_user.password)
        expect(page.get_by_role("button", name="Профиль")).to_be_visible(timeout=50000)