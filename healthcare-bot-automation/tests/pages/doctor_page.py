from selenium.webdriver.common.by import By
from .base_page import BasePage
import time

class DoctorPage(BasePage):
    # --- LOCATORS ---
    # Filter
    FILTER_INPUT = (By.ID, "filterInput")
    FILTER_BTN = (By.ID, "searchBtn")
    
    # Booking Modal
    FIRST_BOOK_BTN = (By.ID, "book_1")
    MODAL_NAME_INPUT = (By.ID, "p_name")
    MODAL_DATE_INPUT = (By.ID, "p_date")
    CONFIRM_BTN = (By.ID, "confirm-book-btn")
    SUCCESS_MSG = (By.ID, "success-msg")
    
    # Chat Widget
    WIDGET_TOGGLE = (By.ID, "chat-toggle")
    WIDGET_INPUT = (By.ID, "mini-input")
    LATEST_WIDGET_MSG = (By.CSS_SELECTOR, "#mini-messages .msg.bot:last-child")
    
    def load(self):
        self.open_url("http://127.0.0.1:5000/doctors")

    # --- FILTER METHODS ---
    def filter_by_specialty(self, specialty):
        self.type_text(self.FILTER_INPUT, specialty)
        self.click(self.FILTER_BTN)

    # --- BOOKING METHODS ---
    def start_booking(self):
        self.click(self.FIRST_BOOK_BTN)
        
    def fill_booking_form(self, name, date):
        self.type_text(self.MODAL_NAME_INPUT, name)
        self.type_text(self.MODAL_DATE_INPUT, date)
        
    def confirm_booking(self):
        self.click(self.CONFIRM_BTN)
        
    def is_booking_success(self):
        return self.find(self.SUCCESS_MSG).is_displayed()
        
    # --- CHAT METHODS (Restored!) ---
    def open_chat_widget(self):
        self.click(self.WIDGET_TOGGLE)
        time.sleep(1)
        
    def send_widget_message(self, text):
        self.type_text(self.WIDGET_INPUT, text + "\n")
        time.sleep(1.5) # Wait for bot response
        
    def get_widget_response(self):
        return self.find(self.LATEST_WIDGET_MSG).text