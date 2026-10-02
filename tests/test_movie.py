import pytest

from data.movies.movie_data import build_movie_payload

pytestmark = pytest.mark.movie

NONEXISTENT_VALUE = -1


class TestMovie:
    def test_get_movies_with_pagination_and_filters(self, api_manager):
        response = api_manager.movies_api.get_movies(
            params={
                "genreId": 5,
                "minPrice": 1,
                "maxPrice": 1000,
                "locations": ["MSK", "SPB"],
                "published": True,
                "createdAt": "asc",
                "page": 1,
                "pageSize": 10,
            },
        )
        assert response.status_code == 200, \
            f"expected 200, got {response.status_code}"

    def test_get_movies_without_parameters(self, api_manager):
        response = api_manager.movies_api.get_movies()
        assert response.status_code == 200, \
            f"expected 200, got {response.status_code}"

    def test_get_movies_with_uncorrected_max_price_parameter(self, api_manager):
        response = api_manager.movies_api.get_movies(params={"maxPrice": NONEXISTENT_VALUE})
        assert response.status_code == 400, \
            f"expected 400, got {response.status_code}"

    def test_create_movie_with_correct_data_and_delete_them(self, super_admin_api_manager):
        payload = build_movie_payload()
        create_response = super_admin_api_manager.movies_api.create_movie(movie_data=payload)
        assert create_response.status_code == 201, \
            f"expected 201, got {create_response.status_code}"
        movie_id = create_response.json()["id"]

        delete_response = super_admin_api_manager.movies_api.delete_movie(movie_id=movie_id)
        assert delete_response.status_code == 200, \
            f"expected 200, got {delete_response.status_code}"

        get_response = super_admin_api_manager.movies_api.get_movie(movie_id=movie_id)
        assert get_response.status_code == 404, \
            f"expected 404, got {get_response.status_code}"

    def test_create_movie_with_nonexistent_parameter(self, super_admin_api_manager):
        payload = build_movie_payload()
        payload["nonexistent_parameter"] = ""

        response = super_admin_api_manager.movies_api.create_movie(movie_data=payload)
        assert response.status_code == 400, \
            f"expected 400, got {response.status_code}"

    def test_create_movie_with_taken_name(self, super_admin_api_manager, created_movie):
        second_payload = build_movie_payload()
        second_payload["name"] = created_movie["name"]
        second_response = super_admin_api_manager.movies_api.create_movie(movie_data=second_payload)
        assert second_response.status_code == 409, \
            f"expected 409, got {second_response.status_code}"

    def test_create_movie_with_only_user_role(self, user_api_manager):
        payload = build_movie_payload()

        response = user_api_manager.movies_api.create_movie(movie_data=payload)
        assert response.status_code == 403, \
            f"expected 403, got {response.status_code}"

    def test_get_existent_movie_by_id(self, api_manager, created_movie):
        response = api_manager.movies_api.get_movie(movie_id=created_movie["id"])
        assert response.status_code == 200, \
            f"expected 200, got {response.status_code}"

        response_data = response.json()
        assert response_data["id"] == created_movie["id"], \
            f"expected {created_movie['id']}, got {response_data['id']}"

    def test_get_nonexistent_movie_by_id(self, api_manager):
        response = api_manager.movies_api.get_movie(movie_id=NONEXISTENT_VALUE)
        assert response.status_code == 404, \
            f"expected 404, got {response.status_code}"

    def test_delete_movie_with_nonexistent_id(self, super_admin_api_manager):
        response = super_admin_api_manager.movies_api.delete_movie(movie_id=NONEXISTENT_VALUE)
        assert response.status_code == 404, \
            f"expected 404, got {response.status_code}"

    def test_update_movie_with_correct_data(self, super_admin_api_manager, created_movie):
        created_movie_id = created_movie["id"]
        new_movie_data = build_movie_payload()
        response = super_admin_api_manager.movies_api.update_movie(movie_id=created_movie_id, movie_data=new_movie_data)
        assert response.status_code == 200, \
            f"expected 200, got {response.status_code}"

    @pytest.mark.xfail(reason="not working")
    def test_update_movie_with_nonexistent_parameter(self, super_admin_api_manager, created_movie):
        created_movie_id = created_movie["id"]
        new_movie_data = build_movie_payload()
        new_movie_data["nonexistent_parameter"] = ""
        response = super_admin_api_manager.movies_api.update_movie(movie_id=created_movie_id, movie_data=new_movie_data)
        assert response.status_code == 400, \
            f"expected 400, got {response.status_code}"

    def test_update_movie_with_nonexistent_id(self, super_admin_api_manager):
        movie_data = build_movie_payload()
        response = super_admin_api_manager.movies_api.update_movie(movie_id=NONEXISTENT_VALUE, movie_data=movie_data)
        assert response.status_code == 404, \
            f"expected 404, got {response.status_code}"