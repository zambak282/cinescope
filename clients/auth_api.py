from config.base_urls import AUTH_BASE_URL
from custom_requester.custom_requester import CustomRequester

REGISTER = '/register'
LOGIN = '/login'
LOGOUT = '/logout'

class AuthApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=AUTH_BASE_URL)

    def authenticate(self, user_creds):
        login_data = {
            "email": user_creds[0],
            "password": user_creds[1]
        }
        response = self.login_user(login_data).json()
        if "access_token" not in response:
            raise KeyError("token is missing")
        token = response["accessToken"]
        self._update_session_headers({"authorization": f"Bearer {token}"})

    def register_user(self, user_data):
        return self.send_request(
            method="POST",
            endpoint=REGISTER,
            json=user_data
        )

    def login_user(self, login_data):
        return self.send_request(
            method="POST",
            endpoint=LOGIN,
            json=login_data
        )

    def logout_user(self):
        return self.send_request(
            method="GET",
            endpoint=LOGOUT
        )