---
marp: true
theme: default
paginate: true
style: |
  /* ── Typography ─────────────────────────────── */
  section {
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    font-size: 26px;
    padding: 50px 60px;
  }
  h1 { font-size: 42px; letter-spacing: -0.5px; }
  h2 { font-size: 36px; letter-spacing: -0.3px; }
  h3 { font-size: 28px; }
  table { font-size: 22px; }
  code { font-size: 20px; }
  pre { font-size: 18px; }
  blockquote { border-left: 4px solid #00c9a7; }
  strong { color: #1a1f36; }

  /* ── Dark slides ────────────────────────────── */
  section.dark {
    background: #1a1f36;
    color: #cdd6e4;
  }
  section.dark h1,
  section.dark h2,
  section.dark h3 {
    color: #ffffff;
  }
  section.dark strong {
    color: #00c9a7;
  }
  section.dark a {
    color: #00c9a7;
  }
  section.dark::after {
    color: #4a5270;
  }

  /* ── Accent slides (centered, dramatic) ───── */
  section.accent {
    background: #1a1f36;
    color: #cdd6e4;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  section.accent h2 {
    color: #ffffff;
    font-size: 40px;
  }
  section.accent h3 {
    color: #00c9a7;
    font-size: 32px;
  }
  section.accent strong {
    color: #00c9a7;
  }
  section.accent::after {
    color: #4a5270;
  }
---

<!-- _class: dark -->
<!-- _paginate: false -->

# Presentation Title
# Subtitle or Tagline

<br>

**Your Name** | Team or Date

<!--
SPEAKER NOTES:
"Opening line that hooks the audience."
-->

---

## The Problem

A clear statement of the problem you're solving.

- Point one
- Point two
- Point three

**Why does this matter?**

---

![bg right:45% contain](screenshot.png)

## Evidence

> "A quote or data point that supports your case."

Explain what the audience is looking at.

**Key insight** that connects evidence to your argument.

---

## Solution Overview

<style scoped>table { font-size: 21px; }</style>

| Feature | Benefit |
|---------|---------|
| **Feature 1** | What it enables |
| **Feature 2** | What it enables |
| **Feature 3** | What it enables |
| **Feature 4** | What it enables |

---

<!-- _class: accent -->

## The Pivot Point

<br>

A dramatic statement that transitions
from problem to solution.

<br>

### What if there was a better way?

---

## Demo or Details

Content that shows your solution in action.

```bash
# Installation or usage example
npm install my-tool
my-tool start
```

---

## Who Benefits

| Role | Use Case |
|------|----------|
| **Role 1** | How they use it |
| **Role 2** | How they use it |
| **Role 3** | How they use it |

---

<!-- _class: dark -->

## What's Next

**Now:** Current state

**Next:** Near-term plans

**Vision:** Long-term aspiration

[https://your-link-here](https://your-link-here)

<!--
SPEAKER NOTES:
"Closing line — a clear call to action."
-->
