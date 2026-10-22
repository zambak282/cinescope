from playwright.sync_api import Page


class CinescopeLoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://dev-cinescope.f5qa.ru/login"

        self.email_input = '[data-qa-id="login_email_input"]'
        self.password_input = '[data-qa-id="login_password_input"]'
        self.submit_button = '[data-qa-id="login_submit_button"]'

    def open(self):
        self.page.goto(self.url)

    def login(self, email: str, password: str):
        self.page.fill(self.email_input, email)
        self.page.fill(self.password_input, password)
        self.page.click(self.submit_button)
