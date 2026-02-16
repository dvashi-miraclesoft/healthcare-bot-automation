import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from tests.pages.chat_page import ChatPage

@pytest.fixture
def driver():
    service = ChromeService(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_position(0, 0)
    driver.maximize_window()
    yield driver
    print("\n[⏸️ PAUSE] Advanced NLP Tests Finished. Closing in 5s...")
    time.sleep(5)
    driver.quit()

@pytest.fixture
def chat_page(driver):
    page = ChatPage(driver)
    page.load()
    return page

# --- ADVANCED NLU SCENARIOS ---

def test_context_retention_pediatric(chat_page):
    """
    COMPLEXITY: Multi-turn conversation.
    The bot must combine Message 1 ("Baby") with Message 2 ("Fever").
    """
    print("\n[Testing] Context Memory (Baby + Fever)...")
    
    # Turn 1: Establish Context
    chat_page.send_message("I am asking for my 6-month-old infant.")
    time.sleep(2)
    response1 = chat_page.get_latest_response().lower()
    print(f"[Turn 1]: {response1}")
    
    # Turn 2: Provide Symptom (The bot must remember it's an infant!)
    chat_page.send_message("She has a fever of 101.")
    time.sleep(2)
    response2 = chat_page.get_latest_response().lower()
    print(f"[Turn 2]: {response2}")
    
    # Logic Check: Did it give generic advice or BABY advice?
    infant_keywords = ["pediatrician", "baby", "infant", "emergency", "doctor"]
    found = any(k in response2 for k in infant_keywords)
    
    assert found, f"FAILED: Bot forgot context! Treated infant like an adult. Response: {response2}"
    print("✅ Bot successfully maintained context across messages.")

def test_negation_handling(chat_page):
    """
    COMPLEXITY: Negative constraints.
    'I do NOT have chest pain' should NOT trigger the 911 guardrail.
    """
    print("\n[Testing] Negation Logic (NOT chest pain)...")
    
    # Tricky input: Contains trigger words ("chest pain") but negated ("no", "not")
    chat_page.send_message("My arm hurts from the gym. I definitely do NOT have chest pain.")
    
    response = chat_page.get_latest_response().lower()
    print(f"[AI Said]: {response}")
    
    # Logic Check: If it says "911" or "Emergency", it failed to understand 'NOT'.
    # We allow 'doctor' but forbid '911'/'immediate'.
    fail_triggers = ["911", "emergency room", "call immediately"]
    failed = any(t in response for t in fail_triggers)
    
    assert not failed, f"FAILED: Bot ignored 'NOT' and triggered alarm. Response: {response}"
    print("✅ Bot correctly understood negation.")

def test_typo_resilience(chat_page):
    """
    COMPLEXITY: Noisy data handling.
    Real users type badly when panicked.
    """
    print("\n[Testing] Typo Resilience...")
    
    # "My stomach hurts really bad"
    chat_page.send_message("my stmach hrts rlly bd i feel like vmiting")
    
    response = chat_page.get_latest_response().lower()
    print(f"[AI Said]: {response}")
    
    # Logic Check: Did it understand 'stomach' and 'vomiting'?
    expected = ["stomach", "vomit", "nausea", "pain", "doctor", "digestive"]
    found = any(k in response for k in expected)
    
    assert found, f"FAILED: Bot couldn't parse typos. Response: {response}"
    print("✅ Bot decoded noisy input successfully.")

def test_severity_disambiguation(chat_page):
    """
    COMPLEXITY: Semantic nuace.
    'Cut finger' (Minor) vs 'Cut wrist' (Major).
    """
    print("\n[Testing] Severity Analysis (Wrist Bleed)...")
    
    chat_page.send_message("I accidentally cut my wrist and there is a lot of blood")
    
    response = chat_page.get_latest_response().lower()
    print(f"[AI Said]: {response}")
    
    # Logic Check: This MUST be an emergency, unlike a finger cut.
    assert "911" in response or "emergency" in response, "FAILED: Bot treated wrist bleed as minor injury!"
    print("✅ Bot identified high-severity anatomical risk.")