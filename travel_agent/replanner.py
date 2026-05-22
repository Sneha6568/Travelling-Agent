def analyze_feedback(user_input):
    text = user_input.lower()

    if "not good" in text:
        return {"intent": "dissatisfaction"}

    if "expensive" in text or "cheap" in text:
        return {"intent": "modify_budget", "action": "reduce"}

    if "change destination" in text:
        return {"intent": "change_destination"}

    if "mountain" in text:
        return {"intent": "change_preference", "value": "mountain"}

    if "beach" in text:
        return {"intent": "change_preference", "value": "beach"}

    if "days" in text:
        return {"intent": "change_duration"}
    
    if " or " in text:
        places = [p.strip().title() for p in text.split(" or ")]
        return {
            "intent": "compare",
            "options": places
        }

    return {"intent": None}


def apply_replanning(state, feedback):
    intent = feedback.get("intent")

    if intent == "modify_budget":
        if state.budget:
            state.budget = int(state.budget * 0.8)

    elif intent == "change_preference":
        state.preferences = [feedback.get("value")]
        state.destination = None

    elif intent == "change_destination":
        state.destination = None

    elif intent == "change_duration":
        state.trip_duration += 1

    elif intent == "dissatisfaction":
        state.destination = None

    return state