import google.generativeai as genai
import os

# Set your key
os.environ["GEMINI_API_KEY"] = "YOUR_GEMINI_API_KEY"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

print("---------------- AVAILABLE MODELS ----------------")
try:
    for m in genai.list_models():
        # Only show models that can generate chat text
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model Name: {m.name}")
except Exception as e:
    print(f"Error: {e}")
print("--------------------------------------------------")