from playwright.sync_api import Locator, Page


class RegistrationPage:
    """Page Object Model for the Registration page."""

    def __init__(self, page: Page):
        self.page = page

        # ===== Registration Form =====
        self.txt_first_name = page.locator("#input-firstname")
        self.txt_last_name = page.locator("#input-lastname")
        self.txt_email = page.locator("#input-email")
        self.txt_telephone = page.locator("#input-telephone")
        self.txt_password = page.locator("#input-password")
        self.txt_confirm_password = page.locator("#input-confirm")

        # ===== Controls =====
        self.chk_privacy_policy = page.locator("input[name='agree']")
        self.btn_continue = page.locator("input[value='Continue']")

        # ===== Success Message =====
        self.lbl_registration_success = page.locator(
            "h1:has-text('Your Account Has Been Created!')"
        )

        # ===== Validation Messages =====
        self.lbl_first_name_validation = page.locator(
            "text='First Name must be between 1 and 32 characters!'"
        )

        self.lbl_last_name_validation = page.locator(
            "text='Last Name must be between 1 and 32 characters!'"
        )

        self.lbl_email_validation = page.locator(
            "text='E-Mail Address does not appear to be valid!'"
        )

        self.lbl_telephone_validation = page.locator(
            "text='Telephone must be between 3 and 32 characters!'"
        )

        self.lbl_password_validation = page.locator(
            "text='Password must be between 4 and 20 characters!'"
        )

        self.lbl_privacy_policy_validation = page.locator(
            ".alert.alert-danger.alert-dismissible"
        )

    # ==========================================================
    # Registration Actions
    # ==========================================================

    def set_first_name(self, first_name: str) -> None:
        """Enter the first name."""
        self.txt_first_name.fill(first_name)

    def set_last_name(self, last_name: str) -> None:
        """Enter the last name."""
        self.txt_last_name.fill(last_name)

    def set_email(self, email: str) -> None:
        """Enter the email address."""
        self.txt_email.fill(email)

    def set_telephone(self, telephone: str) -> None:
        """Enter the telephone number."""
        self.txt_telephone.fill(telephone)

    def set_password(self, password: str) -> None:
        """Enter the password."""
        self.txt_password.fill(password)

    def set_confirm_password(self, password: str) -> None:
        """Enter the confirm password."""
        self.txt_confirm_password.fill(password)

    def accept_privacy_policy(self) -> None:
        """Accept the Privacy Policy."""
        self.chk_privacy_policy.check()

    def submit_registration(self) -> None:
        """Submit the registration form."""
        self.btn_continue.click()

    # ==========================================================
    # Business Workflow
    # ==========================================================

    def complete_registration(
        self,
        first_name: str,
        last_name: str,
        email: str,
        telephone: str,
        password: str,
    ) -> None:
        """
        Complete the registration workflow.

        This method is intended for successful registration scenarios.
        """

        self.set_first_name(first_name)
        self.set_last_name(last_name)
        self.set_email(email)
        self.set_telephone(telephone)
        self.set_password(password)
        self.set_confirm_password(password)
        self.accept_privacy_policy()
        self.submit_registration()

    # ==========================================================
    # Getter Methods
    # ==========================================================

    def get_registration_success_message(self) -> Locator:
        """Return the registration success message locator."""
        return self.lbl_registration_success

    def get_first_name_validation_message(self) -> Locator:
        """Return the First Name validation message locator."""
        return self.lbl_first_name_validation

    def get_last_name_validation_message(self) -> Locator:
        """Return the Last Name validation message locator."""
        return self.lbl_last_name_validation

    def get_email_validation_message(self) -> Locator:
        """Return the Email validation message locator."""
        return self.lbl_email_validation

    def get_telephone_validation_message(self) -> Locator:
        """Return the Telephone validation message locator."""
        return self.lbl_telephone_validation

    def get_password_validation_message(self) -> Locator:
        """Return the Password validation message locator."""
        return self.lbl_password_validation

    def get_privacy_policy_validation_message(self) -> Locator:
        """Return the Privacy Policy validation message locator."""
        return self.lbl_privacy_policy_validation
