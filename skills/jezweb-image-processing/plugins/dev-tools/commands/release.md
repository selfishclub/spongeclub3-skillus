---
description: Prepare and publish a GitHub release
argument-hint: "[version]"
allowed-tools: "*"
---

Load the `github-release` skill and prepare a release.

If $ARGUMENTS contains a version (e.g. `v1.2.0`), use it. Otherwise, determine the next version from git tags.

Workflow: secrets scan → personal artifact check → LICENSE/README validation → create tag → publish via gh CLI.
