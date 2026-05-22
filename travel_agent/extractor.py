import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load env variables
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_with_llm(user_input):
    prompt = f"""
    Extract the following fields from user input:

    - budget (number in INR)
    - travel_month
    - destination
    - preferences (beach, mountains, city, adventure, nightlife)
    - trip_duration (number of days)

    Return ONLY valid JSON.

    User Input:
    "{user_input}"
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a data extraction assistant. Always return clean JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    output = response.choices[0].message.content.strip()

    # Clean markdown if present
    if output.startswith("```"):
        output = output.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(output)
    except:
        print("⚠️ Extraction failed:", output)
        return {}


def update_state_from_llm(data, state):

    if data.get("budget"):
        try:
            state.budget = int(data["budget"])
        except:
            pass

    if data.get("travel_month"):
        state.dates = data["travel_month"]

    if data.get("destination"):
        state.destination = data["destination"]

    if data.get("preferences"):
        state.preferences = data["preferences"]

    if data.get("trip_duration"):
        try:
            state.trip_duration = int(data["trip_duration"])
        except:
            pass