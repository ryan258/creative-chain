# SOLO-IDEAFLOW-OS Happy Path Test Prompts

This document contains a set of copy-paste prompts and example responses to quickly test the full happy path of the SOLO-IDEAFLOW-OS application. Use these to ensure the workflow, chaining, and menu options work as expected every time.

---

## 1. Start the App

```bash
python main.py
```

---

## 2. Idea Generation (Default or Explicit)

**Prompt:**
```
Generate ideas for a new eco-friendly windsurf board.
```
_or_
```
mode=idea_jam | Generate ideas for a new eco-friendly windsurf board.
```

---

## 3. Pick an Idea to Prototype

**Prompt:**
```
1
```
_or select another idea number as shown.

---

## 4. Prototype Step

**Prompt:**
```
y
```
(Sends prototype to critic for feedback)

---

## 5. Critique Step

**Prompt:**
```
reiterate
```
_or_
```
critic
```
_or provide your own feedback to generate a new iteration.

---

## 6. Save as Project Brief

**Prompt:**
```
save
```
(Creates a markdown project brief in `/ideas`)

---

## 7. Restart or Exit

**Prompt:**
```
restart
```
_or_
```
exit
```

---

## 8. Chained Workflow Example

**Prompt:**
```
modes=[idea_jam → prototype → critic] | Generate and evaluate concepts for a collapsible windsurf sail.
```

---

## 9. Vault Search Example

**Prompt:**
```
mode=vault | command=search | tags=windsurf,app
```

---

## Tips
- Use these prompts in order for a full happy path test, or jump to any section to test specific features.
- You can copy/paste directly into the terminal or app prompt.
- Update this file with new features or menu options as the app evolves.
