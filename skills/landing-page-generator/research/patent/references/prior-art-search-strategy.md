# Prior-Art Search Strategy

Reference for conducting comprehensive prior-art searches.

## 1. Search scope decisions

For each invention, decide search scope:

- **Patent vs non-patent vs both** (always do both for thorough searches)
- **Issued + published applications** (both are prior art)
- **Geographic scope** (US? EU? Global?)
- **Date range** (typically all prior to filing date; 20-year horizon)
- **Language** (translate as needed; non-English art is real)

## 2. Patent databases

### Free
- **USPTO** (patft.uspto.gov, appft.uspto.gov) — US issued + applications
- **EPO Espacenet** (worldwide.espacenet.com) — strongest for global; ~140M docs
- **Google Patents** (patents.google.com) — fast + decent UX; classification-aware
- **WIPO PatentScope** (patentscope.wipo.int) — PCT applications + many national
- **JPO** (jpo.go.jp) — Japan
- **CNIPA** (english.cnipa.gov.cn) — China
- **Lens.org** — academic + patent integration; free

### Paid (specialized)
- **PatBase** — comprehensive global
- **STN / Derwent** — premium chemistry / pharma
- **PatSnap** — landscape analytics
- **Innography** / **Questel Orbit** — analytics + visualization

Most prior-art searches use **Espacenet + Google Patents + USPTO** as the core, adding regional databases when needed.

## 3. Classification systems

### CPC (Cooperative Patent Classification)
- Used by USPTO + EPO
- Hierarchical: 9 sections (A-H, Y), thousands of subgroups
- Example: H04L 63/02 — security in computer networks

### IPC (International Patent Classification)
- WIPO standard
- Used by JPO, CNIPA, others
- Similar structure; broader than CPC

### USPC (US Patent Classification)
- Legacy; partially deprecated
- Some pre-2015 searches still useful

### How to find classifications
- Use Espacenet's "Classification search" tool
- Look at top results in keyword search; note their classifications
- Browse hierarchy in CPC viewer

A search by classification finds art a keyword search misses.

## 4. Search query patterns

### Boolean combinations
- `(A AND B) OR (A AND C)` — multiple novel-feature combinations
- `A NOT B` — exclude well-known applications
- `"phrase"` — exact phrases
- `term*` — truncation

### Field-specific
- `TI=` — title
- `AB=` — abstract
- `CL=` — claims
- `CPC=` — classification
- `IN=` — inventor
- `AS=` — assignee
- `PD=` — publication date

### Multi-field examples
- `TI=("neural network") AND CPC=G06N` — neural network classified in AI
- `(CL=("battery") AND CL=("solid state")) AND PD>=2020` — recent solid-state batteries

## 5. Non-patent prior art

Often dominant in fast-moving fields (especially software / ML).

### Sources
- **Google Scholar** + journal databases (see `research/litreview`)
- **arXiv** (CS, physics, math)
- **GitHub** + open-source repositories
- **Conference proceedings** (NeurIPS, CVPR, IEEE, ACM)
- **Industry whitepapers**
- **Trade publications**
- **Conference talks** (YouTube, slides)
- **Blog posts** (especially from research labs)
- **Wayback Machine** for older web disclosures

### Capture
- Date of disclosure (essential — must be before filing date)
- URL + archived copy (sources disappear)
- Specific page / section / claim mapped

## 6. The systematic search process

1. **Define the invention.** What's claimed novel?
2. **Identify keywords + synonyms.** Use thesauri, machine-translation hint, inventor input.
3. **Identify classifications.** Find them via Espacenet classification search + reading similar art.
4. **Initial broad search.** ~100-500 hits per query.
5. **Refine.** Narrow by date, classification, jurisdiction.
6. **Screen abstracts.** Mark relevant.
7. **Full read on relevant.** Identify claim-by-claim relevance.
8. **Citation chain.** Follow forward + backward citations from key references.
9. **Non-patent search.** Targeted at the same concepts.
10. **Document.** Search log with date, query, hits, decisions.

## 7. Citation network walking

Useful technique: from one relevant patent, walk:

- **Backward citations:** what did inventors cite as prior art?
- **Forward citations:** what later patents cited this?
- **Cited-by from non-patent literature:** academic citations

Often finds the most relevant art faster than keyword search.

## 8. Common search pitfalls

- **Keyword-only search.** Misses translations + synonyms + reclassified art.
- **One-database search.** Different databases index differently.
- **English-only.** Japanese + Chinese + German patents have unique art.
- **Recent-only.** Older patents are prior art too (even if expired for FTO, they bar patentability).
- **No classification search.** Misses art that uses different keywords.
- **Skipping non-patent literature.** Especially in software / biotech.
- **No documentation.** Can't reproduce the search; can't defend its thoroughness.

## 9. Search documentation

For each search:

- Date executed
- Database
- Query string
- Filters applied
- Total hits
- Relevant hits (after screening)
- Notes per relevant hit (what it discloses; impact on claims)

Keep search log: defensive record (good faith effort) + reusable for next round.

## 10. When to engage a professional searcher

- Pre-filing search for significant inventions
- Freedom-to-operate analysis
- Patent infringement litigation defense
- Complex chemistry / biotech (specialized expertise)
- Pre-acquisition due diligence

Professional searchers: deeper databases, classification expertise,
defensible methodology. Cost: $500-$5K depending on scope.

## 11. AI tools in patent search (2026)

LLM-assisted tools (Patlytics, IPRally, others):
- Useful for: initial idea generation, claim drafting suggestions
- Not yet replacement for systematic search
- Risk: false-confidence in completeness
- Always verify against authoritative databases

## 12. Common pitfalls

- **Self-disclosure as prior art.** Your own talk last year invalidates your patent (outside US).
- **Forgetting commercial use.** Sales activity > 1 year before filing = bar.
- **Missing one-year US grace period.** US has one; many countries don't.
- **Searching after disclosure.** Search before; novelty erodes the moment you disclose.
- **Citing only your own patents.** Examiner finds others; trust erodes.
- **No professional review on big inventions.** Penny-wise, pound-foolish.
