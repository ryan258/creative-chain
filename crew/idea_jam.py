import os
from openai import OpenAI
from crew.prototype import GPTPrototypeCrew
from crew.critic import InteractivePrototypeToCriticCrew

class InteractiveIdeaJamToPrototypeCrew:
    def __init__(self):
        self.model = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def run(self, user_input):
        # Check for "num_ideas=" and "variation=" in the user_input
        import re
        num_ideas = 40
        topic = user_input
        variation_factors = []
        # Parse num_ideas
        match = re.search(r"num_ideas\s*=\s*(\d+)", user_input)
        if match:
            num_ideas = int(match.group(1))
            topic = re.sub(r"num_ideas\s*=\s*\d+\s*\|?", "", topic).strip()
        else:
            # Ask interactively if not specified
            try:
                num_ideas_in = input(f"How many ideas would you like to generate? (Enter for default {num_ideas}): ").strip()
                if num_ideas_in:
                    num_ideas = int(num_ideas_in)
            except Exception:
                pass
        # Parse variation factors (comma or | separated)
        match = re.search(r"variation\s*=\s*([\w,| ]+)", user_input)
        if match:
            variation_factors = [v.strip() for v in re.split(r",|\|", match.group(1)) if v.strip()]
            topic = re.sub(r"variation\s*=\s*[\w,| ]+\s*\|?", "", topic).strip()
        # If not specified, ask interactively
        if not variation_factors:
            print("\nVariation factors help diversify your ideas. Available options:")
            print("  1. technology  2. business model  3. whimsy scale  4. (blank for none/random)")
            var_in = input("Enter variation factors (comma or | separated, or blank for random): ").strip()
            if var_in:
                variation_factors = [v.strip() for v in re.split(r",|\|", var_in) if v.strip()]
        # If still not specified, randomize
        if not variation_factors:
            import random
            all_factors = ['technology', 'business model', 'whimsy scale']
            variation_factors = random.sample(all_factors, k=random.randint(1, len(all_factors)))
            print(f"[Randomized variation factors: {', '.join(variation_factors)}]")
        # Compose variation string for prompt
        variation_str = ", ".join(variation_factors)
        prompt = (
            "You are a creative brainstorming assistant. "
            f"Generate exactly {num_ideas} unique, fun, and imaginative ideas based on this topic: '" + topic + "'. "
            f"Vary the ideas across these axes: {variation_str}. "
            f"Number the ideas 1 to {num_ideas} with no skipped numbers. Do not stop until you have listed all {num_ideas} ideas. "
            "For each idea, give a one-sentence summary. "
            "After the list, group the ideas into 3 distinct clusters based on their themes, approaches, or styles. "
            "For each cluster, provide a short summary of what unites the ideas in that group and list the idea numbers included. "
            "Format the clusters as: CLUSTER 1: <summary> (Ideas: #, #, #...)"
        )
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": "You are a helpful creative assistant."},
                         {"role": "user", "content": prompt}],
                max_tokens=2048,
                temperature=0.9
            )
            ideas_text = response.choices[0].message.content
            # Parse all ideas into a list
            ideas = []
            clusters = []
            in_cluster_section = False
            for line in ideas_text.split("\n"):
                if line.strip().lower().startswith("cluster"):
                    in_cluster_section = True
                    clusters.append(line.strip())
                    continue
                if in_cluster_section:
                    if line.strip():
                        clusters.append(line.strip())
                    continue
                if line.strip() and (line.strip()[0].isdigit() and line.strip()[1] in ".)"):
                    # Remove number and punctuation
                    idea = line.strip().split(".", 1)[-1].strip()
                    ideas.append(idea)
            # If not enough ideas, re-prompt for missing ones
            retry_count = 0
            max_retries = 5
            while len(ideas) < num_ideas and retry_count < max_retries:
                missing = num_ideas - len(ideas)
                print(f"\n[Warning: Only {len(ideas)} ideas generated, requesting {missing} more to reach {num_ideas}] (Attempt {retry_count+1}/{max_retries})")
                followup_prompt = (
                    f"Continue the previous list. Generate {missing} more unique ideas for the topic: '{topic}'. "
                    f"Vary the ideas across these axes: {variation_str}. "
                    f"Number them from {len(ideas)+1} to {num_ideas}. For each idea, give a one-sentence summary. "
                    "After the list, group all the ideas into the same 3 clusters as before (update if needed). "
                    "Format the clusters as: CLUSTER 1: <summary> (Ideas: #, #, #...)"
                )
                followup_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "system", "content": "You are a helpful creative assistant."},
                             {"role": "user", "content": followup_prompt}],
                    max_tokens=1024,
                    temperature=0.9
                )
                followup_text = followup_response.choices[0].message.content
                new_ideas = []
                in_cluster_section_followup = False
                new_clusters = []
                for line in followup_text.split("\n"):
                    if line.strip().lower().startswith("cluster"):
                        in_cluster_section_followup = True
                        new_clusters.append(line.strip())
                        continue
                    if in_cluster_section_followup:
                        if line.strip():
                            new_clusters.append(line.strip())
                        continue
                    if line.strip() and (line.strip()[0].isdigit() and line.strip()[1] in ".)"):
                        idx = int(line.strip().split(".", 1)[0])
                        if idx > len(ideas) and idx <= num_ideas:
                            idea = line.strip().split(".", 1)[-1].strip()
                            new_ideas.append((idx, idea))
                if not new_ideas:
                    print("[Error: No new ideas generated in follow-up. Stopping retries.]")
                    break
                # Sort and append new ideas by their number
                new_ideas.sort()
                for idx, idea in new_ideas:
                    if len(ideas) < idx-1:
                        # Fill any skipped numbers with a placeholder
                        for _ in range(len(ideas), idx-1):
                            ideas.append("[Placeholder: Idea missing]")
                    ideas.append(idea)
                ideas = ideas[:num_ideas]  # Truncate if somehow too many
                # Always update clusters if new ones found
                if new_clusters:
                    clusters = new_clusters
                retry_count += 1
            if len(ideas) < num_ideas:
                print(f"\n[Warning: Only {len(ideas)} unique ideas could be generated after {retry_count} retries.]")
            if not ideas:
                return f"IDEAS:\n{ideas_text}\n\n[Could not extract ideas for selection]"
            # Show ideas and clusters, then prompt for selection
            print("\nIDEAS:")
            for idx, idea in enumerate(ideas, 1):
                print(f"  {idx}. {idea}")
            if clusters:
                print("\n3-CLUSTER SUMMARY:")
                for cl in clusters:
                    print(f"  {cl}")
            else:
                print("\n[No clusters found. Try generating more ideas or rephrasing your prompt.]")
                print("\n--- RAW LLM OUTPUT FOR DEBUGGING ---\n")
                print(ideas_text)
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
            # Show the prototype and present options before sending to critic
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
                    return PostCritiqueInteractiveLoop(chosen_idea, prototype, critique.split("CRITIQUE:\n", 1)[-1] if "CRITIQUE:" in critique else critique, last_topic=topic).run()
                elif choice == "restart":
                    print("\nRestarting from the beginning...\n")
                    from crew import build_crew
                    return build_crew("idea_jam").run(input("Enter your new creative prompt: "))
                elif choice == "":
                    print("\nReturning to idea selection...")
                    from crew import build_crew
                    return build_crew("idea_jam").run(input("Enter your creative prompt again (or press Enter to reuse previous): "))
                else:
                    from crew.reiterate import GPTReiterateCrew
                    reiteration = GPTReiterateCrew().run([prototype, choice])
                    print("\nREITERATION (based on your feedback):\n" + reiteration)
                    # Immediately send reiteration to critic and enter post-critique loop
                    from crew.critic import GPTCriticCrew
                    critique = GPTCriticCrew().run([chosen_idea, reiteration])
                    from crew.interactive_loop import PostCritiqueInteractiveLoop
                    return PostCritiqueInteractiveLoop(chosen_idea, reiteration, critique.split("CRITIQUE:\n", 1)[-1] if "CRITIQUE:" in critique else critique, last_topic=topic).run()
        except Exception as e:
            return f"[Error generating ideas: {e}]"
