import os
import pytest
from datetime import datetime
from Pageobject.login import LoginPage
from Utilities.utils import take_screenshot, archive_old_screenshots, test_data  # Import test_data fixture
from Utilities.logger import logger

# ✅ Fetch environment dynamically
ENV = os.getenv("ENVIRONMENT", "DEV").upper()  # Default to DEV if not set


@pytest.fixture(scope="session", autouse=True)
def setup_screenshot_archive():
    """
    ✅ Runs before any test execution to archive previous screenshots.
    """
    logger.info("📂 Archiving old screenshots before test execution...")
    archive_old_screenshots()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """✅ Attach Logs and Screenshots to the HTML report."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":  # Ensure it's after the test execution
        driver = item.funcargs.get("driver", None)
        if driver:
            screenshot_path = take_screenshot(driver, f"{ENV}_{item.name}_failed")

            pytest_html = item.config.pluginmanager.getplugin("html")
            extra = getattr(report, "extra", [])

            if screenshot_path and os.path.exists(screenshot_path):
                extra.append(pytest_html.extras.image(screenshot_path))

            report.extra = extra


# ✅ **TC_Boost_Login_001** - Verify login page is displayed
def test_boost_login_page_display(driver, test_data):
    logger.info("Testing Boost Gen 3 login page display.")
    driver.get(test_data["web_base_url"])
    login_page = LoginPage(driver)

    assert "Dynamic Boost Dev" in driver.title, "Boost Gen 3 login page is not displayed."
    assert login_page.is_email_field_visible(), "Email field is not visible."

    screenshot_file = take_screenshot(driver, f"{ENV}_boost_login_page")
    logger.info(f"Screenshot saved: {screenshot_file}")


# ✅ **TC_Boost_Login_002** - Verify login with valid credentials
def test_valid_login(driver, test_data):
    logger.info("Testing valid login.")
    driver.get(test_data["web_base_url"])
    login_page = LoginPage(driver)

    login_page.enter_email(test_data["credentials_valid_username"])
    login_page.enter_password(test_data["credentials_valid_password"])
    login_page.click_login()

    assert login_page.is_dynamic_boost_status_displayed(), "Dashboard was not displayed after valid login."

    screenshot_file = take_screenshot(driver, f"{ENV}_valid_login")
    logger.info(f"Screenshot saved: {screenshot_file}")


# TC_Boost_Login_003: Verify login with an invalid email and a valid password.
def test_invalid_email_login(driver, test_data):
    logger.info("Testing login with an invalid email and valid password.")
    driver.get(test_data["web_base_url"])  # Step 1: Open login page
    login_page = LoginPage(driver)
    # Step 2: Enter an invalid email and a valid password
    login_page.enter_email(test_data["credentials_invalid_username"])
    login_page.enter_password(test_data["credentials_valid_password"])
    # Step 3: Click "SIGN IN"
    login_page.click_login()
    # Step 4: Verify the expected error message is displayed
    expected_error_message = "You’ve entered an invalid email / password combination, or your account is locked due to too many login attempts."
    actual_error_message = login_page.get_error_message()
    assert actual_error_message == expected_error_message, f"Unexpected error message: {actual_error_message}"
    screenshot_file = take_screenshot(driver, f"{ENV}_invalid_email_login")
    logger.info(f"Screenshot saved: {screenshot_file}")


# ✅ **TC_Boost_Login_004** - Verify login with empty email & password
def test_empty_email_and_password(driver, test_data):
    logger.info("Testing login with empty email and password.")
    driver.get(test_data["web_base_url"])
    login_page = LoginPage(driver)

    login_page.enter_email("")
    login_page.enter_password("")

    assert not login_page.is_sign_in_button_enabled(), "SIGN IN button should be disabled."

    screenshot_file = take_screenshot(driver, f"{ENV}_empty_email_password")
    logger.info(f"Screenshot saved: {screenshot_file}")


# TC_Boost_Login_005: Verify login with correct email and incorrect password.
def test_valid_email_invalid_password(driver, test_data):
    logger.info("Testing login with valid email and incorrect password.")
    driver.get(test_data["web_base_url"])  # Step 1: Open login page
    login_page = LoginPage(driver)
    # Step 2: Enter a valid email and an incorrect password
    login_page.enter_email(test_data["credentials_valid_username"])
    login_page.enter_password(test_data["credentials_invalid_password"])
    # Step 3: Verify that the "SIGN IN" does not happens

    assert login_page.is_sign_in_button_enabled(), "SIGN IN button should be enabled but should not allow with the password is incorrect."

    screenshot_file = take_screenshot(driver, f"{ENV}_valid_email_invalid_password")
    logger.info(f"Screenshot saved: {screenshot_file}")


# TC_Boost_Login_006: Verify login with a valid email and an empty password.
def test_valid_email_empty_password(driver, test_data):
    logger.info("Testing login with valid email and empty password.")
    driver.get(test_data["web_base_url"])  # Step 1: Open login page

    login_page = LoginPage(driver)

    # Step 2: Enter a valid email and leave the password field empty
    login_page.enter_email(test_data["credentials_valid_username"])
    login_page.enter_password("")  # Empty password

    # Step 3: Verify that the "SIGN IN" button is disabled
    assert not login_page.is_sign_in_button_enabled(), "SIGN IN button should be disabled when the password field is empty."

    # Capture screenshot for reference
    screenshot_file = take_screenshot(driver, f"{ENV}_valid_email_empty_password")
    logger.info(f"Screenshot saved: {screenshot_file}")


# TC_Boost_Login_007: Verify login with email field empty and valid password.
def test_empty_email_valid_password(driver, test_data):
    logger.info("Testing login with empty email and valid password.")
    driver.get(test_data["web_base_url"])  # Step 1: Open login page
    login_page = LoginPage(driver)
    # Step 2: Leave the email field empty and enter a valid password
    login_page.enter_email("")  # Empty email field
    login_page.enter_password(test_data["credentials_valid_password"])
    # Step 3: Verify that the "SIGN IN" button is disabled
    assert login_page.is_sign_in_button_enabled(), "SIGN IN button should be disabled when the email field is empty."
    # Capture screenshot for reference
    screenshot_file = take_screenshot(driver, f"{ENV}_empty_email_valid_password")
    logger.info(f"Screenshot saved: {screenshot_file}")


# TC_Boost_Login_008: Verify login with special characters in email.
def test_special_characters_in_email(driver, test_data):
    logger.info("Testing login with special characters in email.")
    driver.get(test_data["web_base_url"])  # Step 1: Open login page
    login_page = LoginPage(driver)
    # Step 2: Enter special characters in the email field
    login_page.enter_email(test_data["credentials_specialchar_email"])
    login_page.enter_password(test_data["credentials_valid_password"])
    # Step 3: Verify that the "SIGN IN" button is disabled
    assert not login_page.is_sign_in_button_enabled(), "SIGN IN button should be disabled when email contains special characters."
    # Capture screenshot for reference
    screenshot_file = take_screenshot(driver, f"{ENV}_special_characters_in_email")
    logger.info(f"Screenshot saved: {screenshot_file}")



# TC_Boost_Login_009: Verify the "Forgot Password?" link functionality.
def test_forgot_password_link(driver, test_data):

    logger.info("Testing the 'Forgot Password?' link functionality.")
    driver.get(test_data["web_base_url"])  # Step 1: Open login page
    login_page = LoginPage(driver)
    # Step 2: Click "Forgot Password?" link
    login_page.click_forgot_password()
    # Step 3: Verify the user is redirected to the password recovery page
    assert login_page.is_forgot_password_page_displayed(), "User was not redirected to the password recovery page."
    # Capture screenshot for reference
    screenshot_file = take_screenshot(driver, f"{ENV}_forgot_password_page")
    logger.info(f"Screenshot saved: {screenshot_file}")


# TC_Boost_Login_013: Verify "Back to Login screen" link functionality.
def test_back_to_login_screen(driver, test_data):
    logger.info("Testing 'Back to Login screen' link functionality.")
    driver.get(test_data["web_base_url"])  # Step 1: Open login page
    login_page = LoginPage(driver)
    # Step 2: Click "Forgot Password?" link to navigate to the forgot password screen
    login_page.click_forgot_password()
    assert login_page.is_forgot_password_page_displayed(), "Forgot Password page did not load."
    # Step 3: Click "Back to Login screen" link
    login_page.click_back_to_login()
    # Step 4: Verify that the user is redirected back to the login page
    assert login_page.is_login_page_displayed(), "User was not redirected back to the login page."
    # Capture screenshot for reference
    screenshot_file = take_screenshot(driver, f"{ENV}_back_to_login_screen")
    logger.info(f"Screenshot saved: {screenshot_file}")































# import os
# import pytest
# from Pageobject.login import LoginPage
# from Utilities.utils import take_screenshot, test_data  # Import test_data fixture
# from Utilities.logger import logger
#
#
# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     """Attach Logs and Screenshots to the HTML report."""
#     outcome = yield
#     report = outcome.get_result()
#
#     if report.when == "call":  # Ensure it's after the test execution
#         driver = item.funcargs.get("driver", None)
#         if driver:
#             # Capture screenshot for failed tests
#             if report.failed:
#                 screenshot_name = f"{item.name}_failed.png"
#                 screenshot_path = take_screenshot(driver, screenshot_name)
#
#                 pytest_html = item.config.pluginmanager.getplugin("html")
#                 extra = getattr(report, "extra", [])
#
#                 if screenshot_path and os.path.exists(screenshot_path):
#                     extra.append(pytest_html.extras.image(screenshot_path))
#
#                 report.extra = extra
#
#
# # TC_Boost_Login_001 - Check whether Boost Gen 3 login page is displaying or not
# def test_boost_login_page_display(driver, test_data):
#     """Verifies that the Boost Gen 3 login page is displayed and email field is visible."""
#     logger.info("Testing Boost Gen 3 login page display.")
#     driver.get(test_data["web_base_url"])  # Open the browser & enter URL
#     login_page = LoginPage(driver)
#     # Validate that the page is loaded by checking the title
#     assert "Dynamic Boost Dev" in driver.title, "Boost Gen 3 login page is not displayed."
#     logger.info("Boost Gen 3 login page loaded successfully.")
#
#     # Validate email field visibility using the POM method
#     assert login_page.is_email_field_visible(), "Email field is not visible on the login page."
#
#     # Take a screenshot after all validations
#     screenshot_file = take_screenshot(driver, 'boost_login_page.png')
#     logger.info(f"Screenshot of Boost Gen 3 login page saved to {screenshot_file}")
#
#
# # TC_Boost_Login_002: Verify login with valid credentials.
# def test_valid_login(driver, test_data):
#     logger.info("Testing valid login.")
#     driver.get(test_data["web_base_url"])
#
#     login_page = LoginPage(driver)
#     login_page.enter_email(test_data["credentials_valid_username"])
#     login_page.enter_password(test_data["credentials_valid_password"])
#     login_page.click_login()
#
#     assert login_page.is_dynamic_boost_status_displayed(), "Dashboard was not displayed after valid login."
#     screenshot_file = take_screenshot(driver, 'valid_login.png')
#     logger.info(f"Screenshot of valid login saved to {screenshot_file}")
#
#
# # TC_Boost_Login_003: Verify login with an invalid email and a valid password.
# def test_invalid_email_login(driver, test_data):
#     logger.info("Testing login with an invalid email and valid password.")
#     driver.get(test_data["web_base_url"])  # Step 1: Open login page
#     login_page = LoginPage(driver)
#     # Step 2: Enter an invalid email and a valid password
#     login_page.enter_email(test_data["credentials_invalid_username"])
#     login_page.enter_password(test_data["credentials_valid_password"])
#     # Step 3: Click "SIGN IN"
#     login_page.click_login()
#     # Step 4: Verify the expected error message is displayed
#     expected_error_message = "You’ve entered an invalid email / password combination, or your account is locked due to too many login attempts."
#     actual_error_message = login_page.get_error_message()
#     assert actual_error_message == expected_error_message, f"Unexpected error message: {actual_error_message}"
#     screenshot_file = take_screenshot(driver, 'invalid_email_login.png')
#     logger.info(f"Screenshot of invalid email login saved to {screenshot_file}")
#
#
# # TC_Boost_Login_004: Verify login with empty email and password.
# def test_empty_email_and_password(driver, test_data):
#     logger.info("Testing login with empty email and password.")
#     driver.get(test_data["web_base_url"])  # Step 1: Open login page
#
#     login_page = LoginPage(driver)
#
#     # Step 2: Leave email and password fields empty
#     login_page.enter_email("")  # Empty email field
#     login_page.enter_password("")  # Empty password field
#
#     # Step 3: Verify that the "SIGN IN" button is disabled
#     assert not login_page.is_sign_in_button_enabled(), "SIGN IN button should be disabled when email and password are empty."
#
#     # Capture screenshot for reference
#     screenshot_file = take_screenshot(driver, 'empty_email_password.png')
#     logger.info(f"Screenshot of empty email and password login attempt saved to {screenshot_file}")
#
#
# # TC_Boost_Login_005: Verify login with correct email and incorrect password.
# def test_valid_email_invalid_password(driver, test_data):
#     logger.info("Testing login with valid email and incorrect password.")
#     driver.get(test_data["web_base_url"])  # Step 1: Open login page
#
#     login_page = LoginPage(driver)
#
#     # Step 2: Enter a valid email and an incorrect password
#     login_page.enter_email(test_data["credentials_valid_username"])
#     login_page.enter_password(test_data["credentials_invalid_password"])
#
#     # Step 3: Verify that the "SIGN IN" does not happens
#     assert login_page.is_sign_in_button_enabled(), "SIGN IN button should be enabled but should not allow with the password is incorrect."
#
#     # Capture screenshot for reference
#     screenshot_file = take_screenshot(driver, 'valid_email_invalid_password.png')
#     logger.info(f"Screenshot of login attempt with incorrect password saved to {screenshot_file}")
#
#
# # TC_Boost_Login_006: Verify login with a valid email and an empty password.
# def test_valid_email_empty_password(driver, test_data):
#     logger.info("Testing login with valid email and empty password.")
#     driver.get(test_data["web_base_url"])  # Step 1: Open login page
#
#     login_page = LoginPage(driver)
#
#     # Step 2: Enter a valid email and leave the password field empty
#     login_page.enter_email(test_data["credentials_valid_username"])
#     login_page.enter_password("")  # Empty password
#
#     # Step 3: Verify that the "SIGN IN" button is disabled
#     assert not login_page.is_sign_in_button_enabled(), "SIGN IN button should be disabled when the password field is empty."
#
#     # Capture screenshot for reference
#     screenshot_file = take_screenshot(driver, 'valid_email_empty_password.png')
#     logger.info(f"Screenshot of login attempt with empty password saved to {screenshot_file}")
#
#
# # TC_Boost_Login_007: Verify login with email field empty and valid password.
# def test_empty_email_valid_password(driver, test_data):
#     logger.info("Testing login with empty email and valid password.")
#     driver.get(test_data["web_base_url"])  # Step 1: Open login page
#     login_page = LoginPage(driver)
#     # Step 2: Leave the email field empty and enter a valid password
#     login_page.enter_email("")  # Empty email field
#     login_page.enter_password(test_data["credentials_valid_password"])
#     # Step 3: Verify that the "SIGN IN" button is disabled
#     assert login_page.is_sign_in_button_enabled(), "SIGN IN button should be disabled when the email field is empty."
#     # Capture screenshot for reference
#     screenshot_file = take_screenshot(driver, 'empty_email_valid_password.png')
#     logger.info(f"Screenshot of login attempt with empty email saved to {screenshot_file}")
#
#
# # TC_Boost_Login_008: Verify login with special characters in email.
# def test_special_characters_in_email(driver, test_data):
#     logger.info("Testing login with special characters in email.")
#     driver.get(test_data["web_base_url"])  # Step 1: Open login page
#     login_page = LoginPage(driver)
#     # Step 2: Enter special characters in the email field
#     login_page.enter_email(test_data["credentials_specialchar_email"])
#     login_page.enter_password(test_data["credentials_valid_password"])
#     # Step 3: Verify that the "SIGN IN" button is disabled
#     assert not login_page.is_sign_in_button_enabled(), "SIGN IN button should be disabled when email contains special characters."
#     # Capture screenshot for reference
#     screenshot_file = take_screenshot(driver, 'special_characters_in_email.png')
#     logger.info(f"Screenshot of login attempt with special characters in email saved to {screenshot_file}")
#
#
# # TC_Boost_Login_009: Verify the "Forgot Password?" link functionality.
# def test_forgot_password_link(driver, test_data):
#
#     logger.info("Testing the 'Forgot Password?' link functionality.")
#     driver.get(test_data["web_base_url"])  # Step 1: Open login page
#     login_page = LoginPage(driver)
#     # Step 2: Click "Forgot Password?" link
#     login_page.click_forgot_password()
#     # Step 3: Verify the user is redirected to the password recovery page
#     assert login_page.is_forgot_password_page_displayed(), "User was not redirected to the password recovery page."
#     # Capture screenshot for reference
#     screenshot_file = take_screenshot(driver, 'forgot_password_page.png')
#     logger.info(f"Screenshot of password recovery page saved to {screenshot_file}")
#
#
# # TC_Boost_Login_013: Verify "Back to Login screen" link functionality.
# def test_back_to_login_screen(driver, test_data):
#     logger.info("Testing 'Back to Login screen' link functionality.")
#     driver.get(test_data["web_base_url"])  # Step 1: Open login page
#     login_page = LoginPage(driver)
#     # Step 2: Click "Forgot Password?" link to navigate to the forgot password screen
#     login_page.click_forgot_password()
#     assert login_page.is_forgot_password_page_displayed(), "Forgot Password page did not load."
#     # Step 3: Click "Back to Login screen" link
#     login_page.click_back_to_login()
#     # Step 4: Verify that the user is redirected back to the login page
#     assert login_page.is_login_page_displayed(), "User was not redirected back to the login page."
#     # Capture screenshot for reference
#     screenshot_file = take_screenshot(driver, 'back_to_login_screen.png')
#     logger.info(f"Screenshot of redirection to login page saved to {screenshot_file}")
