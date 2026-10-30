import time

from playwright.sync_api import Page, expect

from config.base_urls import BASE_URL
from pages.base_page import BasePage


class CinescopeLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}/login"

        self.email_input = '[data-qa-id="login_email_input"]'
        self.password_input = '[data-qa-id="login_password_input"]'
        self.submit_button = '[data-qa-id="login_submit_button"]'
        self.profile_button = '[data-qa-id="profile_page_button"]'

    def open(self):
        self.page.goto(self.url)

    def login(self, email: str, password: str) -> None:
        self.page.fill(self.email_input, email)
        self.page.fill(self.password_input, password)
        self.page.click(self.submit_button)

    def expect_profile_button_visible(self, timeout: int = 10000):
        expect(self.page.locator(self.profile_button)).to_be_visible(timeout=timeout)