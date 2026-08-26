#!/usr/bin/env python3
"""Brains Trust — multi-model consultation on the brains-trust skill itself"""
import os, sys, json, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

GEMINI_KEY = os.environ.get('GEMINI_API_KEY', '')
OPENROUTER_KEY = os.environ.get('OPENROUTER_API_KEY', '')

# Read the full files to include in prompt
skill_dir = '/Users/jez/Documents/claude-skills/plugins/dev-tools/skills/brains-trust'
files = {}
for f in ['SKILL.md', 'references/prompt-templates.md', 'references/provider-api-patterns.md']:
    with open(os.path.join(skill_dir, f)) as fh:
        files[f] = fh.read()

# Build prompt with full file contents
prompt = open('/Users/jez/Documents/claude-skills/.claude/artifacts/brains-trust-prompt.txt').read()
# Replace the placeholders with actual content
prompt = prompt.replace('[See full SKILL.md content above — 130 lines covering setup, patterns, modes, workflow, rules]', files['SKILL.md'])
prompt = prompt.replace('[AI-to-AI templates for 7 modes plus devil\'s advocate framing — ~125 lines]', files['references/prompt-templates.md'])
prompt = prompt.replace('[Python patterns for OpenRouter, Gemini direct, OpenAI direct, parallel execution, error handling — ~204 lines]', files['references/provider-api-patterns.md'])

def call_gemini(prompt):
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={GEMINI_KEY}'
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.3}
    }).encode()
    req = urllib.request.Request(url, data=payload, headers={
        'Content-Type': 'application/json',
        'User-Agent': 'brains-trust/1.0'
    })
    resp = urllib.request.urlopen(req, timeout=120)
    result = json.loads(resp.read())
    return result['candidates'][0]['content']['parts'][0]['text']

def call_openrouter(model_id, prompt):
    payload = json.dumps({
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(
        'https://openrouter.ai/api/v1/chat/completions',
        data=payload,
        headers={
            'Authorization': f'Bearer {OPENROUTER_KEY}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://github.com/jezweb/claude-skills',
            'X-Title': 'Brains Trust',
        }
    )
    resp = urllib.request.urlopen(req, timeout=120)
    result = json.loads(resp.read())
    return result['choices'][0]['message']['content']

results = {}
with ThreadPoolExecutor(max_workers=2) as executor:
    futures = {}
    if GEMINI_KEY:
        futures[executor.submit(call_gemini, prompt)] = 'gemini-2.5-pro'
    if OPENROUTER_KEY:
        futures[executor.submit(call_openrouter, 'qwen/qwen3.5-plus-02-15', prompt)] = 'qwen3.5-plus'

    for future in as_completed(futures):
        model = futures[future]
        try:
            results[model] = future.result()
            print(f"\n{'='*60}")
            print(f"=== {model} ===")
            print(f"{'='*60}\n")
            print(results[model])
        except Exception as e:
            print(f"\n--- {model} ERROR: {e} ---")

# Save responses
for model, text in results.items():
    path = f'/Users/jez/Documents/claude-skills/.claude/artifacts/brains-trust-{model}.md'
    with open(path, 'w') as f:
        f.write(f"# {model} Response\n\n{text}")
    print(f"\nSaved to {path}")
