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
class TestRegistrationLoginReview:
    @allure.title("Регистрация, логин и создание отзыва")
    def test_registration_login_review(self, created_movie, register_page, login_page, film_page, page):
        with allure.step("1. Регистрация пользователя"):
            name = DataGenerator.generate_random_name()
            email = DataGenerator.generate_random_email()
            password = DataGenerator.generate_random_password()

            page.goto("https://dev-cinescope.f5qa.ru/register")
            register_page.register(name, email, password)
            expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(timeout=10000)

        with allure.step("2. Логин созданного пользователя"):
            login_page.login(email, password)
            expect(page.get_by_role("button", name="Профиль")).to_be_visible(timeout=10000)

        with allure.step("3. Открытие страницы созданного фильма"):
            film_page.open_film(created_movie["id"])

        with allure.step("4. Оставление отзыва со случайными текстом и оценкой"):
            review_text = DataGenerator.generate_review_text()
            allure.attach(review_text, name="Текст отправленного отзыва", attachment_type=allure.attachment_type.TEXT)
            film_page.write_review(review_text)
            film_page.select_rating(randint(1, 5))
            film_page.submit_review()

        with allure.step("5. Проверка появления отзыва на странице"):
            expect(film_page.page.get_by_text(review_text)).to_be_visible(timeout=10000)