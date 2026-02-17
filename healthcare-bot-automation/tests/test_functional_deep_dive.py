import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from tests.pages.doctor_page import DoctorPage
from tests.pages.guide_page import GuidePage

@pytest.fixture
def driver():
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.set_window_position(0,0)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_smart_doctor_search(driver):
    """
    STORY: User filters for a Cardiologist, then asks the AI for details.
    """
    print("\n[Testing] Smart Doctor Search (Logic + Chat)...")
    page = DoctorPage(driver)
    page.load()
    
    # 1. LOGIC: Filter for 'Cardiologist'
    print("   > Filtering for Cardiologist...")
    page.filter_by_specialty("Cardiologist")
    time.sleep(1)
    
    # Verify visual count drops to 1
    assert page.get_visible_card_count() == 1, "Filter failed!"
    
    # 2. CHAT: Open Widget & Ask
    print("   > Asking AI about insurance...")
    page.open_chat_widget()
    page.send_widget_message("Does Dr. Smith take Aetna?")
    
    # Verify AI response
    response = page.get_widget_response()
    print(f"   [AI Said]: {response}")
    assert "help" in response.lower(), "Chatbot failed to respond!"
    
    print("✅ Doctor Page: Filter Logic + Chatbot Verified.")

def test_interactive_health_guide(driver):
    """
    STORY: User reads an article, votes it 'Helpful', then asks AI to summarize.
    """
    print("\n[Testing] Interactive Health Guide (State + Chat)...")
    page = GuidePage(driver)
    page.load()
    
    # 1. LOGIC: Click 'Helpful' Vote
    print("   > Voting on article...")
    page.click_helpful_vote()
    time.sleep(0.5)
    
    # Verify button turns green (Active state)
    assert page.is_vote_active(), "Vote button didn't activate!"
    
    # 2. CHAT: Open Widget & Research
    print("   > Asking AI for summary...")
    page.open_chat_widget()
    page.send_widget_message("Summarize flu symptoms")
    
    # Verify AI response
    response = page.get_widget_response()
    print(f"   [AI Said]: {response}")
    assert "found" in response.lower() or "article" in response.lower()
    
    print("✅ Guide Page: Interaction + Chatbot Verified.")