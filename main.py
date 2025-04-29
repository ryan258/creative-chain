import os
from dotenv import load_dotenv
from crew import build_crew, get_mode_from_input

if __name__ == "__main__":
    load_dotenv()
    print("Welcome to SOLO-IDEAFLOW-OS!")
    user_input = input("Enter your creative prompt or command: ")
    mode = get_mode_from_input(user_input)
    # Pass user_input as last_topic into the workflow
    result = build_crew(mode).run(user_input)
    print("\nResult:\n", result)
