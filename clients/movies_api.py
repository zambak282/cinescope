from config.base_urls import API_BASE_URL
from config.endpoints import MOVIES
from custom_requester.custom_requester import CustomRequester


class MoviesApi(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=API_BASE_URL)

    def get_movies(self, params=None):
        return self.send_request(
            method="GET",
            endpoint=MOVIES,
            params=params
        )

    def get_movie(self, movie_id):
        return self.send_request(
            method="GET",
            endpoint=f"{MOVIES}/{movie_id}"
        )

    def create_movie(self, movie_data):
        return self.send_request(
            method="POST",
            endpoint=MOVIES,
            json=movie_data
        )

    def delete_movie(self, movie_id):
        return self.send_request(
            method="DELETE",
            endpoint=f"{MOVIES}/{movie_id}"
        )

    def update_movie(self, movie_id, movie_data):
        return self.send_request(
            method="PATCH",
            endpoint=f"{MOVIES}/{movie_id}",
            json=movie_data
        )