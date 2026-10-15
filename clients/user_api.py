from config.base_urls import AUTH_BASE_URL
from config.endpoints import USER
from custom_requester.custom_requester import CustomRequester


class UserApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=AUTH_BASE_URL)

    def get_user_by_token(self):
        return self.send_request(
            method="POST",
            endpoint=f"{USER}/me",
        )

    def get_user(self, user_locator):
        return self.send_request(
            method="GET",
            endpoint=f"{USER}/{user_locator}",
        )

    def create_user(self, user_data):
        return self.send_request(
            method="POST",
            endpoint=f"{USER}",
            json=user_data,
        )

    def delete_user(self, user_id):
        return self.send_request(
            method="DELETE",
            endpoint=f"{USER}/{user_id}",
        )