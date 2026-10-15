from constants.roles import Roles
from models.auth import RegisterUserRequest
from utils.data_generator import DataGenerator


def build_register_user_payload(**overrides) -> dict:
    password = overrides.pop("password", DataGenerator.generate_random_password())
    payload = {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": password,
        "passwordRepeat": password,
        "roles": [Roles.USER.value],
    }
    payload.update(overrides)

    RegisterUserRequest(**payload)   # валидация

    return payload