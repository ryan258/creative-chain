import os
from openai import OpenAI

class GPTReiterateCrew:
    def __init__(self):
        self.model = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def run(self, proto_and_feedback):
        prototype, feedback = proto_and_feedback
        prompt = (
            f"You are an expert at iterating on creative prototypes. "
            f"Here is the current prototype: '{prototype}'.\nHere is the feedback: '{feedback}'.\n"
            "Revise or extend the prototype based on the feedback. Make it more actionable, creative, or clear."
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": "You are a helpful iteration assistant."},
                         {"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.8
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[Error generating reiteration: {e}]"
