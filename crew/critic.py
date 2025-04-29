import os
from openai import OpenAI

class InteractivePrototypeToCriticCrew:
    def __init__(self):
        self.model = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def run(self, idea_and_proto):
        idea, prototype = idea_and_proto
        prompt = (
            f"You are an exceptionally constructive, actionable, and supportive critic. "
            f"Here is an idea: '{idea}'.\nHere is its prototype: '{prototype}'.\n"
            "Your job is to help the creator iterate forward most productively towards an amazing final product.\n"
            "Give concise, specific, and actionable positive and negative feedback on the prototype.\n"
            "For each negative point, suggest a concrete way to address or improve it.\n"
            "Format as: Positive: ... Negative: ... Suggestions: ..."
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": "You are a helpful critic."},
                         {"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[Error generating critique: {e}]"

class GPTCriticCrew:
    def __init__(self):
        self.model = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
    def run(self, idea_and_proto):
        idea, prototype = idea_and_proto
        prompt = (
            f"You are an exceptionally constructive, actionable, and supportive critic. "
            f"Here is an idea: '{idea}'.\nHere is its prototype: '{prototype}'.\n"
            "Your job is to help the creator iterate forward most productively towards an amazing final product.\n"
            "Give concise, specific, and actionable positive and negative feedback on the prototype.\n"
            "For each negative point, suggest a concrete way to address or improve it.\n"
            "Format as: Positive: ... Negative: ... Suggestions: ..."
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": "You are a helpful critic."},
                         {"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[Error generating critique: {e}]"
