import os
from selenium.webdriver.support import expected_conditions as EC


import pytest
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from Pageobject.login import LoginPage
from Pageobject.dashboard import DashboardPage
from Utilities.utils import take_screenshot, archive_old_screenshots, test_data
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


# ✅ **Generic Login Fixture**
@pytest.fixture(scope="function")
def login_and_navigate_to_dashboard(driver, test_data):
    """
    ✅ Logs in with valid credentials and navigates to the Dashboard page.
    Returns the DashboardPage instance.
    """
    logger.info("🔐 Logging into the application and navigating to the Dashboard.")
    driver.get(test_data["web_base_url"])

    login_page = LoginPage(driver)
    login_page.enter_email(test_data["credentials_valid_username"])
    login_page.enter_password(test_data["credentials_valid_password"])
    login_page.click_login()

    dashboard_page = DashboardPage(driver)
    assert dashboard_page.is_dynamic_boost_status_heading_visible(), "Dashboard did not load properly."

    return dashboard_page


# ✅ **TC_Dashboard_001** - Verify "Dynamic Boost Status" heading is visible
def test_dynamic_boost_status_heading(login_and_navigate_to_dashboard, driver):
    logger.info("📌 Verifying Dynamic Boost Status heading visibility.")
    dashboard_page = login_and_navigate_to_dashboard
    assert dashboard_page.is_dynamic_boost_status_heading_visible(), "Dynamic Boost Status heading is not visible."
    take_screenshot(driver, f"{ENV}_dashboard_status_heading")


# ✅ **TC_Dashboard_002** - Verify "Last Updated Timestamp" is visible
def test_last_updated_timestamp(login_and_navigate_to_dashboard, driver):
    logger.info("📌 Verifying Last Updated Timestamp visibility.")
    dashboard_page = login_and_navigate_to_dashboard
    assert dashboard_page.is_last_updated_timestamp_visible(), "Last Updated timestamp is not visible."
    take_screenshot(driver, f"{ENV}_dashboard_last_updated")


# ✅ TC_Boost_Login_003: Verify login with an invalid email and a valid password.
def test_invalid_email_login(driver, test_data):
    logger.info("Testing login with an invalid email and valid password.")
    driver.get(test_data["web_base_url"])  # Step 1: Open login page

    login_page = LoginPage(driver)

    # Step 2: Enter an invalid email and a valid password
    login_page.enter_email(test_data["credentials_invalid_username"])
    login_page.enter_password(test_data["credentials_valid_password"])

    # Step 3: Click "SIGN IN"
    login_page.click_login()

    # ✅ Step 4: Explicitly wait for the error message
    error_locator = (By.XPATH, "//*[@id='root']/div/div[1]/div/div[1]")  # Update if needed
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(error_locator))
    except:
        logger.error("Error message did not appear within the wait time in headless mode.")
        assert False, "Error message not displayed in headless mode."

    # ✅ Step 5: Verify the expected error message is displayed
    expected_error_message = "You’ve entered an invalid email / password combination, or your account is locked due to too many login attempts."
    actual_error_message = login_page.get_error_message()

    assert actual_error_message == expected_error_message, f"Unexpected error message: {actual_error_message}"

    # ✅ Step 6: Capture screenshot for debugging
    screenshot_file = take_screenshot(driver, f"{ENV}_invalid_email_login")
    logger.info(f"Screenshot saved: {screenshot_file}")

# ✅ **TC_Dashboard_004** - Verify "Profile Icon" is visible
def test_profile_icon(login_and_navigate_to_dashboard, driver):
    logger.info("📌 Verifying Profile Icon visibility.")
    dashboard_page = login_and_navigate_to_dashboard
    assert dashboard_page.is_profile_icon_visible(), "Profile icon is not visible."
    take_screenshot(driver, f"{ENV}_dashboard_profile_icon")


# ✅ **TC_Dashboard_005** - Verify "Status Menu" is visible & clickable
def test_status_menu(login_and_navigate_to_dashboard, driver):
    logger.info("📌 Verifying Status Menu visibility and clickability.")
    dashboard_page = login_and_navigate_to_dashboard
    assert dashboard_page.is_status_menu_visible_and_clickable(), "Status menu is not visible or clickable."
    take_screenshot(driver, f"{ENV}_dashboard_status_menu")


# ✅ **TC_Dashboard_006** - Verify "Sources Menu" is visible & clickable
def test_sources_menu(login_and_navigate_to_dashboard, driver):
    logger.info("📌 Verifying Sources Menu visibility and clickability.")
    dashboard_page = login_and_navigate_to_dashboard
    assert dashboard_page.is_sources_menu_visible_and_clickable(), "Sources menu is not visible or clickable."
    take_screenshot(driver, f"{ENV}_dashboard_sources_menu")


# ✅ **TC_Dashboard_007** - Verify "Payments Menu" is visible & clickable
def test_payments_menu(login_and_navigate_to_dashboard, driver):
    logger.info("📌 Verifying Payments Menu visibility and clickability.")
    dashboard_page = login_and_navigate_to_dashboard
    assert dashboard_page.is_payments_menu_visible_and_clickable(), "Payments menu is not visible or clickable."
    take_screenshot(driver, f"{ENV}_dashboard_payments_menu")


# ✅ **TC_Dashboard_008** - Verify "Invoices Menu" is visible & clickable
def test_invoices_menu(login_and_navigate_to_dashboard, driver):
    logger.info("📌 Verifying Invoices Menu visibility and clickability.")
    dashboard_page = login_and_navigate_to_dashboard
    assert dashboard_page.is_invoices_menu_visible_and_clickable(), "Invoices menu is not visible or clickable."
    take_screenshot(driver, f"{ENV}_dashboard_invoices_menu")


# ✅ **TC_Dashboard_009** - Verify "Gateways Dropdown" is visible
def test_gateways_dropdown(login_and_navigate_to_dashboard, driver):
    logger.info("📌 Verifying Gateways Dropdown visibility.")
    dashboard_page = login_and_navigate_to_dashboard
    assert dashboard_page.is_gateways_dropdown_visible(), "Gateways dropdown is not visible."
    take_screenshot(driver, f"{ENV}_dashboard_gateways_dropdown")


# ✅ **TC_Dashboard_010** - Verify "Exceptions Badge" is visible
def test_exceptions_badge(login_and_navigate_to_dashboard, driver):
    logger.info("📌 Verifying Exceptions Badge visibility.")
    dashboard_page = login_and_navigate_to_dashboard
    assert dashboard_page.is_exceptions_badge_visible(), "Exceptions badge is not visible."
    take_screenshot(driver, f"{ENV}_dashboard_exceptions_badge")


# ✅ **TC_Dashboard_011** - Verify "Source Documents Received" section
def test_source_documents_received_section(login_and_navigate_to_dashboard, driver):
    logger.info("📌 Verifying Source Documents Received section visibility.")
    dashboard_page = login_and_navigate_to_dashboard
    assert dashboard_page.is_source_documents_received_section_visible(), "Source Documents Received section is not visible."
    take_screenshot(driver, f"{ENV}_dashboard_source_documents")


# ✅ **TC_Dashboard_012** - Verify "Emails Section" visibility
def test_emails_section(login_and_navigate_to_dashboard, driver):
    logger.info("📌 Verifying Emails Section visibility.")
    dashboard_page = login_and_navigate_to_dashboard
    assert dashboard_page.is_emails_section_visible(), "Emails section is not visible."
    take_screenshot(driver, f"{ENV}_dashboard_emails_section")


# ✅ **TC_Dashboard_013** - Verify "Payments by Status" section
def test_payments_by_status_section(login_and_navigate_to_dashboard, driver):
    logger.info("📌 Verifying Payments by Status section visibility.")
    dashboard_page = login_and_navigate_to_dashboard
    assert dashboard_page.is_payments_by_status_section_visible(), "Payments by Status section is not visible."
    take_screenshot(driver, f"{ENV}_dashboard_payments_status")


# ✅ **TC_Dashboard_014** - Verify "Gateways Section" is visible
def test_gateways_section(login_and_navigate_to_dashboard, driver):
    logger.info("📌 Verifying Gateways Section visibility.")
    dashboard_page = login_and_navigate_to_dashboard
    assert dashboard_page.is_gateways_section_visible(), "Gateways section is not visible."
    take_screenshot(driver, f"{ENV}_dashboard_gateways_section")


# ✅ **TC_Dashboard_015** - Verify "Payments by Source" section
def test_payments_by_source_section(login_and_navigate_to_dashboard, driver):
    logger.info("📌 Verifying Payments by Source section visibility.")
    dashboard_page = login_and_navigate_to_dashboard
    assert dashboard_page.is_payments_by_source_section_visible(), "Payments by Source section is not visible."
    take_screenshot(driver, f"{ENV}_dashboard_payments_by_source")

