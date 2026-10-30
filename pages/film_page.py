import allure
from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class CinescopeFilmPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}/movies"

        self.review_input = '[data-qa-id="movie_review_input"]'
        self.review_submit_button = '[data-qa-id="movie_review_submit_button"]'
        self.rating_combobox = page.get_by_role("combobox")

    @allure.step("Переход на страницу фильма: {film_id}")
    def open_film(self, film_id: int):
        self.open_url(f"{self.url}/{film_id}")

    @allure.step("Проверка видимости отзыва с текстом: {review_text}")
    def expect_review_visible(self, review_text: str, timeout: int = 10000):
        expect(self.page.get_by_text(review_text)).to_be_visible(timeout=timeout)

    def select_rating_value(self, rating: int):
        return self.page.get_by_role("option", name=str(rating), exact=True)

    @allure.step("Написание отзыва с рейтингом: {rating} и текстом: {text}")
    def leave_review(self, rating: int, text: str):
        self.enter_text(self.review_input, text)

        self.rating_combobox.click()
        self.select_rating_value(rating).click()

        self.page.click(self.review_submit_button)