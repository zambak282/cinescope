from random import randint

import allure
import pytest
from playwright.sync_api import Page, expect

from pages.register_page import CinescopeRegisterPage


pytestmark = pytest.mark.ui


@allure.epic("Тестирование UI")
@allure.feature("Регистрация")
class TestRegistration:
    @allure.title("Успешная регистрация нового пользователя")
    def test_registration(self, register_page, page):
        email = f"aqatest{randint(1, 999999)}@email.qa"
        register_page.register("Серега Серега", email, "qwerty123Q")
        expect(page.get_by_text("Подтвердите свою почту")).to_be_visible()