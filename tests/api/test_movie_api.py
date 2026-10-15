import allure
import pytest

from conftest import super_admin
from data.movie_data import build_movie_payload
from models.movie import GetMovieResponse, GetMoviesResponse, CreateMovieResponse, CreateMovieRequest, \
    UpdateMovieRequest, UpdateMovieResponse

pytestmark = [
    pytest.mark.movie,
    pytest.mark.api,
    ]


@allure.epic("Тестирование фильмов")
@allure.feature("Тестирование фильмов через API")
@allure.link("https://api.dev-cinescope.f5qa.ru/swagger#/", name="Swagger Movies API")
class TestMovieApi:
    NONEXISTENT_VALUE = -1

    @allure.story("Пагинация и фильтры")
    @allure.title("Получение фильтров с пагинацией и всеми фильтрами")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "filters")
    def test_get_movies_with_pagination_and_filters(self, super_admin):
        with allure.step("1. Подготовка параметров"):
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

        with allure.step("2. Получение фильмов GET /movies с параметрами и проверка статуса ответа"):
            response = super_admin.api.movies_api.get_movies(params=params)
            assert response.status_code == 200, \
                f"expected 200, got {response.status_code}"

        with allure.step("3. Выделение pydantic-модели"):
            movies_response = GetMoviesResponse(**response.json())

        with allure.step("4. Проверка корректности применения пагинации: полей номера и размера страницы"
                         " и подходит ли количество возвращенных фильмов"):
            assert movies_response.page == params["page"], \
                f"expected {params['page']}, got {movies_response.page}"
            assert movies_response.pageSize == params["pageSize"], \
                f"expected {params['pageSize']}, got {movies_response.pageSize}"
            movies = movies_response.movies
            assert len(movies) == min(params["pageSize"], movies_response.count), \
                f"expected {params['pageSize']}, got {len(movies)}"

        with allure.step("5. Проверка корректности применения фильтров"):
            for movie in movies:
                assert movie.genreId == params["genreId"], \
                    f"expected {params['genreId']}, got {movie.genreId}"
                assert params["minPrice"] <= movie.price <= params["maxPrice"], \
                    f"price is not between {params['minPrice']} and {params['maxPrice']}"
                assert movie.location in params["locations"], \
                    f"location is not in {params['locations']}"
                assert movie.published == params["published"], \
                f"expected {params['published']}, got {movie.published}"

        with allure.step("6. Проверка сортировки"):
            dates = [movie.createdAt for movie in movies]
            assert dates == sorted(dates), \
                f"expected {sorted(dates)}, got {dates}"

    @allure.story("Фильтры")
    @allure.title("Получение фильмов с фильтром: {params}")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "filters")
    @pytest.mark.parametrize("params,expected_status", [
        ({"minPrice": 100, "maxPrice": 1000}, 200),
        ({"minPrice": 200}, 200),
        ({"maxPrice": 500}, 200),
        ({"locations": ["MSK", "SPB"]}, 200),
        ({"locations": ["MSK"]}, 200),
        ({"genreId": 1}, 200),
        ({"genreId": 5}, 200),
    ], ids=[
        "minPrice_and_maxPrice",
        "minPrice_only",
        "maxPrice_only",
        "locations_MSK_SPB",
        "location_MSK",
        "genreId_1",
        "genreId_5",
    ])
    def test_get_movies_with_filter(self, super_admin, params, expected_status):
        response = super_admin.api.movies_api.get_movies(params=params)
        assert response.status_code == expected_status, \
            f"expected {expected_status}, got {response.status_code}"
        if expected_status != 200:
            return

        movies_response = GetMoviesResponse(**response.json())
        movies = movies_response.movies
        for movie in movies:
            if "minPrice" in params:
                assert movie.price > params["minPrice"], \
                    f"price {movie.price} < minPrice {params['minPrice']}"

            if "maxPrice" in params:
                assert movie.price < params["maxPrice"], \
                    f"price {movie.price} > maxPrice {params['maxPrice']}"

            if "locations" in params:
                assert movie.location in params["locations"], \
                    f"location {movie.location} not in {params['locations']}"

            if "genreId" in params:
                assert movie.genreId == params["genreId"], \
                    f"genre id {movie.genreId} is not {params['genreId']}"

    @allure.story("Без параметров")
    @allure.title("Получение фильмов без параметров")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("api")
    def test_get_movies_without_parameters(self, super_admin):
        response = super_admin.api.movies_api.get_movies()
        assert response.status_code == 200, \
            f"expected 200, got {response.status_code}"
        GetMoviesResponse(**response.json())

    @allure.story("Валидация параметров")
    @allure.title("Получение фильмов с невалидным maxPrice")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("api", "negative")
    def test_get_movies_with_uncorrected_max_price_parameter(self, super_admin):
        response = super_admin.api.movies_api.get_movies(params={"maxPrice": self.NONEXISTENT_VALUE})
        assert response.status_code == 400, \
            f"expected 400, got {response.status_code}"

    @allure.story("Успешное создание")
    @allure.title("Создание фильма с корректными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api")
    def test_create_movie_with_correct_data(self, super_admin):
        payload = build_movie_payload()
        CreateMovieRequest(**payload)
        response = super_admin.api.movies_api.create_movie(movie_data=payload)
        assert response.status_code == 201, \
            f"expected 201, got {response.status_code}"

        created_movie = CreateMovieResponse(**response.json())

        actual = created_movie.model_dump(include=set(payload.keys()))
        assert actual == payload, f"expected {payload}, got {actual}"

        super_admin.api.movies_api.delete_movie(movie_id=created_movie.id)

    @allure.story("Валидация параметров")
    @allure.title("Создание фильма с несуществующим параметром")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api", "negative")
    def test_create_movie_with_nonexistent_parameter(self, super_admin):
        payload = build_movie_payload()
        payload["nonexistent_parameter"] = ""

        response = super_admin.api.movies_api.create_movie(movie_data=payload)
        assert response.status_code == 400, \
            f"expected 400, got {response.status_code}"

    @allure.story("Конфликт имен")
    @allure.title("Создание фильма с существующим названием")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api", "negative")
    def test_create_movie_with_taken_name(self, super_admin, created_movie):
        second_payload = build_movie_payload()
        second_payload["name"] = created_movie["name"]
        second_response = super_admin.api.movies_api.create_movie(movie_data=second_payload)
        assert second_response.status_code == 409, \
            f"expected 409, got {second_response.status_code}"

    @allure.story("Права доступа")
    @allure.title("Создание фильма под ролью USER")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api", "security", "negative")
    def test_create_movie_with_only_user_role(self, common_user):
        payload = build_movie_payload()

        response = common_user.api.movies_api.create_movie(movie_data=payload)
        assert response.status_code == 403, \
            f"expected 403, got {response.status_code}"

    @allure.story("Существующий фильм")
    @allure.title("Получение существующего фильма по id")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("api")
    def test_get_existent_movie_by_id(self, super_admin, created_movie):
        response = super_admin.api.movies_api.get_movie(movie_id=created_movie["id"])
        assert response.status_code == 200, \
            f"expected 200, got {response.status_code}"

        get_movie = GetMovieResponse(**response.json())

        assert get_movie.id == created_movie["id"], \
            f"expected {created_movie['id']}, got {get_movie.id}"


    @allure.story("Несуществующий фильм")
    @allure.title("Получение несуществующего фильма по id")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api", "negative")
    def test_get_nonexistent_movie_by_id(self, super_admin):
        response = super_admin.api.movies_api.get_movie(movie_id=self.NONEXISTENT_VALUE)
        assert response.status_code == 404, \
            f"expected 404, got {response.status_code}"

    @allure.story("Успешное удаление")
    @allure.title("Удаление существующего фильма с проверкой")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api")
    def test_delete_movie_with_correct_data(self, super_admin, created_movie):
        response = super_admin.api.movies_api.delete_movie(movie_id=created_movie["id"])
        assert response.status_code == 200, \
            f"expected 200, got {response.status_code}"

        get_response = super_admin.api.movies_api.get_movie(movie_id=created_movie["id"])
        assert get_response.status_code == 404, \
            f"expected 404, got {get_response.status_code}"

    @allure.story("Неуспешное удаление")
    @allure.title("Удаление фильма по несуществующему id")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("api", "negative")
    def test_delete_movie_with_nonexistent_id(self, super_admin):
        response = super_admin.api.movies_api.delete_movie(movie_id=self.NONEXISTENT_VALUE)
        assert response.status_code == 404, \
            f"expected 404, got {response.status_code}"

    @allure.story("Успешное обновление")
    @allure.title("Обновление фильма с корректными данными")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.tag("api")
    def test_update_movie_with_correct_data(self, super_admin, created_movie):
        created_movie_id = created_movie["id"]
        new_movie_data = build_movie_payload()
        UpdateMovieRequest(**new_movie_data)
        update_response = super_admin.api.movies_api.update_movie(
            movie_id=created_movie_id, movie_data=new_movie_data
        )
        assert update_response.status_code == 200, \
            f"UPDATE: expected 200, got {update_response.status_code}"

        get_response = super_admin.api.movies_api.get_movie(movie_id=created_movie_id)
        assert get_response.status_code == 200, \
            f"GET: expected 200, got {get_response.status_code}"

        get_movie = GetMovieResponse(**get_response.json())
        actual = get_movie.model_dump(include=set(new_movie_data.keys()))
        assert actual == new_movie_data, f"expected {new_movie_data}, got {actual}"

    @allure.story("Обновление несуществующего параметра")
    @allure.title("Обновление с несуществующим параметром")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("api", "negative")
    @pytest.mark.xfail(reason="not working")
    def test_update_movie_with_nonexistent_parameter(self, super_admin, created_movie):
        created_movie_id = created_movie["id"]
        new_movie_data = build_movie_payload()
        new_movie_data["nonexistent_parameter"] = ""
        response = super_admin.api.movies_api.update_movie(movie_id=created_movie_id, movie_data=new_movie_data)
        assert response.status_code == 400, \
            f"expected 400, got {response.status_code}"

    @allure.story("Обновление несуществующего фильма")
    @allure.title("Обновление фильма по несуществующему id")
    @allure.severity(allure.severity_level.MINOR)
    @allure.tag("api", "negative")
    def test_update_movie_with_nonexistent_id(self, super_admin):
        movie_data = build_movie_payload()
        response = super_admin.api.movies_api.update_movie(movie_id=self.NONEXISTENT_VALUE, movie_data=movie_data)
        assert response.status_code == 404, \
            f"expected 404, got {response.status_code}"