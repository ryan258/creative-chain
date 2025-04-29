import re
import os
from agents import VaultAgent
from crew.reiterate import GPTReiterateCrew
from crew.critic import GPTCriticCrew

class PostCritiqueInteractiveLoop:
    def __init__(self, idea, prototype, critique, last_topic=None):
        self.idea = idea
        self.prototype = prototype
        self.critique = critique
        self.last_topic = last_topic or idea  # Use idea as fallback for topic

    def run(self):
        while True:
            print("\nPROTOTYPE:\n" + self.prototype)
            print("\nCRITIQUE:\n" + self.critique)
            print("\nWhat would you like to do next?")
            print("  1. reiterate - Improve this prototype (using your feedback or the critique)")
            print("  2. critic    - Get another critique on the current prototype")
            print("  3. pick      - Pick a new idea/prototype")
            print("  4. restart   - Restart the workflow from the beginning (idea jam mode)")
            print("  5. save      - Save this idea/prototype as a creative project brief for development")
            print("  6. exit      - Exit the program")
            choice = input("\nChoose: (1/2/3/4/5/6 or reiterate/critic/pick/restart/save/exit): ").strip().lower()
            if choice in ["1", "reiterate"]:
                feedback = input("\nEnter your feedback or press Enter to use the critique suggestions: ").strip()
                if not feedback:
                    feedback = self.critique
                reiteration = GPTReiterateCrew().run([self.prototype, feedback])
                print("\nREITERATION (based on feedback):\n" + reiteration)
                self.prototype = reiteration
            elif choice in ["2", "critic"]:
                new_critique = GPTCriticCrew().run([self.idea, self.prototype])
                self.critique = new_critique.split("CRITIQUE:\n", 1)[-1] if "CRITIQUE:" in new_critique else new_critique
            elif choice in ["3", "pick"]:
                print("\nReturning to idea selection...")
                from crew import build_crew
                topic = input("Enter your creative prompt again (or press Enter to reuse previous): ").strip()
                if not topic:
                    topic = self.last_topic
                return build_crew("idea_jam").run(topic)
            elif choice in ["4", "restart"]:
                print("\nRestarting from the beginning...\n")
                from crew import build_crew
                return build_crew("idea_jam").run(input("Enter your new creative prompt: "))
            elif choice in ["5", "save"]:
                vault = VaultAgent()
                brief = f"# PROJECT BRIEF\n\n**Idea:** {self.idea}\n\n**Prototype:** {self.prototype}\n\n**Critique:** {self.critique}"
                archive_result = vault.archive(brief)
                os.makedirs("ideas", exist_ok=True)
                title_match = re.search(r"\*\*(.*?)\*\*", self.idea)
                if title_match:
                    base_title = title_match.group(1).strip()
                else:
                    import datetime
                    base_title = f"idea_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S') }"
                # Sanitize filename for Windows
                base_title = re.sub(r'[<>:"/\\|?*]', '', base_title)
                base_title = base_title.replace(' ', '_')
                filename = f"ideas/{base_title}.md"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(brief)
                print(f"\nSaved to Vault: {archive_result}\nSaved as markdown: {filename}\n")
            elif choice in ["6", "exit"]:
                print("\nExiting. Have a creative day!")
                exit(0)
            else:
                print("\nInvalid choice. Please select one of: 1/2/3/4/5/6 or reiterate, critic, pick, restart, save, exit.")
