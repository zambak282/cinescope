import pytest

pytestmark = pytest.mark.movie


def test_get_movie_with_pagination_and_filter_by_genre(movie_requester):
    response = movie_requester.send_request(
        method="GET",
        endpoint="/movies",
        params={"genreId": 5, "page": 1, "pageSize": 10},
    )
    assert response.status_code == 200, \
        f"Expected 200, got {response.status_code}"