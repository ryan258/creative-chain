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
    def __init__(self, critics=1):
        self.model = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.critics = critics

    def run(self, idea_and_proto):
        idea, prototype = idea_and_proto
        results = []
        for i in range(self.critics):
            prompt = (
                f"You are an exceptionally constructive, actionable, and supportive critic.\n"
                f"Here is an idea: '{idea}'.\n"
                f"Here is its prototype: '{prototype}'.\n"
                "Your job is to help the creator iterate forward most productively towards an amazing final product.\n"
                "Give concise, specific, and actionable feedback in the following structure:\n"
                "\nPOSITIVE: (What works well)\nNEGATIVE: (What needs improvement)\nSUGGESTIONS: (Concrete ways to improve negatives)\n"
                "\nNow, analyze the prototype for: regressions (what got worse), neutral shifts (changes that neither improved nor worsened), and improvements (what got better).\n"
                "List each under REGRESSIONS, NEUTRAL SHIFTS, and IMPROVEMENTS.\n"
                "\nProvide a STOPLIGHT VERDICT (GREEN/YELLOW/RED) for overall quality and readiness.\n"
                "\nCreate a DELTA TABLE with these columns: Aspect | +Delta (improved) | -Delta (regressed) | Neutral.\n"
                "Aspects: usability, load_time, accessibility. Use placeholder values if unsure.\n"
                "\nFormat the output as:\n"
                "POSITIVE: ...\nNEGATIVE: ...\nSUGGESTIONS: ...\n\nREGRESSIONS: ...\nNEUTRAL SHIFTS: ...\nIMPROVEMENTS: ...\n\nSTOPLIGHT VERDICT: ...\n\nDELTA TABLE:\n| Aspect       | +Delta | -Delta | Neutral |\n|--------------|--------|--------|---------|\n| usability    |   ?    |   ?    |    ?    |\n| load_time    |   ?    |   ?    |    ?    |\n| accessibility|   ?    |   ?    |    ?    |"
            )
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "system", "content": "You are a helpful, constructive critic."},
                             {"role": "user", "content": prompt}],
                    max_tokens=700,
                    temperature=0.7
                )
                results.append(f"CRITIC {i+1} RESPONSE:\n{response.choices[0].message.content}\n")
            except Exception as e:
                results.append(f"CRITIC {i+1} ERROR: [Error generating critique: {e}]")
        return f"PROTOTYPE:\n{prototype}\n\n" + "\n".join(results)
