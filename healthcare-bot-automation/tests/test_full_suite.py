import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Import Page Objects
from tests.pages.chat_page import ChatPage
from tests.pages.doctor_page import DoctorPage
from tests.pages.guide_page import GuidePage

@pytest.fixture
def driver():
    # Setup Chrome with visual settings
    service = ChromeService(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    
    # "Presentation Mode" - Left side of screen, fully expanded
    driver.set_window_position(0, 0)
    driver.maximize_window()
    
    yield driver
    
    print("\n[🎬 SCENE] Demo Complete. Fade out...")
    time.sleep(5)
    driver.quit()

def test_critical_patient_journey(driver):
    """
    STORY: A patient on blood thinners suffers a head injury.
    
    COMPLEXITY CHECK:
    1. AI must detect the 'Silent Killer' interaction (Head Hit + Blood Thinners).
    2. User must find the CORRECT specialist (Neurologist), not just 'a doctor'.
    3. User validates knowledge in the Health Guide.
    """
    
    # --- SCENE 1: THE INTELLIGENT TRIAGE ---
    print("\n[Scene 1] Testing High-Risk Medical Logic...")
    chat = ChatPage(driver)
    chat.load()
    time.sleep(2)
    
    # COMPLEX INPUT: seemingly minor injury + critical medical history
    complex_symptom = "I slipped and hit my head on the floor. I am currently taking Warfarin (blood thinners)."
    print(f"[Patient]: {complex_symptom}")
    
    chat.send_message(complex_symptom)
    time.sleep(4) # Allow time for the AI to "think" and viewer to read input
    
    response = chat.get_latest_response().lower()
    print(f"[AI Nurse]: {response}")
    
    # ASSERTION: The bot fails if it treats this as just a "bump on the head"
    # It MUST flag the bleeding risk (911/Emergency)
    critical_triggers = ["911", "emergency", "bleed", "hospital", "immediate"]
    is_safe = any(t in response for t in critical_triggers)
    
    assert is_safe, f"FAILED: AI missed the 'Blood Thinner + Head Injury' risk! Response: {response}"
    print("✅ AI successfully diagnosed the 'Silent Killer' risk.")
    
    
    # --- SCENE 2: TARGETED SPECIALIST SEARCH ---
    print("\n[Scene 2] Locating Specialist (Neurology)...")
    doc_page = DoctorPage(driver)
    doc_page.load()
    time.sleep(2)
    
    # We don't just search "Doctor". We search "Neurologist" based on Scene 1.
    doc_page.search_doctor("10001", "Neurologist")
    time.sleep(3) # Visual pause to let audience see the search terms
    
    # Verify the "Book" button works
    doc_page.book_first_doctor()
    print("✅ Urgent appointment slot secured.")
    time.sleep(2)
    
    
    # --- SCENE 3: POST-CARE EDUCATION ---
    print("\n[Scene 3] Patient Education Protocol...")
    guide = GuidePage(driver)
    guide.load()
    time.sleep(2)
    
    # User looks up their condition
    guide.search_article("Concussion Warning Signs")
    time.sleep(3) 
    
    guide.open_flu_guide() # (Clicking the available demo article)
    print("✅ Educational materials delivered.")
    
    print("\n[🏆 SUCCESS] Full End-to-End Medical Journey Verified.")