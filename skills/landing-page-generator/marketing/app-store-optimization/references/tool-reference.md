# Tool Reference

Read this when invoking the skill's Python scripts — full CLI/library usage, classes, methods, parameters, returns, and convenience functions for all eight ASO tools.

---

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| [keyword_analyzer.py](../scripts/keyword_analyzer.py) | Analyze keywords for volume and competition | `python keyword_analyzer.py --keywords "todo,task,planner"` |
| [metadata_optimizer.py](../scripts/metadata_optimizer.py) | Validate metadata character limits and density | `python metadata_optimizer.py --platform ios --title "App Title"` |
| [competitor_analyzer.py](../scripts/competitor_analyzer.py) | Extract and compare competitor keywords | `python competitor_analyzer.py --competitors "App1,App2,App3"` |
| [aso_scorer.py](../scripts/aso_scorer.py) | Calculate overall ASO health score | `python aso_scorer.py --app-id com.example.app` |
| [ab_test_planner.py](../scripts/ab_test_planner.py) | Plan tests and calculate sample sizes | `python ab_test_planner.py --cvr 0.05 --lift 0.10` |
| [review_analyzer.py](../scripts/review_analyzer.py) | Analyze review sentiment and themes | `python review_analyzer.py --app-id com.example.app` |
| [launch_checklist.py](../scripts/launch_checklist.py) | Generate platform-specific launch checklists | `python launch_checklist.py --platform ios` |
| [localization_helper.py](../scripts/localization_helper.py) | Manage multi-language metadata | `python localization_helper.py --locales "en,es,de,ja"` |

### Assets

| Template | Purpose |
|----------|---------|
| [aso-audit-template.md](../assets/aso-audit-template.md) | Structured audit checklist for app store listings |

---

## keyword_analyzer.py

**Type:** Python library (imported, not CLI)

**Classes:**
- `KeywordAnalyzer` -- Core analysis class

**Key Methods:**

| Method | Parameters | Returns |
|--------|-----------|---------|
| `analyze_keyword()` | `keyword: str`, `search_volume: int = 0`, `competing_apps: int = 0`, `relevance_score: float = 0.0` | Dict with keyword analysis (potential score 0-100, difficulty score 0-100, recommendation) |
| `compare_keywords()` | `keywords_data: List[Dict]` (each dict: keyword, search_volume, competing_apps, relevance_score) | Ranked keywords with primary/secondary/long-tail categorization |
| `find_long_tail_opportunities()` | `base_keyword: str`, `modifiers: List[str]` | Long-tail keyword variations with competition estimates |
| `extract_keywords_from_text()` | `text: str`, `min_word_length: int = 3` | Top 50 keywords/phrases by frequency |
| `calculate_keyword_density()` | `text: str`, `target_keywords: List[str]` | Dict of keyword: density percentage |

**Convenience Function:** `analyze_keyword_set(keywords_data)` -- Analyzes and ranks a full keyword set in one call.

## metadata_optimizer.py

**Type:** Python library (imported, not CLI)

**Classes:**
- `MetadataOptimizer(platform: str = 'apple')` -- Platform must be `'apple'` or `'google'`

**Key Methods:**

| Method | Parameters | Returns |
|--------|-----------|---------|
| `optimize_title()` | `app_name: str`, `target_keywords: List[str]`, `include_brand: bool = True` | Title options with length, keywords included, pros/cons, recommendation |
| `optimize_description()` | `app_info: Dict` (name, key_features, unique_value, target_audience), `target_keywords: List[str]`, `description_type: str = 'full'` | Optimized description with keyword density analysis. Types: `'full'`, `'short'` (Google), `'subtitle'` (Apple) |
| `optimize_keyword_field()` | `target_keywords: List[str]`, `app_title: str = ""`, `app_description: str = ""` | Apple-only. Optimized 100-char keyword field (no spaces, no plurals, no title duplicates) |
| `validate_character_limits()` | `metadata: Dict[str, str]` | Validation report with errors, warnings, usage percentages |
| `calculate_keyword_density()` | `text: str`, `target_keywords: List[str]` | Per-keyword density with status (too_low / optimal / too_high) |

**Convenience Function:** `optimize_app_metadata(platform, app_info, target_keywords)` -- Optimizes title, description, and keyword field in one call.

## competitor_analyzer.py

**Type:** Python library (imported, not CLI)

**Classes:**
- `CompetitorAnalyzer(category: str, platform: str = 'apple')`

**Key Methods:**

| Method | Parameters | Returns |
|--------|-----------|---------|
| `analyze_competitor()` | `app_data: Dict` (app_name, title, description, rating, ratings_count, keywords) | Title analysis, description analysis, keyword strategy, competitive strength score (0-100) |
| `compare_competitors()` | `competitors_data: List[Dict]` | Ranked competitors, common keywords, keyword gaps, best practices, opportunities |
| `identify_gaps()` | `your_app_data: Dict`, `competitors_data: List[Dict]` | Keyword gaps, rating gaps, content gaps, competitive positioning assessment |

**Convenience Function:** `analyze_competitor_set(category, competitors_data, platform='apple')` -- Full competitive analysis in one call.

## aso_scorer.py

**Type:** Python library (imported, not CLI)

**Classes:**
- `ASOScorer` -- Calculates weighted ASO health score (0-100)

**Key Methods:**

| Method | Parameters | Returns |
|--------|-----------|---------|
| `calculate_overall_score()` | `metadata: Dict`, `ratings: Dict`, `keyword_performance: Dict`, `conversion: Dict` | Overall score, health status, breakdown by component, prioritized recommendations, strengths, weaknesses |
| `score_metadata_quality()` | `metadata: Dict` (title_keyword_count, title_length, description_length, description_quality, keyword_density) | Score 0-100 |
| `score_ratings_reviews()` | `ratings: Dict` (average_rating, total_ratings, recent_ratings_30d) | Score 0-100 |
| `score_keyword_performance()` | `keyword_performance: Dict` (top_10, top_50, top_100, improving_keywords) | Score 0-100 |
| `score_conversion_metrics()` | `conversion: Dict` (impression_to_install, downloads_last_30_days, downloads_trend) | Score 0-100 |

**Weights:** metadata_quality 25%, ratings_reviews 25%, keyword_performance 25%, conversion_metrics 25%.

**Convenience Function:** `calculate_aso_score(metadata, ratings, keyword_performance, conversion)`

## ab_test_planner.py

**Type:** Python library (imported, not CLI)

**Classes:**
- `ABTestPlanner`

**Key Methods:**

| Method | Parameters | Returns |
|--------|-----------|---------|
| `design_test()` | `test_type: str` (`'icon'`, `'screenshot'`, `'title'`, `'description'`), `variant_a: Dict`, `variant_b: Dict`, `hypothesis: str`, `success_metric: str = 'conversion_rate'` | Test design with ID, variants, secondary metrics, best practices |
| `calculate_sample_size()` | `baseline_conversion: float`, `minimum_detectable_effect: float`, `confidence_level: str = 'standard'` (`'high'`/`'standard'`/`'exploratory'`), `power: float = 0.80` | Sample size per variant, duration estimates for low/medium/high traffic |
| `calculate_significance()` | `variant_a_conversions: int`, `variant_a_visitors: int`, `variant_b_conversions: int`, `variant_b_visitors: int` | Z-score, p-value, significance at 90%/95%, decision recommendation |
| `track_test_results()` | `test_id: str`, `results_data: Dict` | Progress tracking, current significance, next steps |
| `generate_test_report()` | `test_id: str`, `final_results: Dict` | Complete report with insights, implementation plan, learnings |

**Convenience Function:** `plan_ab_test(test_type, variant_a, variant_b, hypothesis, baseline_conversion)`

## review_analyzer.py

**Type:** Python library (imported, not CLI)

**Classes:**
- `ReviewAnalyzer(app_name: str)`

**Key Methods:**

| Method | Parameters | Returns |
|--------|-----------|---------|
| `analyze_sentiment()` | `reviews: List[Dict]` (each: text, rating, date) | Sentiment distribution (positive/neutral/negative %), average rating, detailed sentiments |
| `extract_common_themes()` | `reviews: List[Dict]`, `min_mentions: int = 3` | Common words, phrases, categorized themes (features, performance, usability, support, pricing) |
| `identify_issues()` | `reviews: List[Dict]`, `rating_threshold: int = 3` | Categorized issues (crashes, bugs, performance, compatibility) with severity scores and priority |
| `find_feature_requests()` | `reviews: List[Dict]` | Clustered and prioritized feature requests |
| `track_sentiment_trends()` | `reviews_by_period: Dict[str, List[Dict]]` | Trend direction (improving/declining/stable), period-over-period comparison |
| `generate_response_templates()` | `issue_category: str` (`'crash'`, `'bug'`, `'feature_request'`, `'positive'`, `'negative_general'`) | Response templates for review management |

**Convenience Function:** `analyze_reviews(app_name, reviews)` -- Runs sentiment, themes, issues, and feature requests in one call.

## launch_checklist.py

**Type:** Python library (imported, not CLI)

**Classes:**
- `LaunchChecklistGenerator(platform: str = 'both')` -- Platform: `'apple'`, `'google'`, or `'both'`

**Key Methods:**

| Method | Parameters | Returns |
|--------|-----------|---------|
| `generate_prelaunch_checklist()` | `app_info: Dict` (name, category, target_audience), `launch_date: Optional[str]` (YYYY-MM-DD) | Platform-specific checklists, universal checklist, timeline with milestones, completion summary |
| `validate_app_store_compliance()` | `app_data: Dict`, `platform: str = 'apple'` | Compliance validation with errors, warnings, recommendations |
| `create_update_plan()` | `current_version: str`, `planned_features: List[str]`, `update_frequency: str = 'monthly'` | Version schedule, feature distribution, What's New templates |
| `optimize_launch_timing()` | `app_category: str`, `target_audience: str`, `current_date: Optional[str]` | Optimal dates, day-of-week recommendation, seasonal considerations |
| `plan_seasonal_campaigns()` | `app_category: str`, `current_month: int = None` | Seasonal opportunities, campaign ideas, implementation timeline |

**Convenience Function:** `generate_launch_checklist(platform, app_info, launch_date)`

## localization_helper.py

**Type:** Python library (imported, not CLI)

**Classes:**
- `LocalizationHelper(app_category: str = 'general')`

**Key Methods:**

| Method | Parameters | Returns |
|--------|-----------|---------|
| `identify_target_markets()` | `current_market: str = 'en-US'`, `budget_level: str = 'medium'` (`'low'`/`'medium'`/`'high'`), `target_market_count: int = 5` | Prioritized markets (tier 1/2/3), estimated costs, phased implementation plan |
| `translate_metadata()` | `source_metadata: Dict[str, str]`, `source_language: str`, `target_language: str`, `platform: str = 'apple'` | Character limit validation per field with language-specific multipliers, translation notes |
| `adapt_keywords()` | `source_keywords: List[str]`, `source_language: str`, `target_language: str`, `target_market: str` | Adaptation strategy per keyword (full_localization / adapt_and_translate / direct_translation), cultural considerations |
| `validate_translations()` | `translated_metadata: Dict[str, str]`, `target_language: str`, `platform: str = 'apple'` | Character limit validation, quality checks (placeholders, excessive punctuation) |
| `calculate_localization_roi()` | `target_markets: List[str]`, `current_monthly_downloads: int`, `localization_cost: float`, `expected_lift_percentage: float = 0.15` | Market breakdown, expected monthly lift, payback period, annual ROI |

**Convenience Function:** `plan_localization_strategy(current_market, budget_level, monthly_downloads)`
