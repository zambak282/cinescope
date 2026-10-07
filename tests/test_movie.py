import pytest

from data.movies.movie_data import build_movie_payload

pytestmark = pytest.mark.movie

NONEXISTENT_VALUE = -1


class TestMovie:
    def test_get_movies_with_pagination_and_filters(self, api_manager):
        params = {
            "genreId": 5,
            "minPrice": 1,
            "maxPrice": 1000,
            "locations": ["MSK", "SPB"],
            "published": True,
            "createdAt": "asc",
            "page": 2,
            "pageSize": 5,
        }

        response = api_manager.movies_api.get_movies(params=params)
        assert response.status_code == 200, \
            f"expected 200, got {response.status_code}"

        data = response.json()

        for field in ("movies", "count", "page", "pageSize", "pageCount"):
            assert field in data, \
                f"no {field} in {list(data)}"

        assert data["page"] == params["page"], \
            f"expected {params['page']}, got {data['page']}"
        assert data["pageSize"] == params["pageSize"], \
            f"expected {params['pageSize']}, got {data['pageSize']}"

        movies = data["movies"]
        assert len(movies) == min(params["pageSize"], data["count"]), \
            f"expected {params['pageSize']}, got {len(movies)}"

        for movie in movies:
            assert movie["genreId"] == params["genreId"], \
                f"expected {params['genreId']}, got {movie['genreId']}"
            assert params["minPrice"] <= movie["price"] <= params["maxPrice"], \
                f"price is not between {params['minPrice']} and {params['maxPrice']}"
            assert movie["location"] in params["locations"], \
                f"location is not in {params['locations']}"
            assert movie["published"] == params["published"], \
                f"expected params['published'], got {movie['published']}"

        dates = [m["createdAt"] for m in movies]
        assert dates == sorted(dates), \
            f"expected {sorted(dates)}, got {dates}"

    def test_get_movies_without_parameters(self, api_manager):
        response = api_manager.movies_api.get_movies()
        assert response.status_code == 200, \
            f"expected 200, got {response.status_code}"

    def test_get_movies_with_uncorrected_max_price_parameter(self, api_manager):
        response = api_manager.movies_api.get_movies(params={"maxPrice": NONEXISTENT_VALUE})
        assert response.status_code == 400, \
            f"expected 400, got {response.status_code}"

    def test_create_movie_with_correct_data(self, super_admin_api_manager):
        payload = build_movie_payload()
        response = super_admin_api_manager.movies_api.create_movie(movie_data=payload)
        assert response.status_code == 201, \
            f"expected 201, got {response.status_code}"
        data = response.json()

        for field in ("name", "price", "description", "imageUrl", "location", "published", "genreId"):
            assert data[field] == payload[field], \
                f"expected {field}, got {data[field]}"

        super_admin_api_manager.movies_api.delete_movie(movie_id=data["id"])

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

    def test_delete_movie_with_correct_data(self, super_admin_api_manager, created_movie):
        response = super_admin_api_manager.movies_api.delete_movie(movie_id=created_movie["id"])
        assert response.status_code == 200, \
            f"expected 200, got {response.status_code}"

        get_response = super_admin_api_manager.movies_api.get_movie(movie_id=created_movie["id"])
        assert get_response.status_code == 404, \
            f"expected 404, got {get_response.status_code}"

    def test_delete_movie_with_nonexistent_id(self, super_admin_api_manager):
        response = super_admin_api_manager.movies_api.delete_movie(movie_id=NONEXISTENT_VALUE)
        assert response.status_code == 404, \
            f"expected 404, got {response.status_code}"

    def test_update_movie_with_correct_data(self, super_admin_api_manager, created_movie):
        created_movie_id = created_movie["id"]
        new_movie_data = build_movie_payload()
        update_response = super_admin_api_manager.movies_api.update_movie(
            movie_id=created_movie_id, movie_data=new_movie_data
        )
        assert update_response.status_code == 200, \
            f"UPDATE: expected 200, got {update_response.status_code}"

        get_response = super_admin_api_manager.movies_api.get_movie(movie_id=created_movie_id)
        assert get_response.status_code == 200, \
            f"GET: expected 200, got {get_response.status_code}"

        get_response_data = get_response.json()
        for field in ("name", "price", "description", "imageUrl", "location", "published", "genreId"):
            assert get_response_data[field] == new_movie_data[field], \
                f"expected {new_movie_data[field]}, got {get_response_data[field]}"

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