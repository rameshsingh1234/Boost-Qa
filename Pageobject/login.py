from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from Utilities.logger import logger  # Import centralized logger


class LoginPage:
    """Page Object Model for the Login Page with Generic Waits."""

    def __init__(self, driver, implicit_wait=15, explicit_wait=15):
        """
        Initialize LoginPage with WebDriver.
        :param driver: WebDriver instance
        :param implicit_wait: Default implicit wait time
        :param explicit_wait: Default explicit wait time
        """
        self.driver = driver
        self.driver.implicitly_wait(implicit_wait)  # Set implicit wait globally
        self.wait = WebDriverWait(driver, explicit_wait)  # Set explicit wait

        # Locators
        self.email_field = (By.ID, "email")
        self.password_field = (By.ID, "password")
        self.submit_button = (By.XPATH, '//*[@id="root"]/div/div/form/button[2]')
        self.error_message = (By.XPATH, "//*[@id='root']/div/div[1]/div/div[1]")

    def wait_for_element(self, locator, condition=EC.presence_of_element_located, timeout=15):
        """Generic method to wait for an element with a given condition."""
        try:
            return WebDriverWait(self.driver, timeout).until(condition(locator))
        except TimeoutException:
            logger.error(f"Element {locator} was not found within {timeout} seconds.")
            return None

    def enter_email(self, username):
        """Enters the email in the login field."""
        logger.info(f"Entering email: {username}")
        email_element = self.wait_for_element(self.email_field, EC.presence_of_element_located)
        if email_element:
            email_element.clear()
            email_element.send_keys(username)
        else:
            raise TimeoutException("Email field not found on the login page.")

    def enter_password(self, password):
        """Enters the password in the login field."""
        logger.info("Entering password.")
        password_element = self.wait_for_element(self.password_field, EC.presence_of_element_located)
        if password_element:
            password_element.clear()
            password_element.send_keys(password)
        else:
            raise TimeoutException("Password field not found on the login page.")

    def click_login(self):
        """Clicks the login button."""
        logger.info("Clicking the login button.")
        login_button = self.wait_for_element(self.submit_button, EC.element_to_be_clickable)
        if login_button:
            login_button.click()
        else:
            raise TimeoutException("Login button is not clickable.")

    def is_email_field_visible(self):
        """Checks if the email field is visible on the login page."""
        logger.info("Checking if email field is visible.")
        try:
            email_element = self.wait_for_element(self.email_field, EC.visibility_of_element_located)
            if email_element and email_element.is_displayed():
                logger.info("Email field is visible on the login page.")
                return True
            else:
                logger.warning("Email field is not visible on the login page.")
                return False
        except (TimeoutException, NoSuchElementException):
            logger.error("Email field is not present on the login page.")
            return False

    def is_dynamic_boost_status_displayed(self):
        """Checks if the dashboard page is displayed after login."""
        logger.info("Checking if the user is redirected to the dashboard.")

        dashboard_locator = (
        By.XPATH, "//*[@id='root']/section/header/div[1]/h1")  # Update with correct dashboard element

        try:
            dashboard_element = self.wait_for_element(dashboard_locator, EC.presence_of_element_located, timeout=10)
            if dashboard_element and dashboard_element.is_displayed():
                logger.info("User is successfully redirected to the dashboard.")
                return True
            else:
                logger.warning("Dashboard is not displayed after login.")
                return False
        except (TimeoutException, NoSuchElementException):
            logger.error("Dashboard page did not load after login.")
            return False

    def get_error_message(self):
        """Returns the error message text if present."""
        error_locator = (By.XPATH, "//*[@id='root']/div/div[1]/div/div[1]")  # Update if needed

        logger.info("Checking for error message after login attempt.")

        error_element = self.wait_for_element(error_locator, EC.presence_of_element_located, timeout=10)
        if error_element:
            error_message = error_element.text.strip()
            logger.warning(f"Login failed. Error message: {error_message}")
            return error_message
        else:
            logger.info("No error message found.")
            return None

    def is_sign_in_button_enabled(self):
        """Checks if the 'SIGN IN' button is enabled."""
        logger.info("Checking if the 'SIGN IN' button is enabled.")

        try:
            sign_in_button = self.wait_for_element(self.submit_button, EC.presence_of_element_located, timeout=5)
            if sign_in_button and sign_in_button.is_enabled():
                logger.warning("SIGN IN button is enabled, but it should be disabled.")
                return True
            else:
                logger.info("SIGN IN button is correctly disabled.")
                return False
        except (TimeoutException, NoSuchElementException):
            logger.error("SIGN IN button not found on the login page.")
            return False

    def click_forgot_password(self):
        """Clicks the 'Forgot Password?' link."""
        logger.info("Clicking the 'Forgot Password?' link.")
        forgot_password_locator = (By.XPATH, "//*[@id='root']/div/div/form/button[1]")  # Update if needed

        try:
            forgot_password_link = self.wait_for_element(forgot_password_locator, EC.element_to_be_clickable, timeout=5)
            if forgot_password_link:
                forgot_password_link.click()
                logger.info("'Forgot Password?' link clicked successfully.")
            else:
                logger.warning("'Forgot Password?' link not found.")
        except TimeoutException:
            logger.error("'Forgot Password?' link was not clickable.")
            raise

    def is_forgot_password_page_displayed(self):
        """Verifies that the user is redirected to the password recovery page."""
        logger.info("Verifying password recovery page redirection.")
        forgot_password_header_locator = (By.XPATH, "//*[@id='root']/div/div/form/h2")  # Update if needed

        try:
            header_element = self.wait_for_element(forgot_password_header_locator, EC.presence_of_element_located,
                                                   timeout=10)
            if header_element and header_element.is_displayed():
                logger.info("User is successfully redirected to the password recovery page.")
                return True
            else:
                logger.warning("Password recovery page is not displayed.")
                return False
        except (TimeoutException, NoSuchElementException):
            logger.error("Password recovery page did not load.")
            return False

    def click_back_to_login(self):
        """Clicks the 'Back to Login screen' link."""
        logger.info("Clicking the 'Back to Login screen' link.")
        back_to_login_locator = (By.XPATH, "//*[@id='root']/div/div/form/button[1]")  # Update if needed

        try:
            back_to_login_link = self.wait_for_element(back_to_login_locator, EC.element_to_be_clickable, timeout=5)
            if back_to_login_link:
                back_to_login_link.click()
                logger.info("'Back to Login screen' link clicked successfully.")
            else:
                logger.warning("'Back to Login screen' link not found.")
        except TimeoutException:
            logger.error("'Back to Login screen' link was not clickable.")
            raise

    def is_login_page_displayed(self):
        """Verifies that the user is redirected back to the login page."""
        logger.info("Verifying redirection back to the login page.")
        login_page_header_locator = (
        By.XPATH, "//*[@id='root']/div/div/form/h2")  # Update with the correct login page header element

        try:
            header_element = self.wait_for_element(login_page_header_locator, EC.presence_of_element_located,
                                                   timeout=10)
            if header_element and header_element.is_displayed():
                logger.info("User is successfully redirected back to the login page.")
                return True
            else:
                logger.warning("Login page is not displayed.")
                return False
        except (TimeoutException, NoSuchElementException):
            logger.error("Login page did not load.")
            return False






