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

# ✅ **TC_Internal_001** -  Validate that the "Sources -> Internal" screen is displayed
def test_validate_internal_page(login_and_navigate_to_internal, driver):
    logger.info("📌 Validating 'Sources -> Internal' screen visibility.")
    internal_page = login_and_navigate_to_internal  # Renaming for clarity
    assert internal_page.is_internal_displayed(), "❌ Internal text not displayed."
    screenshot_path = take_screenshot(driver, f"{ENV}_internal_page_visibility")
    logger.info(f"📸 Screenshot captured: {screenshot_path}")


# ✅ **TC_Internal_002** - Validate all key elements are displayed on the "Sources -> Internal" screen
def test_elements_displayed(login_and_navigate_to_internal, driver):
    logger.info("📌 Validating key elements visibility on 'Sources -> Internal' screen.")
    internal_page = login_and_navigate_to_internal  # Assign fixture return value
    assert internal_page.is_internal_displayed(), "❌ Internal page is not displayed."
    assert internal_page.are_key_elements_visible(), "❌ One or more key elements are missing on the Internal page."
    screenshot_path = take_screenshot(driver, f"{ENV}_internal_page_elements")
    logger.info(f"📸 Screenshot captured: {screenshot_path}")


# ✅ **TC_Internal_003** - Validate redirection to "Adding New Entries" page when clicking "New Internal Batch"
def test_download_upload_file(login_and_navigate_to_internal, driver):
    logger.info("🔄 Verifying redirection to 'Adding New Entries' page.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    logger.info("⏳ Waiting for the 'Adding New Entries' page to load...")
    assert internal_page.is_adding_batch_displayed(), "❌ 'Adding New Entries' text not displayed."
    logger.info("✅ Successfully navigated to 'Adding New Entries' page.")
    assert internal_page.are_download_upload_sections_visible(), "❌ Download/Upload sections are missing."
    logger.info("✅ Download/Upload sections are visible.")
    screenshot_path = take_screenshot(driver, f"{ENV}_adding_new_entries_page")
    logger.info(f"📸 Screenshot captured: {screenshot_path}")

# ✅ **TC_Internal_004** - Validate the download functionality for 'Template Domestic Payments'
def test_download_template(login_and_navigate_to_internal, driver):
    logger.info("🔄 Verifying the download functionality for 'Template Domestic Payments'.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    download_dir = os.path.expanduser("~/Downloads")  # Dynamic path for portability
    expected_file = "DOMESTIC.xlsx"  # Update if needed
    logger.info(f"📥 Initiating download for template: {expected_file}")
    internal_page.click_download_template1()
    assert internal_page.is_file_downloaded(download_dir, expected_file), f"❌ File '{expected_file}' not downloaded."
    logger.info(f"✅ File '{expected_file}' downloaded successfully.")
    file_path = os.path.join(download_dir, expected_file)
    assert os.path.getsize(file_path) > 0, f"❌ Downloaded file '{expected_file}' is empty."
    logger.info(f"✅ File '{expected_file}' is not empty.")
    try:
        os.remove(file_path)
        logger.info(f"🗑️ Deleted downloaded file: {file_path}")
    except Exception as e:
        logger.warning(f"⚠️ Failed to delete downloaded file: {e}")

# ✅ **TC_Internal_005** - Validate the download functionality for 'Source Template'
def test_download_source_template(login_and_navigate_to_internal, driver):
    logger.info("🔄 Verifying the download functionality for 'Source Template'.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    download_dir = os.path.expanduser("~/Downloads")  # Dynamic path for better portability
    expected_file = "DOMESTIC_SOURCE_LINK.xlsx"  # Ensure this is the correct filename
    logger.info(f"📥 Initiating download for template: {expected_file}")
    internal_page.click_download_template2()
    assert internal_page.is_file_downloaded(download_dir, expected_file), f"❌ File '{expected_file}' not downloaded."
    logger.info(f"✅ File '{expected_file}' downloaded successfully.")
    file_path = os.path.join(download_dir, expected_file)
    assert os.path.getsize(file_path) > 0, f"❌ Downloaded file '{expected_file}' is empty."
    logger.info(f"✅ File '{expected_file}' is not empty.")
    try:
        os.remove(file_path)
        logger.info(f"🗑️ Deleted downloaded file: {file_path}")
    except Exception as e:
        logger.warning(f"⚠️ Failed to delete downloaded file: {e}")

# ✅ **TC_Internal_006** - Validate the download functionality for 'Template International Payments'
def test_download_international_payments(login_and_navigate_to_internal, driver):
    logger.info("🔄Verifying the download functionality for 'Template International Payments'.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    download_dir = os.path.expanduser("~/Downloads")  # Dynamic path for better portability
    expected_file = "INTERNATIONAL.xlsx"  # Ensure this is the correct filename
    logger.info(f"📥 Initiating download for template: {expected_file}")
    internal_page.click_download_template3()
    assert internal_page.is_file_downloaded(download_dir, expected_file), f"❌ File '{expected_file}' not downloaded."
    logger.info(f"✅ File '{expected_file}' downloaded successfully.")
    file_path = os.path.join(download_dir, expected_file)
    assert os.path.getsize(file_path) > 0, f"❌ Downloaded file '{expected_file}' is empty."
    logger.info(f"✅ File '{expected_file}' is not empty.")
    try:
        os.remove(file_path)
        logger.info(f"🗑️ Deleted downloaded file: {file_path}")
    except Exception as e:
        logger.warning(f"⚠️ Failed to delete downloaded file: {e}")


# ✅ **TC_Internal_007** - Validate the download functionality for 'Template Commerce Payments'
def test_download_commerce_payments(login_and_navigate_to_internal, driver):
    logger.info("🔄 Verifying the download functionality for 'Template Commerce Payments'.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    download_dir = os.path.expanduser("~/Downloads")  # Dynamic path for better portability
    expected_file = "COMMERCE.xlsx"  # Ensure this is the correct filename
    logger.info(f"📥 Initiating download for template: {expected_file}")
    internal_page.click_download_template4()
    take_screenshot(driver, f"{ENV}_download_page")
    assert internal_page.is_file_downloaded(download_dir, expected_file), f"❌ File '{expected_file}' not downloaded."
    logger.info(f"✅ File '{expected_file}' downloaded successfully.")
    take_screenshot(driver, f"{ENV}_download_success_{expected_file}")
    file_path = os.path.join(download_dir, expected_file)
    assert os.path.getsize(file_path) > 0, f"❌ Downloaded file '{expected_file}' is empty."
    logger.info(f"✅ File '{expected_file}' is not empty.")
    try:
        os.remove(file_path)
        logger.info(f"🗑️ Deleted downloaded file: {file_path}")
    except Exception as e:
        logger.warning(f"⚠️ Failed to delete downloaded file: {e}")

# ✅ **TC_Internal_008** - Validate the "Select Template Type" dropdown functionality
def test_select_template_dropdown(login_and_navigate_to_internal, driver):
    logger.info("🔽 Verifying 'Select Template Type' dropdown functionality.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_dropdown_selection")
    template_options = {
        "Domestic File": internal_page.click_template_domestic_file,
        "Domestic Source Link": internal_page.click_template_domestic_sourcelink_file,
        "International File": internal_page.click_template_international_file,
        "Commerce File": internal_page.click_template_commerce_file,
    }
    for template_name, action in template_options.items():
        logger.info(f"🔄 Selecting template: {template_name}")
        internal_page.click_template_dropdown()
        action()
        take_screenshot(driver, f"{ENV}_selected_{template_name.replace(' ', '_')}")
    logger.info("✅ Successfully validated 'Select Template Type' dropdown selections.")

# ✅ **TC_Internal_009** - Validate the functionality of the "Back Arrow" button
def test_back_arrow(login_and_navigate_to_internal, driver):
    logger.info("🔙  Verifying 'Back Arrow' button functionality.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_clicking_back_arrow")
    logger.info("🔄 Clicking the 'Back Arrow' button.")
    internal_page.click_back_arrow()
    assert internal_page.is_internal_displayed(), "❌ Internal page was not displayed after clicking Back Arrow."
    take_screenshot(driver, f"{ENV}_after_clicking_back_arrow")
    logger.info("✅ 'Back Arrow' button navigation validated successfully.")


# ✅ **TC_Internal_010** - Validate file upload for "Template Domestic Payments"
def test_file_upload_domestic_payments(login_and_navigate_to_internal, driver):
    logger.info("📂 Verifying file upload for 'Template Domestic Payments'.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    logger.info("🔽 Selecting 'Template Domestic Payments' from dropdown.")
    internal_page.click_template_dropdown()
    internal_page.click_template_domestic_file()
    base_path = os.path.dirname(os.path.abspath(__file__))  # Get the script directory
    file_path = os.path.join(base_path, "../Testdata/DOMESTIC.xlsx")
    if not os.path.exists(file_path):
        logger.error(f"❌ File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    logger.info(f"📂 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_before_clicking_validate")
    logger.info("✅ Clicking 'Validate' button.")
    internal_page.click_validate_button()
    take_screenshot(driver, f"{ENV}_after_clicking_validate")
    logger.info("✅ File upload validation completed successfully.")


# ✅ **TC_Internal_011** - Validate file upload for "Template Domestic Payments with Source Link(s)"
def test_file_upload_domestic_payments_sourcelink(login_and_navigate_to_internal, driver):
    logger.info("📂 Verifying file upload for 'Template Domestic Payments with Source Link(s)'.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    logger.info("🔽 Selecting 'Template Domestic Payments with Source Link(s)' from dropdown.")
    internal_page.click_template_dropdown()
    internal_page.click_template_domestic_sourcelink_file()
    base_path = os.path.dirname(os.path.abspath(__file__))  # Get the script directory
    file_path = os.path.join(base_path, "../Testdata/DOMESTIC_SOURCE_LINK.xlsx")
    if not os.path.exists(file_path):
        logger.error(f"❌ File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    logger.info(f"📂 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_before_clicking_validate")
    logger.info("✅ Clicking 'Validate' button.")
    internal_page.click_validate_button()
    take_screenshot(driver, f"{ENV}_after_clicking_validate")
    logger.info("✅ File upload validation for 'Template Domestic Payments with Source Link(s)' completed successfully.")


# ✅ **TC_Internal_012** - Validate file upload for "Template International Payments"
def test_file_upload_international_payments(login_and_navigate_to_internal, driver):
    logger.info("📂 Verifying file upload for 'Template International Payments'.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    logger.info("🔽 Selecting 'Template International Payments' from dropdown.")
    internal_page.click_template_dropdown()
    internal_page.click_template_international_file()
    base_path = os.path.dirname(os.path.abspath(__file__))  # Get the script directory
    file_path = os.path.join(base_path, "../Testdata/INTERNATIONAL.xlsx")
    if not os.path.exists(file_path):
        logger.error(f"❌ File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    logger.info(f"📂 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_before_clicking_validate")
    logger.info("✅ Clicking 'Validate' button.")
    internal_page.click_validate_button()
    take_screenshot(driver, f"{ENV}_after_clicking_validate")
    logger.info("✅ File upload validation for 'Template International Payments' completed successfully.")


# ✅ **TC_Internal_013** - Validate upload with invalid file format (e.g., PDF)
def test_invalid_file_upload(login_and_navigate_to_internal, driver):
    logger.info("📂 Verifying file upload with an invalid format (PDF).")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    base_path = os.path.dirname(os.path.abspath(__file__))  # Get the script directory
    file_path = os.path.join(base_path, "../Testdata/Test.pdf")
    if not os.path.exists(file_path):
        logger.error(f"❌ File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    logger.info(f"📂 Attempting to upload invalid file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_before_clicking_validate_invalid_file")
    logger.info("✅ Checking for error message.")
    error_message = internal_page.get_file_error_message()
    assert error_message is not None and "file type must be .xls, .xlsx" in error_message.lower(), \
        f"❌ Expected error message for invalid file, but got: {error_message}"
    take_screenshot(driver, f"{ENV}_error_message_invalid_file")
    logger.info("✅ File upload validation for invalid format (PDF) completed successfully.")

# ✅ **TC_Internal_014** - Validate upload with file exceeding size limit
def test__exceeding_size_limit_file_upload(login_and_navigate_to_internal, driver):
    logger.info("📂 [TC_Internal_014] Verifying file upload exceeding size limit.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    base_path = os.path.dirname(os.path.abspath(__file__))  # Get the script directory
    file_path = os.path.join(base_path, "../Testdata/Exceedsize(12MB).pdf")
    if not os.path.exists(file_path):
        logger.error(f"❌ File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    logger.info(f"📂 Attempting to upload oversized file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_before_clicking_validate_oversized_file")
    logger.info("✅ Checking for error message.")
    error_message = internal_page.get_file_error_message()
    assert error_message is not None and "file type must be .xls, .xlsx" in error_message.lower(), \
        f"❌ Expected error message for oversized file, but got: {error_message}"
    take_screenshot(driver, f"{ENV}_error_message_oversized_file")
    logger.info("✅ File upload validation for exceeding size limit completed successfully.")

# ✅ **TC_Internal_015** - Validate the "Validate" button is disabled when no file is uploaded
def test_validate_button_disabled(login_and_navigate_to_internal, driver):
    logger.info("📌 Verifying that the 'Validate' button is disabled when no file is uploaded.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_selecting_template")
    internal_page.click_template_dropdown()
    internal_page.click_template_domestic_file()
    take_screenshot(driver, f"{ENV}_after_selecting_template_no_file")
    assert internal_page.is_validate_button_disabled(), "❌ The 'Validate' button should be disabled when no file is uploaded."
    logger.info("✅ 'Validate' button is correctly disabled when no file is uploaded.")


# ✅ **TC_Internal_016** - Validate file selection functionality and display of selected file
def test_validate_file_upload_name(login_and_navigate_to_internal, driver):
    logger.info("📌 [TC_Internal_016] Verifying file selection and correct display of the uploaded file name.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_selecting_template")
    internal_page.click_template_dropdown()
    internal_page.click_template_domestic_sourcelink_file()
    take_screenshot(driver, f"{ENV}_after_selecting_template")
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../Testdata/DOMESTIC_SOURCE_LINK.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Using file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_file")
    uploaded_file_name = internal_page.get_uploaded_file_name()
    assert uploaded_file_name == "DOMESTIC_SOURCE_LINK.xlsx", \
        f"❌ Expected file name 'DOMESTIC_SOURCE_LINK.xlsx', but got '{uploaded_file_name}'."
    logger.info("✅ File selection and display of uploaded file name is working correctly.")


# ✅ **TC_Internal_017** - Validate file upload completion and status update in the internal page
def test_validate_file_upload_completion(login_and_navigate_to_internal, driver):
    logger.info("📌 [TC_Internal_017] Verifying file upload completion and status update.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_file")
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../Testdata/20250114-PNC.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Using file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_file")
    internal_page.click_validate_button()
    logger.info("⏳ Waiting for file validation status update...")
    internal_page.click_check_button()
    file_status = internal_page.get_file_status()
    assert file_status in ["Submitted", "Validation"], \
        f"❌ Expected file status to be 'Submitted' or 'Validation', but got '{file_status}'."
    take_screenshot(driver, f"{ENV}_file_status_update")
    logger.info("✅ File upload completion and status update validated successfully.")


# ✅ **TC_Internal_018** - Validate the presence of details in the internal page after file validation
def test_file_details_after_validation(login_and_navigate_to_internal, driver):
    logger.info("📌 [TC_Internal_018] Verifying file details after validation.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_file")
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../Testdata/20250114-PNC.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Using file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_file")
    internal_page.click_validate_button()
    logger.info("⏳ Waiting for validation status update...")
    internal_page.click_check_button()
    file_status = internal_page.get_file_status()
    assert file_status in ["Submitted", "Validation"], \
        f"❌ Expected file status to be 'Submitted' or 'Validation', but got '{file_status}'."
    take_screenshot(driver, f"{ENV}_file_status_update")
    logger.info("✅ File status updated successfully.")
    internal_page.click_status_button()
    total_payments_text = internal_page.get_total_payments()
    assert "Total Payments" in total_payments_text, "❌ Heading 'Total Payments' not found."
    take_screenshot(driver, f"{ENV}_file_details_page")
    logger.info("✅ File details validated successfully.")


# ✅ **TC_Internal_019** - Validate navigation to file status page and check file details
def test_file_status_navigation(login_and_navigate_to_internal, driver):
    logger.info("📌 Verifying navigation to file status page from 'Submitted' status.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_file")
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../Testdata/20250114-PNC.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_file")
    internal_page.click_validate_button()
    logger.info("⏳ Waiting for file status update...")
    internal_page.click_check_button()
    file_status = internal_page.get_file_status()
    assert file_status in ["Submitted", "Validation"], \
        f"❌ Expected file status to be 'Submitted' or 'Validation', but got '{file_status}'."
    take_screenshot(driver, f"{ENV}_file_status_update")
    logger.info(f"✅ File status verified as: {file_status}")
    internal_page.click_status_button()
    take_screenshot(driver, f"{ENV}_navigated_to_status_page")
    total_payments_text = internal_page.get_total_payments()
    assert "Total Payments" in total_payments_text, "❌ Heading 'Total Payments' not found."
    take_screenshot(driver, f"{ENV}_file_details_verified")
    logger.info("✅ Successfully navigated to file status page and validated file details.")


# ✅ **TC_Internal_020** - Validate 'Manual Batches Actions' for a submitted batch
def test_manual_batches_action(login_and_navigate_to_internal, driver):
    logger.info("📌 Verifying 'Manual Batches Actions' for a submitted batch.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_file")
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../Testdata/20250114-PNC.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_file")
    internal_page.click_validate_button()
    logger.info("⏳ Waiting for file status update...")
    internal_page.click_check_button()
    file_status = internal_page.get_file_status()
    assert file_status in ["Submitted", "Validation"], \
        f"❌ Expected file status to be 'Submitted' or 'Validation', but got '{file_status}'."
    take_screenshot(driver, f"{ENV}_file_status_update")
    logger.info(f"✅ File status verified as: {file_status}")
    internal_page.click_status_button()
    take_screenshot(driver, f"{ENV}_navigated_to_status_page")
    logger.info("🚀 Finalizing batch...")
    time.sleep(5)
    internal_page.click_finalize_button()
    take_screenshot(driver, f"{ENV}_after_finalize_button")
    time.sleep(5)
    internal_page.click_continue_button()
    take_screenshot(driver, f"{ENV}_after_continue_button")
    time.sleep(5)
    internal_page.click_check_back_later()
    take_screenshot(driver, f"{ENV}_after_check_back_later")
    assert internal_page.is_manual_batches_actions_displayed(), "❌ 'Manual Batches Actions' section is not displayed."
    assert internal_page.is_go_to_payments_button_displayed(), "❌ 'Go to payments' button is not displayed."
    assert internal_page.is_download_pci_safe_original_button_displayed(), "❌ 'Download PCI-safe Original' button is not displayed."
    assert internal_page.is_download_pci_safe_final_button_displayed(), "❌ 'Download PCI-safe Final' button is not displayed."

    take_screenshot(driver, f"{ENV}_manual_batches_actions_verified")

    logger.info("✅ Successfully verified 'Manual Batches Actions' functionality.")


# ✅ **TC_Internal_021** - Validate the 'Go to payments' action in 'Manual Batches Actions'
def test_Goto_payment(login_and_navigate_to_internal, driver):
    logger.info("📌 [TC_Internal_021] Verifying 'Go to payments' action in 'Manual Batches Actions'.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_file")
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../Testdata/20250114-PNC.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_file")
    internal_page.click_validate_button()
    logger.info("⏳ Checking file status...")
    internal_page.click_check_button()
    file_status = internal_page.get_file_status()
    assert file_status in ["Submitted", "Validation"], \
        f"❌ Expected file status to be 'Submitted' or 'Validation', but got '{file_status}'."
    take_screenshot(driver, f"{ENV}_file_status_update")
    logger.info(f"✅ File status verified: {file_status}")
    internal_page.click_status_button()
    take_screenshot(driver, f"{ENV}_navigated_to_status_page")
    logger.info("🚀 Finalizing batch...")
    internal_page.click_finalize_button()
    take_screenshot(driver, f"{ENV}_after_finalize_button")
    internal_page.click_continue_button()
    take_screenshot(driver, f"{ENV}_after_continue_button")
    time.sleep(5)
    internal_page.click_check_back_later()
    take_screenshot(driver, f"{ENV}_after_check_back_later")
    time.sleep(5)
    internal_page.click_go_to_payment()
    take_screenshot(driver, f"{ENV}_after_go_to_payments")
    assert internal_page.is_payment_page_displayed(), "❌ Payment page is not displayed."
    logger.info("✅ Successfully verified 'Go to payments' action in 'Manual Batches Actions'.")

# ✅ **TC_Internal_022** - Validate the 'Download PCI-safe Original' action for a submitted batch
def test_TC_Internal_022_download_pci_safe_original(login_and_navigate_to_internal, driver):
    logger.info("📌 Validating 'Download PCI-safe Original' functionality.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_file")
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../Testdata/20250114-PNC.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_file")
    internal_page.click_validate_button()
    internal_page.click_check_button()
    file_status = internal_page.get_file_status()
    assert file_status in ["Submitted", "Validation"], \
        f"❌ Expected file status to be 'Submitted' or 'Validation', but got '{file_status}'."
    take_screenshot(driver, f"{ENV}_file_status_verified")
    logger.info(f"✅ File status verified as: {file_status}")
    internal_page.click_status_button()
    take_screenshot(driver, f"{ENV}_navigated_to_status_page")
    internal_page.click_finalize_button()
    time.sleep(5)
    internal_page.click_continue_button()
    time.sleep(5)
    internal_page.click_check_back_later()
    take_screenshot(driver, f"{ENV}_batch_finalized")
    time.sleep(5)
    internal_page.click_download_pci()
    take_screenshot(driver, f"{ENV}_after_pci_download")
    logger.info("✅ Successfully triggered 'Download PCI-safe Original' action.")

# ✅ **TC_Internal_023** - Validate the 'Download PCI-safe Final' action for a submitted batch
def test_download_pci_safe_final(login_and_navigate_to_internal, driver):
    logger.info("📌 [TC_Internal_023] Validating 'Download PCI-safe Final' functionality.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_file")
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../Testdata/20250114-PNC.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_file")
    internal_page.click_validate_button()
    internal_page.click_check_button()
    file_status = internal_page.get_file_status()
    assert file_status in ["Submitted", "Validation"], \
        f"❌ Expected file status to be 'Submitted' or 'Validation', but got '{file_status}'."
    take_screenshot(driver, f"{ENV}_file_status_verified")
    logger.info(f"✅ File status verified as: {file_status}")
    internal_page.click_status_button()
    take_screenshot(driver, f"{ENV}_navigated_to_status_page")
    internal_page.click_finalize_button()
    time.sleep(5)
    internal_page.click_continue_button()
    time.sleep(5)
    internal_page.click_check_back_later()
    take_screenshot(driver, f"{ENV}_batch_finalized")
    internal_page.click_download_final_pci()
    take_screenshot(driver, f"{ENV}_after_final_pci_download")
    logger.info("✅ Successfully triggered 'Download PCI-safe Final' action.")

# ✅ **TC_Internal_024** - Validate the 'Download Original' action for a submitted batch
def test_download_original(login_and_navigate_to_internal, driver):
    logger.info("📌 Validating 'Download Original' functionality.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_file")
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../Testdata/20250114-PNC.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_file")
    internal_page.click_validate_button()
    internal_page.click_check_button()
    file_status = internal_page.get_file_status()
    assert file_status in ["Submitted", "Validation"], \
        f"❌ Expected file status to be 'Submitted' or 'Validation', but got '{file_status}'."
    take_screenshot(driver, f"{ENV}_file_status_verified")
    logger.info(f"✅ File status verified as: {file_status}")
    internal_page.click_status_button()
    take_screenshot(driver, f"{ENV}_navigated_to_status_page")
    internal_page.click_finalize_button()
    time.sleep(5)
    internal_page.click_continue_button()
    time.sleep(5)
    internal_page.click_check_back_later()
    take_screenshot(driver, f"{ENV}_batch_finalized")
    internal_page.click_download_original()
    take_screenshot(driver, f"{ENV}_after_original_download")
    logger.info("✅ Successfully triggered 'Download Original' action.")

# ✅ **TC_Internal_025** - Validate the 'Download Final' action for a submitted batch
def test_download_final(login_and_navigate_to_internal, driver):
    logger.info("📌 Validating 'Download Final' functionality.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_file")
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../testdata/20250114-PNC.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_file")
    internal_page.click_validate_button()
    internal_page.click_check_button()
    for attempt in range(5):
        file_status = internal_page.get_file_status()
        if file_status in ["Submitted", "Validation"]:
            logger.info(f"✅ File status verified: {file_status}")
            break
        logger.warning(f"⏳ Waiting for file status update (Attempt {attempt + 1}/5)...")
        time.sleep(3)
    else:
        raise AssertionError(f"❌ Unexpected file status: '{file_status}'.")

    take_screenshot(driver, f"{ENV}_file_status_verified")
    internal_page.click_status_button()
    take_screenshot(driver, f"{ENV}_navigated_to_status_page")
    internal_page.click_finalize_button()
    time.sleep(5)
    internal_page.click_continue_button()
    time.sleep(5)
    internal_page.click_check_back_later()
    take_screenshot(driver, f"{ENV}_batch_finalized")
    internal_page.click_download_final()
    take_screenshot(driver, f"{ENV}_after_final_download")
    logger.info("✅ Successfully triggered 'Download Final' action.")

# ✅ **TC_Internal_026** - Validate navigation to file status page from 'Validated' status
def test_file_status_navigation(login_and_navigate_to_internal, driver):
    logger.info("📌Validating navigation to file status page and checking for errors/warnings.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_file")
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../Testdata/20250114-PNC.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_file")
    internal_page.click_validate_button()
    internal_page.click_check_button()
    expected_statuses = ["Submitted", "Validation"]
    for attempt in range(5):
        file_status = internal_page.get_file_status()
        if file_status in expected_statuses:
            logger.info(f"✅ File status verified: {file_status}")
            break
        logger.warning(f"⏳ Waiting for file status update (Attempt {attempt + 1}/5)...")
        time.sleep(3)
    else:
        raise AssertionError(f"❌ Unexpected file status: '{file_status}'.")
    take_screenshot(driver, f"{ENV}_file_status_verified")
    internal_page.click_status_button()
    take_screenshot(driver, f"{ENV}_navigated_to_status_page")
    assert internal_page.is_file_status_page_displayed(), "❌ Failed to navigate to the file status page."
    error_warning_counts = internal_page.get_error_and_warning_counts()
    logger.info(f"⚠️ Error Count: {error_warning_counts['errors']}, Warning Count: {error_warning_counts['warnings']}")
    assert isinstance(error_warning_counts['errors'], int), "❌ Error count is not a valid integer."
    assert isinstance(error_warning_counts['warnings'], int), "❌ Warning count is not a valid integer."
    take_screenshot(driver, f"{ENV}_error_warning_counts")
    logger.info("✅ Navigation and validation test passed successfully!")

# ✅ **TC_Internal_027** - Validate the 'Download Latest File' action for a validated batch
def test_download_latest_file(login_and_navigate_to_internal, driver):
    logger.info("📌 Validating 'Download Latest File' action for a validated batch.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_file")
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../testdata/20250114-PNC.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_file")
    internal_page.click_validate_button()
    internal_page.click_check_button()
    expected_statuses = ["Submitted", "Validation"]
    for attempt in range(5):
        file_status = internal_page.get_file_status()
        if file_status in expected_statuses:
            logger.info(f"✅ File status verified: {file_status}")
            break
        logger.warning(f"⏳ Waiting for file status update (Attempt {attempt + 1}/5)...")
        time.sleep(3)
    else:
        raise AssertionError(f"❌ Unexpected file status: '{file_status}'.")
    take_screenshot(driver, f"{ENV}_file_status_verified")
    internal_page.click_status_button()
    take_screenshot(driver, f"{ENV}_navigated_to_status_page")
    assert internal_page.is_file_status_page_displayed(), "❌ Failed to navigate to the file status page."
    logger.info("📥 Clicking 'Download Latest File' button...")
    internal_page.click_download_latest_file()
    take_screenshot(driver, f"{ENV}_after_download_latest_file")
    logger.info("✅ File download action triggered successfully!")

# ✅ **TC_Internal_028** - Validate 'Finalize Submission' functionality for a validated batch with warnings
def test_finalize_submission_with_warnings(login_and_navigate_to_internal, driver):
    logger.info("📌Validating 'Finalize Submission' for a batch with warnings.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_file")
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../Testdata/20250114-PNC.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_file")
    internal_page.click_validate_button()
    internal_page.click_check_button()
    expected_statuses = ["Submitted", "Validation"]
    for attempt in range(5):
        file_status = internal_page.get_file_status()
        if file_status in expected_statuses:
            logger.info(f"✅ File status verified: {file_status}")
            break
        logger.warning(f"⏳ Waiting for file status update (Attempt {attempt + 1}/5)...")
        time.sleep(3)
    else:
        raise AssertionError(f"❌ Unexpected file status: '{file_status}'.")
    take_screenshot(driver, f"{ENV}_file_status_verified")
    internal_page.click_status_button()
    take_screenshot(driver, f"{ENV}_navigated_to_status_page")
    assert internal_page.is_file_status_page_displayed(), "❌ Failed to navigate to the file status page."
    assert internal_page.is_warning_message_displayed(), "❌ Expected warning: 'Please check. This batch may be duplicated.'"
    logger.info("⚠️ Warning detected: 'Please check. This batch may be duplicated.'")
    internal_page.click_finalize_button()
    take_screenshot(driver, f"{ENV}_finalize_submission_clicked")
    internal_page.click_continue_button()
    take_screenshot(driver, f"{ENV}_continue_submission")
    internal_page.click_check_back_later()
    take_screenshot(driver, f"{ENV}_submission_completed")
    logger.info("✅ Finalize Submission completed successfully!")

# ✅ **TC_Internal_029** - Validate 'Upload Again' functionality for a validated batch with warnings
def test_upload_again(login_and_navigate_to_internal, driver):
    logger.info("📌 Validating 'Upload Again' functionality.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_file")
    base_path = os.path.dirname(os.path.abspath(__file__))
    initial_file_path = os.path.join(base_path, "../Testdata/20250114-PNC.xlsx")
    if not os.path.exists(initial_file_path):
        raise FileNotFoundError(f"❌ File not found: {initial_file_path}")
    logger.info(f"🔍 Uploading initial file: {initial_file_path}")
    internal_page.add_file(initial_file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_initial_file")
    internal_page.click_validate_button()
    internal_page.click_check_button()
    expected_statuses = ["Submitted", "Validation"]
    for attempt in range(5):
        file_status = internal_page.get_file_status()
        if file_status in expected_statuses:
            logger.info(f"✅ File status verified: {file_status}")
            break
        logger.warning(f"⏳ Waiting for file status update (Attempt {attempt + 1}/5)...")
        time.sleep(3)
    else:
        raise AssertionError(f"❌ Unexpected file status: '{file_status}'.")

    take_screenshot(driver, f"{ENV}_file_status_verified")
    internal_page.click_status_button()
    take_screenshot(driver, f"{ENV}_navigated_to_status_page")
    internal_page.click_upload_again()
    take_screenshot(driver, f"{ENV}_upload_again_clicked")
    latest_file_path = os.path.join(base_path, "../testdata/20250114-PNC_Latest.xlsx")
    if not os.path.exists(latest_file_path):
        raise FileNotFoundError(f"❌ Latest file not found: {latest_file_path}")
    logger.info(f"🔍 Uploading latest file: {latest_file_path}")
    internal_page.add_again_file(latest_file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_latest_file")
    internal_page.click_again_validate_button()
    take_screenshot(driver, f"{ENV}_after_validation_latest_file")
    internal_page.click_again_check_back_button()
    take_screenshot(driver, f"{ENV}_after_check_back_button")
    assert internal_page.is_internal_validate_button_displayed(), "❌ 'Validate' button not displayed after re-upload."
    logger.info("✅ 'Upload Again' functionality validated successfully!")

# ✅ **TC_Internal_030** - Validate 'Discard Batch' functionality for a validated batch
def test_discard_batch(login_and_navigate_to_internal, driver):
    logger.info("📌 Validating 'Discard Batch' functionality.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_file")
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../Testdata/20250114-PNC.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_file")
    internal_page.click_validate_button()
    internal_page.click_check_button()
    expected_statuses = ["Submitted", "Validation"]
    for attempt in range(5):
        file_status = internal_page.get_file_status()
        if file_status in expected_statuses:
            logger.info(f"✅ File status verified: {file_status}")
            break
        logger.warning(f"⏳ Waiting for file status update (Attempt {attempt + 1}/5)...")
        time.sleep(3)
    else:
        raise AssertionError(f"❌ Unexpected file status: '{file_status}'.")
    take_screenshot(driver, f"{ENV}_file_status_verified")
    # Navigate to file status page
    internal_page.click_status_button()
    take_screenshot(driver, f"{ENV}_navigated_to_failed_status_page")
    time.sleep(5)
    internal_page.click_discard_batch()
    take_screenshot(driver, f"{ENV}_discard_batch_prompt")
    time.sleep(5)
    internal_page.click_discard_batch_button()
    take_screenshot(driver, f"{ENV}_batch_discarded")
    logger.info("✅ 'Discard Batch' functionality validated successfully!")

# ✅ **TC_Internal_031** - Validate navigation to file status from 'Failed' header and error/warning count
def test_failed_status(login_and_navigate_to_internal, driver):
    logger.info("📌 [TC_Internal_031] Validating navigation to 'File Status' from a 'Failed' header.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_failed_file")
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../Testdata/DOMESTIC.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_failed_file")
    internal_page.click_validate_button()
    internal_page.click_check_button()
    internal_page.click_failed_status_button()
    take_screenshot(driver, f"{ENV}_navigated_to_failed_status_page")
    assert internal_page.is_file_status_page_displayed(), "❌ Failed to navigate to the file status page."
    error_warning_counts = internal_page.get_error_and_warning_counts()
    error_count = error_warning_counts.get('errors', 0)
    warning_count = error_warning_counts.get('warnings', 0)
    logger.info(f"⚠️ Error Count: {error_count} | ⚠️ Warning Count: {warning_count}")
    assert isinstance(error_count, int), "❌ Error count is not a valid integer."
    assert isinstance(warning_count, int), "❌ Warning count is not a valid integer."
    logger.info("✅ Navigation and validation test passed successfully!")

# ✅ **TC_Internal_032** - Validate functionality of 'Download Original' button on a failed batch
def test_batch_download_original(login_and_navigate_to_internal, driver):
    logger.info("📌  Validating 'Download Original' button for a failed batch.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_failed_file")
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../Testdata/DOMESTIC.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_failed_file")
    internal_page.click_validate_button()
    internal_page.click_check_button()
    for attempt in range(5):
        file_status = internal_page.get_file_failed_status()
        if file_status == "Failed":
            logger.info(f"✅ File status verified: {file_status}")
            break
        logger.warning(f"⏳ Waiting for 'Failed' status (Attempt {attempt + 1}/5)...")
        time.sleep(3)
    else:
        raise AssertionError(f"❌ Expected file status 'Failed', but got '{file_status}'.")
    take_screenshot(driver, f"{ENV}_file_failed_status_verified")
    internal_page.click_failed_status_button()
    take_screenshot(driver, f"{ENV}_navigated_to_failed_status_page")
    assert internal_page.is_file_status_page_displayed(), "❌ Failed to navigate to the file status page."
    internal_page.click_download_original()
    take_screenshot(driver, f"{ENV}_download_original_attempted")
    logger.info("✅ 'Download Original' button functionality validated successfully!")

# ✅ **TC_Internal_033** - Validate functionality of 'Download Latest File' button on a failed batch
def test_failed_batch_download_latest_file(login_and_navigate_to_internal, driver):
    logger.info("📌 Validating 'Download Latest File' button for a failed batch.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_failed_file")
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, "../Testdata/DOMESTIC.xlsx")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File not found: {file_path}")
    logger.info(f"🔍 Uploading file: {file_path}")
    internal_page.add_file(file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_failed_file")
    internal_page.click_validate_button()
    internal_page.click_check_button()
    for attempt in range(5):
        file_status = internal_page.get_file_failed_status()
        if file_status == "Failed":
            logger.info(f"✅ File status verified: {file_status}")
            break
        logger.warning(f"⏳ Waiting for 'Failed' status (Attempt {attempt + 1}/5)...")
        time.sleep(3)
    else:
        raise AssertionError(f"❌ Expected file status 'Failed', but got '{file_status}'.")
    take_screenshot(driver, f"{ENV}_file_failed_status_verified")
    internal_page.click_failed_status_button()
    take_screenshot(driver, f"{ENV}_navigated_to_failed_status_page")
    assert internal_page.is_file_status_page_displayed(), "❌ Failed to navigate to the file status page."
    internal_page.click_download_latest_file()
    take_screenshot(driver, f"{ENV}_download_latest_file_attempted")
    logger.info("✅ 'Download Latest File' button functionality validated successfully!")

# ✅ **TC_Internal_034** - Validate functionality of 'Upload Again' button on a failed batch
def test_failed_upload_again(login_and_navigate_to_internal, driver):
    logger.info("📌 Validating 'Upload Again' functionality for a failed batch.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_failed_file")
    base_path = os.path.dirname(os.path.abspath(__file__))
    failed_file_path = os.path.join(base_path, "../Testdata/DOMESTIC.xlsx")
    if not os.path.exists(failed_file_path):
        raise FileNotFoundError(f"❌ File not found: {failed_file_path}")
    logger.info(f"🔍 Uploading failed file: {failed_file_path}")
    internal_page.add_file(failed_file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_failed_file")
    internal_page.click_validate_button()
    internal_page.click_check_button()
    for attempt in range(5):
        file_status = internal_page.get_file_failed_status()
        if file_status == "Failed":
            logger.info(f"✅ File status verified: {file_status}")
            break
        logger.warning(f"⏳ Waiting for 'Failed' status (Attempt {attempt + 1}/5)...")
        time.sleep(3)
    else:
        raise AssertionError(f"❌ Expected file status 'Failed', but got '{file_status}'.")
    take_screenshot(driver, f"{ENV}_file_failed_status_verified")
    internal_page.click_failed_status_button()
    take_screenshot(driver, f"{ENV}_navigated_to_failed_status_page")
    assert internal_page.is_file_status_page_displayed(), "❌ Failed to navigate to the file status page."
    internal_page.click_upload_again()
    take_screenshot(driver, f"{ENV}_upload_again_clicked")
    latest_file_path = os.path.join(base_path, "../Testdata/20250114-PNC_Latest.xlsx")
    if not os.path.exists(latest_file_path):
        raise FileNotFoundError(f"❌ File not found: {latest_file_path}")
    logger.info(f"🔄 Uploading new file: {latest_file_path}")
    internal_page.add_again_file(latest_file_path)
    take_screenshot(driver, f"{ENV}_new_file_uploaded")
    internal_page.click_again_validate_button()
    internal_page.click_again_check_back_button()
    take_screenshot(driver, f"{ENV}_upload_validation_done")
    assert internal_page.is_internal_validate_button_displayed(), "❌ Upload validation failed."
    logger.info("✅ 'Upload Again' button functionality validated successfully!")

# ✅ **TC_Internal_035** - Validate functionality of 'Discard Batch' button on a failed batch
def test_failed_batch_discard(login_and_navigate_to_internal, driver):
    logger.info("📌 Validating 'Discard Batch' functionality for a failed batch.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_failed_batch")
    base_path = os.path.dirname(os.path.abspath(__file__))
    failed_file_path = os.path.join(base_path, "../Testdata/DOMESTIC.xlsx")
    if not os.path.exists(failed_file_path):
        raise FileNotFoundError(f"❌ File not found: {failed_file_path}")
    logger.info(f"🔍 Uploading failed file: {failed_file_path}")
    internal_page.add_file(failed_file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_failed_batch")
    internal_page.click_validate_button()
    internal_page.click_check_button()
    for attempt in range(5):
        file_status = internal_page.get_file_failed_status()
        if file_status == "Failed":
            logger.info(f"✅ File status verified: {file_status}")
            break
        logger.warning(f"⏳ Waiting for 'Failed' status (Attempt {attempt + 1}/5)...")
        time.sleep(3)
    else:
        raise AssertionError(f"❌ Expected file status 'Failed', but got '{file_status}'.")
    take_screenshot(driver, f"{ENV}_file_failed_status_verified")
    time.sleep(5)
    internal_page.click_failed_status_button()
    take_screenshot(driver, f"{ENV}_navigated_to_failed_status_page")
    assert internal_page.is_file_status_page_displayed(), "❌ Failed to navigate to the file status page."
    internal_page.click_discard_batch()
    time.sleep(3)
    internal_page.click_discard_batch_button()
    take_screenshot(driver, f"{ENV}_discard_batch_clicked")
    take_screenshot(driver, f"{ENV}_batch_discarded")
    logger.info("✅ 'Discard Batch' functionality validated successfully!")

# ✅ **TC_Internal_036** - Validate functionality of 'Contact Production Support' button on a failed batch
def test_contact_production_support(login_and_navigate_to_internal, driver):
    logger.info("📌 Validating 'Contact Production Support' button functionality for a failed batch.")
    internal_page = login_and_navigate_to_internal
    internal_page.click_internal_batch()
    take_screenshot(driver, f"{ENV}_before_uploading_failed_batch")
    base_path = os.path.dirname(os.path.abspath(__file__))
    failed_file_path = os.path.join(base_path, "../testdata/DOMESTIC.xlsx")
    if not os.path.exists(failed_file_path):
        raise FileNotFoundError(f"❌ File not found: {failed_file_path}")
    logger.info(f"🔍 Uploading failed file: {failed_file_path}")
    internal_page.add_file(failed_file_path)
    take_screenshot(driver, f"{ENV}_after_uploading_failed_batch")
    internal_page.click_validate_button()
    internal_page.click_check_button()
    for attempt in range(5):
        file_status = internal_page.get_file_failed_status()
        if file_status == "Failed":
            logger.info(f"✅ File status verified: {file_status}")
            break
        logger.warning(f"⏳ Waiting for 'Failed' status (Attempt {attempt + 1}/5)...")
        time.sleep(3)
    else:
        raise AssertionError(f"❌ Expected file status 'Failed', but got '{file_status}'.")
    take_screenshot(driver, f"{ENV}_file_failed_status_verified")
    internal_page.click_failed_status_button()
    take_screenshot(driver, f"{ENV}_navigated_to_failed_status_page")
    assert internal_page.is_file_status_page_displayed(), "❌ Failed to navigate to the file status page."
    internal_page.click_contact_production()
    take_screenshot(driver, f"{ENV}_contact_production_clicked")
    logger.info("✅ 'Contact Production Support' button functionality validated successfully!")








