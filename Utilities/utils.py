import os
import shutil
import pytest
from datetime import datetime
from Utilities.logger import logger  # Import centralized logger

# ✅ Fetch environment dynamically (Default to DEV)
ENV = os.getenv("ENVIRONMENT", "DEV").upper()

# ✅ Define Screenshot Paths
SCREENSHOT_DIR = os.path.join(os.getcwd(), "Screenshots", ENV)  # Store per environment
ARCHIVE_DIR = os.path.join(SCREENSHOT_DIR, "archive")  # Archive folder


# ✅ Archive old Screenshots before running tests
def archive_old_screenshots():
    """Moves old Screenshots to an archive folder before new test execution."""
    os.makedirs(ARCHIVE_DIR, exist_ok=True)  # Ensure archive directory exists

    for file in os.listdir(SCREENSHOT_DIR):
        if file.endswith(".png") and not file.startswith("archive"):
            old_screenshot = os.path.join(SCREENSHOT_DIR, file)
            new_archive_path = os.path.join(ARCHIVE_DIR, file)

            try:
                shutil.move(old_screenshot, new_archive_path)  # Move file to archive
                logger.info(f"📂 Archived old screenshot: {file}")
            except Exception as e:
                logger.error(f"❌ Failed to archive {file}: {e}")


# ✅ Capture Screenshot with Correct Naming Convention
def take_screenshot(driver, test_name):
    """Captures a screenshot and saves it with correct format inside the environment folder."""

    # ✅ Ensure Screenshot directory exists
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    # ✅ Generate filename format: ENV_testname_YYYY-MM-DD_HH-MM-SS.png
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_filename = f"{test_name}_{timestamp}.png"

    # ✅ Define the full path
    screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_filename)

    try:
        driver.save_screenshot(screenshot_path)
        logger.info(f"✅ Screenshot saved: {screenshot_path}")
        return screenshot_path  # Return path for pytest attachment
    except Exception as e:
        logger.error(f"❌ Failed to take screenshot: {e}")
        return None


# ✅ Fetch Environment-Specific Test Data
def get_test_data(env=None):
    """
    Dynamically fetches test data from system environment variables based on the set environment.

    :param env: Environment variable (DEV, UAT, PROD)
    :return: Dictionary of test data for the selected environment
    """
    if not env:
        env = os.getenv("ENVIRONMENT", "DEV").upper()  # Read from system env

    prefix = f"{env}_"  # Prefix for environment variables

    # Fetch all matching environment variables dynamically
    test_data = {
        key[len(prefix):].lower(): value
        for key, value in os.environ.items()
        if key.startswith(prefix) and value
    }

    if not test_data:
        logger.error(f"❌ No environment variables found for {env}. Please check your settings.")
        raise ValueError(f"❌ Missing environment variables for {env}")

    logger.info(f"✅ Test data loaded for {env} environment: {test_data}")
    return test_data


# ✅ Pytest Fixture to Inject Test Data into Tests
@pytest.fixture(scope="function")
def test_data(request):
    """Pytest fixture to load test data dynamically from system environment based on --env parameter."""
    env = request.config.getoption("--env")  # Capture the --env parameter from pytest
    return get_test_data(env)




# import configparser
# import os
#
# import pytest
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.firefox.service import Service as FirefoxService
# from selenium.webdriver.edge.service import Service as EdgeService
# from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.firefox.options import Options as FirefoxOptions
# from selenium.webdriver.edge.options import Options as EdgeOptions
# from Utilities.logger import logger  # Import centralized logger
#
#
#
# SCREENSHOT_DIR = os.path.join(os.getcwd(), "Screenshots")
#
# def take_screenshot(driver, filename):
#     """Captures a screenshot and saves it to the 'Screenshots' directory."""
#     # Ensure the directory exists
#     os.makedirs(SCREENSHOT_DIR, exist_ok=True)
#     # Generate the full path for the screenshot
#     screenshot_path = os.path.join(SCREENSHOT_DIR, filename)
#     try:
#         driver.save_screenshot(screenshot_path)
#         print(f"✅ Screenshot saved: {screenshot_path}")
#         return screenshot_path  # Return the path for pytest attachment
#     except Exception as e:
#         print(f"❌ Failed to take screenshot: {e}")
#         return None
#
#
# def get_test_data(env=None):
#     """
#     Dynamically fetches test data from system environment variables based on the set environment.
#
#     :param env: Environment variable (DEV, UAT, PROD) passed from main.py
#     :return: Dictionary of test data for the selected environment
#     """
#     if not env:
#         env = os.getenv("ENVIRONMENT", None)  # Read from system env if not passed
#         if not env:
#             raise ValueError("❌ ERROR: No environment variable set. Use --env=DEV/UAT/PROD.")
#
#     env = env.upper()  # Ensure uppercase for consistency
#     prefix = f"{env}_"
#
#     # Fetch all environment variables that match the selected environment
#     test_data = {
#         key[len(prefix):].lower(): value
#         for key, value in os.environ.items()
#         if key.startswith(prefix) and value
#     }
#
#     if not test_data:
#         logger.error(f"❌ No environment variables found for {env}. Please check your settings.")
#         raise ValueError(f"❌ Missing environment variables for {env}")
#
#     logger.info(f"✅ Test data loaded for {env} environment: {test_data}")
#     return test_data
# # Pytest fixture to inject test data into tests
#
# @pytest.fixture(scope="function")
# def test_data(request):
#     """Pytest fixture to load test data dynamically from system environment based on --env parameter."""
#     env = request.config.getoption("--env")  # Capture the --env parameter from pytest
#     return get_test_data(env)
#
