from tools import recommend_destination, split_budget, generate_itinerary


class TravelAgent:

    def handle_followups(self, state):
        if state.is_budget_missing():
            return "Bhaiji, what’s your budget for the trip?"

        if state.is_dates_missing():
            return "Nice 👍 When are you planning to travel?"

        return None

    def plan_trip(self, state):
        # Recommendation
        if not state.destination:
            recs = recommend_destination(
                state.budget,
                state.dates,
                state.preferences
            )

            chosen = recs[0]["name"] if recs else "Goa"
            alternatives = [r["name"] for r in recs[1:]] if len(recs) > 1 else []
        else:
            chosen = state.destination
            alternatives = []

        # Cost
        budget_split = split_budget(
            state.budget,
            chosen,
            state.trip_duration
        )

        # Itinerary
        itinerary = generate_itinerary(
            chosen,
            state.trip_duration,
            state.preferences
        )

        return {
            "destination": chosen,
            "budget": budget_split,
            "itinerary": itinerary,
            "alternatives": alternatives
        }