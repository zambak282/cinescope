import pytest

pytestmark = pytest.mark.auth


class TestAuth:
    def test_register_user(self, unauthorized_api_manager, test_user_data):
        response = unauthorized_api_manager.auth_api.register_user(test_user_data)
        assert response.status_code == 201, \
            f"Expected 201, got {response.status_code}"

        response_data = response.json()
        assert response_data["email"] == test_user_data["email"]
        assert "id" in response_data
        assert "USER" in response_data["roles"]

    def test_register_and_login_user(self, unauthorized_api_manager, registered_user):
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"],
        }
        response = unauthorized_api_manager.auth_api.login_user(login_data)
        assert response.status_code == 200, \
            f"Expected 200, got {response.status_code}"

        response_data = response.json()
        assert "accessToken" in response_data
        assert response_data["user"]["email"] == registered_user["email"]

    @pytest.mark.skip
    def test_logout_user(self, unauthorized_api_manager):
        response = unauthorized_api_manager.auth_api.logout_user()
        assert response.status_code == 200, f"Expected 204, got {response.status_code}"