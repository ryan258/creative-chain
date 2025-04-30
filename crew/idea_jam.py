import os
from openai import OpenAI
from crew.prototype import GPTPrototypeCrew
from crew.critic import InteractivePrototypeToCriticCrew

class InteractiveIdeaJamToPrototypeCrew:
    def __init__(self):
        self.model = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def _generate_ideas_and_clusters(self, user_input, num_ideas=None):
        import re, json
        default_num_ideas = 40
        topic = user_input
        variation_factors = []
        if num_ideas is not None:
            n_ideas = num_ideas
        else:
            match = re.search(r"num_ideas\s*=\s*(\d+)", user_input)
            if match:
                n_ideas = int(match.group(1))
                topic = re.sub(r"num_ideas\s*=\s*\d+\s*\|?", "", topic).strip()
            else:
                n_ideas = default_num_ideas
        match = re.search(r"variation\s*=\s*([\w,| ]+)", user_input)
        if match:
            variation_factors = [v.strip() for v in re.split(r",|\|", match.group(1)) if v.strip()]
            topic = re.sub(r"variation\s*=\s*[\w,| ]+\s*\|?", "", topic).strip()
        if not variation_factors:
            variation_factors = []
        prompt = (
            f"You are a creative ideation assistant. "
            f"Given the topic: '{topic}', generate a list of {n_ideas} imaginative ideas. "
            f"Vary the ideas across these axes: {', '.join(variation_factors)}. "
            "After generating the list, group the ideas into 2-4 clusters based on common themes. "
            "Return ONLY a valid JSON object in this format: {'clusters': [ {'title': '...', 'desc': '...', 'ideas': [ {'text': '...'} ] } ]}. Do not include any text before or after the JSON."
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": "You are a helpful creative assistant."},
                         {"role": "user", "content": prompt}],
                max_tokens=1800,
                temperature=0.9
            )
            ideas_text = response.choices[0].message.content
            try:
                data = json.loads(ideas_text)
                clusters = data.get('clusters', [])
                ideas = []
                for cidx, cluster in enumerate(clusters):
                    for idea in cluster.get('ideas', []):
                        ideas.append({
                            'text': idea.get('text', str(idea)),
                            'cluster': cluster.get('title', ''),
                            'cluster_desc': cluster.get('desc', ''),
                            'cluster_idx': cidx
                        })
                ideas = ideas[:n_ideas]
                return {'ideas': ideas, 'clusters': clusters}
            except Exception as e:
                return {'ideas': [], 'clusters': [], 'error': f'Could not parse LLM output as JSON: {e}', 'raw': ideas_text}
        except Exception as e:
            return {'ideas': [], 'clusters': [], 'error': f'Error generating ideas: {e}'}

    def run_web(self, user_input):
        """Web-friendly version: returns ideas/clusters for Flask route."""
        import flask
        num_ideas = None
        try:
            num_ideas = flask.session.get('num_ideas', None)
        except Exception:
            pass
        return self._generate_ideas_and_clusters(user_input, num_ideas=num_ideas)

    def run(self, user_input):
        import re
        result = self._generate_ideas_and_clusters(user_input)
        ideas = result.get('ideas', [])
        clusters = result.get('clusters', [])
        if not ideas:
            print("[No ideas generated. Try again or check your prompt.]")
            if 'error' in result:
                print(result['error'])
            if 'raw' in result:
                print("\n--- RAW LLM OUTPUT FOR DEBUGGING ---\n")
                print(result['raw'])
            return None
        print("\nIDEAS:")
        for idx, idea in enumerate(ideas, 1):
            print(f"  {idx}. {idea['text']}")
        if clusters:
            print("\nCLUSTERS:")
            for cl in clusters:
                print(f"- {cl.get('title', '')}: {cl.get('desc', '')}")
        sel = input(f"\nWhich idea do you want to prototype? (1-{len(ideas)}, Enter for 1): ").strip()
        try:
            sel_idx = int(sel) - 1 if sel else 0
            if not (0 <= sel_idx < len(ideas)):
                sel_idx = 0
        except Exception:
            sel_idx = 0
        chosen_idea = ideas[sel_idx]['text']
        prototype = GPTPrototypeCrew().run(chosen_idea)
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
                return self.run(user_input)
            else:
                from crew.reiterate import GPTReiterateCrew
                reiteration = GPTReiterateCrew().run([prototype, choice])
                print("\nREITERATION (based on your feedback):\n" + reiteration)
                from crew.critic import GPTCriticCrew
                critique = GPTCriticCrew().run([chosen_idea, reiteration])
                from crew.interactive_loop import PostCritiqueInteractiveLoop
                return PostCritiqueInteractiveLoop(chosen_idea, reiteration, critique.split("CRITIQUE:\n", 1)[-1] if "CRITIQUE:" in critique else critique, last_topic=user_input).run()
