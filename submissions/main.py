import os
from uuid import uuid4
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
import graph
import re

load_dotenv()

def print_assistant_response(updates):
    """Helper function to print assistant responses from stream updates."""
    if "messages" in updates and updates["messages"]:
        msg = updates["messages"][-1]
        # Handle both dictionary and message object formats
        if isinstance(msg, dict):
            role = msg.get("role")
            content = msg.get("content", "")
            if role == "assistant" and content:  
                final_answer = re.sub(r'<think>.*?</think>\s*', '', content, flags=re.DOTALL).strip()
                if final_answer:
                    print(f"Aza Man: {final_answer}")
        elif hasattr(msg, "content"): 
            content = msg.content
            if content:  
                final_answer = re.sub(r'<think>.*?</think>\s*', '', content, flags=re.DOTALL).strip()
                if final_answer:
                    print(f"Aza Man: {final_answer}")

def main() -> None:
    """Run the Aza Man financial assistant interactively."""
    unique_id = uuid4().hex[:8]
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = f"Aza Man - {unique_id}"

    # Use USER_ID from environment or prompt for it
    user_id = os.getenv("USER_ID")
    if not user_id:
        user_id = input("Enter your User ID (e.g., jake00): ").strip() or "user1"

    thread_id = f"thread_{user_id}"
    config = {"configurable": {"user_id": user_id, "thread_id": thread_id}}

    # Load initial state from checkpointer
    initial_state = graph.graph.get_state(config).values or {}
    print("Welcome to Aza Man, your AI financial assistant!")
    if initial_state.get("username"):
        print(f"Welcome back, {initial_state['username']}! Your last session data is loaded.")
    else:
        print("No prior user data found. Starting fresh!")
        # Manually print the welcome message instead of streaming it
        print("Aza Man: Welcome to Aza Man, your AI financial assistant!")

    while True:
        user_input = input("You: ")
        if user_input.lower().strip() == "exit":
            print("Goodbye!")
            break

        # Stream user input and print assistant responses
        for chunk in graph.graph.stream({"messages": [HumanMessage(content=user_input)]}, config, stream_mode="updates"):
            for node, updates in chunk.items():
                print_assistant_response(updates)

if __name__ == "__main__":
    main()