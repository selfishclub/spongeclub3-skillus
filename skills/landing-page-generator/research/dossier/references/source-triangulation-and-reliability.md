# Source Triangulation & Reliability Reference

Reference for assessing and triangulating sources in dossier research.

## 1. Source reliability — the Admiralty Code

A military-intelligence framework still useful for any intelligence research:

### Reliability of source
| Code | Label | Description |
|------|-------|-------------|
| A | Completely reliable | History of completely reliable info |
| B | Usually reliable | Mostly reliable; small history of errors |
| C | Fairly reliable | Mixed; some history of errors |
| D | Not usually reliable | Limited history; mixed |
| E | Unreliable | Known inaccuracies |
| F | Cannot be judged | New source; no track record |

### Credibility of information
| Code | Label | Description |
|------|-------|-------------|
| 1 | Confirmed | Confirmed by other independent sources |
| 2 | Probably true | Not confirmed; consistent with other info |
| 3 | Possibly true | Not confirmed; reasonable |
| 4 | Doubtful | Inconsistent with other info |
| 5 | Improbable | Contradicted by other info |
| 6 | Cannot be judged | New info; no validation |

A B-2 source is workable. An F-6 source is barely usable.

## 2. Common source types by reliability

### A-tier (use as primary)
- Audited financial statements
- Regulatory filings (10-K, S-1, EDGAR)
- Court records (verified judgments)
- Peer-reviewed scientific papers (in field)
- Government statistics (with caveats)

### B-tier (workable; cite primary when possible)
- Major news outlets with editorial standards (NYT, WSJ, FT, Bloomberg, Reuters)
- Trade press (specialized industry publications)
- Industry reports (Gartner, IDC, Forrester — note bias)
- LinkedIn (people facts)
- Conference proceedings

### C-tier (use with caution; triangulate)
- Mid-tier news outlets
- Crunchbase, PitchBook (private company data; sometimes outdated)
- TechCrunch, Forbes (mix of journalism + PR)
- Industry blogs (variable quality)

### D-tier (use sparingly; flag)
- Social media (X, LinkedIn posts, Reddit)
- Niche blogs without track record
- Company press releases (PR voice)
- Marketing materials

### E-tier (avoid)
- Tabloids
- Aggregator sites with no editorial
- AI-generated content (often inaccurate)
- Pseudo-news / content farms

## 3. Independence of sources

Two sources are **independent** when they didn't both derive from the
same underlying source.

### Examples of NOT independent
- Two news articles both citing the same press release
- Two reviews on the same review aggregator
- An analyst report citing another analyst report
- LinkedIn posts that repost the same content

### Examples of independent
- Press release + independently-reported news article
- Court filing + independent expert interview
- Trade publication report + earnings call disclosure
- Crunchbase data + LinkedIn data (different schemas)

For triangulation, you need genuinely independent sources.

## 4. Triangulation rules

For each significant claim:

- **N=1 source:** flag as anecdotal; note uncertainty
- **N=2 independent sources:** workable; standard for most claims
- **N=3+ independent sources:** confirmed; safe to assert

### "Significant claim"
- Anything that drives a recommendation
- Anything load-bearing for an argument
- Anything about numbers, dates, ownership, relationships

### "Not significant"
- Atmospheric / scene-setting facts
- Well-established background

## 5. Hidden bias in common sources

### Industry reports (Gartner, IDC, Forrester)
- Pay-to-play (some vendors pay for coverage)
- Survey methodology may have selection bias
- Forecasts often anchored on prior reports
- Use as one input, not definitive

### Crunchbase / PitchBook
- Private companies self-report (or don't)
- Funding amounts sometimes round-up
- Headcount lags reality
- Acquisition rumors mixed with confirmed deals

### LinkedIn
- Self-reported (people inflate titles)
- Lagging (departures often delayed in updating)
- Self-selection on company size, geography

### News articles
- Source attribution matters (anonymous source ≠ named)
- Reporter expertise in subject (general vs specialized)
- Editorial slant (publication tone)

### Company press releases
- Always positive
- May omit context
- Use for confirmation of facts (dates, partnerships); not for interpretation

## 6. Documenting sources

Per source used:

```
[Source title / URL]
- Source type: [type]
- Reliability: [A/B/C/D/E/F]
- Accessed: [date]
- Notes: [context for any caveats]
```

Per claim:

```
[Claim]
- Confirmed by: [source 1] (B-2), [source 2] (B-1)
- Credibility: 1 (confirmed)
- Notes: [any caveats]
```

## 7. Web sources — special discipline

Web sources can change or disappear. Practices:

- Always capture access date
- Use Wayback Machine to archive (web.archive.org/save/)
- Save PDF copies of critical web sources
- Note original URL + archive URL
- Flag any source that may move (blogs, social posts)

## 8. Verification techniques

### For people facts
- Cross-check LinkedIn + personal site + published bio
- Look at conference bios over time
- Check court records for legal name verification

### For company facts
- Cross-check Crunchbase + LinkedIn + their own site
- Look at job postings (hiring patterns reveal direction)
- Check SEC filings for public companies
- Check Companies House (UK) or equivalent for private

### For financial claims
- Look for audited statements vs management estimates
- Compare to peer companies (sanity check)
- Look at footnotes (often where the real story lives)

### For relationship / partnership claims
- Both parties should disclose
- Look for the announcement on BOTH sides
- Verify on official channels

## 9. Red flags in sources

- Anonymous sources for specific factual claims (vs anonymous for sensitive opinions)
- Single-source major claims
- Sources that contradict known public record
- Sources with conflicts of interest unstated
- Sources that benefit financially from the conclusion
- Sources you can't verify exist

## 10. Reporting source quality

The dossier should include a brief methodology section:

```
METHODOLOGY
- Subject: [name]
- Research period: [start - end]
- Sources used: [count] across [tier ranges]
- Key limitations: [what we couldn't access]
- Confidence level: [overall]
- Update needed by: [date]
```

This calibrates the reader.

## 11. Common pitfalls

- **Citation chain treated as triangulation.** Multiple cites of one source = one source.
- **Press release treated as fact.** PR voice; verify with independent reporting.
- **AI-generated summary treated as source.** Verify against primary.
- **Forgetting access date.** Web sources change.
- **No source documentation.** Future-you can't refresh.
- **Source reliability assumed by venue alone.** Bad articles appear in good publications.
- **No flag on uncertain claims.** Reader treats everything as confirmed.
