from state import TravelState
from agent import TravelAgent
from extractor import extract_with_llm, update_state_from_llm
from replanner import analyze_feedback, apply_replanning
from tools import compare_destinations



def display_plan(plan):
    print("\n🔥 Master, here’s your plan:\n")

    print(f"🌍 Destination: {plan['destination']}")

    print("\n💰 Budget Breakdown:")
    for k, v in plan["budget"].items():
        print(f"  {k}: ₹{v}")

    print("\n🗺️ Itinerary:")
    for day in plan["itinerary"]:
        print(f"  {day}")

    if plan["alternatives"]:
        print("\n🔁 Alternatives:")
        for alt in plan["alternatives"]:
            print(f"  {alt}")


def main():
    state = TravelState()
    agent = TravelAgent()

    print("🤖 Travel Agent Started (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        # 🔥 STEP 1: Check if it's feedback
        feedback = analyze_feedback(user_input)
        if feedback.get("intent") == "compare":
            options = feedback.get("options")

            print("Agent: Master, let me compare these for you 👇\n")

            comparison = compare_destinations(
                options,
                state.budget,
                state.dates,
                state.preferences
            )

            print(comparison)
            continue

        if feedback.get("intent"):
            state = apply_replanning(state, feedback)
            print("Agent: Got it Master 👍 Let me adjust the plan...")

        else:
            # 🔥 STEP 2: Normal extraction
            data = extract_with_llm(user_input)
            update_state_from_llm(data, state)

        # 🔥 STEP 3: Follow-up
        followup = agent.handle_followups(state)

        if followup:
            print("Agent:", followup)
            continue

        # 🔥 STEP 4: Planning
        plan = agent.plan_trip(state)
        display_plan(plan)

if __name__ == "__main__":
    main()