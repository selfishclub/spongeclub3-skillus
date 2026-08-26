# Tool CLI Reference

Read this when running `chunking_optimizer.py`, `retrieval_evaluator.py`, or `rag_pipeline_designer.py` — full flag/parameter tables, usage examples, and output formats. (These scripts live at the skill root.)

### chunking_optimizer.py

**Purpose:** Analyzes a document corpus and evaluates multiple chunking strategies (fixed-size, sentence-based, paragraph-based, semantic/heading-aware) to recommend the optimal approach with configuration parameters.

**Usage:**
```bash
python chunking_optimizer.py <directory> [options]
```

**Flags / Parameters:**

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `directory` | positional, required | -- | Directory containing text/markdown documents to analyze |
| `--output`, `-o` | string | None | Output file path for results in JSON format |
| `--config`, `-c` | string | None | JSON configuration file to customize strategy parameters (fixed_sizes, overlaps, sentence_max_sizes, paragraph_max_sizes, semantic_max_sizes) |
| `--extensions` | string list | `.txt .md .markdown` | File extensions to include when scanning the corpus |
| `--verbose`, `-v` | flag | off | Print all strategy scores in addition to the recommendation |

**Example:**
```bash
python chunking_optimizer.py ./docs --output results.json --extensions .txt .md --verbose
```

**Output Formats:**
- **Console** -- Corpus summary, recommended strategy name, performance score, reasoning text, and two sample chunks. With `--verbose`, all strategy scores are listed.
- **JSON** (`--output`) -- Full results object containing `corpus_info`, `strategy_results` (per-strategy size statistics, boundary quality, semantic coherence, vocabulary statistics, performance score), `recommendation` (best strategy, all scores, reasoning), and `sample_chunks`.

---

### retrieval_evaluator.py

**Purpose:** Evaluates retrieval system performance using a built-in TF-IDF baseline retriever and standard information retrieval metrics: Precision@K, Recall@K, MRR, and NDCG. Includes failure analysis and improvement recommendations.

**Usage:**
```bash
python retrieval_evaluator.py <queries> <corpus> <ground_truth> [options]
```

**Flags / Parameters:**

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `queries` | positional, required | -- | JSON file containing queries (list of `{"id": ..., "query": ...}` objects, or `{"queries": [...]}`) |
| `corpus` | positional, required | -- | Directory containing the document corpus |
| `ground_truth` | positional, required | -- | JSON file mapping query IDs to lists of relevant document IDs |
| `--output`, `-o` | string | None | Output file path for results in JSON format |
| `--k-values` | int list | `1 3 5 10` | K values used when computing Precision@K, Recall@K, and NDCG@K |
| `--extensions` | string list | `.txt .md .markdown` | File extensions to include from the corpus directory |
| `--verbose`, `-v` | flag | off | Print detailed per-metric values and failure analysis counts |

**Example:**
```bash
python retrieval_evaluator.py queries.json ./corpus ground_truth.json --output eval.json --k-values 1 5 10 --verbose
```

**Output Formats:**
- **Console** -- Evaluation summary table (Precision@1, Precision@5, Recall@5, MRR, NDCG@5) with performance assessment and numbered improvement recommendations. With `--verbose`, all aggregate metrics and failure analysis counts are printed.
- **JSON** (`--output`) -- Full results object containing `aggregate_metrics`, `query_results` (per-query metrics, retrieved docs, relevant docs), `failure_analysis` (poor precision/recall counts, zero-result counts, query length analysis, failure patterns), `evaluation_summary`, and `recommendations`.

---

### rag_pipeline_designer.py

**Purpose:** Accepts a system requirements specification and generates a complete RAG pipeline design including component recommendations (chunking, embedding, vector DB, retrieval, reranking, evaluation), cost projections, a Mermaid architecture diagram, and deployment configuration templates.

**Usage:**
```bash
python rag_pipeline_designer.py <requirements> [options]
```

**Flags / Parameters:**

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `requirements` | positional, required | -- | JSON file containing system requirements (document_types, document_count, avg_document_size, queries_per_day, query_patterns, latency_requirement, budget_monthly, accuracy_priority, cost_priority, maintenance_complexity) |
| `--output`, `-o` | string | None | Output file path for the pipeline design in JSON format |
| `--verbose`, `-v` | flag | off | Print full configuration templates for each component |

**Example:**
```bash
python rag_pipeline_designer.py requirements.json --output pipeline_design.json --verbose
```

**Output Formats:**
- **Console** -- Design summary with total monthly cost, per-component recommendations (name, rationale, cost), and a Mermaid architecture diagram. With `--verbose`, full JSON configuration templates for each component are printed.
- **JSON** (`--output`) -- Complete pipeline design object containing per-component `ComponentRecommendation` fields (name, type, config, rationale, pros, cons, cost_monthly), `total_cost`, `architecture_diagram` (Mermaid markup), and `config_templates` (per-component configs plus deployment/scaling/monitoring settings).
