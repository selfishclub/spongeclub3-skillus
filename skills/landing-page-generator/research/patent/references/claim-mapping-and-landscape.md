# Claim Mapping & Landscape Reference

Reference for analyzing patent claims and mapping IP landscapes.

## 1. Anatomy of a patent

- **Title** — short descriptor
- **Abstract** — public-facing summary (cannot be used to interpret claims)
- **Field of the invention** — broad area
- **Background** — prior art context
- **Summary** — high-level invention description
- **Detailed description** — full implementation (enablement requirement)
- **Drawings + figures**
- **Claims** — THE legal scope; what's actually protected
- **Bibliography** — cited prior art

The claims are what matter. Everything else supports them.

## 2. Claim types

### Independent claims
- Stand alone; don't reference other claims
- Define the broadest scope
- Usually 1-3 per patent
- Highest litigation value

### Dependent claims
- Reference and narrow an independent claim
- Add features ("the system of claim 1, wherein...")
- Provide fallback if independent claim is invalidated

### Method claims
- "A method for X comprising: step a, step b, step c"
- Process protection
- Often used for software/algorithms

### System claims
- "A system comprising: component 1, component 2"
- Physical/structural protection

### Apparatus claims
- "An apparatus for X comprising: component A, component B"
- Similar to system; mechanical bias

### Composition claims (chemistry)
- "A composition comprising: component A, B, C"
- Chemical formulations

### Use claims
- "Use of compound X for Y" (varies by jurisdiction; not always allowed)

## 3. Reading a claim

A claim is a single sentence with a defined structure:

```
[Preamble], comprising:
[Element 1];
[Element 2]; and
[Element 3].
```

The preamble may be limiting or non-limiting (case-by-case interpretation).

The body lists elements that must ALL be present for infringement.

### "Comprising" vs "consisting of"
- **Comprising:** open; additional elements OK (broader)
- **Consisting of:** closed; only these elements (narrower)
- **Consisting essentially of:** open to materials that don't affect essential features

This single word change is huge in litigation.

## 4. Claim mapping

For each candidate prior art (or competitor patent), map its claims to
your invention element-by-element.

### For prior art search
Goal: does the prior art disclose every element of my claim?
- If yes → my claim is anticipated (not novel)
- If most → may be obviousness combination with another reference

### For FTO
Goal: does my product practice every element of their claim?
- If yes → potential infringement
- If no (one element missing) → not infringing that claim

### Mapping matrix
| Your claim element | Prior art reference | Where (column/line) | Verdict |
|--------------------|---------------------|---------------------|---------|
| A | Smith 2018 | col 3:14-22 | Discloses |
| B | Smith 2018 | col 5:1-10 | Discloses |
| C | Jones 2019 | col 2:5-15 | Discloses |
| D | (none found) | | Novel |

If you find D for everything, the invention is novel. If you find a single reference disclosing all elements, the claim is anticipated.

## 5. Doctrine of equivalents

A claim covers not only literal infringement but also "equivalents":

- Substantially the same function
- In substantially the same way
- To achieve substantially the same result

This expands claim scope and complicates FTO analysis. Don't assume "we use Y instead of X" avoids infringement.

## 6. Landscape analysis dimensions

When mapping a landscape:

### By owner
- Who has filed most? (likely category leaders)
- Who's recently entered? (new threats)
- Who's exited? (signal about market)
- Who's been acquired (and where did patents go)?

### By technology cluster
- Group patents by CPC/IPC
- Find density (crowded areas) + sparseness (white space)
- White space = opportunity (or area no one's interested)

### By recency
- Filings increasing? (hot area)
- Filings declining? (mature or dying)
- Recent priority dates = recent invention

### By geography
- Where is filing concentrated?
- Where is product activity vs filing?
- National advantages (e.g., heavy biotech filing in EU)

### By claim type
- Method vs system vs composition mix
- Tells you about commercialization model

### By assignee transitions
- Inventor changes (talent moves)
- Assignee transfers (acquisitions, licensing deals)

## 7. White space identification

A white space candidate:

- No or few patents in a CPC subgroup relevant to your invention
- Existing patents are old (filing date > 10 years ago, expiration close)
- Existing patents have narrow claims (room to file broader)
- Existing patents have weak prior art behind them (could be invalidated)

White space is not always opportunity:
- Maybe no one cares (no market)
- Maybe it's not patentable (subject matter or obviousness)
- Maybe it's covered by older art too broad to easily find

Validate with market evidence + commercial diligence.

## 8. Patent strength signals

For each patent, assess:

- **Claim breadth** — narrow claims are weaker
- **Prosecution history** — many narrowing amendments = weaker
- **Citations** — highly cited = important
- **Family size** — large international family = strategic priority
- **Continuation activity** — ongoing prosecutions = active strategy
- **Litigation history** — survived challenges = strong; lost at PTAB = weak
- **Assignee** — sophisticated patentee (big tech, NPE) = more enforceable

A strong patent in an area you operate in is a real risk.

## 9. Visualizing the landscape

Useful visualizations:

### Filing timeline
- Year on x-axis, count on y-axis
- Cluster by assignee
- Shows market entry, hot periods

### Bubble chart
- X: filing year; Y: # citations; Size: family size
- Identifies dominant patents

### Network graph
- Patents as nodes; citations as edges
- Shows knowledge flow + key documents

### Heatmap
- CPC subgroups × assignees
- Color = patent count
- Identifies hotspots

## 10. Landscape outputs for strategy

A useful landscape report includes:

1. **Executive summary** — top 3 takeaways
2. **Market context** — why this area, why now
3. **Key players** — top 5-10 by patent activity
4. **Technology subareas** — clusters with hot/cold designation
5. **White space candidates** — areas thin on art
6. **Top risk patents** — for FTO purposes
7. **Recommended next steps** — file here, design-around here, license here

## 11. Common pitfalls

- **Counting patents = importance.** Some big assignees file noise; some small assignees file critical IP.
- **Ignoring patent quality.** Strong vs weak patents have different risk profiles.
- **Focus only on issued patents.** Pending applications are tomorrow's grants.
- **Forgetting continuations.** Active continuations expand scope over time.
- **Landscape without market context.** Patents without business case = expensive paperwork.
- **One-time landscape.** Refresh quarterly; landscapes shift.
