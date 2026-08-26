# Search Strategy & PRISMA Reference

Practical reference for building reproducible literature search strategies.

## 1. The research question — PICO / PEO frames

### PICO (intervention questions)
- **P**opulation / problem
- **I**ntervention or phenomenon
- **C**omparator
- **O**utcome

Example: "In adults with type-2 diabetes (P), does intermittent fasting
(I) compared to caloric restriction (C) reduce HbA1c (O)?"

### PEO (qualitative questions)
- **P**opulation / problem
- **E**xposure / experience
- **O**utcome

Example: "What is the experience (E) of patients (P) recovering from
hip replacement surgery in the first month (O)?"

### Other frames
- SPIDER (qualitative): Sample / Phenomenon of Interest / Design / Evaluation / Research type
- ECLIPSE (policy / management): Expectation / Client group / Location / Impact / Professionals / Service
- BeHEMoTh (theory-related)

A well-framed question makes everything downstream easier.

## 2. Search strategy components

For each search:

- **Databases:** which to search (PubMed, Web of Science, Scopus, IEEE Xplore, ACM DL, JSTOR, SSRN, arXiv, Google Scholar)
- **Search string:** Boolean syntax with synonyms + truncation + proximity
- **Filters:** date range, language, type (journal, conference, preprint)
- **Date executed:** when ran (results change over time)
- **Hits returned:** count
- **Duplicates removed:** count

Document everything. A search strategy that can't be reproduced isn't a strategy.

## 3. Search syntax patterns

### Boolean
- `cancer AND prevention` — both terms
- `cancer OR neoplasm` — either term (capture synonyms)
- `cancer NOT melanoma` — exclude

### Truncation
- `prevent*` — preventive, prevention, preventing
- `child?` — child, children

### Phrase
- `"machine learning"` — exact phrase

### Proximity (database-dependent)
- `learning NEAR/3 reinforcement` — within 3 words
- `learning ADJ2 reinforcement` — within 2 words

### Field tags
- `"deep learning"[Title]` — limit to title field
- `Smith[Author]` — author search
- `Nature[Journal]` — venue search

## 4. Sources of search terms

- Thesauri (MeSH for medical; subject-specific elsewhere)
- Synonyms from existing relevant papers
- Subject indexes
- Citation chains (cited-by + references)
- Field experts' input
- Iteration: run search; review hits; add missed terms

## 5. PRISMA discipline (adapted)

PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses)
is the gold standard for medical systematic reviews and increasingly used
in other fields.

### Key elements
- **Protocol pre-registered** (PROSPERO for medical; OSF for others)
- **Search strategy** documented and reproducible
- **Inclusion / exclusion criteria** specified before screening
- **Screening process** documented (typically two reviewers)
- **PRISMA flow diagram** showing: records identified → screened → included
- **Quality assessment** of included studies
- **Synthesis approach** (narrative, thematic, meta-analysis)
- **Limitations** explicitly stated

### Flow diagram structure
```
Records identified through database searching (n=____)
+ Additional records identified through other sources (n=____)
= Records after duplicates removed (n=____)
→ Records screened by title/abstract (n=____)
  → Records excluded (n=____)
→ Full-text articles assessed for eligibility (n=____)
  → Full-text articles excluded, with reasons (n=____)
→ Studies included in qualitative synthesis (n=____)
→ Studies included in quantitative synthesis (n=____)
```

A PRISMA-style flow forces honesty: you can see how thin (or thick) the
included pool is.

## 6. Screening process

### Single-reviewer screening
- Faster
- Higher risk of inconsistency
- Acceptable for scoping reviews

### Dual-independent screening
- Two reviewers screen independently
- Resolve disagreements through discussion or third reviewer
- Standard for systematic reviews

### Automated assistance
- ML-assisted screening (Rayyan, Covidence, ASReview)
- Useful for large result sets
- Don't replace human judgment for inclusion decisions

## 7. Inclusion / exclusion criteria

Common criteria:

- **Date range** (last 5 years; or no limit)
- **Language** (English; multi-language teams may be broader)
- **Source type** (peer-reviewed journal; conference; gray literature; preprint)
- **Study type** (empirical; theoretical; review)
- **Population** (matches PICO)
- **Methodology** (e.g., RCT, mixed-methods, case study)
- **Outcome reported** (matches PICO)

Specify all upfront. Don't add criteria post-hoc to shrink the result set;
this is bias.

## 8. Search strategy quality criteria

A reproducible search strategy answers:

- Could someone else run this exact search and get similar results?
- Are the databases and date documented?
- Are the search terms / Boolean documented in full?
- Are the filters documented?
- Are inclusions and exclusions defined and applied consistently?
- Is the screening process documented?
- Is there a flow diagram showing the funnel?

If any answer is "no," the search isn't reproducible.

## 9. When systematic doesn't fit

Not every review is systematic. Alternatives:

### Scoping review
- Broader scope; less stringent criteria
- Maps a field rather than answers specific question
- Useful when literature is large or fragmented

### Rapid review
- Tighter timeline (weeks not months)
- Single reviewer; limited databases
- Adequate for policy / decision support, not for medical claims

### Narrative review
- Author-driven
- May not be reproducible
- Useful for synthesizing established knowledge with expertise

Be clear about which type of review you're producing.

## 10. Common pitfalls

- **Google Scholar as the only database.** Inconsistent indexing; not comprehensive.
- **No subject thesaurus.** Misses synonyms.
- **Single-reviewer screening on important reviews.** Inconsistent application.
- **Criteria added post-hoc.** Bias.
- **No documentation of excluded items.** Can't reproduce.
- **No flow diagram.** Can't see how thin the included set is.
- **Over-reliance on recent papers.** Misses foundational work.
- **Excluding by impact factor only.** Misses important non-prestige work.
- **No discussion of search limitations.** Reader can't assess trust.
