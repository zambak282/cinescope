from random import randint

import allure
import pytest

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

            register_page.open()
            register_page.register(name, email, password)
            register_page.expect_email_confirmation_visible()

        with allure.step("2. Логин созданного пользователя"):
            login_page.login(email, password)
            login_page.expect_profile_button_visible()

        with allure.step("3. Открытие страницы созданного фильма"):
            film_page.open_film(created_movie["id"])

        with allure.step("4. Оставление отзыва со случайными текстом и оценкой"):
            review_text = DataGenerator.generate_review_text()
            allure.attach(review_text, name="Текст отправленного отзыва", attachment_type=allure.attachment_type.TEXT)
            film_page.leave_review(randint(1, 5), review_text)

        with allure.step("5. Проверка появления отзыва на странице"):
            film_page.expect_review_visible(review_text)