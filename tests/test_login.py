import os


def test_login(home_page, login_page):

    username = os.getenv(
        "TEST_USERNAME"
    )

    password = os.getenv(
        "TEST_PASSWORD"
    )

    home_page.click_my_account()

    home_page.click_login()

    login_page.login(
        username,
        password
    )