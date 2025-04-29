# SOLO-IDEAFLOW-OS Development Roadmap

**Last Updated:** April 29, 2025

## Vision

To create an AI-powered partner using **CrewAI** that streamlines the **Solo Innovator's Ideaflow** (brainstorm → prototype → critique → reiterate → vault), enabling rapid generation, testing, and refinement of ideas within a unified, interactive system.

## Guiding Principles

* **Modular Design:** Leverage CrewAI's agent/task structure to represent distinct workflow modes.
* **Actionable Output:** Prioritize concise, structured, and useful outputs from agents.
* **Iterative Development:** Build core functionality first and enhance features incrementally.
* **Solo Creator Focus:** Keep the end-user (a solo innovator) in mind for usability and features.
* **Honest Feedback Loop:** Ensure the `critic` and `reiterate` modes provide genuine value for improvement.

## Progress Update (as of April 29, 2025)

### What We've Done

- [x] **IdeaJamAgent (Basic):** Generates creative ideas from a topic using GPT-4o-mini.
- [x] **Interactive Step Selection:** After each step, user can pick next action (prototyping, critique, feedback, restart).
- [x] **PrototypeAgent (Basic):** Produces concise prototype descriptions from chosen ideas.
- [x] **CriticAgent (Basic):** Gives actionable, constructive feedback on prototypes.
- [x] **Post-Critique Interactive Loop:** After critique, user can reiterate, re-critique, pick a new idea, restart, exit, or now **save** as a project brief.
- [x] **VaultAgent (Stub):** Added `save` option to archive idea/prototype/critique as a creative project brief for handoff to a team.
- [x] **Minimal Typing Experience:** All steps designed for hands-free/low-typing, menu-driven interaction.
- [x] **Exit Only on Explicit Command:** Program only exits if user types 'exit'.

### Where We Are At

- The core interactive workflow is implemented and stable for continuous creative iteration.
- User can now archive their best ideas and iterations at any time for future development.
- The system is ready for further enhancements, especially around persistence, richer Vault features, and more advanced agent behaviors.

## Recent Progress (April 29, 2025)

- Project briefs now saved as markdown in /ideas
- Menu options now numbered and selectable by number or word
- HAPPYPATH.md created for easy workflow testing
- .gitignore updated to exclude /ideas/*.md

## Development Phases

This roadmap outlines a potential path. Tasks can be moved between phases based on priority and dependencies. Status indicators:
* `[ ]` Planned
* `[/]` In Progress
* `[x]` Done

---

### Phase 0: Foundation & Setup (Getting Ready)

*Goal: Establish the basic project structure, environment, and core CrewAI setup.*

* `[x]` Initialize GitHub repository with `README.md`, `.gitignore`.
* `[x]` Set up Python virtual environment (using `venv`).
* `[x]` Install core dependencies (`crewai`, LLM provider library, `python-dotenv`). Manage with `requirements.txt`.
* `[x]` Configure `.env` for API keys (LLM provider minimum).
* `[x]` Create basic project structure (`main.py`, `crew.py`, potentially `agents.yaml`/`tasks.yaml` if using config files).
* `[ ]` Implement basic LLM connection test within CrewAI.
* `[ ]` Define placeholder `Agent` structures in code or YAML (roles, goals, backstories).
* `[x]` Implement rudimentary mode selection logic (e.g., parse `mode=` from input in `main.py` or entry script).

---

### Phase 1: Core Workflow Loop - MVP (Proof of Concept)

*Goal: Implement a minimal viable loop for idea generation, prototyping, and critique.*

* `[x]` **Implement `IdeaJamAgent` (Basic):**
    * `[x]` Generate a fixed number of ideas based on a topic. (GPT-4o-mini powered, working)
* `[x]` **Add Interactive Selection Between Steps:**
    * `[x]` After idea generation, allow user to pick which idea to prototype ("man in the middle" pattern).
    * `[x]` After prototyping, allow user to pick which prototype to send to critique, add feedback, or restart (pattern reusable for all steps).
* `[x]` **Implement `PrototypeAgent` (Basic):**
    * `[x]` Generate a simple text description based on a selected idea. (GPT-4o-mini powered, working)
* `[x]` **Implement `CriticAgent` (Basic):**
    * `[x]` Provide exceptionally constructive, actionable positive/negative feedback and concrete suggestions on the prototype description.
* `[x]` **Add Post-Critique Interactive Loop:**
    * `[x]` After critique, let the user choose to iterate, pick a new idea/prototype, restart, exit, or save as a project brief—never get stuck at the end.
* `[x]` **Define Basic `Tasks`:** Create corresponding CrewAI tasks for the above agents.
* `[x]` **Implement Sequential Workflow:** Enable basic chaining like `modes=[idea_jam → prototype → critic]`.
* `[x]` Handle basic user input for the initial topic/prompt.

---

### Phase 2: Enhancing Core Modes (Adding Depth)

*Goal: Flesh out the core MVP modes with the specific features defined in the original instructions.*

* `[x]` **`IdeaJamAgent` Enhancements:**
    * `[x]` Control number of ideas generated (use default, allow override).
    * `[x]` Implement variation factors (technology, business model, whimsy scale).
    * `[x]` Add 3-cluster summary output.
* `[x]` **`CriticAgent` Enhancements:**
    * `[x]` Implement detailed feedback structure (regressions, neutral shifts, improvements).
    * `[x]` Generate ± delta table (usability, load_time, accessibility - placeholders for now).
    * `[x]` Implement STOPLIGHT verdict (GREEN/YELLOW/RED).
    * `[x]` Add support for multiple critics (`critics=X`, now always 3 by default).
    * `[x]` Aggregate and summarize multi-critic feedback for reiteration (hands-off, auto-summarized, summary shown to user).
* `[ ]` **`PrototypeAgent` Enhancements:**
    * `[ ]` Implement specific output formats (UI layout description, code skeleton + TODOs).
* `[x]` **Implement `ReiterateAgent` (Core):**
    * `[x]` Basic capability to receive artifact + critique and generate a new version (now uses multi-critic summary).

---

**Current Status:**
- The workflow supports accessible, hands-off ideation, prototyping, and critique with multi-perspective, summarized feedback.
- You are here: **CriticAgent Enhancements (multi-critic, summary, and transparency complete).**
- Next up: PrototypeAgent output format improvements or additional features as prioritized.

---

### Phase 3: Supporting Modes & Persistence (Expanding Utility)

*Goal: Implement the `vault` for memory and the helper modes (`assist`, `consult`).*

* `[ ]` **Implement `VaultAgent` & Tasks:**
    * `[ ]` Design basic persistence mechanism (e.g., JSON file, SQLite DB).
    * `[ ]` Implement `tag` command.
    * `[ ]` Implement `search` command (by tag/keyword).
    * `[ ]` Implement `remix` command (basic concept).
    * `[ ]` Implement `weekly_review` summary.
    * `[ ]` Implement JSON snippet output.
    * `[ ]` Add confirmation prompt for exposing potentially private notes.
* `[ ]` **Implement `AssistAgent`:** Simple pass-through to LLM for general Q&A.
* `[ ]` **Implement `ConsultAgent`:** Generate 3 concise inspiration seeds (trends, analogs, quotes).

---

### Phase 4: Enhancements, Polish & Global Features (Maturing the System)

*Goal: Implement global controls, improve robustness, and refine user experience.*

* `[ ]` **Implement Global Guidelines:**
    * `[ ]` Enforce structured output (lists, tables etc.) where applicable.
    * `[ ]` Implement token budget monitoring/warnings.
    * `[ ]` Implement delta citation logic in `reiterate`.
    * `[ ]` Refine `critic` prompts for honest feedback tone.
    * `[ ]` Implement internal risk check placeholder (privacy, bias, safety).
    * `[ ]` Implement missing info handling (ask one question).
* `[ ]` **Implement Global Commands:**
    * `[ ]` `verbosity=brief|normal|full`.
    * `[ ]` `reset` command functionality.
    * `[ ]` `export prompts` command (basic implementation).
* `[ ]` **Implement Tracking & Notifications:**
    * `[ ]` Internal iteration cycle counter.
    * `[ ]` Notification to user every X cycles.
    * `[ ]` Suggestion to checkpoint to Vault after significant iterations.
* `[ ]` **Improve Error Handling:** More graceful handling of API errors, invalid inputs etc.
* `[ ]` **Prompt Engineering:** Review and refine prompts for all agents based on testing.
* `[ ]` **Testing:** Add basic unit or integration tests.
* `[ ]` **Documentation:** Update `README.md`, add usage examples, potentially inline code comments.

---

### Phase 5: Future Exploration (Beyond v2.1 Spec)

*Goal: Consider features and improvements beyond the initial scope.*

* `[ ]` **User Interface:** Explore possibilities (Web UI using Flask/Streamlit, Desktop app?).
* `[ ]` **Advanced Vault:** Semantic search, visual clustering, trend analysis over archived ideas.
* `[ ]` **Tool Integration:** Connect `prototype` mode to actual tools (Figma, Replit, GitHub Gists).
* `[ ]` **Advanced Collaboration:** Explore hierarchical crews or more dynamic agent interactions.
* `[ ]` **User Profiles:** Allow customization of prompts, default modes, preferences.
* `[ ]` **Performance Optimization:** Caching results, parallel task execution where feasible in CrewAI.
* `[ ]` **Deployment:** Package the application for easier distribution or cloud deployment.

---

*This roadmap is a living document and will be updated as the project progresses. Priorities may shift based on development findings and user feedback.*