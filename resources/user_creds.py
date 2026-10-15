import os

from dotenv import load_dotenv

load_dotenv()

class SuperAdminCreds:
    EMAIL = os.getenv("SUPER_ADMIN_EMAIL")
    PASSWORD = os.getenv("SUPER_ADMIN_PASSWORD")

    if not EMAIL or not PASSWORD:
        raise RuntimeError(
            "SUPER_ADMIN_EMAIL, SUPER_ADMIN_PASSWORD must be set in .env file"
        )