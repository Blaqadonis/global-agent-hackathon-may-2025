import argparse
import json
from graph import graph

def main():
    parser = argparse.ArgumentParser(description="Check saved state for a user ID using LangGraph")
    parser.add_argument("--user_id", required=True, help="User ID to check (same as entered in Streamlit)")
    args = parser.parse_args()

    user_id = args.user_id
    thread_id = f"thread_{user_id}"
    config = {"configurable": {"user_id": user_id, "thread_id": thread_id}}

    try:
        graph_state = graph.get_state(config)
        if graph_state.values:
            state_values = graph_state.values
            print(f"Saved state for user_id '{user_id}':")
            print(json.dumps(state_values, indent=2, default=str))
        else:
            print(f"No saved state found for user_id '{user_id}'")
    except Exception as e:
        print(f"Error retrieving state: {e}")

if __name__ == "__main__":
    main()