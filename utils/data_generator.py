from faker import Faker

fake = Faker()


def generate_random_name() -> str:
    return fake.first_name() + fake.last_name()


def generate_random_email() -> str:
    return fake.email()


def generate_random_password() -> str:
    return fake.password()


def generate_random_movie_name() -> str:
    return fake.sentence(nb_words=3).rstrip(".")


def generate_random_movie_description(max_chars: int = 200) -> str:
    return fake.text(max_nb_chars=max_chars)


def generate_random_movie_price(min_price: int = 100, max_price: int = 1000) -> int:
    return fake.random_int(min_price, max_price)