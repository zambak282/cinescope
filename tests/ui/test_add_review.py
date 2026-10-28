import time
from random import random, randint

import allure
import pytest
from playwright.sync_api import expect

from resources.user_creds import SuperAdminCreds
from utils.data_generator import DataGenerator

pytestmark = pytest.mark.ui


@allure.epic("Тестирование UI")
@allure.feature("Отзывы")
class TestReview:
    @allure.title("Корректное создание отзыва")
    def register_login_and_test_review(self, created_user, created_movie, login_page, film_page, page):
        with allure.step("1. Логин пользователя"):
            login_page.login(created_user.email, created_user.password)
            page.wait_for_load_state("networkidle")
            expect(page.get_by_role("button", name="Профиль")).to_be_visible(timeout=10000)

        with allure.step("2. Открытие страницы созданного фильма"):
            film_page.open_film(created_movie["id"])

        with allure.step("3. Оставление отзыва со случайным текстом и оценкой"):
            review_text = DataGenerator.generate_review_text()
            allure.attach(review_text, name="Текст отправленного отзыва", attachment_type=allure.attachment_type.TEXT)
            film_page.write_review(review_text)
            film_page.select_rating(randint(1, 5))
            film_page.submit_review()

        with allure.step("4. Проверка появления отзыва на странице"):
            expect(film_page.page.get_by_text(review_text)).to_be_visible(timeout=10000)