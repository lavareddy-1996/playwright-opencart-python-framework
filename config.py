import os


class Config:
    BASE_URL = os.getenv(
        "BASE_URL",
        "https://tutorialsninja.com/demo/"
    )

    USERNAME = os.getenv(
        "TEST_USERNAME"
    )

    PASSWORD = os.getenv(
        "TEST_PASSWORD"
    )