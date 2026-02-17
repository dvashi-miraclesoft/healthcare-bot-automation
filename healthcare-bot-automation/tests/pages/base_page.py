import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class BasePage:
    """
    Advanced Automation Engine with 'Demo Mode' visuals.
    """
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15) # Increased timeout for safety

    def open_url(self, url):
        self.driver.get(url)

    def highlight(self, element):
        """Draws a red border around the element so you can see what's happening."""
        self.driver.execute_script("arguments[0].style.border='4px solid #ef4444';", element)
        self.driver.execute_script("arguments[0].style.backgroundColor='rgba(239, 68, 68, 0.1)';", element)
        time.sleep(0.5) # VISUAL PAUSE

    def click(self, locator):
        el = self.wait.until(EC.element_to_be_clickable(locator))
        self.highlight(el) # Show what we are clicking
        time.sleep(0.5)    # Slow down for demo
        el.click()

    def type_text(self, locator, text):
        el = self.wait.until(EC.visibility_of_element_located(locator))
        self.highlight(el)
        el.clear()
        
        # HUMAN TYPING EFFECT (Char by Char)
        for char in text:
            el.send_keys(char)
            time.sleep(0.05) # Typing speed
        
        time.sleep(0.5) # Pause after typing

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))
    
    def find_all(self, locator):
        return self.driver.find_elements(*locator)