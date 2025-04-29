# tasks.py - CrewAI task stubs

def get_tasks_for_mode(mode):
    """Return a list of tasks based on the selected mode for CrewAI agents."""
    if mode == "idea_jam":
        return ["Generate creative ideas"]
    elif mode == "prototype":
        return ["Create a prototype from idea"]
    elif mode == "critic":
        return ["Critique the prototype"]
    elif mode == "reiterate":
        return ["Reiterate based on critique"]
    elif mode == "vault":
        return ["Archive idea/prototype/critique as project brief"]
    else:
        return [f"Stub task for mode: {mode}"]
