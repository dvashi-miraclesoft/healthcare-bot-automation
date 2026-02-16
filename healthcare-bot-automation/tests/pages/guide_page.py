from selenium.webdriver.common.by import By
from .base_page import BasePage

class GuidePage(BasePage):
    # Locators
    SEARCH_BOX = (By.ID, "articleSearch")
    READ_FLU_LINK = (By.ID, "read_flu")
    
    def load(self):
        self.open_url("http://127.0.0.1:5000/guide")

    def search_article(self, topic):
        self.type_text(self.SEARCH_BOX, topic)
    
    def open_flu_guide(self):
        self.click(self.READ_FLU_LINK)