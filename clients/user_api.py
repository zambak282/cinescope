from config.base_urls import API_BASE_URL
from custom_requester.custom_requester import CustomRequester

USER = '/user'

class UserApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=API_BASE_URL)

    def get_user_info_by_token(self):
        return self.send_request(
            method="POST",
            endpoint=f"{USER}/me"
        )

    def delete_user(self, user_id):
        return self.send_request(
            method="DELETE",
            endpoint=f"{USER}/{user_id}"
        )