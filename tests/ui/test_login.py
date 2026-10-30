import allure
import pytest
from playwright.sync_api import expect


pytestmark = pytest.mark.ui


@allure.epic("Тестирование UI")
@allure.feature("Логин")
class TestLogin:
    @allure.title("Успешный логин пользователя")
    def test_login(self, common_user, login_page, page):
        login_page.login(common_user.email, common_user.password)
        expect(page.get_by_role("button", name="Профиль")).to_be_visible(timeout=50000)