# qwen3.5-plus Response

This is a sophisticated design for a solo-dev tool. It leverages Claude Code's capabilities (script execution, file I/O, web fetch) effectively without over-dependencing on external infrastructure. The "AI-to-AI" framing is particularly strong—it reduces the "please the user" bias in consulted models.

Here is a review based on your five questions, focusing on practical risks and high-value tweaks.

### 1. Missing Features & Patterns (High Value, Low Complexity)

*   **Cost Estimation / Warning:**
    *   **Blind Spot:** "No output token caps" + "Consensus Mode" = Potential bill shock. If a model goes on a reasoning spiral, OpenRouter charges per token.
    *   **Suggestion:** Add a pre-flight check. The Python script should estimate input tokens (prompt size) and warn if the potential cost exceeds a threshold (e.g., "Warning: This consensus run may cost ~$0.50. Proceed?"). Or, set a *reasonable* hard cap (e.g., 8,192 tokens) instead of *no* cap, unless explicitly overridden.
*   **Local Model List Caching:**
    *   **Blind Spot:** Fetching `models.flared.au` on *every* invocation adds latency and creates a single point of failure. If that service is down, your skill dies.
    *   **Suggestion:** Cache the JSON locally (e.g., `.claude/cache/models.json`) with a TTL (e.g., 24 hours). Only fetch if missing or expired. This makes the tool feel instant and resilient.
*   **Progress Indicators for Consensus:**
    *   **Blind Spot:** In consensus mode, the terminal will hang silently while Python waits for 3 APIs. Users might think it crashed.
    *   **Suggestion:** Have the Python script print `Waiting for [model_name]...` as it fires requests, and `[✓] [model_name]` as they return. Simple stdout feedback reduces anxiety.
*   **"Sensitive Mode" Toggle:**
    *   **Blind Spot:** Sending proprietary client code to 3rd party APIs (even via OpenRouter) might violate NDAs or security policies.
    *   **Suggestion:** Add a trigger like `brains trust private` that restricts consultation to local models (if you add Ollama support later) or skips file attachment, sending only abstracted descriptions. For now, just add a confirmation step: "You are about to send 5 files to external APIs. Confirm?"

### 2. Shifts in Thinking

*   **From "No Token Caps" to "Reasonable Limits":**
    *   **Current:** `# No max_tokens — let the model reason fully`
    *   **Shift:** Unlimited output is a financial risk. LLMs sometimes loop or over-explain.
    *   **Recommendation:** Set a high default (e.g., 4096 or 8192). It's enough for deep reasoning but prevents runaway costs. You can add a `--verbose` flag to remove the cap if truly needed.
*   **From "Fetch Every Time" to "Trust but Verify":**
    *   **Current:** Fetch model list before every consultation.
    *   **Shift:** Model IDs don't change *that* frequently.
    *   **Recommendation:** Cache the list (see above). If the cache is missing, *then* fetch. This reduces friction significantly.
*   **From "Script Generation" to "Script Reuse":**
    *   **Current:** Generate `brains-trust.py` every time.
    *   **Shift:** The logic in `provider-api-patterns.md` is static. Regenerating it every time is I/O overhead.
    *   **Recommendation:** Check if `.claude/scripts/brains-trust.py` exists. If yes, reuse it. Only regenerate if the skill definition changes or the file is missing. This speeds up repeated use.

### 3. Default Choices

*   **Consensus vs. Single:**
    *   **Verdict:** **Single should be the default.** Consensus is 3x the cost and 3x the latency. It should be an explicit opt-in (`brains trust consensus`).
*   **Model Selection Logic:**
    *   **Verdict:** **Risk Identified.** Your skill says: *"pick appropriate models based on mode (pro vs flash)"*.
    *   **Problem:** How does the Python script know which ID is "Flash" vs "Pro"? The `models.flared.au` JSON *must* include metadata tags (e.g., `"tier": "flash"`). If it only lists IDs, your script cannot programmatically distinguish them without hardcoded mappings (which you wanted to avoid).
    *   **Fix:** Ensure the JSON source provides tier metadata. If it doesn't, you need a small local mapping file or a heuristic (e.g., if ID contains "flash" or "nano").
*   **Timeout:**
    *   **Verdict:** **120s is good.** Keep it. Some reasoning models (o1, R1) take time.

### 4. UX Friction Points

*   **Artifact Clutter:**
    *   **Issue:** `.claude/artifacts/brains-trust-prompt.txt` and `brains-trust-{model}.md` will accumulate quickly.
    *   **Fix:** Add a cleanup rule. "Keep only the last 5 runs" or add a `brains trust clean` command to wipe the artifacts folder.
*   **Synthesis Overload:**
    *   **Issue:** If consensus returns 3 x 3,000 token responses, Claude Code has to read 9,000 tokens + original code + prompt to synthesize. This might hit *Claude's* context limit or cause laziness.
    *   **Fix:** Instruct the Python script to save files, but instruct Claude to read them *selectively*. Or, ask the consulted models to provide a "Executive Summary" at the top of their response specifically for the synthesizer.
*   **Error Message Usability:**
    *   **Issue:** `HTTP 401` is clear, but `HTTP 400` (bad payload) can be cryptic.
    *   **Fix:** In the Python error handler, print the first 200 chars of the response body. Often the API returns `{"error": "context_window_exceeded"}` which is more helpful than just "400".

### 5. Over/Under-Engineered

*   **Over-Engineered: Generated Python Script for Simple Calls.**
    *   **Critique:** For *Single* mode, generating a script, writing it, executing it, and cleaning up is heavy. Claude Code often has native HTTP tools (`WebFetch` or similar).
    *   **Counter-argument:** You need custom headers (Auth) and parallelism for consensus. `WebFetch` might not support POST with custom auth headers easily depending on the Claude Code version.
    *   **Verdict:** **Keep the script.** It gives you full control over headers, timeouts, and parallelism which is hard to do via CLI tool injection. But **cache the script** (see point 2).
*   **Under-Engineered: Fallback Logic.**
    *   **Critique:** If `models.flared.au` is down, and you have no cached list, the skill fails.
    *   **Fix:** Hardcode a *tiny* fallback list of 3 known stable IDs (e.g., one Gemini, one GPT, one Llama) in the Python script itself. If the fetch fails, use the fallback with a warning: "Using fallback model list due to network error."
*   **Under-Engineered: Privacy Warning.**
    *   **Critique:** No explicit warning about sending code to external APIs.
    *   **Fix:** Add a one-time confirmation or a prominent note in the `When to Use` section about data privacy.

### Summary of Recommended Changes

1.  **Add Cost Guardrails:** Set a high default output token limit (e.g., 8k) rather than unlimited. Warn user in Consensus mode.
2.  **Cache Model List:** Don't fetch `models.flared.au` every time. Cache locally with 24h TTL.
3.  **Verify Model Metadata:** Ensure `models.flared.au` provides "tier" info so the script can distinguish Flash vs. Pro programmatically.
4.  **Reuse Script:** Check if `brains-trust.py` exists before regenerating it.
5.  **Progress Output:** Print "Waiting for..." messages during consensus to prevent user anxiety.
6.  **Fallback List:** Hardcode 3 safe model IDs in the script in case the model list fetch fails.

This design is 90% there. The remaining 10% is mostly about resilience (caching/fallbacks) and cost control. With those tweaks, it's a robust production tool for a solo dev.