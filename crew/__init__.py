import os
from openai import OpenAI

def build_crew(mode):
    if mode == "idea_jam":
        from crew.idea_jam import InteractiveIdeaJamToPrototypeCrew
        return InteractiveIdeaJamToPrototypeCrew()
    elif mode == "prototype":
        from crew.prototype import GPTPrototypeCrew
        return GPTPrototypeCrew()
    elif mode == "critic":
        from crew.critic import InteractivePrototypeToCriticCrew
        return InteractivePrototypeToCriticCrew()
    elif mode == "reiterate":
        from crew.reiterate import GPTReiterateCrew
        return GPTReiterateCrew()
    else:
        raise ValueError(f"Unknown mode: {mode}")

def get_mode_from_input(user_input):
    if user_input.lower().startswith("mode="):
        return user_input.split("|", 1)[0].replace("mode=", "").strip()
    return "idea_jam"

class CrewStub:
    def run(self, *args, **kwargs):
        print("Stub crew: not implemented.")
        return None
