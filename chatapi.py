from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

load_dotenv()
# === CONFIG ===
GENAI_API_KEY =  os.getenv("GENAI_API_KEY")  # Replace with your Gemini API Key
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

# === CONTEXT ===
PROBLEM_CONTEXT = """
India faces challenges in forecasting electricity demand due to varied climates, regional usage patterns, and variable solar generation.
PowerCast is an AI-powered platform that helps forecast demand using historical load data, weather forecasts, and regional behavior.
It helps power distributors plan energy usage, avoid blackouts, reduce wastage, and integrate renewables using an interactive dashboard.
"""

RELEVANT_KEYWORDS = ["electricity", "power", "forecast", "demand", "load", 
                     "AI", "weather", "solar", "PowerCast", "renewable", "energy","hi","hello","historical", "data", "analytics", "grid", "planning", "India"]

# === HELPERS ===

def is_relevant(question: str) -> bool:
    """Check if the question is related to PowerCast."""
    return any(kw in question.lower() for kw in RELEVANT_KEYWORDS)

def build_prompt(user_question: str) -> str:
    """Constructs the final prompt to send to Gemini."""
    return f"""
You are a helpful assistant for the PowerCast platform.

Context:
{PROBLEM_CONTEXT}

Answer ONLY if the question relates to:
-Greetings
- Electricity forecasting
- Power grid planning in India
- PowerCast features
- Renewable energy integration
- Data analytics (load, weather, consumption)
- AI/ML techniques used in PowerCast
To address this, the PowerCast platform uses AI to analyze:
    Historical electricity load data
    Real-time and forecasted weather conditions
    Regional usage behavior
    The goal is to help power distributors:
    Predict electricity demand more accurately
    Prevent shortages, blackouts, and energy waste
    Optimize integration of renewable energy sources like solar
PowerCast includes a web dashboard for:
    Visualizing region-specific trends
    Displaying real-time and forecasted data
    Enabling data-driven operational decisions
    Electricity forecasting
    Indian power grid challenges
    AI models for demand prediction
    PowerCast platform functionality
    Renewable energy integration
    Regional energy planning

User's Question:
{user_question}

If the question is irrelevant (e.g., about movies, random trivia, or politics), respond with:
"Sorry, I can only assist with queries related to the PowerCast electricity forecasting platform."
"""

def ask_powercast_bot(user_question: str) -> str:
    """Call Gemini API with the generated prompt."""
    prompt = build_prompt(user_question)
    response = model.generate_content(prompt)
    return response.text.strip()

# === ROUTES ===

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "No question provided."}), 400

    #print("here")
    answer = ask_powercast_bot(question)
    # else:
    #     answer = "Sorry, I can only assist with queries related to the PowerCast electricity forecasting platform."

    return jsonify({"answer": answer})


# === RUN ===

if __name__ == '__main__':
    app.run(debug=True,port=6969)
