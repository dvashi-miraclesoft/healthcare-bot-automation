from selenium.webdriver.common.by import By
from .base_page import BasePage

class ChatPage(BasePage):
    # --- LOCATORS ---
    INPUT_BOX = (By.ID, "textInput")
    SEND_BUTTON = (By.ID, "buttonInput")
    
    # UPDATED: Matches the new "Enterprise" HTML structure
    # We look for the last 'bubble' inside a 'bot' row
    LAST_BOT_MESSAGE = (By.CSS_SELECTOR, ".msg-row.bot:last-of-type .bubble")
    
    LOADING_INDICATOR = (By.ID, "typing")

    # --- ACTIONS ---
    def load(self):
        self.open_url("http://127.0.0.1:5000")

    def send_message(self, text):
        self.type_text(self.INPUT_BOX, text)
        self.click(self.SEND_BUTTON)

    def get_latest_response(self):
        # 1. Wait for the "..." typing indicator to disappear
        from selenium.webdriver.support import expected_conditions as EC
        self.wait.until(EC.invisibility_of_element_located(self.LOADING_INDICATOR))
        
        # 2. Grab the text from the new bubble
        return self.get_text(self.LAST_BOT_MESSAGE)