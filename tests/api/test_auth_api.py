import pytest

from models.auth import RegisterUserResponse, LoginResponse

pytestmark = pytest.mark.auth


class TestAuth:
    def test_register_user(self, unauthorized_user, generated_user_data):
        response = unauthorized_user.api.auth_api.register_user(generated_user_data)
        assert response.status_code == 201, \
            f"Expected 201, got {response.status_code}"

        register_user_response = RegisterUserResponse(**response.json())

        assert register_user_response.email == generated_user_data["email"]

    def test_login_user(self, unauthorized_user, common_user):
        login_data = common_user.login_data
        response = unauthorized_user.api.auth_api.login_user(login_data)
        assert response.status_code == 201, \
            f"Expected 201, got {response.status_code}"

        login_response = LoginResponse(**response.json())
        assert login_response.user.email == common_user.email

    @pytest.mark.skip
    def test_logout_user(self, unauthorized_user):
        response = unauthorized_user.api.auth_api.logout_user()
        assert response.status_code == 200, f"Expected 204, got {response.status_code}"