import time

import allure
import pytest


pytestmark = pytest.mark.ui


@allure.epic("Тестирование UI")
@allure.feature("Логин")
class TestLogin:
    @allure.title("Успешный логин пользователя")
    def test_login(self, created_user, login_page, page):
        login_page.login(created_user.email, created_user.password)

        time.sleep(5)