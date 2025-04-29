import os
from openai import OpenAI
from agents import IdeaJamAgent, PrototypeAgent, CriticAgent, ReiterateAgent, VaultAgent, AssistAgent, ConsultAgent
from tasks import get_tasks_for_mode

# This function builds the crew based on the selected mode(s)
def build_crew(mode):
    if mode == "idea_jam":
        return GPTIdeaJamCrew()
    # TODO: Add logic for other modes
    return CrewStub(mode)

class CrewStub:
    def __init__(self, mode):
        self.mode = mode
    def run(self, user_input):
        return f"[Stub] Would run mode: {self.mode} with input: {user_input}"

class GPTIdeaJamCrew:
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
            return response.choices[0].message.content
        except Exception as e:
            return f"[Error generating ideas: {e}]"

def get_mode_from_input(user_input):
    # TODO: Parse mode from user input string
    return "idea_jam"
