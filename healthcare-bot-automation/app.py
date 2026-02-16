import os
import time
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

app = Flask(__name__)

# --- CONFIGURATION ---
# Replace with your actual API Key
os.environ["GEMINI_API_KEY"] = "YOUR_GEMINI_API_KEY"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# --- SAFETY SETTINGS ---
# We disable blocks so the bot can handle "overdose" or "blood" queries 
# without triggering the content filter.
safety_config = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

# Initialize the Model
# If this gives a 404 error, switch 'gemini-1.5-flash' to 'gemini-pro'
model = genai.GenerativeModel('gemini-flash-latest', safety_settings=safety_config)

SYSTEM_INSTRUCTION = """
You are 'MediBot', a professional medical triage assistant.

RULES:
1. TRIGGERING EMERGENCY: If the user states they ARE experiencing "chest pain", "difficulty breathing", "severe bleeding", or "overdose", start with "CRITICAL WARNING: CALL 911 IMMEDIATELY."
2. NEGATION HANDLING: If a user mentions a critical symptom but explicitly states they do NOT have it (e.g., "I don't have chest pain"), do NOT trigger the 911 warning.
3. CONCISE: Keep answers under 50 words.
4. DOCTOR ADVICE: Always advise consulting a real doctor.
5. EMPATHY: Be professional and empathetic.
"""

def get_ai_response(user_input):
    """
    Fetches AI response with a SMART RETRY system.
    If Quota Exceeded (429), it waits and tries again.
    """
    retries = 3
    base_wait_time = 20  # Seconds to wait if quota hits
    
    for attempt in range(retries):
        try:
            # Create a chat session
            chat = model.start_chat(history=[])
            full_prompt = f"{SYSTEM_INSTRUCTION}\n\nUser: {user_input}"
            response = chat.send_message(full_prompt)
            return response.text
            
        except Exception as e:
            error_str = str(e)
            # Check for Quota/Rate Limit errors (429)
            if "429" in error_str or "Resource exhausted" in error_str:
                print(f"⚠️ Quota Limit Hit! Waiting {base_wait_time} seconds before retry #{attempt + 1}...")
                time.sleep(base_wait_time)
                continue  # Retry the loop
            
            # If it's a model not found error (404), stop trying
            if "404" in error_str:
                return f"System Error: Model not found. Please check your API key or model name in app.py. Details: {e}"
                
            print(f"------------ API ERROR: {e} ------------")
            return "I am currently experiencing technical difficulties. Please consult a doctor directly."
            
    return "System Notice: The AI is currently overloaded with requests. Please try again in 1 minute."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    response = get_ai_response(userText)
    return jsonify({"response": response})

@app.route("/doctors")
def doctors():
    """Renders the 'Find a Doctor' dashboard."""
    return render_template("doctors.html")

@app.route("/guide")
def guide():
    """Renders the 'Health Guide' library."""
    return render_template("guide.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)