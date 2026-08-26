---
name: your-skill-name
description: A one-sentence description of what this skill does. Be specific about the workflow and when to use it.
---

# Skill Name — Workflow Title

One-paragraph summary of what this skill does and why.

## Prerequisites

List any tools, CLIs, or dependencies the user needs installed.

```bash
# Example: check for and install a dependency
command --version 2>/dev/null || npm install -g command
```

## Core Workflow

### 0. Gather requirements

Ask the user what they need before starting work.

### 1. Generate the artifact

Create the initial output (presentation, document, etc.).

### 2. Export for visual inspection

Export to an image format so Claude can visually inspect the result.

```bash
# Export command here
```

### 3. Visual QA

Read each exported image using the Read tool. Check for common issues:

- [ ] **Issue category 1**: What to look for
- [ ] **Issue category 2**: What to look for

### 4. Fix issues

Edit the source to address problems found in QA.

### 5. Iterate

Repeat steps 2-4. Do **up to 3 iterations** total. Stop early if QA passes.

If issues remain after 3 iterations, report them to the user with specifics.

### 6. Final export

Ask the user which output format they want, then export.

## Tips

- Tip 1
- Tip 2
