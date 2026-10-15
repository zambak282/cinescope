import allure
import pytest

from data.movie_data import build_movie_payload
from utils.data_generator import DataGenerator


pytestmark = [
    pytest.mark.movie,
    pytest.mark.integration,
]


@allure.epic("Интеграционные тесты фильмов")
@allure.feature("Синхронизация с БД")
class TestMovieDB:
    @allure.story("Создание и удаление фильма")
    @allure.title("Фильм создаётся в БД через API и удаляется из БД через API")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("integration", "db", "smoke", "regression")
    def test_movie_db_create_and_delete(self, super_admin, db_helper):
        with allure.step("1. Создание пейлода и получение названия фильма"):
            payload = build_movie_payload()
            movie_name = payload["name"]

        with allure.step("2. Проверка, существует ли фильм в БД по названию"):
            assert db_helper.movie_exists_by_name(movie_name) is False, \
                f"Movie {movie_name} already exists"

        with allure.step("3. Создание фильма через API"):
            create_response = super_admin.api.movies_api.create_movie(payload)
            assert create_response.status_code == 201, create_response.text
            created_movie = create_response.json()

        with allure.step("4. Получение фильма из БД по id и проверка корректности записанных данных"):
            db_movie = db_helper.get_movie_by_id(created_movie["id"])
            assert db_movie is not None, \
                f"Movie {movie_name} not found"
            assert db_movie.name == created_movie["name"], \
                f"db movie name {db_movie.name} and the payload movie name {created_movie["name"]} are different"
            assert db_movie.price == created_movie["price"], \
                f"db movie price {db_movie.price} and the payload movie price {created_movie["price"]} are different"
            assert db_movie.description == created_movie["description"], \
                f"db movie description {db_movie.description} and the payload movie description {created_movie["description"]} are different"
            assert db_movie.image_url == created_movie["imageUrl"], \
                f"db movie image_url {db_movie.image_url} and the payload movie image_url {created_movie["imageUrl"]} are different"
            assert db_movie.location == created_movie["location"], \
                f"db movie location {db_movie.location} and the payload movie location {created_movie["location"]} are different"
            assert db_movie.published == created_movie["published"], \
                f"db movie published {db_movie.published} and the payload movie published {created_movie["published"]} are different"
            assert db_movie.genre_id == created_movie["genreId"], \
                f"db movie genre_id {db_movie.genre_id} and the payload movie genre_id {created_movie["genreId"]} are different"

        with allure.step("5. Удаление фильма через API"):
            delete_response = super_admin.api.movies_api.delete_movie(created_movie["id"])
            assert delete_response.status_code == 200, delete_response.text

        with allure.step("6. Проверка корректности удаления теста"):
            assert db_helper.get_movie_by_id(created_movie["id"]) is None, \
                f"db movie id {created_movie['id']} not deleted"


    @allure.story("Удаление конкретного фильма через API")
    @allure.title("Удаление фильма через API удаляет запись из БД, создает перед удалением, если записи нет")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("integration", "db", "regression")
    def test_delete_movie(self, super_admin, db_helper):
        with allure.step("1. Указание id фильма"):
            movie_id = 54

        with allure.step("2. Проверка, существует ли фильм с таким id. Если нет - создается новый"):
            is_exists = db_helper.movie_exists_by_id(movie_id)
            if not is_exists:
                movie = DataGenerator.generate_movie_data()
                movie["id"] = movie_id
                db_helper.create_movie(movie)

        with allure.step("3. Получение фильма по id через API"):
            get_response = super_admin.api.movies_api.get_movie(movie_id)
            assert get_response.status_code == 200, get_response.text

        with allure.step("4. Удаление филма по id через API"):
            delete_response = super_admin.api.movies_api.delete_movie(movie_id)
            assert delete_response.status_code == 200, delete_response.text

        with allure.step("5. Попытка получения удаленного фильма по id"):
            get_response = super_admin.api.movies_api.get_movie(movie_id)
            assert get_response.status_code == 404, get_response.text