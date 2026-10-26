from playwright.sync_api import Page

from config.base_urls import BASE_URL
from pages.base_page import BasePage


class CinescopeFilmPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}/movies"

        self.review_input = '[data-qa-id="movie_review_input"]'
        self.review_submit_button = '[data-qa-id="movie_review_submit_button"]'

    def open_film(self, film_id: int):
        self.page.goto(f"{self.url}/{film_id}")

    def write_review(self, text: str):
        self.page.fill(self.review_input, text)

    def select_rating(self, rating: int):
        self.page.get_by_role("combobox").click()
        self.page.get_by_role("option", name=str(rating), exact=True).click()

    def submit_review(self):
        self.page.click(self.review_submit_button)