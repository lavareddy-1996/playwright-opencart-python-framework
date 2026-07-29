from playwright.sync_api import Page


class HomePage:
    """Page Object Model for the Home page."""

    def __init__(self, page: Page):
        self.page = page

        # Navigation
        self.lnk_my_account = page.locator('span:has-text("My Account")')
        self.lnk_register = page.locator('a:has-text("Register")')
        self.lnk_login = page.locator('a:has-text("Login")')

        # Search
        self.txt_search_box = page.locator('input[placeholder="Search"]')
        self.btn_search = page.locator('#search button[type="button"]')

    def get_home_page_title(self) -> str:
        """Return the Home page title."""
        return self.page.title()

    def click_my_account(self) -> None:
        """Click the My Account menu."""
        self.lnk_my_account.click()

    def click_register(self) -> None:
        """Click the Register link."""
        self.lnk_register.click()

    def click_login(self) -> None:
        """Click the Login link."""
        self.lnk_login.click()

    def enter_product_name(self, product_name: str) -> None:
        """Enter the product name into the search box."""
        self.txt_search_box.fill(product_name)

    def click_search(self) -> None:
        """Click the Search button."""
        self.btn_search.click()
