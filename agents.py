# agents.py - CrewAI agent stubs

class IdeaJamAgent:
    def __init__(self):
        pass
    def generate_ideas(self, topic):
        return ["Idea 1", "Idea 2", "Idea 3"]

class PrototypeAgent:
    def __init__(self):
        pass
    def create_prototype(self, idea):
        return f"Prototype for {idea}"

class CriticAgent:
    def __init__(self):
        pass
    def critique(self, prototype):
        return "Positive: ... Negative: ..."

class ReiterateAgent:
    def __init__(self):
        pass
    def reiterate(self, artifact, critique):
        return f"Improved version of {artifact}"

class VaultAgent:
    def __init__(self):
        pass
    def archive(self, idea):
        return f"Archived: {idea}"

class AssistAgent:
    def __init__(self):
        pass
    def answer(self, question):
        return "Answer stub"

class ConsultAgent:
    def __init__(self):
        pass
    def consult(self, topic):
        return ["Trend 1", "Analog 1", "Quote 1"]
