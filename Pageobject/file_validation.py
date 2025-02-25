from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PaymentPage:
    def __init__(self, driver):
        self.driver = driver

    # Locators
    BUYER_NAME_HEADER = (By.XPATH, '//*[@id="root"]/section/div[1]/div/div[2]/div/div/div[2]/div/div/div[5]/div[1]')  # Replace with the actual header locator
    MERCHANT_NAME_HEADER = (By.XPATH, '//*[@id="root"]/section/div[1]/div/div[2]/div/div/div[2]/div/div/div[6]/div[1]')  # Replace with the actual header locator
    SOURCE_NAME = (By.XPATH, '//*[@id="root"]/section/div[1]/div/div[2]/div/div/div[2]/div/div/div[4]/div[1]')
    TOTAL_AMOUNT_PAYMENT =(By.XPATH, '//span[contains(text(), "Total Payments Amount:")]')

    def is_buyer_name_header_displayed(self):
        """Check if the Buyer Name header is displayed."""
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.BUYER_NAME_HEADER)
        ).is_displayed()

    def is_merchant_name_header_displayed(self):
        """Check if the Merchant Name header is displayed."""
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.MERCHANT_NAME_HEADER)
        ).is_displayed()

    def is_source_name_header_displayed(self):
        """Check if the Merchant Name header is displayed."""
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.SOURCE_NAME)
        ).text

    def is_total_payment_amount(self):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.SOURCE_NAME)
        ).text




