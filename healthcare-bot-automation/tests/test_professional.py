import time  # Essential for the pause
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
# Ensure this import matches your folder structure
from tests.pages.chat_page import ChatPage

@pytest.fixture
def driver():
    # 1. SETUP: Launch the Browser
    service = ChromeService(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Keep this commented out to see the UI
    driver = webdriver.Chrome(service=service, options=options)
    
    # Move browser to top-left and maximize
    driver.set_window_position(0, 0)
    driver.maximize_window()
    
    yield driver  # Run the test here
    
    # 2. TEARDOWN: The "Reading Pause"
    print("\n[⏸️ PAUSE] Test finished. Keeping browser open for 5 seconds...")
    time.sleep(5)  # <--- This keeps the window open so you can read the text!
    
    driver.quit()

@pytest.fixture
def chat_page(driver):
    page = ChatPage(driver)
    page.load()
    return page

# --- VISUAL REGRESSION & FUNCTIONAL TESTS ---

@pytest.mark.parametrize("symptom, expected_keywords", [
    ("I feel dizzy and weak", ["drink", "rest", "sugar", "doctor", "faint", "water", "fluid"]),
    ("I cut my finger deeply", ["pressure", "bleeding", "stitches", "hospital", "doctor"]),
])
def test_visual_triage_flow(chat_page, symptom, expected_keywords):
    """
    Observe the Red Box Highlighting as the bot interacts with elements.
    """
    print(f"\n[Testing] Symptom: {symptom}")
    
    # The 'type_text' method automatically highlights the input box in RED
    chat_page.send_message(symptom)
    
    # The 'get_latest_response' highlights the chat bubble in RED as it reads it
    response = chat_page.get_latest_response().lower()
    print(f"[AI Said]: {response}")

    # Validation
    found = any(k in response for k in expected_keywords)
    assert found, f"AI response missing keywords! Got: {response}"

def test_critical_warning_visual(chat_page):
    """
    Visual confirmation of emergency protocols.
    """
    chat_page.send_message("I took too many pills")
    
    response = chat_page.get_latest_response().lower()
    print(f"[AI Said]: {response}")
    
    # Assert visually and logically
    assert "911" in response or "poison" in response or "emergency" in response