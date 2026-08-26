# Source Quality Assessment Reference

Reference for evaluating the quality of literature sources.

## 1. Quality dimensions

A useful 6-dimension model:

### Methodology
- Is the study design appropriate for the question?
- Is the method described in enough detail to reproduce?
- Are limitations acknowledged?

### Sample / data
- Is the sample adequate for the claim?
- Is it representative?
- Are the data reliable?

### Peer review
- Has the work been peer-reviewed?
- Where (impact factor, reputation)?
- Have peers cited it positively or critically?

### Reproducibility
- Is data / code available?
- Are analyses described in enough detail?
- Has anyone replicated the findings?

### Recency
- Is the source current?
- For fast-moving fields: < 2 years
- For stable fields: < 10 years

### Citation impact
- How often has it been cited?
- By whom (field leaders or marginal voices)?
- Critical or supportive citations?

A single weak dimension is rarely fatal; multiple weaknesses are a flag.

## 2. Source hierarchy (typical)

### Tier 1 (highest)
- Peer-reviewed journal articles in field-leading venues
- Systematic reviews / meta-analyses
- Replicated studies

### Tier 2
- Peer-reviewed journal articles in mid-tier venues
- Conference proceedings (field-dependent — top venues for CS rival journals)
- Working papers from established institutions
- Government reports (rigorous)

### Tier 3
- Preprints (not yet peer-reviewed)
- Conference posters / abstracts
- Dissertations
- Industry research reports

### Tier 4
- Trade publications
- Quality journalism
- Books with editorial review

### Tier 5 (lowest)
- Self-published / non-reviewed
- Op-eds
- Blogs (with rare exceptions for field experts)
- Social media

Field-specific tier assignments vary. In ML / AI, top conferences (NeurIPS, ICML, CVPR) are Tier 1; journals are sometimes slower.

## 3. Field-specific quality signals

### Medical / clinical
- Randomized controlled trial (RCT) is gold for interventions
- Cochrane reviews for synthesis
- Pre-registration in ClinicalTrials.gov
- CONSORT / STROBE / PRISMA compliance

### Social science
- Pre-registration on OSF
- Power calculations reported
- Effect sizes reported (not just p-values)
- Replication studies cited

### Computer science / ML
- Open code (GitHub link)
- Standard benchmarks used
- Hyperparameter settings reported
- Reproducibility checklist (NeurIPS standard)

### Humanities
- Source criticism
- Engagement with established scholarship
- Methodological transparency
- Peer-reviewed venues

## 4. Red flags

### Methodology
- Sample too small for the claim
- No control / comparison group
- No discussion of limitations
- Cherry-picked analyses
- Post-hoc rationalization

### Statistical
- P-values reported without effect sizes
- Multiple comparisons without correction
- Outliers excluded without justification
- Misleading visualizations

### Authorship / venue
- Predatory journals (Beall's list)
- Pay-to-publish without peer review
- Conflicts of interest not disclosed
- Author list inflation

### Citation patterns
- Self-citation cycles (small group cites only each other)
- Citing only supportive evidence
- Citing without engaging with the cited work

## 5. Using citation count carefully

Citation count is a signal, not the truth:

### Pros
- Indicates field engagement
- Higher count = more eyes / scrutiny
- Useful for finding seminal work

### Cons
- Recent work cited less by definition
- Field-size affects baseline
- Citation count includes critical citations
- Citation gaming exists (citation rings, self-citation)

Compare within field + period. Don't trust raw counts across disciplines.

## 6. The "famous but wrong" problem

Highly-cited papers can be wrong. Examples:

- Studies that didn't replicate (psychology replication crisis)
- Findings later retracted but still cited
- Famous experiments with methodological problems revealed later

Check: has the work been replicated? Are there critical responses?
Has it been retracted (retractionwatch.com)?

## 7. Preprints — opportunity + caution

### When preprints add value
- Fast-moving fields where journal cycle is too slow
- Methods papers that have working code
- Replications of recent work
- Pre-registered studies with results posted

### When to be cautious
- Strong claims without peer review
- Hot topics where rigor is sacrificed
- Authors without track record
- Lack of methodology detail

Preprints are not negative signals; they need extra evaluation.

## 8. Gray literature

Gray literature = non-traditional publication (reports, working papers, theses).

### When useful
- Niche topics not covered in peer-reviewed literature
- Recent developments (industry / NGO reports)
- Theses with novel data
- Policy documents

### Cautions
- No peer review
- Author bias (industry-sponsored = check)
- May not be archived (citation rot)
- Quality varies wildly

Track gray literature usage transparently in your review.

## 9. Source assessment workflow

For each candidate source:

1. **Title + abstract:** is it likely relevant? (yes / maybe / no)
2. **Quick scan:** methodology + author + venue + date (decide: read in full?)
3. **Full read** of included sources
4. **Quality score:** rate each dimension
5. **Relevance score:** how directly does it answer your question?
6. **Notes:** what does it contribute? what are its limitations?
7. **Tag:** themes + methodology + key findings

## 10. Common pitfalls

- **Including by venue alone.** A bad paper in a great venue is still bad.
- **Excluding by venue alone.** A great paper in a small venue is still great.
- **Citation chain following without checking.** Errors propagate.
- **Mistaking citation for endorsement.** Critical citations exist.
- **Single source treated as fact.** Triangulate.
- **No quality scoring.** All sources weighted equally is wrong.
- **No discussion of source limitations in the review.** Hides what reader needs.
