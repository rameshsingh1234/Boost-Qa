import os

import openpyxl
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import pytest
from datetime import datetime
from file_headers_iter import extract_headers
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import pytest
import os
import time
from file_headers_iter import extract_headers
from Pageobject.login import LoginPage
from Pageobject.internal import InternalPage
from Pageobject.payment import PaymentPage
from Pageobject.file_validation import PaymentPage
from Utilities.utils import take_screenshot, archive_old_screenshots, test_data
from Utilities.logger import logger

# ✅ Fetch environment dynamically
ENV = os.getenv("ENVIRONMENT", "DEV").upper()  # Default to DEV if not set


@pytest.fixture(scope="session", autouse=True)
def setup_screenshot_archive():
    """
    ✅ Runs before any test execution to archive previous Screenshots.
    """
    logger.info("📂 Archiving old Screenshots before test execution...")
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
def login_and_navigate_to_internal(driver, test_data):
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
    # Open the base URL and log in
    # Wait for login to complete
    # Navigate to the Internal page
    internal_page = InternalPage(driver)
    internal_page.click_dropdown()
    internal_page.select_dropdown_option()

    return internal_page

#1. The user uploads a PNC file.
#After successful file submission, the user navigates to the payment screen.
#On the payment screen:
#The **payer's name** from the PNC file is displayed as the **buyer's name**.
#The **supplier's name** from the PNC file is displayed as the **merchant's name**
def test_validate_header_name(login_and_navigate_to_internal, driver):
    logger.info("📌 Validate PNC file upload and mapping of payer and supplier names on the payment screen.")
    # Path to the PNC file
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../testdata/20250114-PNC.xlsx")

    # Step 1: Extract headers from the PNC file
    global_headers = extract_headers(file_path)
    logger.info("Extracted Headers:")
    for sheet, headers in global_headers.items():
        logger.info(f"\nSheet: {sheet}")
        logger.info(f"Headers: {', '.join(filter(None, headers))}")  # Fixed line

    # Step 2: Upload the PNC file
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_payment_batch")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_payment_batch")

    # Step 3: Validate and finalize the submission
    internal_page.click_validate_button()
    internal_page.click_check_button()

    for attempt in range(5):
        file_status = internal_page.get_file_status()
        if file_status in ["Submitted", "Validation"]:
            logger.info(f"✅ File status verified: {file_status}")
            break
        logger.warning(f"⏳ Waiting for status update (Attempt {attempt + 1}/5)...")
        time.sleep(3)
    else:
        raise AssertionError(f"❌ Expected file status 'Submitted' or 'Validation', but got '{file_status}'.")

    take_screenshot(driver, f"{ENV}_file_status_verified")
    time.sleep(60)
    internal_page.click_status_button()
    take_screenshot(driver, f"{ENV}_status_button_clicked")
    time.sleep(5)

    internal_page.click_finalize_button()
    take_screenshot(driver, f"{ENV}_finalize_submission_clicked")
    time.sleep(5)

    internal_page.click_continue_button()
    take_screenshot(driver, f"{ENV}_continue_button_clicked")
    time.sleep(5)

    internal_page.click_check_back_later()
    take_screenshot(driver, f"{ENV}_check_back_later_clicked")
    time.sleep(5)

    # Step 4: Navigate to the payment screen
    internal_page.click_go_to_payment()
    take_screenshot(driver, f"{ENV}_navigated_to_payments")
    time.sleep(5)
    # Step 5: Validate header transformation on the payment screen
    # payment_page = PaymentPage(driver)
    # payment_page.click_payment_record()
    internal_page.click_payment_row()
    take_screenshot(driver, f"{ENV}_payment_record_clicked")
    time.sleep(5)
    payment_page = PaymentPage(driver)
    # Validate that payer's name is displayed as buyer's name and supplier's name as merchant's name
    assert payment_page.is_buyer_name_header_displayed(), "Buyer Name header is not displayed."
    assert payment_page.is_merchant_name_header_displayed(), "Merchant Name header is not displayed."

    logger.info("✅ Navigation to 'Payments' page validated successfully!")
    logger.info("Header transformation validated successfully:")
    logger.info(f"Payer's Name header is displayed as Buyer's Name.")
    logger.info(f"Supplier's Name header is displayed as Merchant's Name.")

#2.verify the header source name in the PNC file with the header source name on the payment screen.
def test_validate_source_name(login_and_navigate_to_internal, driver):
    logger.info("📌 Validate PNC file upload and mapping of payer and supplier names on the payment screen.")
    # Path to the PNC file
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../testdata/20250114-PNC.xlsx")

    # Step 1: Extract headers from the PNC file
    global_headers = extract_headers(file_path)
    logger.info("Extracted Headers:")
    for sheet, headers in global_headers.items():
        logger.info(f"\nSheet: {sheet}")
        logger.info(f"Headers: {', '.join(filter(None, headers))}")  # Fixed line

    # Step 2: Upload the PNC file
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_payment_batch")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_payment_batch")

    # Step 3: Validate and finalize the submission
    internal_page.click_validate_button()
    internal_page.click_check_button()

    for attempt in range(5):
        file_status = internal_page.get_file_status()
        if file_status in ["Submitted", "Validation"]:
            logger.info(f"✅ File status verified: {file_status}")
            break
        logger.warning(f"⏳ Waiting for status update (Attempt {attempt + 1}/5)...")
        time.sleep(3)
    else:
        raise AssertionError(f"❌ Expected file status 'Submitted' or 'Validation', but got '{file_status}'.")

    take_screenshot(driver, f"{ENV}_file_status_verified")
    internal_page.click_status_button()
    take_screenshot(driver, f"{ENV}_status_button_clicked")
    time.sleep(5)

    internal_page.click_finalize_button()
    take_screenshot(driver, f"{ENV}_finalize_submission_clicked")
    time.sleep(5)

    internal_page.click_continue_button()
    take_screenshot(driver, f"{ENV}_continue_button_clicked")
    time.sleep(5)

    internal_page.click_check_back_later()
    take_screenshot(driver, f"{ENV}_check_back_later_clicked")
    time.sleep(5)

    # Step 4: Navigate to the payment screen
    internal_page.click_go_to_payment()
    take_screenshot(driver, f"{ENV}_navigated_to_payments")
    time.sleep(5)

    # Step 5: Validate header transformation on the payment screen
    internal_page.click_payment_row()
    take_screenshot(driver, f"{ENV}_payment_record_clicked")
    time.sleep(5)

    payment_page = PaymentPage(driver)
    # Step 5: Validate Source short name is displayed as Source Name
    source_name = payment_page.is_source_name_header_displayed()
    assert source_name == "Source Name", f"Source name '{source_name}' does not match 'Source Name'"

    logger.info("Validation successful:")
    logger.info(f"Source short name is displayed as Source Name ({source_name}).")

#3
# def test_validate_total(login_and_navigate_to_internal, driver):
#     logger.info("📌 Validate PNC file upload and mapping of payer and supplier names on the payment screen.")
#     # Path to the PNC file
#     base_path = os.path.dirname(os.path.abspath(__file__))
#     file_path = os.path.join(base_path, "../testdata/20250114-PNC.xlsx")
#
#     # Step 1: Extract headers from the PNC file
#     global_headers = extract_headers(file_path)
#     logger.info("Extracted Headers:")
#     for sheet, headers in global_headers.items():
#         logger.info(f"\nSheet: {sheet}")
#         logger.info(f"Headers: {', '.join(filter(None, headers))}")  # Fixed line
#
#     # Step 2: Upload the PNC file
#     internal_page = login_and_navigate_to_internal
#     internal_page.click_internal_batch()
#     take_screenshot(driver, f"{ENV}_before_uploading_payment_batch")
#
#     if not os.path.exists(file_path):
#         raise FileNotFoundError(f"❌ File not found: {file_path}")
#     logger.info(f"🔍 Uploading file: {file_path}")
#     internal_page.add_file(file_path)
#     take_screenshot(driver, f"{ENV}_after_uploading_payment_batch")
#
#     # Step 3: Validate and finalize the submission
#     internal_page.click_validate_button()
#     internal_page.click_check_button()
#
#     for attempt in range(5):
#         file_status = internal_page.get_file_status()
#         if file_status in ["Submitted", "Validation"]:
#             logger.info(f"✅ File status verified: {file_status}")
#             break
#         logger.warning(f"⏳ Waiting for status update (Attempt {attempt + 1}/5)...")
#         time.sleep(3)
#     else:
#         raise AssertionError(f"❌ Expected file status 'Submitted' or 'Validation', but got '{file_status}'.")
#
#     take_screenshot(driver, f"{ENV}_file_status_verified")
#     internal_page.click_status_button()
#     take_screenshot(driver, f"{ENV}_status_button_clicked")
#     time.sleep(5)
#
#     # internal_page.click_finalize_button()
#     # take_screenshot(driver, f"{ENV}_finalize_submission_clicked")
#     # time.sleep(5)
#     #
#     # internal_page.click_continue_button()
#     # take_screenshot(driver, f"{ENV}_continue_button_clicked")
#     # time.sleep(5)
#     #
#     # internal_page.click_check_back_later()
#     # take_screenshot(driver, f"{ENV}_check_back_later_clicked")
#     # time.sleep(5)
#     #
#     # # Step 4: Navigate to the payment screen
#     # internal_page.click_go_to_payment()
#     # take_screenshot(driver, f"{ENV}_navigated_to_payments")
#     # time.sleep(5)
#     #
#     # # Step 5: Validate header transformation on the payment screen
#     # internal_page.click_payment_row()
#     # take_screenshot(driver, f"{ENV}_payment_record_clicked")
#     # time.sleep(5)
#
#     payment_page = PaymentPage(driver)
#     # Step 5: Validate Source short name is displayed as Source Name
#     total_payment_amount_name = payment_page.is_source_name_header_displayed()
#     assert total_payment_amount_name == "Source Name", f"Source name '{total_payment_amount_name}' does not match 'Source Name'"
#
#     logger.info("Validation successful:")
#     logger.info(f"Source short name is displayed as Source Name ({total_payment_amount_name}).")

def test_validate_total(login_and_navigate_to_internal, driver):
    logger.info("📌 Validate PNC file upload and mapping of payer and supplier names on the payment screen.")
    # Path to the PNC file
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../testdata/20250114-PNC.xlsx")

    # Step 1: Extract headers from the PNC file
    # Step 1: Extract headers from the PNC file
    global_headers = extract_headers(file_path)
    logger.info("Extracted Headers:")
    for sheet, headers in global_headers.items():
        logger.info(f"\nSheet: {sheet}")
        logger.info(f"Headers: {', '.join(filter(None, headers))}")  # Fixed line

    # Step 2: Extract Total Amount from the PNC file
    workbook = openpyxl.load_workbook(file_path, data_only=True)
    sheet = workbook["Transactions"]  # Assuming the sheet name is "Transactions"

    # Find the index of the "Total Amount" column
    total_amount_col = None
    for idx, header in enumerate(global_headers["Transactions"]):
        if header and "total amount" in str(header).lower():
            total_amount_col = idx
            break

    if total_amount_col is None:
        raise ValueError("Total Amount column not found in the sheet.")

    # Extract the first row of data (assuming the first row after the header contains the data)
    data_row = sheet.iter_rows(min_row=2, max_row=2, values_only=True)
    data_row = next(data_row, None)

    if not data_row:
        raise ValueError("No data found in the sheet.")

    total_amount = data_row[total_amount_col]
    logger.info(f"Total Amount from PNC file: {total_amount}")

    # Step 3: Upload the PNC file
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_payment_batch")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_payment_batch")

    # Step 4: Validate and finalize the submission
    internal_page.click_validate_button()
    internal_page.click_check_button()

    for attempt in range(5):
        file_status = internal_page.get_file_status()
        if file_status in ["Submitted", "Validation"]:
            logger.info(f"✅ File status verified: {file_status}")
            break
        logger.warning(f"⏳ Waiting for status update (Attempt {attempt + 1}/5)...")
        time.sleep(3)
    else:
        raise AssertionError(f"❌ Expected file status 'Submitted' or 'Validation', but got '{file_status}'.")

    take_screenshot(driver, f"{ENV}_file_status_verified")
    internal_page.click_status_button()
    take_screenshot(driver, f"{ENV}_status_button_clicked")
    time.sleep(5)

    # Step 5: Retrieve Total Payments Amount from the file validation screen
    payment_page = PaymentPage(driver)
    total_payments_amount = payment_page.is_total_payment_amount()
    logger.info(f"Total Payments Amount from file validation screen: {total_payments_amount}")

    # Step 6: Compare the Total Amount from the PNC file with the Total Payments Amount on the screen
    assert total_amount == total_payments_amount, f"Total Amount '{total_amount}' does not match Total Payments Amount '{total_payments_amount}'"

    logger.info("Validation successful:")
    logger.info(f"Total Amount ({total_amount}) matches Total Payments Amount ({total_payments_amount}).")



