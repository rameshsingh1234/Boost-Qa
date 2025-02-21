import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import pytest
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from Pageobject.login import LoginPage
from Pageobject.internal import InternalPage
from Pageobject.payment import PaymentPage
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

# ✅ **TC_Payment_001** - Validate navigation to 'Payments' page after finalizing a batch
def test_goto_payments(login_and_navigate_to_internal, driver):
    logger.info("📌 [Validating 'Go to Payments' functionality after finalizing submission.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_payment_batch")
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../testdata/20250114-PNC.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_payment_batch")
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
    internal_page.click_go_to_payment()
    take_screenshot(driver, f"{ENV}_navigated_to_payments")
    payment_page = PaymentPage(driver)
    payment_page.click_payment_record()
    take_screenshot(driver, f"{ENV}_payment_record_clicked")
    logger.info("✅ Navigation to 'Payments' page validated successfully!")

# ✅ **TC_Payment_002** - Verify navigation to detailed payment information screen
def test_payment_tab(login_and_navigate_to_internal, driver):
    logger.info("📌 [Validating 'Go to Payments' functionality after finalizing submission.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_payment_batch")
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../testdata/20250114-PNC.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_payment_batch")
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
    # Navigate through the finalization steps
    internal_page.click_status_button()
    take_screenshot(driver, f"{ENV}_status_button_clicked")
    time.sleep(5)
    internal_page.click_finalize_button()
    take_screenshot(driver, f"{ENV}_finalize_submission_clicked")
    time.sleep(5)
    internal_page.click_continue_button()
    take_screenshot(driver, f"{ENV}_continue_button_clicked")
    time.sleep(3)
    internal_page.click_check_back_later()
    take_screenshot(driver, f"{ENV}_check_back_later_clicked")
    time.sleep(3)
    internal_page.click_go_to_payment()
    take_screenshot(driver, f"{ENV}_navigated_to_payments")
    payment_page = PaymentPage(driver)
    payment_page.click_payment_record()
    take_screenshot(driver, f"{ENV}_payment_record_clicked")
    payment_page.is_payment_tab_displayed()
    logger.info("✅ Payment information screen test passed successfully!")

# ✅ **TC_Payment_003** -  Validate that details are correctly displayed for a selected payment
def test_payment_displayed(login_and_navigate_to_internal, driver):
    logger.info("📌 [Validating 'Go to Payments' functionality after finalizing submission.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_payment_batch")
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../testdata/20250114-PNC.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_payment_batch")
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
    # Navigate through the finalization steps
    internal_page.click_status_button()
    take_screenshot(driver, f"{ENV}_status_button_clicked")
    time.sleep(5)
    internal_page.click_finalize_button()
    take_screenshot(driver, f"{ENV}_finalize_submission_clicked")
    time.sleep(5)
    internal_page.click_continue_button()
    take_screenshot(driver, f"{ENV}_continue_button_clicked")
    time.sleep(3)
    internal_page.click_check_back_later()
    take_screenshot(driver, f"{ENV}_check_back_later_clicked")
    time.sleep(3)
    internal_page.click_go_to_payment()
    take_screenshot(driver, f"{ENV}_navigated_to_payments")
    payment_page = PaymentPage(driver)
    payment_page.click_payment_record()
    take_screenshot(driver, f"{ENV}_payment_record_clicked")
    logger.info(f"📊 Payment status: {payment_page.get_payment_status()}")
    logger.info(f"🏷️ Source name: {payment_page.get_source_name()}")
    logger.info(f"👤 Buyer name: {payment_page.get_buyer_name()}")
    logger.info(f"🏬 Merchant name: {payment_page.get_merchant_name()}")
    logger.info("✅ Payment display test passed successfully!")

#✅ **TC_Payment_004** -Validate the display of payment, additional, invoice, source, trace, and audit details for a selected payment.
def test_display_payment_details(login_and_navigate_to_internal, driver):
    logger.info("📌 [Validating 'Go to Payments' functionality after finalizing submission.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_payment_batch")
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../Testdata/20250114-PNC_Latest.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_payment_batch")
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
    # Navigate through the finalization steps
    internal_page.click_status_button()
    take_screenshot(driver, f"{ENV}_status_button_clicked")
    time.sleep(5)
    internal_page.click_finalize_button()
    take_screenshot(driver, f"{ENV}_finalize_submission_clicked")
    time.sleep(5)
    internal_page.click_continue_button()
    take_screenshot(driver, f"{ENV}_continue_button_clicked")
    time.sleep(3)
    internal_page.click_check_back_later()
    take_screenshot(driver, f"{ENV}_check_back_later_clicked")
    time.sleep(3)
    internal_page.click_go_to_payment()
    take_screenshot(driver, f"{ENV}_navigated_to_payments")
    payment_page = PaymentPage(driver)
    payment_page.click_payment_record()
    take_screenshot(driver, f"{ENV}_payment_record_clicked")
    logger.info("Step 3: Logging payment details.")

    # Log all payment details
    logger.info(f"📅 Received date: {payment_page.get_received_date()}")
    logger.info(f"📅 Process date: {payment_page.get_process_date()}")
    logger.info(f"📊 Payment status: {payment_page.get_payment_status()}")
    logger.info(f"🏷️ Source name: {payment_page.get_source_name()}")
    logger.info(f"👤 Buyer name: {payment_page.get_buyer_name()}")
    logger.info(f"🏬 Merchant name: {payment_page.get_merchant_name()}")



#5.✅ **TC_Payment_005** -  Validate the functionality of payment actions.
def test_payment_action(login_and_navigate_to_internal, driver):
    logger.info("📌 [Validating 'Go to Payments' functionality after finalizing submission.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_payment_batch")
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../testdata/20250114-PNC.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_payment_batch")
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
    # Navigate through the finalization steps
    internal_page.click_status_button()
    take_screenshot(driver, f"{ENV}_status_button_clicked")
    time.sleep(5)
    internal_page.click_finalize_button()
    take_screenshot(driver, f"{ENV}_finalize_submission_clicked")
    time.sleep(5)
    internal_page.click_continue_button()
    take_screenshot(driver, f"{ENV}_continue_button_clicked")
    time.sleep(3)
    internal_page.click_check_back_later()
    take_screenshot(driver, f"{ENV}_check_back_later_clicked")
    time.sleep(3)
    internal_page.click_go_to_payment()
    take_screenshot(driver, f"{ENV}_navigated_to_payments")
    time.sleep(3)
    payment_page = PaymentPage(driver)
    payment_page.click_payment_record()
    take_screenshot(driver, f"{ENV}_payment_record_clicked")
    time.sleep(3)
    payment_page.click_add_note()
    take_screenshot(driver, f"{ENV}_add_note_clicked")
    time.sleep(3)
    payment_page.click_cancel_button()
    take_screenshot(driver, f"{ENV}_cancel_button_clicked")
    time.sleep(3)
    payment_page.click_download_payment_details()
    take_screenshot(driver, f"{ENV}_download_payment_details_clicked")
    time.sleep(3)
    payment_page.click_link_source()
    take_screenshot(driver, f"{ENV}_link_source_clicked")
    logger.info("✅ Payment actions test passed successfully!")

#✅ **TC_Payment_006** Validate the functionality of 'Add Note to Payment
def test_add_note(login_and_navigate_to_internal, driver):
    logger.info("📌 [Validating 'Go to Payments' functionality after finalizing submission.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_payment_batch")
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../testdata/20250114-PNC.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_payment_batch")
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
    time.sleep(3)
    internal_page.click_check_back_later()
    take_screenshot(driver, f"{ENV}_check_back_later_clicked")
    time.sleep(3)
    internal_page.click_go_to_payment()
    take_screenshot(driver, f"{ENV}_navigated_to_payments")
    time.sleep(3)
    payment_page = PaymentPage(driver)
    payment_page.click_payment_record()
    take_screenshot(driver, f"{ENV}_payment_record_clicked")
    time.sleep(3)
    logger.info("Step 1: Clicking on 'Add Note to Payment' button.")
    payment_page.click_add_note()
    logger.info("Step 2: Entering note text: 'Test note entry'.")
    payment_page.enter_note_text("Test note entry")
    logger.info("Step 3: Clicking 'Submit' button.")
    payment_page.submit_note()

#7.✅ **TC_Payment_007** - Validate the functionality of 'Download Payment Details''
def test_Download_payment(login_and_navigate_to_internal, driver):
    logger.info("📌 [Validating 'Go to Payments' functionality after finalizing submission.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_payment_batch")
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../testdata/20250114-PNC.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_payment_batch")
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
    # Navigate through the finalization steps
    internal_page.click_status_button()
    take_screenshot(driver, f"{ENV}_status_button_clicked")
    time.sleep(5)
    internal_page.click_finalize_button()
    take_screenshot(driver, f"{ENV}_finalize_submission_clicked")
    time.sleep(5)
    internal_page.click_continue_button()
    take_screenshot(driver, f"{ENV}_continue_button_clicked")
    time.sleep(3)
    internal_page.click_check_back_later()
    take_screenshot(driver, f"{ENV}_check_back_later_clicked")
    time.sleep(3)
    internal_page.click_go_to_payment()
    take_screenshot(driver, f"{ENV}_navigated_to_payments")
    time.sleep(3)
    payment_page = PaymentPage(driver)
    payment_page.click_payment_record()
    take_screenshot(driver, f"{ENV}_payment_record_clicked")
    time.sleep(3)
    payment_page.click_download_payment_details()
    take_screenshot(driver, f"{ENV}_download_payment_details_clicked")

#✅ **TC_Payment_008** .Validate the functionality of 'Link Source to Payment'
def test_link_source(login_and_navigate_to_internal, driver):
    logger.info("📌 [Validating 'Go to Payments' functionality after finalizing submission.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_payment_batch")
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../testdata/20250114-PNC.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_payment_batch")
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
    # Navigate through the finalization steps
    internal_page.click_status_button()
    take_screenshot(driver, f"{ENV}_status_button_clicked")
    time.sleep(5)
    internal_page.click_finalize_button()
    take_screenshot(driver, f"{ENV}_finalize_submission_clicked")
    time.sleep(5)
    internal_page.click_continue_button()
    take_screenshot(driver, f"{ENV}_continue_button_clicked")
    time.sleep(3)
    internal_page.click_check_back_later()
    take_screenshot(driver, f"{ENV}_check_back_later_clicked")
    time.sleep(3)
    internal_page.click_go_to_payment()
    take_screenshot(driver, f"{ENV}_navigated_to_payments")
    time.sleep(3)
    payment_page = PaymentPage(driver)
    payment_page.click_payment_record()
    take_screenshot(driver, f"{ENV}_payment_record_clicked")
    time.sleep(3)
    payment_page.click_link_source()
    take_screenshot(driver, f"{ENV}_link_source_clicked")
    time.sleep(3)

# #✅ **TC_Payment_006** Validate the functionality of 'Add Note to Payment
# def test_add_note(login_and_navigate_to_internal, driver):
#     logger.info("📌 [Validating 'Go to Payments' functionality after finalizing submission.")
#     internal_page = login_and_navigate_to_internal
#     internal_page.click_internal_batch()
#     take_screenshot(driver, f"{ENV}_before_uploading_payment_batch")
#     base_path = os.path.dirname(os.path.abspath(__file__))
#     file_path = os.path.join(base_path, "../testdata/20250114-PNC.xlsx")
#     if not os.path.exists(file_path):
#         raise FileNotFoundError(f"❌ File not found: {file_path}")
#     logger.info(f"🔍 Uploading file: {file_path}")
#     internal_page.add_file(file_path)
#     take_screenshot(driver, f"{ENV}_after_uploading_payment_batch")
#     internal_page.click_validate_button()
#     internal_page.click_check_button()
#     for attempt in range(5):
#         file_status = internal_page.get_file_status()
#         if file_status in ["Submitted", "Validation"]:
#             logger.info(f"✅ File status verified: {file_status}")
#             break
#         logger.warning(f"⏳ Waiting for status update (Attempt {attempt + 1}/5)...")
#         time.sleep(3)
#     else:
#         raise AssertionError(f"❌ Expected file status 'Submitted' or 'Validation', but got '{file_status}'.")
#     take_screenshot(driver, f"{ENV}_file_status_verified")
#     internal_page.click_status_button()
#     take_screenshot(driver, f"{ENV}_status_button_clicked")
#     time.sleep(5)
#     internal_page.click_finalize_button()
#     take_screenshot(driver, f"{ENV}_finalize_submission_clicked")
#     time.sleep(5)
#     internal_page.click_continue_button()
#     take_screenshot(driver, f"{ENV}_continue_button_clicked")
#     time.sleep(3)
#     internal_page.click_check_back_later()
#     take_screenshot(driver, f"{ENV}_check_back_later_clicked")
#     time.sleep(3)
#     internal_page.click_go_to_payment()
#     take_screenshot(driver, f"{ENV}_navigated_to_payments")
#     time.sleep(3)
#     payment_page = PaymentPage(driver)
#     payment_page.click_payment_record()
#     take_screenshot(driver, f"{ENV}_payment_record_clicked")
#     time.sleep(3)
#     logger.info("Step 1: Clicking on 'Add Note to Payment' button.")
#     payment_page.click_add_note()
#     logger.info("Step 2: Entering note text: 'Test note entry'.")
#     payment_page.enter_note_text("Test note entry")
#     logger.info("Step 3: Clicking 'Submit' button.")
#     payment_page.submit_note()
#
#
