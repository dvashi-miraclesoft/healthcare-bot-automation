from selenium.webdriver.common.by import By
from .base_page import BasePage
import time

class GuidePage(BasePage):
    # --- LOCATORS ---
    READ_FLU_LINK = (By.ID, "read_flu")
    READER_VIEW = (By.ID, "article-reader")
    EMAIL_BTN = (By.ID, "email-btn")
    EMAIL_TOAST = (By.ID, "email-toast")
    
    # Chat Widget
    WIDGET_TOGGLE = (By.ID, "chat-toggle")
    WIDGET_INPUT = (By.ID, "mini-input")
    LATEST_WIDGET_MSG = (By.CSS_SELECTOR, "#mini-messages .msg.bot:last-child")
    
    def load(self):
        self.open_url("http://127.0.0.1:5000/guide")

    # --- READER METHODS ---
    def open_flu_guide(self):
        self.click(self.READ_FLU_LINK)
        
    def is_reader_open(self):
        return self.find(self.READER_VIEW).is_displayed()
        
    def email_article_to_self(self):
        self.click(self.EMAIL_BTN)
        time.sleep(1.5) 
        
    def is_email_sent(self):
        return self.find(self.EMAIL_TOAST).is_displayed()

    # --- CHAT METHODS (Restored!) ---
    def open_chat_widget(self):
        self.click(self.WIDGET_TOGGLE)
        time.sleep(1)
        
    def send_widget_message(self, text):
        self.type_text(self.WIDGET_INPUT, text + "\n")
        time.sleep(1.5)
        
    def get_widget_response(self):
        return self.find(self.LATEST_WIDGET_MSG).text