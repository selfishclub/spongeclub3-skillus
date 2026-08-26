# Best Practices, Anti-Patterns, Troubleshooting & Success Criteria

Read this before authoring or shipping a cross-platform skill, and when a tool
produces unexpected output.

---

## Best Practices

### Skill Authoring

1. **Keep descriptions discovery-friendly** - Use third-person, keyword-rich descriptions that start with "This skill should be used when..."
2. **One skill, one concern** - Each skill should cover a coherent domain, not an entire discipline
3. **Scripts use standard library only** - No pip install requirements for core functionality
4. **Include both SKILL.md and agents/openai.yaml** - Makes the skill usable on any platform immediately
5. **Test scripts independently** - Every Python tool should work standalone via `python script.py --help`

### Codex CLI Usage

1. **Start with suggest mode** - Use `--approval-mode suggest` until you trust the skill
2. **Scope skill contexts narrowly** - Pass specific files with `--file` instead of entire directories
3. **Use project-local skills** - Avoid global installation for project-specific skills
4. **Pin versions in teams** - Use skills-index.json for version consistency across team members
5. **Review generated configs** - Always review auto-generated `agents/openai.yaml` before deploying

### Cross-Platform Compatibility

1. **Relative paths everywhere** - Scripts reference `scripts/`, `references/`, `assets/` with relative paths
2. **No shell-specific syntax** - Avoid bash-isms in scripts; stick to Python for portability
3. **Standard YAML only** - No YAML extensions or anchors that might confuse parsers
4. **UTF-8 encoding** - All files should be UTF-8 encoded
5. **Unix line endings** - Use LF, not CRLF (configure `.gitattributes`)

### Performance

1. **Keep skills small** - Under 1MB total for fast loading and distribution
2. **Minimize reference files** - Include only essential knowledge, not entire docs
3. **Lazy-load expensive tools** - Split heavy scripts into separate files
4. **Cache tool outputs** - Use `--json` output for piping into other tools

---

## Anti-Patterns

- **Converting without reviewing** -- auto-generated `agents/openai.yaml` needs human review for instruction accuracy and tool command paths
- **Global skill installation** -- project-specific skills should stay in `.codex/skills/`, not `~/.codex/skills/`, to avoid version conflicts across projects
- **Duplicating logic in SKILL.md and openai.yaml** -- keep `SKILL.md` as source of truth; `openai.yaml` should reference shared scripts, not rewrite instructions
- **Shell-specific syntax in scripts** -- bash-isms break on Windows; stick to Python for all automation logic
- **Ignoring strict validation warnings** -- optional directories (`references/`, `assets/`) that are missing degrade skill quality even if not required
- **Skipping version pinning** -- teams without `skills-index.json` version pinning get inconsistent behavior across members

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Converter produces empty `instructions` field | SKILL.md has no `## Best Practices` or `### Workflow` headings for the parser to extract | Add clearly labeled `### Workflow N:` and `## Best Practices` sections with bulleted items in the source SKILL.md |
| Validator fails with "No valid YAML frontmatter" | SKILL.md does not start with `---` on the very first line, or the closing `---` delimiter is missing | Ensure the file begins with `---` on line 1, followed by frontmatter fields, followed by a closing `---` line with no leading whitespace |
| `agents/openai.yaml` tool references show "missing script" error | The `command` field path in openai.yaml does not match the actual filename in `scripts/` | Verify that each tool's `command` value uses the exact filename (case-sensitive) under `scripts/` and uses the prefix `python scripts/` |
| Index builder returns 0 skills | Subdirectories scanned do not contain a `SKILL.md` file, or the target path points to a single skill instead of a parent directory | Pass the parent directory that contains skill subdirectories, not a single skill folder. Hidden directories (dot-prefixed) are also skipped |
| Validator warns "Description should use third-person, discovery-friendly format" | The `description` frontmatter field does not contain recognized discovery patterns like "This skill should be used when" | Rewrite the description to begin with "This skill should be used when the user asks to..." or include verbs like "analyzes", "generates", "provides" |
| Converter overwrites existing `agents/openai.yaml` without backup | Running the converter with output-dir set to the same directory as the source skill | Use `--output-dir` to write to a separate directory, or manually back up the existing `agents/openai.yaml` before converting |
| Strict validation fails on optional missing directories | Running `--strict` treats warnings (missing `references/`, `assets/`, license field) as errors | Either create the missing optional directories and fields, or run without `--strict` to allow warnings |

---

## Success Criteria

- Converted skills pass `cross_platform_validator.py --strict` with zero errors and zero warnings
- Generated `agents/openai.yaml` contains a valid `name`, `description`, `instructions`, and `tools` section that matches the source SKILL.md
- Skills index built from 50+ skill directories completes in under 10 seconds with accurate metadata extraction
- All three Python tools exit with code 0 on valid input and exit with code 1 on invalid input, enabling reliable CI/CD integration
- Batch conversion of an entire skill domain (e.g., all `engineering/` skills) produces Codex-compatible output with no manual edits required for structure
- Cross-platform skills load and function correctly in both Claude Code (via SKILL.md) and Codex CLI (via `agents/openai.yaml`) without platform-specific workarounds
- Generated `skills-index.json` is valid JSON parseable by any standard JSON parser and includes complete metadata for every scanned skill
