# Pitfalls, Best Practices, Troubleshooting & Success Criteria

Read this when a monorepo task misbehaves, when reviewing for anti-patterns, or when validating a monorepo setup against the quality bar.

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Running `turbo run build` without `--filter` on every PR | Always use `--filter='...[origin/main]'` in CI |
| `workspace:*` breaks npm publish | Use `pnpm changeset publish` which replaces automatically |
| All packages rebuild when unrelated file changes | Tune `inputs` in turbo.json to exclude docs, config files |
| Shared tsconfig breaks type-checks across packages | Each package extends root but overrides `rootDir`/`outDir` |
| Git history lost during migration | Use `git filter-repo --to-subdirectory-filter` before merging |
| Remote cache misses in CI | Verify TURBO_TOKEN and TURBO_TEAM; check with `--summarize` |
| Import cycles between packages | Use `madge --circular` to detect; refactor shared code to a new package |

## Best Practices

1. **Root package.json has no runtime dependencies** — only devDependencies and scripts
2. **Always scope commands with --filter in CI** — running everything defeats the monorepo purpose
3. **Remote cache is not optional** — without it, monorepo CI is slower than multi-repo
4. **Shared configs extend from root** — tsconfig.base.json, eslint.base.js, vitest shared config
5. **`packages/types` is pure TypeScript** — no runtime code, no dependencies, fastest to build
6. **Changesets over manual versioning** — never hand-edit package.json versions in a monorepo
7. **Impact analysis before merging shared package changes** — check affected packages, communicate blast radius
8. **Keep workspace:* for internal deps** — real version ranges are for external npm packages only

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `turbo run build` rebuilds everything despite no changes | Inputs glob is too broad or `globalDependencies` includes volatile files | Narrow `inputs` in turbo.json; exclude `.env`, docs, and test fixtures from build inputs |
| `ERR_PNPM_PEER_DEP_ISSUES` on install | Peer dependency mismatches across workspace packages | Add `peerDependencyRules.ignoreMissing` or `peerDependencyRules.allowAny` in root `.npmrc` or `package.json` |
| Remote cache reports 0% hit rate in CI | TURBO_TOKEN or TURBO_TEAM not set, or `inputs`/`outputs` changed between runs | Verify env vars with `turbo run build --summarize`; ensure inputs/outputs are stable across branches |
| `workspace:*` version appears in published package | Published with `npm publish` or `pnpm publish` instead of Changesets | Always use `pnpm changeset publish` which replaces `workspace:*` with resolved versions automatically |
| Circular dependency detected between packages | Two packages import from each other directly | Run `madge --circular` to identify the cycle; extract shared code into a new leaf package with no internal deps |
| TypeScript `Cannot find module '@repo/ui'` in IDE | IDE TypeScript server not resolving workspace paths | Add `paths` mapping in root `tsconfig.json` or use TypeScript project references; restart TS server after changes |
| CI takes longer after monorepo migration than multi-repo | Missing remote cache, no `--filter`, or `fetch-depth: 1` preventing git comparisons | Enable remote caching, use `--filter='...[origin/main]'`, and set `fetch-depth: 0` in checkout action |

## Success Criteria

- **Build time reduction**: CI pipeline completes affected-only builds in under 50% of full-build time within 2 weeks of adoption
- **Cache hit rate**: Remote cache achieves 70%+ hit rate on PR builds after initial warm-up period
- **Impact visibility**: Every PR includes an affected-packages summary showing blast radius of changes
- **Zero full rebuilds in CI**: No CI workflow runs all packages unconditionally; every pipeline uses `--filter` or equivalent
- **Publishing reliability**: Changesets workflow produces correct versions and changelogs with zero manual `package.json` edits per release cycle
- **Migration completeness**: Multi-repo to monorepo migration preserves 100% of git history for all migrated packages
- **Developer onboarding**: New team members can run, build, and test any package locally within 15 minutes using documented workspace commands
