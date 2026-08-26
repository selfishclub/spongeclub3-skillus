# Staleness Detection & Quarterly Review

Read this when automating staleness detection in CI or running the quarterly runbook review process.

## Staleness Detection Automation

```bash
#!/bin/bash
# check-runbook-staleness.sh
# Run weekly in CI to detect stale runbooks

RUNBOOK_DIR="docs/runbooks"
EXIT_CODE=0

for runbook in "$RUNBOOK_DIR"/*.md; do
  LAST_VERIFIED=$(grep -oP 'Last verified:\s*\K\d{4}-\d{2}-\d{2}' "$runbook" 2>/dev/null)
  if [ -z "$LAST_VERIFIED" ]; then
    echo "WARNING: $runbook has no 'Last verified' date"
    continue
  fi

  # Extract referenced config files
  CONFIG_FILES=$(grep -oP 'git log.*-- \K[^\x60]+' "$runbook" 2>/dev/null)
  for config in $CONFIG_FILES; do
    if [ -f "$config" ]; then
      LAST_MODIFIED=$(git log -1 --format=%ci -- "$config" | cut -d' ' -f1)
      if [[ "$LAST_MODIFIED" > "$LAST_VERIFIED" ]]; then
        echo "STALE: $runbook references $config (modified $LAST_MODIFIED, verified $LAST_VERIFIED)"
        EXIT_CODE=1
      fi
    fi
  done
done

exit $EXIT_CODE
```

## Quarterly Review Process

Every quarter (add to team calendar):

1. **Run each command in staging** — does it still work?
2. **Check config drift** — compare config modification dates vs runbook verification date
3. **Test rollback procedures** — actually roll back in staging
4. **Update contact info** — L1/L2/L3 assignments may have changed
5. **Add new failure modes** discovered in the past quarter
6. **Update "Last verified" date** at the top of each reviewed runbook
7. **Archive obsolete runbooks** — services get decommissioned
