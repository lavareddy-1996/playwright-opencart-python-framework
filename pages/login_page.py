from playwright.sync_api import Page
from pages.my_account_page import MyAccountPage


class LoginPage:
    """Page Object Model for the Login page."""

    def __init__(self, page: Page):
        self.page = page

        # Locators
        self.txt_email_address = page.locator("#input-email")
        self.txt_password = page.locator("#input-password")
        self.btn_login = page.locator('input[value="Login"]')
        self.lbl_login_error = page.locator(".alert.alert-danger.alert-dismissible")

    def set_email(self, email: str) -> None:
        """Enter the email address."""
        self.txt_email_address.fill(email)

    def set_password(self, password: str) -> None:
        """Enter the password."""
        self.txt_password.fill(password)

    def click_login(self) -> None:
        """Click the Login button."""
        self.btn_login.click()

    def login(self, email: str, password: str) -> MyAccountPage:
        """
        Perform a complete login.

        Returns:
            MyAccountPage: Page object after successful login.
        """
        self.set_email(email)
        self.set_password(password)
        self.click_login()
        return MyAccountPage(self.page)

    def get_login_error_message(self):
        """Return the login error message locator."""
        return self.lbl_login_error
