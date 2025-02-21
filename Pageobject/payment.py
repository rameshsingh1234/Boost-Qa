import logging
import time
from selenium.common import NoSuchElementException, TimeoutException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PaymentPage:
    def __init__(self, driver):
        self.driver = driver
        # Locators
        self.payment_record = (By.XPATH, '//*[@id="root"]/div[2]/div/div[2]/div[2]/div/div/div[1]/div[5]')
        self.payment_tab = (By.XPATH, '//*[@id="root"]/section/div[1]/div/div[1]/div[3]/div/button[1]')
        self.received_date = (By.XPATH, "//div[contains(text(), 'Received Date')]/following-sibling::div")
        self.process_date = (By.XPATH, "//div[contains(text(), 'Process Date')]/following-sibling::div")
        self.payment_status = (By.XPATH, "//div[contains(text(), 'Payment Status')]/following-sibling::div")
        self.source_name = (By.XPATH, "//div[contains(text(), 'Source Name')]/following-sibling::div")
        self.buyer_name = (By.XPATH, "//div[contains(text(), 'Buyer Name')]/following-sibling::div")
        self.merchant_name = (By.XPATH, "//div[contains(text(), 'Merchant Name')]/following-sibling::div")
        self.add_note = (By.XPATH, '//*[@id="action_item_add_note_to_payment"]/p')
        self.note_text_area = (By.XPATH, '//*[@id="add-note"]')
        self.submit = (By.XPATH, '//*[@id="addNotes-dialog"]/div[3]/div/div/section/button[2]')
        self.cancel = (By.XPATH, '//*[@id="addNotes-dialog"]/div[3]/div/div/section/button[1]')
        self.download_payment_details = (By.XPATH, '//*[@id="action_item_download_payment_details"]/p')
        self.link_source = (By.XPATH, '//*[@id="action_item_link_source"]/p')

    def click_payment_record(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.payment_record)).click()
            logging.info("Clicked on the payment record.")
        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f"Failed to click payment record: {e}")
            raise

    def is_payment_tab_displayed(self):
        try:
            return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.payment_tab)).is_displayed()
        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f"Payment tab not displayed: {e}")
            return False

    def get_received_date(self):
        try:
            return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.received_date)).text
        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f"Failed to get received date: {e}")
            raise

    def get_process_date(self):
        try:
            return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.process_date)).text
        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f"Failed to get process date: {e}")
            raise

    def get_payment_status(self):
        try:
            return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.payment_status)).text
        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f"Failed to get payment status: {e}")
            raise

    def get_source_name(self):
        try:
            return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.source_name)).text
        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f"Failed to get source name: {e}")
            raise

    def get_buyer_name(self):
        try:
            return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.buyer_name)).text
        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f"Failed to get buyer name: {e}")
            raise

    def get_merchant_name(self):
        try:
            return WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.merchant_name)).text
        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f"Failed to get merchant name: {e}")
            raise

    def click_add_note(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.add_note)).click()
            logging.info("Clicked on 'Add Note'.")
        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f"Failed to click 'Add Note': {e}")
            raise
    # def click_note_text(self):
    #     try:
    #         WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.note_text_area)).click()
    #         logging.info("Clicked on 'Add Note'.")
    #     except (NoSuchElementException, TimeoutException) as e:
    #         logging.error(f"Failed to click 'Add Note': {e}")
    #         raise
    #
    # def enter_note_text(self, note_text):
    #     """Enter text into the note text area."""
    #     try:
    #         WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.note_text_area)).send_keys(note_text)
    #         logging.info(f"Entered note text: {note_text}")
    #     except Exception as e:
    #         logging.error(f"Failed to enter note text: {e}")
    #         raise

    def click_download_payment_details(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.download_payment_details)).click()
            logging.info("Clicked on 'Download Payment Details'.")
        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f"Failed to click 'Download Payment Details': {e}")
            raise

    def click_link_source(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.link_source)).click()
            logging.info("Clicked on 'Link Source'.")
        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f"Failed to click 'Link Source': {e}")
            raise

    def click_cancel_button(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.cancel)).click()
            logging.info("Clicked on 'cancel button'.")
        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f"Failed to click 'cancel button': {e}")
            raise

    def click_submit_button(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.submit)).click()
            logging.info("Clicked on 'cancel button'.")
        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f"Failed to click 'cancel button': {e}")
            raise

    def enter_note_text(self, note_text):
        """Enter text into the note text area."""
        try:
            # Wait for the text area to be visible and interactable
            text_area = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.note_text_area))
            logging.info(f"Text area found: {text_area}")
            text_area.clear()  # Clear any existing text
            text_area.send_keys(note_text)
            logging.info(f"Entered note text: {note_text}")
        except TimeoutException:
            logging.error("❌ Note text area is not interactable.")
            # Take a screenshot for debugging
            self.driver.save_screenshot("note_text_area_error.png")
            raise

    def submit_note(self):
        """Click the 'Submit' button to add the note."""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.submit)).click()