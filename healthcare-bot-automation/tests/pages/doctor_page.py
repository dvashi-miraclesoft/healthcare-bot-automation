from selenium.webdriver.common.by import By
from .base_page import BasePage

class DoctorPage(BasePage):
    # Locators
    ZIP_INPUT = (By.ID, "zipInput")
    SPEC_INPUT = (By.ID, "specInput")
    SEARCH_BTN = (By.ID, "searchBtn")
    FIRST_BOOK_BTN = (By.ID, "book_1")
    
    def load(self):
        self.open_url("http://127.0.0.1:5000/doctors")

    def search_doctor(self, zipcode, specialty):
        self.type_text(self.ZIP_INPUT, zipcode)
        self.type_text(self.SPEC_INPUT, specialty)
        self.click(self.SEARCH_BTN)
    
    def book_first_doctor(self):
        self.click(self.FIRST_BOOK_BTN)