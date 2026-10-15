import pytest

from models.user import CreateUserResponse, GetUserResponse

pytestmark = pytest.mark.user


class TestUser:
    def test_create_user(self, super_admin, common_user_data):
        create_response = super_admin.api.user_api.create_user(common_user_data)
        assert create_response.status_code == 201, \
            f"expected 201, got {create_response.status_code}"

        create_user_response = CreateUserResponse(**create_response.json())
        assert create_user_response.email == common_user_data["email"], \
            f"{create_user_response.email} should have {common_user_data['email']}"
        assert create_user_response.fullName == common_user_data["fullName"], \
            f"{create_user_response.fullName} should have {common_user_data['fullName']}"
        assert create_user_response.roles == common_user_data["roles"], \
            f"{create_user_response.roles} should have {common_user_data['roles']}"
        assert create_user_response.verified == common_user_data["verified"], \
            f"{create_user_response.verified} should have {common_user_data['verified']}"

        delete_response = super_admin.api.user_api.delete_user(create_user_response.id)
        assert delete_response.status_code == 200, \
            f"expected 200, got {delete_response.status_code}"

    def test_get_user_by_locator(self, super_admin, common_user_data):
        create_user_response = super_admin.api.user_api.create_user(common_user_data)
        assert create_user_response.status_code == 201, \
            f"expected 201, got {create_user_response.status_code}"
        created_user_data = create_user_response.json()

        response_by_id = super_admin.api.user_api.get_user(created_user_data["id"])
        assert response_by_id.status_code == 200, \
            f"expected 200, got {response_by_id.status_code}"
        response_by_email = super_admin.api.user_api.get_user(created_user_data["email"])
        assert response_by_email.status_code == 200, \
            f"expected 200, got {response_by_email.status_code}"

        get_user_response_by_id = GetUserResponse(**response_by_id.json())
        get_user_response_by_email = GetUserResponse(**response_by_email.json())

        assert get_user_response_by_id == get_user_response_by_email, \
            "response data must be identical"
        assert get_user_response_by_id.email == common_user_data["email"], \
            f"{get_user_response_by_id.email} must be {common_user_data['email']}"
        assert get_user_response_by_id.fullName == common_user_data["fullName"], \
            f"{get_user_response_by_id.fullName} must be {common_user_data['fullName']}"
        assert get_user_response_by_id.roles == common_user_data["roles"], \
            f"{get_user_response_by_id.roles} must be {common_user_data['roles']}"
        assert get_user_response_by_id.verified == common_user_data["verified"], \
            f"{get_user_response_by_id.verified} must be {common_user_data['verified']}"
        assert get_user_response_by_id.banned == common_user_data["banned"], \
            f"{get_user_response_by_id.banned} must be {common_user_data['banned']}"

        super_admin.api.user_api.delete_user(created_user_data["id"])

