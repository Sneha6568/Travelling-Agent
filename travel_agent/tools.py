import os
import json
from groq import Groq
from dotenv import load_dotenv

# Load env
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = os.getenv("GROQ_MODEL")


def compare_destinations(options, budget, month, preferences):
    prompt = f"""
    Compare the following travel destinations:

    Destinations: {options}
    Budget: ₹{budget}
    Travel Month: {month}
    Preferences: {preferences}

    Provide:
    - Best use-case for each place
    - Budget suitability
    - Seasonal insights
    - Unique highlights

    Then give a FINAL recommendation based on user context.

    Return in clean text (NOT JSON).
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a travel expert. Give structured and helpful comparisons."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()

def recommend_destination(budget, month, preferences):
    prompt = f"""
    Suggest top 3 travel destinations based on:

    - Budget: ₹{budget}
    - Travel Month: {month}
    - Preferences: {preferences}

    Rules:
    - Destinations should match budget realistically
    - Consider seasonal suitability (weather, best time)
    - Keep mix of popular and hidden gems
    - Focus on Indian + nearby international options (if budget allows)

    Return ONLY valid JSON in this format:
    {{
      "destinations": [
        {{
          "name": "Place Name",
          "reason": "Why it fits"
        }}
      ]
    }}
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a travel recommendation expert. Always return JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    output = response.choices[0].message.content.strip()

    # Clean markdown
    if output.startswith("```"):
        output = output.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(output)
        return data.get("destinations", [])
    except:
        print("⚠️ Recommendation parsing failed:", output)
        return [
            {"name": "Goa", "reason": "Default fallback"},
            {"name": "Manali", "reason": "Fallback mountain option"}
        ]


def split_budget(budget, destination, duration):
    return {
        "transport": int(budget * 0.3),
        "stay": int(budget * 0.35),
        "food": int(budget * 0.2),
        "activities": int(budget * 0.15)
    }


def generate_itinerary(destination, duration, preferences):
    prompt = f"""
    Create a detailed {duration}-day travel itinerary for {destination}.

    Consider:
    - Local attractions
    - Popular activities
    - User preferences: {preferences}

    Rules:
    - Make it realistic and location-specific
    - Each day should have unique activities
    - Keep it concise (1 line per day)

    Return ONLY valid JSON in this format:
    {{
      "plan": [
        "Day 1: ...",
        "Day 2: ..."
      ]
    }}
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a travel planner AI. Always return JSON."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    output = response.choices[0].message.content.strip()

    if output.startswith("```"):
        output = output.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(output)
        return data.get("plan", [])
    except:
        print("⚠️ Itinerary parsing failed:", output)
        return [f"Day {i+1}: Explore {destination}" for i in range(duration)]