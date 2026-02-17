# MediBot Pro: AI-Driven Clinical Triage & Lifecycle Automation

An enterprise-grade healthcare automation suite demonstrating a complete patient journey—from high-risk AI triage to specialist booking and medical education.

## 🚀 Project Overview
This project showcases an "AI-First" healthcare platform. It features a sophisticated frontend with integrated AI widgets and a robust Selenium automation framework that validates not just UI elements, but **clinical reasoning logic**.

### Key Features:
* **Intelligent Triage**: Detects high-risk scenarios (e.g., Head Injury + Blood Thinners) using keyword-aware NLP.
* **Dynamic Specialist Filtering**: Real-time JavaScript filtering for medical specialties.
* **Integrated AI Widgets**: Context-aware assistants on every page (Doctor Search & Health Guide).
* **End-to-End Lifecycle**: Automated flows for triage, appointment booking via modals, and article distribution.

---

## 🏗️ Technical Architecture


* **Backend**: Python Flask
* **Frontend**: HTML5, CSS3 (Plus Jakarta Sans), JavaScript (ES6)
* **Automation**: Selenium WebDriver, PyTest, Page Object Model (POM)
* **Design Pattern**: "Cinematic Demo" mode with element highlighting and human-like interaction speeds.

---

## 🧪 Automation Suite
The testing framework is divided into three tiers:

1.  **Clinical Journey (`test_full_suite.py`)**: Validates the end-to-end patient story.
2.  **AI Brain (`test_ai_brain.py`)**: Tests context retention, safety guardrails, and ambiguity handling.
3.  **Functional Deep-Dive (`test_functional_deep_dive.py`)**: Validates JS-driven logic like filtering and UI state persistence.

### Running the Tests:
```bash
# Run the full cinematic journey
pytest tests/test_full_suite.py -v -s

# Run the functional logic tests
pytest tests/test_functional_deep_dive.py -v -s
