from random import randint

import allure
import pytest

from utils.data_generator import DataGenerator


pytestmark = pytest.mark.ui


@allure.epic("Тестирование UI")
@allure.feature("Отзывы")
class TestReview:
    @allure.title("Корректное создание отзыва")
    def test_add_review(self, logged_in_user, created_movie, film_page):
        with allure.step("1. Открытие страницы созданного фильма"):
            film_page.open_film(created_movie["id"])

        with allure.step("2. Оставление отзыва со случайным текстом и оценкой"):
            review_text = DataGenerator.generate_review_text()
            allure.attach(review_text, name="Текст отправленного отзыва", attachment_type=allure.attachment_type.TEXT)
            film_page.leave_review(randint(1, 5), review_text)

        with allure.step("3. Проверка появления отзыва на странице"):
            film_page.expect_review_visible(review_text)