import logging
import os
import time
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


##

class InternalPage:
    def __init__(self, driver):
        self.driver = driver
        self.dropdown = '//*[@id="root"]/header/nav/div/ul/li[2]/button'
        self.dropdown_option = '//*[@id="Sources-tables"]/div[3]/ul/li[3]'
        self.internal_text = '//*[@id="root"]/div[2]/section/h3'
        self.internal_batch = '//*[@id="grid-actions"]/button[1]'
        self.adding_text = '//*[@id="root"]/h1'
        self.created_header = '//*[@id="root"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div[1]/div/div[1]/span/span'
        self.batch_header = '//*[@id="root"]/div[2]/div/div[2]/div[1]/div/div/div[3]/div[1]/div/div[1]/span'
        self.file_header = '//*[@id="root"]/div[2]/div/div[2]/div[1]/div/div/div[5]/div[1]/div/div[1]/span/span'
        self.status_header = '//*[@id="root"]/div[2]/div/div[2]/div[1]/div/div/div[4]/div[1]/div/div[1]/span/span'
        self.download_file = '//*[@id="root"]/section/div[1]/div/section/h5'
        self.upload_file = '//*[@id="root"]/section/div[2]/div/section[1]/section/h5'
        self.download_template1_button = '//*[@id="root"]/section/div[1]/div/ul/li[1]/button'
        self.download_template2_button = '//*[@id="root"]/section/div[1]/div/ul/li[2]/button'
        self.download_template3_button = '//*[@id="root"]/section/div[1]/div/ul/li[3]/button'
        self.download_template4_button = '//*[@id="root"]/section/div[1]/div/ul/li[4]/button'
        self.back_arrow = '//*[@id="root"]/section/button'
        self.temp_dropdown = '//*[@id="root"]/section/div[2]/div/section[1]/div/div'
        self.Domestic_Payments_dropdown = 'Template Domestic Payments'
        self.upload_button = '//*[@id="root"]/section/div[2]/div/section[2]/input'
        self.validate_button = '//*[@id="root"]/section/div[2]/div/div/button'
        self.Domestic_Payments_sourcelink_dropdown = "Template Domestic Payments with Source Link(s)"
        self.International_payments = 'Template International Payments'
        self.Commerce_payment = 'Template Commerce Payments'
        self.error_message_file = '//*[@id="root"]/section/div[2]/div/section[2]/section/span'
        self.upload_filename = '//*[@id="root"]/section/div[2]/div/section[2]/section/ul/li/p'
        self.popup_message = '//*[@id="upload-status-notification"]/div'
        self.check_back = '//*[@id="upload-status-notification"]/div[3]/div/div/div/button'
        self.file_status_submit = '//*[@id="root"]/div[2]/div/div[2]/div[2]/div/div/div[7]/div[5]/div/span'
        self.file_status_validate = '//*[@id="root"]/div[2]/div/div[2]/div[2]/div/div/div[1]/div[5]/div/span[1]'
        self.file_status_failed = '//*[@id="root"]/div[2]/div/div[2]/div[2]/div/div/div[1]/div[5]/div/span[1]'
        self.total_payment = '//*[@id="root"]/section/div[1]/div/div[1]/div[3]/p[2]/span[1]'
        self.total_invoice = '//*[@id="root"]/section/div[1]/div/div[1]/div[3]/p[2]/span[3]'
        self.error = '//*[@id="root"]/section/div[1]/div/div[1]/div[2]/span'
        self.warring = '//*[@id="root"]/section/div[1]/div/div[1]/div[2]/span'
        self.finalize_submission = '//*[@id="action_item_finalize_submission"]/div'
        self.continue_submission = '//*[@id="finalize"]/div[3]/div/div/div/button[2]'
        self.manual_batches_actions = '//*[@id="root"]/section/div[2]/h3'
        self.go_to_payments_button = '//*[@id="action_item_go_to_payments"]/p'
        self.download_pci_safe_original_button = '//*[@id="action_item_download_pci_safe_original"]/p'
        self.download_pci_safe_final_button = '//*[@id="action_item_download_pci_safe_final"]/p'
        self.payment_page = '//*[@id="root"]/div[2]/section/h3'
        self.check_back_later = '/html/body/div[5]/div[3]/div/div/div/button'
        self.download_pci = '//*[@id="action_item_download_pci_safe_original"]/p'
        self.download_original = '//*[@id="action_item_download_original"]/p'
        self.download_final = '//*[@id="action_item_download_final"]/p'
        self.file_status = ' //*[@id="root"]/section/div[1]/div/div[3]/p[2]'
        self.download_latest = '//*[@id="action_item_download_latest_file"]/p'
        self.warring_message = '//*[@id="root"]/section/div[1]/div/div[2]'
        self.upload_again = '//*[@id="action_item_upload_again"]/p'
        self.upload_again_button= '//*[@id="upload-again"]/div[3]/div/div/section/section[2]/input'
        self.again_validate_button = '//*[@id="upload-again"]/div[3]/div/div/section/div/button'
        self.again_check_back_latter = '//*[@id="upload-status-notification"]/div[3]/div/div/div/button'
        self.internal_page_validate = '//*[@id="root"]/div[2]/div/div[2]/div[2]/div/div/div[1]/div[5]/div/span[1]'
        self.discard_batch = '//*[@id="action_item_discard_batch"]'
        self.discard_button ='//*[@id="discard-batch"]/div[3]/div/div/div/button[2]'
        self.contact_production = '//*[@id="action_item_contact_production_support"]/p'
        # self.success_message = '//*[@id="successMessage"]'

    def click_dropdown(self):
        self.driver.find_element(By.XPATH, self.dropdown).click()

    def select_dropdown_option(self):
        self.driver.find_element(By.XPATH, self.dropdown_option).click()

    def is_internal_displayed(self):
        """Check if 'Dynamic Boost Status' text is displayed on the dashboard."""
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.internal_text))
            ).is_displayed()
        except:
            return False

    def click_internal_batch(self):
        self.driver.find_element(By.XPATH, self.internal_batch).click()

    def is_adding_batch_displayed(self):

        try:
            return WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.adding_text))
            ).is_displayed()
        except:
            return False

    def is_element_visible(self, xpath):
        """Generic method to check if an element is visible on the page."""
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            ).is_displayed()
        except TimeoutException:
            return False

    def are_key_elements_visible(self):
        """Verify that the key columns are displayed on the 'Internal' page."""
        return all([
            self.is_element_visible(self.created_header),
            self.is_element_visible(self.batch_header),
            self.is_element_visible(self.file_header),
            self.is_element_visible(self.status_header)
        ])

    def are_download_upload_sections_visible(self):
        """Verify that 'Download Files' and 'Upload File' sections are present."""
        try:
            download_visible = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.download_file))
            ).is_displayed()
            upload_visible = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.upload_file))
            ).is_displayed()
            return download_visible and upload_visible
        except TimeoutException:
            return False

    def click_download_template1(self):
        """Click the 'Download' button for 'Template Domestic Payments'."""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.download_template1_button))
        ).click()

    def click_download_template2(self):
        """Click the 'Download' button for 'Template Domestic Payments'."""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.download_template2_button))
        ).click()

    def click_download_template3(self):
        """Click the 'Download' button for 'Template Domestic Payments'."""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.download_template3_button))
        ).click()

    def click_download_template4(self):
        """Click the 'Download' button for 'Template Domestic Payments'."""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.download_template4_button))
        ).click()

    def is_file_downloaded(self, download_dir, file_name, timeout=15):
        """Verify if the file is downloaded within the timeout period."""
        file_path = os.path.join(download_dir, file_name)
        start_time = time.time()

        while time.time() - start_time < timeout:
            # Check if file exists and is not a partial download
            if os.path.exists(file_path) and not file_name.endswith('.crdownload'):
                print(f"File found: {file_path}")  # Debug log
                return True
            else:
                print(f"File not found or still downloading: {file_path}")  # Debug log

            time.sleep(1)  # Reduced sleep time for quicker checks

        return False

    def is_option_clickable(self, option_name):
        option = self.driver.find_element(By.XPATH, [option_name])
        return option.is_enabled() and option.is_displayed()

    def click_back_arrow(self):
        self.driver.find_element(By.XPATH, self.back_arrow).click()

    def click_template_dropdown(self):
        self.driver.find_element(By.XPATH, self.temp_dropdown).click()

    def click_template_domestic_file(self):
        self.driver.find_element(By.NAME, self.Domestic_Payments_dropdown).click()

    # def add_file(self, file_path):
    #     self.driver.find_element(By.XPATH, self.upload_button).send_keys(file_path)
    def add_file(self, file_name):
        """Uploads a file by sending the file path to the upload button."""
        file_path = os.path.abspath(file_name)
        print("Uploading file:", file_path)  # Debugging output
        self.driver.find_element(By.XPATH, self.upload_button).send_keys(file_path)

    def click_validate_button(self):
        """Clicks the Validate button to process the file."""
        self.driver.find_element(By.XPATH, self.validate_button).click()

    def click_template_domestic_sourcelink_file(self):
        self.driver.find_element(By.NAME, self.Domestic_Payments_sourcelink_dropdown).click()

    def click_template_international_file(self):
        self.driver.find_element(By.NAME, self.International_payments).click()

    def click_template_commerce_file(self):
        self.driver.find_element(By.NAME, self.Commerce_payment).click()

    def get_file_error_message(self):
        try:
            return self.driver.find_element(By.XPATH, self.error_message_file).text
        except NoSuchElementException:
            return None

    def is_validate_button_disabled(self):
        """Checks if the 'Validate' button is disabled."""
        validate_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self.validate_button))
        )
        return "disabled" in validate_button.get_attribute("class")

    def get_uploaded_file_name(self):
        """Returns the name of the file displayed after upload."""
        file_name_display = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self.upload_filename))
        )
        return file_name_display.text

    def is_popup_message_displayed(self):
        """Check if the popup message is displayed."""
        popup_message = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self.popup_message))
        )
        return "We’re validating your file!This could take a few minutes.  " in popup_message.text

    def click_check_button(self):
        self.driver.find_element(By.XPATH, self.check_back).click()

    def get_file_status(self):
        """Get the file status from the internal page."""
        file_status = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self.file_status))
        )
        return file_status.text
    def get_file_status(self):
        """Returns the status of the uploaded file (e.g., 'Submitted' or 'Validation')."""
        # try:
        #     # Check for 'Submitted' status
        #     submitted_element = self.driver.find_element(By.XPATH,  "(//div[contains(@class, 'MuiDataGrid-cell')]//span[text()='SUBMITTED'])[1]"
        #                                                 )
        #     print("First 'SUBMITTED' status found:", submitted_element.text.strip())
        #
        #     return "SUBMITTED"
        # except:
        #     pass

        try:
            validated_element = self.driver.find_element(By.XPATH,
                                                         "(//div[contains(@class, 'MuiDataGrid-cell')]//span[text()='VALIDATED'])[1]")
            print("First 'VALIDATED' status found:", validated_element.text.strip())

            return "Validation"
        except:
            pass

        try:
            failed_element = self.driver.find_element(By.XPATH,
                                                         "((//div[contains(@class, 'MuiDataGrid-cell')]//span[text()='FAILED'])[1]")
            print("First 'FAILED' status found:", failed_element.text.strip())

            return "Failed"
        except:
            pass

        return None  # If neither status is found

    def click_status_button(self):
        self.driver.find_element(By.XPATH, self.file_status_validate).click()

    def click_failed_status_button(self):
        self.driver.find_element(By.XPATH, self.file_status_failed).click()

    def get_total_payments(self):
        return self.driver.find_element(By.XPATH, self.total_payment).text

    def get_total_invoices(self):
        return self.driver.find_element(By.XPATH, self.total_invoice).text

    def get_errors(self):
        return self.driver.find_element(By.XPATH, self.error).text

    def click_finalize_button(self):
        self.driver.find_element(By.XPATH, self.finalize_submission).click()

    def click_continue_button(self):
        self.driver.find_element(By.XPATH, self.continue_submission).click()

    def is_manual_batches_actions_displayed(self):
        return self.driver.find_element(By.XPATH, self.manual_batches_actions).is_displayed()

    def is_go_to_payments_button_displayed(self):
        return self.driver.find_element(By.XPATH, self.go_to_payments_button).is_displayed()

    def is_download_pci_safe_original_button_displayed(self):
        return self.driver.find_element(By.XPATH, self.download_pci_safe_original_button).is_displayed()

    def is_download_pci_safe_final_button_displayed(self):
        return self.driver.find_element(By.XPATH, self.download_pci_safe_final_button).is_displayed()

    def click_go_to_payment(self):
        self.driver.find_element(By.XPATH, self.go_to_payments_button).click()

    def click_check_back_later(self):
        self.driver.find_element(By.XPATH, self.check_back_later).click()

    def is_payment_page_displayed(self):
        return self.driver.find_element(By.XPATH, self.payment_page).is_displayed()

    def click_download_pci(self):
        self.driver.find_element(By.XPATH, self.download_pci).click()

    def click_download_final_pci(self):
        self.driver.find_element(By.XPATH, self.download_pci_safe_final_button).click()

    def click_download_original(self):
        self.driver.find_element(By.XPATH, self.download_original).click()

    def click_download_final(self):
        self.driver.find_element(By.XPATH, self.download_final).click()

    def is_file_status_page_displayed(self):
        """Verifies whether the file status page is displayed."""
        return self.driver.find_element(By.XPATH, self.file_status).is_displayed()

    def get_error_and_warning_counts(self):
        error_warning_text = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, self.error))  # ✅ Fix applied
        ).text
        numbers = [int(num) for num in error_warning_text.split() if num.isdigit()]

        if len(numbers) >= 2:
            return {"errors": numbers[0], "warnings": numbers[1]}
        else:
            return {"errors": 0, "warnings": 0}

    def click_download_latest_file(self):
        self.driver.find_element(By.XPATH, self.download_latest).click()

    def is_warning_message_displayed(self):
        """Check if the warning message is displayed on the file status page."""
        return self.driver.find_element(By.XPATH, self.warring_message).is_displayed()

    def click_upload_again(self):
        self.driver.find_element(By.XPATH,self.upload_again).click()

    def add_again_file(self, file_name):
        """Uploads a file by sending the file path to the upload button."""
        file_path = os.path.abspath(file_name)
        print("Uploading file:", file_path)  # Debugging output
        self.driver.find_element(By.XPATH, self.upload_again_button).send_keys(file_path)

    def click_again_validate_button(self):
        self.driver.find_element(By.XPATH,self.again_validate_button).click()

    def click_again_check_back_button(self):
        self.driver.find_element(By.XPATH,self.again_check_back_latter).click()

    def is_internal_validate_button_displayed(self):
        return self.driver.find_element(By.XPATH, self.internal_page_validate).is_displayed()

    def click_discard_batch(self):
        self.driver.find_element(By.XPATH, self.discard_batch).click()

    def click_discard_batch_button(self):
        self.driver.find_element(By.XPATH,self.discard_button).click()

    def get_file_failed_status(self):
        """Returns the status of the uploaded file (e.g., 'Submitted', 'Validation', or 'Failed')."""
        statuses = [
            ("FAILED", "Failed"),  # Check for failed status first
            ("SUBMITTED", "Submitted"),
            ("VALIDATED", "Validation")
        ]

        for status_text, status_value in statuses:
            try:
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, f"(//div[contains(@class, 'MuiDataGrid-cell')]//span[text()='{status_text}'])[1]")
                    )
                )
                print(f"First '{status_text}' status found:", element.text.strip())
                return status_value
            except Exception as e:
                print(f"Status '{status_text}' not found. Error: {e}")
                continue

        return None  # If none of the statuses are found

    def click_contact_production(self):
        self.driver.find_element(By.XPATH, self.contact_production).click()