from typing import Optional

from clients.api_manager import ApiManager


class User:
    def __init__(self, email: Optional[str], password: Optional[str], roles: list, api: ApiManager, user_id: Optional[str] = None):
        self.id = user_id
        self.email = email
        self.password = password
        self.roles = roles
        self.api = api

    @property
    def creds(self):
        return self.email, self.password

    @property
    def login_data(self):
        return {"email": self.email, "password": self.password}