# SOLO-IDEAFLOW-OS

**An AI Partner for the Solo Innovator's Workflow**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

SOLO-IDEAFLOW-OS is an AI-powered assistant designed to streamline the creative and iterative process for solo creators, innovators, and entrepreneurs. Built using the **CrewAI** framework, it acts as a collaborative partner, guiding ideas through a structured workflow:

**Brainstorm → Prototype → Critique → Reiterate → Vault**

This system favors **concise, actionable outputs** and prioritizes **evidence-based iteration**, helping you rapidly generate, test, and refine your concepts within a single, unified interface.

## Core Concepts

The system operates using distinct **Modes**. You can select a mode for a specific task or chain them together for a complete workflow.

* **`idea_jam 💡`**: Divergent ideation and brainstorming.
* **`prototype 🛠`**: Rapid mock-ups, UI sketches, or code scaffolds.
* **`critic 🔍`**: Honest, structured feedback and regression checks.
* **`reiterate 🔄`**: Apply critique to generate an improved version.
* **`vault 🏛`**: Archive, search, tag, and remix past ideas.
* **`assist 🤝`**: General Q&A and helper functions outside the main workflow.
* **`consult 🌐`**: Quick external inspiration scans (trends, analogs, quotes).

The goal is to provide a focused, efficient partner that helps you overcome creative blocks and iterate quickly towards viable solutions.

## Technology Stack

* **Python:** 3.10+
* **Framework:** [CrewAI](https://crewai.com/)
* **LLM:** Configurable - Requires an API key for an LLM provider (e.g., OpenAI GPT-4/GPT-4o, Anthropic Claude 3, Groq Llama3, Google Gemini). Configure in your `.env` file.
* **(Optional) Tools:** May integrate specific CrewAI tools (e.g., SerperDevTool for web search).

## Sequential Workflow & Mode Chaining

SOLO-IDEAFLOW-OS supports chaining multiple workflow modes for streamlined, multi-step creative sessions. You can specify a sequence of modes to be executed in order, such as:

```
modes=[idea_jam → prototype → critic]
```

This will:
1. Generate creative ideas from your prompt (idea_jam)
2. Prototype the selected idea (prototype)
3. Critique the resulting prototype (critic)

**Example Usage:**

- To generate and evaluate concepts for a collapsible windsurf sail:
  ```
  modes=[idea_jam → prototype → critic] | Generate and evaluate concepts for a collapsible windsurf sail.
  ```
  The system will walk you through idea generation, prototyping, and critique in sequence, minimizing manual input.

You can also specify a single mode (e.g., `mode=prototype`) for focused tasks, or use the interactive menu to pick your next step at each stage.

## Getting Started

### Prerequisites

* Python (>=3.10, <3.13 recommended for CrewAI compatibility)
* Git
* Access to an LLM provider API and an API Key.
* (Optional but recommended) API Key for search tools like SerperDev if using relevant agents.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/ryan258/SOLO-IDEAFLOW-OS.git](https://github.com/ryan258/SOLO-IDEAFLOW-OS.git)
    cd SOLO-IDEAFLOW-OS
    ```

2.  **Set up a virtual environment:**
    * *Using Python's built-in `venv`*:
        ```bash
        python -m venv venv
        # On macOS/Linux:
        source venv/bin/activate
        # On Windows:
        .\venv\Scripts\activate
        ```
    * *Using `uv` (recommended by CrewAI)*:
        ```bash
        # Install uv if you haven't already (see CrewAI docs)
        uv venv
        source .venv/bin/activate # Adjust activation command based on your OS/shell
        ```

3.  **Install dependencies:**
    * *If using the `crewai create crew` structure:*
        ```bash
        crewai install
        # Or using uv:
        uv pip install -r requirements.txt
        ```
    * *If setting up manually, ensure CrewAI is included in your `requirements.txt` and install:*
        ```bash
        uv pip install -r requirements.txt
        ```

4.  **Configure environment variables:**
    * Create a `.env` file in the project root directory.
    * Copy the contents of `.env.example` (if provided) into `.env`.
    * Add your API keys:
        ```dotenv
        # Example for OpenAI
        OPENAI_API_KEY="sk-..."
        # OPENAI_MODEL_NAME="gpt-4o-mini" # Optional: Specify model

        # Example for Serper (if using search tools)
        # SERPER_API_KEY="..."

        # Add other keys as needed (e.g., GROQ_API_KEY, ANTHROPIC_API_KEY)
        ```
    * **Important:** Add `.env` to your `.gitignore` file to avoid committing secrets.

## Usage

Run the main application script. Depending on how the project is structured (using `crewai create crew` or manually):

```bash
# If using the standard CrewAI project structure:
crewai run

# Or if you have a custom main script:
python main.py
Interact by providing prompts, specifying the mode(s) if needed. The system will confirm the active mode and proceed with the task.

Example Prompts:

Default Mode (idea_jam):

Generate ideas for sustainable windsurf board materials.
(AI should respond starting with ▶ mode: idea_jam 💡)

Specifying a Single Mode:

mode=prototype | Create a basic UI layout sketch for a windsurf tide prediction app.
(AI should respond starting with ▶ mode: prototype 🛠)

Chaining Modes:

modes=[idea_jam → prototype → critic] | Generate and evaluate concepts for a collapsible windsurf sail.
(AI should respond starting with ▶ modes: [idea_jam → prototype → critic] and execute sequentially)

Using Vault:

mode=vault | command=search | tags=windsurf,app
(AI should respond starting with ▶ mode: vault 🏛)

Project Structure (Example)
.
├── .env               # Local environment variables (GITIGNORED!)
├── .env.example       # Example environment variables template
├── agents.yaml        # CrewAI agent definitions (if using YAML config)
├── tasks.yaml         # CrewAI task definitions (if using YAML config)
├── crew.py            # Defines the Crew, Agents, Tasks (if using Python config)
├── main.py            # Main application entry point (or use `crewai run`)
├── tools/             # Directory for custom CrewAI tools (optional)
├── requirements.txt   # Python dependencies managed by uv/pip
├── README.md          # This file
└── .gitignore         # Specifies intentionally untracked files
(Note: The exact structure might differ based on your setup or if generated by crewai create crew)

Contributing
Contributions are welcome! If you have suggestions, bug reports, or want to add features:

Fork the repository.
Create a new branch (git checkout -b feature/YourFeature).
Make your changes.
Commit your changes (git commit -m 'Add some feature').
Push to the branch (git push origin feature/YourFeature).
Open a Pull Request.
Please ensure your code adheres to basic Python best practices and includes comments where necessary.   

License
This project is licensed under the MIT License - see the LICENSE file for details.   

Acknowledgements
Built with the amazing CrewAI framework.
Leverages the power of Large Language Models from providers like OpenAI, Anthropic, Google, Groq, etc.

**Next Steps for You:**

1.  Create a new repository on GitHub.
2.  Save this text as `README.md` in the root of your project locally.
3.  Replace `ryan258` in the clone URL example.
4.  Add a `LICENSE` file (e.g., copy the MIT license text into a file named `LICENSE`).
5.  Create a `.gitignore` file (add `.env`, `venv/`, `.venv/`, `__pycache__/`, `*.pyc` etc.).
6.  Customize the "Technology Stack" and `.env.example` based on the specific LLM and tools you plan to use initially.
7.  As you build, update the "Project Structure" and "Usage" sections to accurately reflect your implementation.
8.  Start coding your first agents and tasks using CrewAI! Good luck with the windsurf id