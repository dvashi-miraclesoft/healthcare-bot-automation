import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """Wrapper for Selenium operations with Visual Highlighting."""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 100)

    def highlight(self, element):
        """Draws a red border around the element for 0.5s (The 'Ghost' Effect)."""
        # JavaScript Injection to change CSS styles
        self.driver.execute_script("arguments[0].style.border='3px solid red';", element)
        self.driver.execute_script("arguments[0].style.boxShadow='0px 0px 10px red';", element)
        time.sleep(0.5) # Pause so human eyes can see the highlight
        # Remove the border (optional, but keeps UI clean)
        self.driver.execute_script("arguments[0].style.border='';", element)
        self.driver.execute_script("arguments[0].style.boxShadow='';", element)

    # --- MISSING METHOD RESTORED BELOW ---
    def open_url(self, url):
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def type_text(self, locator, text):
        element = self.find(locator)
        self.highlight(element)  # Visual Effect
        element.clear()
        element.send_keys(text)

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        self.highlight(element)  # Visual Effect
        element.click()

    def get_text(self, locator):
        element = self.find(locator)
        self.highlight(element) # Visual Effect
        return element.text