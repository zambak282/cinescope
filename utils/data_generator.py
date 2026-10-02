from faker import Faker

fake = Faker()


def generate_random_name() -> str:
    return fake.first_name()+fake.last_name()


def generate_random_email() -> str:
    return fake.email()


def generate_random_password() -> str:
    return fake.password()