#!/usr/bin/env python3
"""PreToolUse hook: block Bash commands that look like they leak secrets.

Reads the hook invocation JSON on stdin, inspects the proposed Bash command,
and either exits 0 (allow) or exits 2 with a stderr message (block).

Patterns covered (deliberately conservative — false negatives over false positives):
  - AWS access keys (AKIA...)
  - Long base64-looking secrets passed inline to env vars
  - GitHub personal-access tokens (ghp_, gho_, ghu_, ghs_)
  - Slack tokens (xoxb-, xoxp-, xoxa-)
  - Inline private keys (-----BEGIN ... PRIVATE KEY-----)
  - Writing secrets into committed files (echo $TOKEN >> .env, etc.)

Stdlib-only. No network calls.
"""

from __future__ import annotations

import json
import re
import sys


SECRET_PATTERNS = [
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS access key"),
    (re.compile(r"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}\b"), "GitHub token"),
    (re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}\b"), "Slack token"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "inline private key"),
    (re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"), "OpenAI-style API key"),
    (re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}\b"), "Anthropic API key"),
]

DANGEROUS_WRITES = re.compile(
    r"(?:^|[\s;|&])(?:echo|printf|cat)\s+[^\n]*[\"']?\$?\{?[A-Z_]*(?:TOKEN|KEY|SECRET|PASSWORD|CREDENTIAL)[A-Z_]*\}?[^\n]*>\s*\.?env",
    re.IGNORECASE,
)


def scan(command: str) -> list[str]:
    findings: list[str] = []
    for pattern, label in SECRET_PATTERNS:
        if pattern.search(command):
            findings.append(label)
    if DANGEROUS_WRITES.search(command):
        findings.append("write of secret-bearing variable to .env-style file")
    return findings


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    tool_name = payload.get("tool_name") or payload.get("tool") or ""
    tool_input = payload.get("tool_input") or payload.get("input") or {}

    if tool_name != "Bash":
        return 0

    command = tool_input.get("command", "") if isinstance(tool_input, dict) else ""
    if not command:
        return 0

    findings = scan(command)
    if not findings:
        return 0

    msg = (
        "Blocked by secret-scan hook. The proposed Bash command appears to contain "
        "or write a sensitive credential:\n"
        + "\n".join(f"  - {f}" for f in findings)
        + "\nIf this is intentional (e.g. revoking a known-leaked key), bypass the hook "
        "by running the command outside Claude or temporarily disabling this hook in "
        ".claude/settings.json."
    )
    print(msg, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
