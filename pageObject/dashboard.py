from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DashboardPage:
    def __init__(self, driver):
        self.driver = driver
        self.dynamic_boost_status_heading = "//*[@id='root']/section/header/div[1]/h1"
        self.last_updated_timestamp = '//*[@id="root"]/section/header/div[1]/p'
        self.dynamic_boost_icon = '//*[@id="root"]/header/nav/a'
        self.profile_icon = '//*[@id="grid-settings-user-menu"]'
        self.status_menu = '//*[@id="root"]/header/nav/div/ul/li[1]/a'
        self.sources_menu = '//*[@id="root"]/header/nav/div/ul/li[2]/button'
        self.payments_menu = '//*[@id="root"]/header/nav/div/ul/li[3]/a/span'
        self.invoices_menu = '//*[@id="root"]/header/nav/div/ul/li[4]/a/span'
        self.gateways_dropdown = '//*[@id="root"]/header/nav/div/ul[1]/li[5]/button'
        self.exceptions_badge = '//*[@id="root"]/header/nav/div/ul/li[6]/a'
        self.source_documents_received_section = '//*[@id="root"]/section/div/section[1]/section/div[1]/div/h3'
        self.emails_section = '//*[@id="root"]/section/div/section[2]/section/div[1]/div/h3'
        self.payments_by_status_section = '//*[@id="root"]/section/div/section[3]/div[1]/div[1]/h3'
        self.gateways_section = '//*[@id="root"]/section/div/section[4]/div[1]/div[1]/h3'
        self.payments_by_source_section = '//*[@id="root"]/section/div/section[5]/div[1]/div[1]/h3'

    def is_dynamic_boost_status_heading_visible(self):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.dynamic_boost_status_heading))
            ).is_displayed()
        except Exception:
            return False

    def is_last_updated_timestamp_visible(self):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.last_updated_timestamp))
            ).is_displayed()
        except Exception:
            return False

    def is_dynamic_boost_icon_visible(self):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.dynamic_boost_icon))
            ).is_displayed()
        except Exception:
            return False

    def is_profile_icon_visible(self):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.profile_icon))
            ).is_displayed()
        except Exception:
            return False

    def is_status_menu_visible_and_clickable(self):
        try:
            status_menu = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.status_menu))
            )
            return status_menu.is_displayed() and status_menu.is_enabled()
        except Exception:
            return False

    def is_sources_menu_visible_and_clickable(self):
        try:
            sources_menu = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.sources_menu))
            )
            return sources_menu.is_displayed() and sources_menu.is_enabled()
        except Exception:
            return False

    def is_payments_menu_visible_and_clickable(self):
        try:
            payments_menu = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.payments_menu))
            )
            return payments_menu.is_displayed() and payments_menu.is_enabled()
        except Exception:
            return False

    def is_invoices_menu_visible_and_clickable(self):
        try:
            invoices_menu = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.invoices_menu))
            )
            return invoices_menu.is_displayed() and invoices_menu.is_enabled()
        except Exception:
            return False

    def is_gateways_dropdown_visible(self):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.gateways_dropdown))
            ).is_displayed()
        except Exception:
            return False

    def is_exceptions_badge_visible(self):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.exceptions_badge))
            ).is_displayed()
        except Exception:
            return False

    def is_source_documents_received_section_visible(self):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.source_documents_received_section))
            ).is_displayed()
        except Exception:
            return False

    def is_emails_section_visible(self):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.emails_section))
            ).is_displayed()
        except Exception:
            return False

    def is_payments_by_status_section_visible(self):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.payments_by_status_section))
            ).is_displayed()
        except Exception:
            return False

    def is_gateways_section_visible(self):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.gateways_section))
            ).is_displayed()
        except Exception:
            return False

    def is_payments_by_source_section_visible(self):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, self.payments_by_source_section))
            ).is_displayed()
        except Exception:
            return False
