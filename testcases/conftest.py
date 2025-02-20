import os
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from Utilities.logger import logger  # Import centralized logger

def pytest_addoption(parser):
    """ ✅ Add CLI options for environment and headless mode """
    parser.addoption("--env", action="store", default="DEV", help="Choose environment: DEV, UAT, PROD")
    parser.addoption("--headless", action="store_true", help="Run tests in headless mode")

def pytest_configure(config):
    """ ✅ Ensure ENVIRONMENT is correctly set before anything imports logger.py """
    env = config.getoption("--env") or "DEV"
    os.environ["ENVIRONMENT"] = env.upper()  # ✅ Set it globally before imports
    print(f"🌍 Using environment: {os.environ['ENVIRONMENT']}")  # Debugging log

# ✅ Load environment variables from .env file (if used)
load_dotenv()

@pytest.fixture(scope="function")
def driver(request):
    """ ✅ Fixture to initialize and quit WebDriver with optional headless mode """
    browser_name = os.getenv('WEB_BROWSER', 'chrome').lower()
    headless = request.config.getoption("--headless")  # Get headless mode flag

    logger.info(f"Launching browser: {browser_name} | Headless mode: {headless}")

    if browser_name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")  # Enable headless mode in Chrome
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920x1080")
        service = ChromeService()
        driver = webdriver.Chrome(service=service, options=options)

    elif browser_name == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")  # Enable headless mode in Firefox
        service = FirefoxService()
        driver = webdriver.Firefox(service=service, options=options)

    elif browser_name == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless")  # Enable headless mode in Edge
        service = EdgeService()
        driver = webdriver.Edge(service=service, options=options)

    else:
        logger.error(f"Unsupported browser: {browser_name}")
        raise ValueError(f"Unsupported browser: {browser_name}")

    driver.maximize_window()
    driver.implicitly_wait(10)
    logger.info("Browser session started.")

    yield driver  # Pass WebDriver instance to test function

    driver.quit()
    logger.info("Browser session ended.")

#



#
#
# import os
# import pytest
# from dotenv import load_dotenv
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.firefox.service import Service as FirefoxService
# from selenium.webdriver.edge.service import Service as EdgeService
# from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.firefox.options import Options as FirefoxOptions
# from selenium.webdriver.edge.options import Options as EdgeOptions
# from Utilities.logger import logger  # Import centralized logger
#
# def pytest_addoption(parser):
#     """ ✅ Add CLI options for environment and headless mode """
#     parser.addoption("--env", action="store", default="DEV", help="Choose environment: DEV, UAT, PROD")
#     parser.addoption("--headless", action="store_true", help="Run tests in headless mode")
#
# def pytest_configure(config):
#     """ ✅ Ensure ENVIRONMENT is correctly set before anything imports logger.py """
#     env = config.getoption("--env") or "DEV"
#     os.environ["ENVIRONMENT"] = env.upper()  # ✅ Set it globally before imports
#     print(f"🌍 Using environment: {os.environ['ENVIRONMENT']}")  # Debugging log
#
# # ✅ Load environment variables from .env file (if used)
# load_dotenv()
#
# @pytest.fixture(scope="function")
# def driver(request):
#     """ ✅ Fixture to initialize and quit WebDriver with optional headless mode """
#     browser_name = os.getenv('WEB_BROWSER', 'chrome').lower()
#     headless = request.config.getoption("--headless")  # Get headless mode flag
#
#     logger.info(f"Launching browser: {browser_name} | Headless mode: {headless}")
#
#     if browser_name == "chrome":
#         options = ChromeOptions()
#         if headless:
#             options.add_argument("--headless=new")  # Enable headless mode in Chrome
#             options.add_argument("--disable-gpu")
#             options.add_argument("--window-size=1920x1080")
#         service = ChromeService()
#         driver = webdriver.Chrome(service=service, options=options)
#
#     elif browser_name == "firefox":
#         options = FirefoxOptions()
#         if headless:
#             options.add_argument("--headless")  # Enable headless mode in Firefox
#         service = FirefoxService()
#         driver = webdriver.Firefox(service=service, options=options)
#
#     elif browser_name == "edge":
#         options = EdgeOptions()
#         if headless:
#             options.add_argument("--headless")  # Enable headless mode in Edge
#         service = EdgeService()
#         driver = webdriver.Edge(service=service, options=options)
#
#     else:
#         logger.error(f"Unsupported browser: {browser_name}")
#         raise ValueError(f"Unsupported browser: {browser_name}")
#
#     driver.maximize_window()
#     driver.implicitly_wait(10)
#     logger.info("Browser session started.")
#
#     yield driver  # Pass WebDriver instance to test function
#
#     driver.quit()
#     logger.info("Browser session ended.")






















# import os
# import pytest
# from dotenv import load_dotenv
#
# def pytest_addoption(parser):
#     """ ✅ Add a custom pytest option for selecting an environment. """
#     parser.addoption(
#         "--env", action="store", default="DEV", help="Choose environment: DEV, UAT, PROD"
#     )
#
# def pytest_configure(config):
#     """ ✅ Ensure ENVIRONMENT is correctly set before anything imports logger.py """
#     env = config.getoption("--env") or "DEV"
#     os.environ["ENVIRONMENT"] = env.upper()  # ✅ Set it globally before imports
#     print(f"🌍 Using environment: {os.environ['ENVIRONMENT']}")  # Debugging log
#
# # ✅ Load environment variables from .env file (if used)
# load_dotenv()
#
#
# # ✅ Only import logger AFTER setting `ENVIRONMENT`
# from Utilities.logger import logger
#
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.firefox.service import Service as FirefoxService
# from selenium.webdriver.edge.service import Service as EdgeService
# from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.firefox.options import Options as FirefoxOptions
# from selenium.webdriver.edge.options import Options as EdgeOptions
#
# @pytest.fixture(scope="function")
# def driver():
#     """Fixture to initialize and quit WebDriver per test function."""
#     browser_name = os.getenv('WEB_BROWSER', 'chrome').lower()
#
#     logger.info(f"Launching browser: {browser_name}")
#
#     if browser_name == "chrome":
#         options = ChromeOptions()
#         service = ChromeService()
#         driver = webdriver.Chrome(service=service, options=options)
#
#     elif browser_name == "firefox":
#         options = FirefoxOptions()
#         service = FirefoxService()
#         driver = webdriver.Firefox(service=service, options=options)
#
#     elif browser_name == "edge":
#         options = EdgeOptions()
#         service = EdgeService()
#         driver = webdriver.Edge(service=service, options=options)
#
#     else:
#         logger.error(f"Unsupported browser: {browser_name}")
#         raise ValueError(f"Unsupported browser: {browser_name}")
#
#     driver.maximize_window()
#     driver.implicitly_wait(10)
#     logger.info("Browser session started.")
#
#     yield driver  # Pass WebDriver instance to test function
#
#     driver.quit()
#     logger.info("Browser session ended.")
#






















# from Utilities.logger import logger
# from dotenv import load_dotenv
# import os
# import pytest
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.firefox.service import Service as FirefoxService
# from selenium.webdriver.edge.service import Service as EdgeService
# from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.firefox.options import Options as FirefoxOptions
# from selenium.webdriver.edge.options import Options as EdgeOptions
# # from Utilities.utils import get_config
# from Utilities.logger import logger  # Import logger
#
# # Load environment variables from .env file
# load_dotenv()
#
# def pytest_addoption(parser):
#     """Add a custom pytest option for selecting an environment."""
#     parser.addoption(
#         "--env", action="store", default="DEV", help="Choose environment: DEV, UAT, PROD"
#     )
#
#
# @pytest.fixture(scope="function")  # Each test gets a fresh browser instance
# def driver():
#     """Fixture to initialize and quit WebDriver per test function."""
#     # Fetch the browser name dynamically based on environment setting
#     browser_name = os.getenv('WEB_BROWSER').lower() if os.getenv('WEB_BROWSER') else 'chrome'
#
#     logger.info(f"Launching browser: {browser_name}")
#
#     if browser_name == "chrome":
#         options = ChromeOptions()
#         service = ChromeService()  # Auto-manages ChromeDriver
#         driver = webdriver.Chrome(service=service, options=options)
#
#     elif browser_name == "firefox":
#         options = FirefoxOptions()
#         service = FirefoxService()
#         driver = webdriver.Firefox(service=service, options=options)
#
#     elif browser_name == "edge":
#         options = EdgeOptions()
#         service = EdgeService()
#         driver = webdriver.Edge(service=service, options=options)
#
#     else:
#         logger.error(f"Unsupported browser: {browser_name}")
#         raise ValueError(f"Unsupported browser: {browser_name}")
#
#     driver.maximize_window()
#     driver.implicitly_wait(10)  # You might want to configure this dynamically as well
#     logger.info("Browser session started.")
#
#     yield driver  # Pass WebDriver instance to test function
#
#     driver.quit()
#     logger.info("Browser session ended.")











#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # import pytest
# # from selenium import webdriver
# # from selenium.webdriver.chrome.service import Service as ChromeService
# # from selenium.webdriver.firefox.service import Service as FirefoxService
# # from selenium.webdriver.edge.service import Service as EdgeService
# # from selenium.webdriver.chrome.options import Options as ChromeOptions
# # from selenium.webdriver.firefox.options import Options as FirefoxOptions
# # from selenium.webdriver.edge.options import Options as EdgeOptions
# # from Utilities.utils import get_config
# # from Utilities.logger import logger  # Import logger
# #
# # config = get_config()
# #
# #
# # @pytest.fixture(scope="function")  # ✅ Each test gets a fresh browser instance
# # def driver():
# #     """Fixture to initialize and quit WebDriver per test function."""
# #     browser_name = config.get('WEB', 'browser').lower()
# #
# #     logger.info(f"Launching browser: {browser_name}")
# #
# #     if browser_name == "chrome":
# #         options = ChromeOptions()
# #         service = ChromeService()  # Auto-manages ChromeDriver
# #         driver = webdriver.Chrome(service=service, options=options)
# #
# #     elif browser_name == "firefox":
# #         options = FirefoxOptions()
# #         service = FirefoxService()
# #         driver = webdriver.Firefox(service=service, options=options)
# #
# #     elif browser_name == "edge":
# #         options = EdgeOptions()
# #         service = EdgeService()
# #         driver = webdriver.Edge(service=service, options=options)
# #
# #     else:
# #         logger.error(f"Unsupported browser: {browser_name}")
# #         raise ValueError(f"Unsupported browser: {browser_name}")
# #
# #     driver.maximize_window()
# #     driver.implicitly_wait(10)
# #     logger.info("Browser session started.")
# #
# #     yield driver  # Pass WebDriver instance to test function
# #
# #     driver.quit()
# #     logger.info("Browser session ended.")
# #
# #
