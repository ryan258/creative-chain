import os
from openai import OpenAI
from agents import IdeaJamAgent, PrototypeAgent, CriticAgent, ReiterateAgent, VaultAgent, AssistAgent, ConsultAgent
from tasks import get_tasks_for_mode

# This function builds the crew based on the selected mode(s)
def build_crew(mode):
    if mode == "idea_jam":
        return InteractiveIdeaJamToPrototypeCrew()
    if mode == "prototype":
        return InteractivePrototypeToCriticCrew()
    if mode == "critic":
        return GPTCriticCrew()
    # TODO: Add logic for other modes
    return CrewStub(mode)

class CrewStub:
    def __init__(self, mode):
        self.mode = mode
    def run(self, user_input):
        return f"[Stub] Would run mode: {self.mode} with input: {user_input}"

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
            return InteractivePrototypeToCriticCrew().run([chosen_idea, prototype])
        except Exception as e:
            return f"[Error generating ideas: {e}]"

class GPTPrototypeCrew:
    def __init__(self):
        self.model = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
    def run(self, idea_text):
        prompt = (
            f"You are a prototyping assistant. Given this idea: '{idea_text}', "
            "write a short, vivid text description of what a first prototype or demo might look like. "
            "Be concrete and imaginative, but keep it concise."
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": "You are a helpful prototyping assistant."},
                         {"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.8
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[Error generating prototype: {e}]"

class InteractivePrototypeToCriticCrew:
    def __init__(self):
        self.model = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
    def run(self, idea_and_proto):
        idea, prototype = idea_and_proto
        while True:
            print("\nPROTOTYPE:")
            print(prototype)
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
                critique = GPTCriticCrew().run([idea, prototype])
                # Always enter the post-critique loop after any critique
                return PostCritiqueInteractiveLoop(idea, prototype, critique.split("CRITIQUE:\n", 1)[-1] if "CRITIQUE:" in critique else critique).run()
            elif choice == "restart":
                print("\nRestarting from the beginning...\n")
                return build_crew("idea_jam").run(input("Enter your new creative prompt: "))
            elif choice == "":
                print("\nReturning to idea selection...")
                return build_crew("idea_jam").run(input("Enter your creative prompt again (or press Enter to reuse previous): "))
            else:
                reiteration = GPTReiterateCrew().run([prototype, choice])
                print("\nREITERATION (based on your feedback):\n" + reiteration)
                # Immediately send reiteration to critic and enter post-critique loop
                critique = GPTCriticCrew().run([idea, reiteration])
                return PostCritiqueInteractiveLoop(idea, reiteration, critique.split("CRITIQUE:\n", 1)[-1] if "CRITIQUE:" in critique else critique).run()

class GPTCriticCrew:
    def __init__(self):
        self.model = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
    def run(self, idea_and_proto):
        idea, prototype = idea_and_proto
        prompt = (
            f"You are an exceptionally constructive, actionable, and supportive critic. "
            f"Here is an idea: '{idea}'.\n"
            f"Here is its prototype: '{prototype}'.\n"
            "Your job is to help the creator iterate forward most productively towards an amazing final product.\n"
            "Give concise, specific, and actionable positive and negative feedback on the prototype.\n"
            "For each negative point, suggest a concrete way to address or improve it.\n"
            "Format as: Positive: ... Negative: ... Suggestions: ..."
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": "You are a helpful, constructive critic."},
                         {"role": "user", "content": prompt}],
                max_tokens=350,
                temperature=0.7
            )
            return f"PROTOTYPE:\n{prototype}\n\nCRITIQUE:\n{response.choices[0].message.content}"
        except Exception as e:
            return f"[Error generating critique: {e}]"

class GPTReiterateCrew:
    def __init__(self):
        self.model = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
    def run(self, proto_and_feedback):
        prototype, feedback = proto_and_feedback
        prompt = (
            f"You are a creative assistant. Here is a prototype: '{prototype}'.\n"
            f"Here is user feedback: '{feedback}'.\n"
            "Revise and improve the prototype based on the feedback. Keep it concise and creative."
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": "You are a helpful creative assistant."},
                         {"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.8
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[Error generating reiteration: {e}]"

class PostCritiqueInteractiveLoop:
    def __init__(self, idea, prototype, critique):
        self.idea = idea
        self.prototype = prototype
        self.critique = critique

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
                return build_crew("idea_jam").run(input("Enter your creative prompt again (or press Enter to reuse previous): "))
            elif choice in ["4", "restart"]:
                print("\nRestarting from the beginning...\n")
                return build_crew("idea_jam").run(input("Enter your new creative prompt: "))
            elif choice in ["5", "save"]:
                from agents import VaultAgent
                import os
                import re
                vault = VaultAgent()
                brief = f"# PROJECT BRIEF\n\n**Idea:** {self.idea}\n\n**Prototype:** {self.prototype}\n\n**Critique:** {self.critique}"
                archive_result = vault.archive(brief)
                os.makedirs("ideas", exist_ok=True)
                title_match = re.search(r"\*\*(.*?)\*\*", self.idea)
                if title_match:
                    base_title = title_match.group(1).strip().replace(" ", "_")
                else:
                    import datetime
                    base_title = f"idea_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
                filename = f"ideas/{base_title}.md"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(brief)
                print(f"\nSaved to Vault: {archive_result}\nSaved as markdown: {filename}\n")
            elif choice in ["6", "exit"]:
                print("\nExiting. Have a creative day!")
                exit(0)
            else:
                print("\nInvalid choice. Please select one of: 1/2/3/4/5/6 or reiterate, critic, pick, restart, save, exit.")

def get_mode_from_input(user_input):
    # TODO: Parse mode from user input string
    return "idea_jam"
