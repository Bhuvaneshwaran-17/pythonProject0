from fastapi import FastAPI
from action import ActionRequest, ActionTrackRequest
from sequence_service import fetch_sequences_for_action, analyze_sequences, track_user_action

app = FastAPI()


@app.post("/predict_next_action")
async def predict_next_action(request: ActionRequest):
    current_action = request.current_action

    # Fetch sequences from DB
    data = fetch_sequences_for_action(current_action)

    # Analyze and format the sequences
    result = analyze_sequences(data, current_action)

    if "error" in result:
        return result

    # Print the sequences in a readable format
    print("\nAction Sequence Analysis:")
    print(f"Current Action: {result['current_action']}")
    print(f"Total Occurrences: {result['total_occurrences']}")
    print("\nPossible Next Actions:")
    print("-" * 50)
    print(f"{'Next Action':<20} {'Frequency':<10} {'Probability':<10}")
    print("-" * 50)

    for seq in result['sequences']:
        print(f"{seq['next_action']:<20} {seq['frequency']:<10} {seq['probability']}%")
    print("-" * 50)

    return result


@app.post("/track_action")
async def track_action(request: ActionTrackRequest):
    action_data = request.dict()
    return track_user_action(action_data)