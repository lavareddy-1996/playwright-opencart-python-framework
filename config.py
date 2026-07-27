import os


class Config:
    """
    Test data / credentials.

    Credentials are read from environment variables so nothing sensitive is
    hard-coded into source that gets pushed to GitHub. Set them in a local
    `.env` file (see `.env.example`) or export them in your shell/CI before
    running the suite. Defaults below are placeholders for this demo store
    and should be overridden per-environment.
    """

    email = os.getenv("OC_TEST_EMAIL", "test.user@example.com")
    password = os.getenv("OC_TEST_PASSWORD", "ChangeMe123!")

    invalid_email = os.getenv("OC_TEST_INVALID_EMAIL", "not.a.real.user@example.com")
    invalid_password = os.getenv("OC_TEST_INVALID_PASSWORD", "WrongPass123!")

    product_name = "MacBook"
    product_quantity = "1"
    total_price = "$602.00"
