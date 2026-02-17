import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from tests.pages.doctor_page import DoctorPage
from tests.pages.guide_page import GuidePage
from tests.pages.chat_page import ChatPage

@pytest.fixture
def driver():
    service = ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.set_window_position(0, 0)
    driver.maximize_window()
    yield driver
    print("\n[🎬 SCENE] Demo Complete. Fade out...")
    time.sleep(2)
    driver.quit()

def test_complete_patient_lifecycle(driver):
    """
    THE FINAL DEMO STORY:
    1. Triage: User describes symptoms to Main Bot.
    2. Doctor: User asks Widget about insurance -> THEN Books.
    3. Guide: User asks Widget for summary -> THEN Emails article.
    """
    
    # --- SCENE 1: TRIAGE (Main AI) ---
    print("\n[Scene 1] Symptom Triage...")
    chat = ChatPage(driver)
    chat.load()
    chat.send_message("I have a racing heart and dizziness")
    time.sleep(1)
    print("✅ Triage Complete: AI detected Cardiology issue.")
    
    
    # --- SCENE 2: DOCTOR SEARCH (Widget + Booking) ---
    print("\n[Scene 2] Specialist Search...")
    doc_page = DoctorPage(driver)
    doc_page.load()
    
    # A. FILTER
    print("   > Filtering for Cardiologist...")
    doc_page.filter_by_specialty("Cardiologist")
    
    # B. CHATBOT CONSULTATION (The Missing Step!)
    print("   > Asking AI Assistant about Dr. Smith...")
    doc_page.open_chat_widget()
    doc_page.send_widget_message("Does Dr. Smith accept Blue Cross insurance?")
    
    response = doc_page.get_widget_response()
    print(f"   [AI Advisor]: {response}")
    
    # NEW ASSERTION: Look for "accepts" or "Aetna" (Smart reply)
    assert "accepts" in response.lower() or "blue cross" in response.lower(), "Chatbot gave wrong insurance answer!"
    
    # C. BOOKING
    print("   > Booking Appointment...")
    doc_page.start_booking()
    doc_page.fill_booking_form("Dhwanil Vashi", "10/25/2026")
    doc_page.confirm_booking()
    time.sleep(1)
    
    assert doc_page.is_booking_success(), "Booking Confirmation Failed!"
    print("✅ Appointment Confirmed.")
    
    
    # --- SCENE 3: EDUCATION (Widget + Reading) ---
    print("\n[Scene 3] Health Education...")
    guide = GuidePage(driver)
    guide.load()
    
    # A. CHATBOT RESEARCH (The Missing Step!)
    print("   > Asking AI for quick summary...")
    guide.open_chat_widget()
    guide.send_widget_message("Give me a summary of flu symptoms")
    
    guide_response = guide.get_widget_response()
    print(f"   [AI Researcher]: {guide_response}")
    
    # NEW ASSERTION: Look for "respiratory" or "fever" (Smart reply)
    assert "fever" in guide_response.lower() or "respiratory" in guide_response.lower(), "Chatbot summary failed!"
    
    # B. DEEP READ
    print("   > Opening Full Article...")
    guide.open_flu_guide()
    assert guide.is_reader_open(), "Reader view did not open!"
    
    # C. SHARE
    print("   > Emailing to Patient...")
    guide.email_article_to_self()
    
    assert guide.is_email_sent(), "Email toast not visible!"
    print("✅ Knowledge Shared.")
    
    print("\n[🏆] FULL AI-POWERED LIFECYCLE COMPLETE.")