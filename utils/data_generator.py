import datetime
import random
import string

from faker import Faker

from constants.roles import Roles
from db_models.movie import LocationEnum

fake = Faker()


class DataGenerator:
    @staticmethod
    def generate_random_name() -> str:
        return fake.first_name() + fake.last_name()

    @staticmethod
    def generate_random_email() -> str:
        return f"1{fake.email()}"

    @staticmethod
    def generate_random_password(length: int = 12) -> str:
        if not 10 <= length <= 20:
            raise ValueError("length must be between 10 and 20")

        letters = string.ascii_letters
        digits = string.digits

        password = [
            random.choice(letters),
            random.choice(digits),
        ]

        all_chars = letters + digits
        password.extend(random.choice(all_chars) for _ in range(length - 2))

        random.shuffle(password)

        return "".join(password)

    @staticmethod
    def generate_random_movie_name() -> str:
        return fake.sentence(nb_words=3).rstrip(".")

    @staticmethod
    def generate_random_movie_description(max_chars: int = 200) -> str:
        return fake.text(max_nb_chars=max_chars)

    @staticmethod
    def generate_random_movie_price(min_price: int = 100, max_price: int = 1000) -> int:
        return fake.random_int(min_price, max_price)

    @staticmethod
    def generate_random_location() -> str:
        return fake.random_element([LocationEnum.SPB, LocationEnum.MSK])

    @staticmethod
    def generate_user_data() -> dict:
        from uuid import uuid4

        return {
            'id': f'{uuid4()}',
            'email': DataGenerator.generate_random_email(),
            'full_name': DataGenerator.generate_random_name(),
            'password': DataGenerator.generate_random_password(),
            'created_at': datetime.datetime.now(),
            'updated_at': datetime.datetime.now(),
            'verified': True,
            'banned': False,
            'roles': [Roles.USER]
        }

    @staticmethod
    def generate_movie_data() -> dict:
        return {
            'id': 1,
            'name': DataGenerator.generate_random_movie_name(),
            'image_url': "https://image.url",
            'price': DataGenerator.generate_random_movie_price(),
            'description': DataGenerator.generate_random_movie_description(),
            'location': DataGenerator.generate_random_location(),
            'published': True,
            'genre_id': 5,
            'rating': random.randint(1, 5),
            'created_at': datetime.datetime.now(),
        }

    @staticmethod
    def generate_review_text(max_chars: int = 150) -> str:
        return fake.text(max_nb_chars=max_chars).replace('\n', ' ')