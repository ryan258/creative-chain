import os
from openai import OpenAI

class GPTPrototypeCrew:
    def __init__(self):
        self.model = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def run(self, idea):
        prompt = (
            f"You are a creative prototyping assistant. "
            f"Given the idea: '{idea}', generate a concise prototype description or plan. "
            "Keep it actionable and inspiring."
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": "You are a helpful prototyping assistant."},
                         {"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.8
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"[Error generating prototype: {e}]"
