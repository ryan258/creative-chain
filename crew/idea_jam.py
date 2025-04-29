import os
from openai import OpenAI
from crew.prototype import GPTPrototypeCrew
from crew.critic import InteractivePrototypeToCriticCrew

class InteractiveIdeaJamToPrototypeCrew:
    def __init__(self):
        self.model = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def run(self, user_input):
        prompt = (
            "You are a creative brainstorming assistant. "
            "Generate 5 unique, fun, and imaginative ideas based on this topic: '" + user_input + "'. "
            "For each idea, give a one-sentence summary. Number the ideas."
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": "You are a helpful creative assistant."},
                         {"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.9
            )
            ideas_text = response.choices[0].message.content
            # Parse all ideas into a list
            ideas = []
            for line in ideas_text.split("\n"):
                if line.strip() and (line.strip()[0].isdigit() and line.strip()[1] in ".)"):
                    # Remove number and punctuation
                    idea = line.strip().split(".", 1)[-1].strip()
                    ideas.append(idea)
            if not ideas:
                return f"IDEAS:\n{ideas_text}\n\n[Could not extract ideas for selection]"
            # Show ideas and prompt for selection
            print("\nIDEAS:")
            for idx, idea in enumerate(ideas, 1):
                print(f"  {idx}. {idea}")
            sel = input(f"\nWhich idea do you want to prototype? (1-{len(ideas)}, Enter for 1): ").strip()
            try:
                sel_idx = int(sel) - 1 if sel else 0
                if not (0 <= sel_idx < len(ideas)):
                    sel_idx = 0
            except Exception:
                sel_idx = 0
            chosen_idea = ideas[sel_idx]
            # Now generate a prototype for the chosen idea
            prototype = GPTPrototypeCrew().run(chosen_idea)
            # Show the prototype and present options before sending to critic
            while True:
                print(f"\nPROTOTYPE for '{chosen_idea}':\n{prototype}")
                print("\nOptions:")
                print("  y     - Send this prototype to the critic for feedback")
                print("  <your feedback> - Enter your own feedback to generate a reiteration")
                print("  <blank> - Show the list of ideas again to pick a different one")
                print("  restart - Restart the workflow from the beginning (idea jam mode)")
                print("  exit    - Exit the program")
                choice = input("\nWhat would you like to do? (y/feedback/blank/restart/exit): ").strip().lower()
                if choice == "exit":
                    print("\nExiting. Have a creative day!")
                    exit(0)
                elif choice == "y":
                    from crew.critic import GPTCriticCrew
                    critique = GPTCriticCrew().run([chosen_idea, prototype])
                    from crew.interactive_loop import PostCritiqueInteractiveLoop
                    return PostCritiqueInteractiveLoop(chosen_idea, prototype, critique.split("CRITIQUE:\n", 1)[-1] if "CRITIQUE:" in critique else critique, last_topic=user_input).run()
                elif choice == "restart":
                    print("\nRestarting from the beginning...\n")
                    from crew import build_crew
                    return build_crew("idea_jam").run(input("Enter your new creative prompt: "))
                elif choice == "":
                    print("\nReturning to idea selection...")
                    from crew import build_crew
                    return build_crew("idea_jam").run(input("Enter your creative prompt again (or press Enter to reuse previous): "))
                else:
                    from crew.reiterate import GPTReiterateCrew
                    reiteration = GPTReiterateCrew().run([prototype, choice])
                    print("\nREITERATION (based on your feedback):\n" + reiteration)
                    # Immediately send reiteration to critic and enter post-critique loop
                    from crew.critic import GPTCriticCrew
                    critique = GPTCriticCrew().run([chosen_idea, reiteration])
                    from crew.interactive_loop import PostCritiqueInteractiveLoop
                    return PostCritiqueInteractiveLoop(chosen_idea, reiteration, critique.split("CRITIQUE:\n", 1)[-1] if "CRITIQUE:" in critique else critique, last_topic=user_input).run()
        except Exception as e:
            return f"[Error generating ideas: {e}]"
