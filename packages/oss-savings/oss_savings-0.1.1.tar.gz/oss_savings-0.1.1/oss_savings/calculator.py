#!/usr/bin/env python3
"""
OSS Savings Calculator v3
Estimates how much money a project saved by using an open-source library
using GitHub API stats with improved heuristics.

Supports both linear LOC-based and COCOMO-lite estimation models.
"""

import argparse
import math
import os
import re
import sys
import time
import urllib.request
import json
from datetime import datetime
from dataclasses import dataclass
from typing import Optional

from oss_savings.deps import detect_package_manager, fetch_dependencies, DependencyTree

# Configurable defaults
DEFAULT_HOURLY_RATE = 175  # SF Bay Area loaded rate
DEFAULT_YEARLY_SALARY = 250_000
BYTES_PER_LOC = 35  # Global fallback

# Per-language bytes per LOC (more accurate than global constant)
BYTES_PER_LOC_BY_LANG = {
    "c": 25,
    "c++": 27,
    "go": 30,
    "rust": 30,
    "java": 32,
    "kotlin": 32,
    "c#": 32,
    "python": 34,
    "ruby": 34,
    "javascript": 30,
    "typescript": 32,
    "swift": 32,
    "objective-c": 30,
    "objective-c++": 30,
    "cuda": 28,
    "assembly": 20,
    "html": 45,
    "xml": 45,
    "markdown": 60,
}

# Language categorization for weighting
DOC_LANGS = {
    "markdown", "restructuredtext", "jupyter notebook", "roff", "tex",
    "rich text format",
}
CONFIG_LANGS = {"json", "yaml", "toml", "xml"}
STYLE_LANGS = {"css", "scss", "less", "stylus"}

# Legacy combined set for backwards compat
DOC_CONFIG_LANGS = DOC_LANGS | CONFIG_LANGS | STYLE_LANGS | {"html", "svg"}

# Performance-critical languages
PERF_LANGS = {"c", "c++", "rust", "go", "assembly", "cuda", "mlir", "zig"}

# Domain complexity weights - FLATTENED to avoid double-counting with LOC/hour
# Most differentiation now comes from DOMAIN_LOC_PER_HOUR
DOMAIN_COMPLEXITY = {
    "ai_ml": 1.10,
    "crypto_security": 1.10,
    "parsers_compilers": 1.05,
    "networking_concurrency": 1.05,
    "data_structures": 1.0,
    "ui_components": 1.0,
    "utilities": 1.0,
}

# LOC per hour by domain (primary complexity differentiator)
DOMAIN_LOC_PER_HOUR = {
    "ai_ml": 8,
    "crypto_security": 8,
    "parsers_compilers": 9,
    "networking_concurrency": 10,
    "data_structures": 10,
    "ui_components": 12,
    "utilities": 12,
}

# COCOMO-lite parameters (a, b) for effort = a * KLOC^b
COCOMO_PARAMS = {
    "ai_ml": (3.0, 1.10),
    "crypto_security": (3.0, 1.10),
    "parsers_compilers": (3.0, 1.08),
    "networking_concurrency": (2.8, 1.07),
    "data_structures": (2.5, 1.05),
    "ui_components": (2.4, 1.05),
    "utilities": (2.4, 1.03),
}
HOURS_PER_PERSON_MONTH = 152  # ~19 days * 8h

# Topics that indicate category
TOPIC_CATEGORIES = {
    "machine-learning": "ai_ml", "deep-learning": "ai_ml", "neural-network": "ai_ml",
    "artificial-intelligence": "ai_ml", "ai": "ai_ml", "ml": "ai_ml",
    "pytorch": "ai_ml", "tensorflow": "ai_ml", "nlp": "ai_ml",
    "computer-vision": "ai_ml", "llm": "ai_ml", "transformer": "ai_ml",
    
    "cryptography": "crypto_security", "security": "crypto_security",
    "encryption": "crypto_security", "authentication": "crypto_security",
    "oauth": "crypto_security", "jwt": "crypto_security",
    
    "compiler": "parsers_compilers", "parser": "parsers_compilers",
    "lexer": "parsers_compilers", "interpreter": "parsers_compilers",
    "programming-language": "parsers_compilers", "transpiler": "parsers_compilers",
    
    "networking": "networking_concurrency", "http": "networking_concurrency",
    "websocket": "networking_concurrency", "grpc": "networking_concurrency",
    "async": "networking_concurrency", "distributed": "networking_concurrency",
    
    "database": "data_structures", "data-structures": "data_structures",
    "algorithm": "data_structures", "algorithms": "data_structures",
    
    "frontend": "ui_components", "ui": "ui_components", "component": "ui_components",
}

# Framework/runtime keywords
FRAMEWORK_KEYWORDS = [
    "runtime", "engine", "framework", "library", "compiler", "reconciler",
    "scheduler", "virtual dom", "fiber", "renderer", "core", "vm",
    "interpreter", "bundler", "transpiler",
]

# Safety/criticality keywords
SAFETY_KEYWORDS = [
    "cryptography", "crypto", "security", "authorization", "authentication",
    "tls", "ssl", "password", "payment", "database", "storage",
    "kubernetes", "orchestration", "infrastructure",
]


@dataclass
class RiskAssessment:
    score: float  # 0-100, higher = more risky
    level: str    # "low", "medium", "high", "critical"
    factors: dict # individual risk factors
    

@dataclass
class RepoStats:
    name: str
    description: str
    topics: list
    languages: dict
    stars: int
    forks: int
    watchers: int
    contributors: int
    created_at: str
    pushed_at: str
    
    raw_loc: int
    core_loc: int
    effective_loc: int
    
    primary_category: str
    domain_weight: float
    perf_factor: float
    safety_factor: float
    contributor_factor: float
    total_complexity: float
    loc_per_hour: int
    
    build_hours: float
    build_dollars: float
    
    years_active: float
    usage_years: float
    activity_factor: float
    maint_hours: float
    maint_dollars: float
    
    total_hours: float
    total_dollars: float
    
    model_used: str = "linear"
    hourly_rate: float = DEFAULT_HOURLY_RATE
    risk: RiskAssessment = None
    dep_tree: DependencyTree = None
    dep_savings: dict = None


def github_api_get(url: str, return_headers: bool = False, _retries: int = 3):
    """Make a GitHub API request with retry for transient errors."""
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "oss-savings-calculator",
    }
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            if return_headers:
                return data, dict(response.headers)
            return data
    except urllib.error.HTTPError as e:
        if e.code in (502, 503, 504) and _retries > 0:
            time.sleep(2)
            return github_api_get(url, return_headers, _retries - 1)
        if e.code == 403:
            print("\nError: GitHub API rate limit exceeded.")
            print("\nTo increase your rate limit from 60 to 5,000 requests/hour:")
            print("  1. Install GitHub CLI: https://cli.github.com/")
            print("  2. Authenticate:        gh auth login")
            print("  3. Export token:        export GITHUB_TOKEN=$(gh auth token)")
            print("\nAdd the export to ~/.zshrc or ~/.bashrc for persistence.")
        elif e.code == 404:
            print("Error: Repository not found.")
        elif e.code in (502, 503, 504):
            print(f"Error: GitHub API timeout ({e.code}) after retries.")
        else:
            print(f"Error: GitHub API returned {e.code}")
        sys.exit(1)


def get_contributor_count(owner: str, repo: str) -> int:
    """Get approximate contributor count using pagination headers."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors?per_page=1&anon=true"
    try:
        _, headers = github_api_get(url, return_headers=True)
        link = headers.get("Link", "")
        match = re.search(r'page=(\d+)>; rel="last"', link)
        if match:
            return int(match.group(1))
        return 1
    except:
        return 0


def parse_repo_url(url_or_name: str) -> tuple:
    """Parse GitHub URL or owner/repo format."""
    match = re.match(r"(?:https?://)?(?:www\.)?github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$", url_or_name)
    if match:
        return match.group(1), match.group(2)
    match = re.match(r"^([^/]+)/([^/]+)$", url_or_name)
    if match:
        return match.group(1), match.group(2)
    print(f"Error: Invalid repository format: {url_or_name}")
    sys.exit(1)


def language_weight(lang_l: str) -> float:
    """Return weight for a language (0 = ignore, 1 = full code)."""
    if lang_l in DOC_LANGS:
        return 0.05
    if lang_l in STYLE_LANGS:
        return 0.20
    if lang_l in CONFIG_LANGS:
        return 0.40
    if lang_l in {"html", "svg"}:
        return 0.15
    return 1.0


def estimate_core_loc(languages: dict) -> tuple:
    """Filter out non-code languages and estimate LOC with per-language accuracy."""
    total_bytes = sum(languages.values())
    core_loc_float = 0.0
    
    for lang, bytes_ in languages.items():
        lang_l = lang.lower()
        weight = language_weight(lang_l)
        if weight == 0.0:
            continue
        bpl = BYTES_PER_LOC_BY_LANG.get(lang_l, BYTES_PER_LOC)
        core_loc_float += (bytes_ * weight) / bpl
    
    raw_loc = int(total_bytes / BYTES_PER_LOC) if total_bytes > 0 else 0
    core_loc = int(core_loc_float)
    return raw_loc, core_loc


def test_docs_ratio(topics: list, description: str) -> float:
    """Estimate what percentage of code is tests/docs/examples."""
    desc = (description or "").lower()
    topics_l = [t.lower() for t in topics]
    
    ratio = 0.25  # Higher default - OSS typically has substantial tests
    
    doc_topics = {"documentation", "docs", "examples", "tutorial", "awesome-list", "learning"}
    doc_keywords = ["examples", "tutorial", "awesome list", "cookbook", "samples", "guide", "handbook"]
    test_keywords = ["test", "tests", "spec", "benchmark", "fuzz"]
    
    if any(t in doc_topics for t in topics_l) or any(k in desc for k in doc_keywords):
        ratio += 0.10
    
    if any(k in desc for k in test_keywords):
        ratio += 0.05
    
    core_keywords = ["runtime", "kernel", "compiler", "engine", "vm", "database", "core", "framework"]
    if any(k in desc for k in core_keywords):
        ratio -= 0.10
    
    return max(0.10, min(ratio, 0.50))


def effective_loc(loc: int) -> int:
    """Apply diminishing returns for very large repos."""
    FULL_RATE_LIMIT = 250_000
    if loc <= FULL_RATE_LIMIT:
        return loc
    
    extra = loc - FULL_RATE_LIMIT
    MEGA_EXPONENT = 0.75
    scaled_extra = int(extra ** MEGA_EXPONENT)
    
    effective = FULL_RATE_LIMIT + scaled_extra
    return min(effective, 2_000_000)


def is_framework_repo(name: str, description: str, topics: list) -> bool:
    """Detect if this repo IS a framework/runtime."""
    desc = (description or "").lower()
    name_l = name.lower()
    topics_l = [t.lower() for t in topics]
    
    major_frameworks = {"react", "vue", "angular", "svelte", "solid", "preact",
                        "express", "fastify", "next", "nuxt", "remix",
                        "django", "flask", "rails", "laravel", "spring"}
    if name_l in major_frameworks:
        return True
    
    if name_l in topics_l:
        return True
    
    for kw in FRAMEWORK_KEYWORDS:
        if kw in desc:
            return True
    
    return False


def determine_category(topics: list, description: str, languages: dict, name: str = "") -> str:
    """Determine the primary complexity category."""
    scores = {cat: 0 for cat in DOMAIN_COMPLEXITY}
    
    for topic in topics:
        if topic.lower() in TOPIC_CATEGORIES:
            scores[TOPIC_CATEGORIES[topic.lower()]] += 10
    
    desc = (description or "").lower()
    desc_keywords = {
        "ai_ml": ["machine learning", "deep learning", "neural", "model", "training", "inference", "tensor"],
        "crypto_security": ["crypto", "encrypt", "security", "auth", "password"],
        "parsers_compilers": ["parser", "compiler", "lexer", "ast", "syntax", "reconciler", "fiber", "scheduler"],
        "networking_concurrency": ["async", "concurrent", "http", "server", "network"],
        "data_structures": ["database", "index", "tree", "graph", "algorithm", "virtual dom", "diff"],
        "ui_components": ["component", "ui", "frontend", "render"],
    }
    for cat, keywords in desc_keywords.items():
        for kw in keywords:
            if kw in desc:
                scores[cat] += 3
    
    lang_names = [l.lower() for l in languages.keys()]
    if "cuda" in lang_names or "mlir" in lang_names:
        scores["ai_ml"] += 15
    
    if is_framework_repo(name, description, topics):
        scores["parsers_compilers"] += 15
        scores["data_structures"] += 10
        scores["ui_components"] = 0
    
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "utilities"


def calc_perf_factor(languages: dict) -> float:
    """Calculate performance-critical language factor."""
    total = sum(languages.values())
    if total == 0:
        return 1.0
    
    perf_bytes = sum(b for l, b in languages.items() if l.lower() in PERF_LANGS)
    perf_ratio = perf_bytes / total
    
    # Up to 1.2x boost, clamped
    factor = 1.0 + 0.2 * perf_ratio
    return max(1.0, min(factor, 1.2))


def calc_safety_factor(topics: list, description: str) -> float:
    """Calculate safety/criticality factor."""
    desc = (description or "").lower()
    topics_l = [t.lower() for t in topics]
    
    score = 0
    safety_topics = {"cryptography", "security", "encryption", "authentication", "database", "infrastructure"}
    score += sum(2 for t in topics_l if t in safety_topics)
    score += sum(1 for k in SAFETY_KEYWORDS if k in desc)
    
    factor = 1.0 + 0.1 * score
    return max(1.0, min(factor, 1.4))


def calc_years_active(created_at: str, pushed_at: str) -> float:
    """Calculate years of active development."""
    try:
        created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        pushed = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
        days = max((pushed - created).days, 365)
        return days / 365.0
    except:
        return 1.0


def get_commit_activity(owner: str, repo: str) -> Optional[int]:
    """Get commits in the last year from commit activity stats."""
    url = f"https://api.github.com/repos/{owner}/{repo}/stats/commit_activity"
    try:
        activity = github_api_get(url)
        if isinstance(activity, list) and activity:
            return sum(week.get("total", 0) for week in activity)
    except:
        pass
    return None


def calc_activity_factor(owner: str, repo: str, stars: int, watchers: int, forks: int, archived: bool = False) -> float:
    """Calculate activity factor using commit stats with popularity fallback."""
    if archived:
        return 0.3
    
    commits_last_year = get_commit_activity(owner, repo)
    
    if commits_last_year is not None and commits_last_year > 0:
        commits_norm = math.log10(commits_last_year + 1)
        factor = 0.4 + 0.4 * commits_norm
        return max(0.3, min(factor, 1.7))
    
    # Fallback to popularity-based
    popularity = stars + 2 * forks + 3 * watchers
    if popularity == 0:
        return 0.5
    score = math.log10(popularity + 10)
    factor = 0.6 + 0.2 * score
    return max(0.5, min(factor, 1.5))


def get_top_contributors(owner: str, repo: str, limit: int = 10) -> list:
    """Get top contributors with their commit counts."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors?per_page={limit}"
    try:
        return github_api_get(url)
    except:
        return []


def assess_risk(repo_data: dict, contributors: int, top_contributors: list) -> RiskAssessment:
    """Assess project risk based on multiple factors."""
    factors = {}
    total_score = 0
    
    # Staleness risk
    pushed_at = repo_data.get("pushed_at", "")
    if pushed_at:
        try:
            pushed = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
            days_since = (datetime.now(pushed.tzinfo) - pushed).days
            if days_since > 365 * 2:
                stale_score = min(30, 15 + (days_since - 730) // 180 * 5)
                factors["staleness"] = {"score": stale_score, "detail": f"No commits in {days_since // 365} years"}
                total_score += stale_score
            elif days_since > 365:
                factors["staleness"] = {"score": 10, "detail": "No commits in over a year"}
                total_score += 10
        except:
            pass
    
    # Bus factor risk
    if top_contributors and len(top_contributors) >= 2:
        total_commits = sum(c.get("contributions", 0) for c in top_contributors)
        if total_commits > 0:
            top1_pct = top_contributors[0].get("contributions", 0) / total_commits * 100
            if top1_pct > 80:
                factors["bus_factor"] = {"score": 25, "detail": f"Top contributor has {top1_pct:.0f}% of commits"}
                total_score += 25
            elif top1_pct > 60:
                factors["bus_factor"] = {"score": 15, "detail": f"Top contributor has {top1_pct:.0f}% of commits"}
                total_score += 15
    elif contributors <= 1:
        factors["bus_factor"] = {"score": 20, "detail": "Single maintainer"}
        total_score += 20
    
    # Issue backlog risk
    open_issues = repo_data.get("open_issues_count", 0)
    if open_issues > 5000:
        factors["issue_backlog"] = {"score": 15, "detail": f"Very high issue backlog ({open_issues:,} open)"}
        total_score += 15
    elif open_issues > 1000:
        factors["issue_backlog"] = {"score": 8, "detail": f"High issue backlog ({open_issues:,} open)"}
        total_score += 8
    elif open_issues > 500:
        factors["issue_backlog"] = {"score": 3, "detail": f"Moderate issue backlog ({open_issues:,} open)"}
        total_score += 3
    
    # Archived/disabled
    if repo_data.get("archived"):
        factors["archived"] = {"score": 40, "detail": "Repository is archived"}
        total_score += 40
    if repo_data.get("disabled"):
        factors["disabled"] = {"score": 50, "detail": "Repository is disabled"}
        total_score += 50
    
    # Low popularity risk for important deps
    stars = repo_data.get("stargazers_count", 0)
    if stars < 100:
        factors["low_popularity"] = {"score": 10, "detail": f"Low visibility ({stars} stars)"}
        total_score += 10
    
    total_score = min(100, total_score)
    
    if total_score >= 60:
        level = "critical"
    elif total_score >= 40:
        level = "high"
    elif total_score >= 20:
        level = "medium"
    else:
        level = "low"
    
    return RiskAssessment(score=total_score, level=level, factors=factors)


def calc_contributor_factor(contributors: int) -> float:
    """More contributors = more coordination overhead saved."""
    if contributors <= 1:
        return 1.0
    factor = 1.0 + 0.15 * min(math.log10(contributors), 3.33)
    return min(factor, 1.5)


def estimate_build_hours_linear(eff_loc: int, loc_per_hour: int, total_complexity: float) -> float:
    """Linear LOC-based build estimation."""
    base_hours = eff_loc / loc_per_hour
    return base_hours * total_complexity


def estimate_build_hours_cocomo(eff_loc: int, primary_category: str, total_complexity: float) -> float:
    """COCOMO-lite build estimation (superlinear scaling)."""
    kloc = eff_loc / 1000.0
    a, b = COCOMO_PARAMS.get(primary_category, (2.5, 1.05))
    person_months = a * (kloc ** b) * total_complexity
    return person_months * HOURS_PER_PERSON_MONTH


def estimate_maintenance_hours(
    base_hours: float,
    total_complexity: float,
    usage_years: float,
    activity_factor: float,
) -> float:
    """Estimate total maintenance hours over the usage period."""
    effective_years = min(usage_years, 10.0)
    
    # Base: 15% of build per year, adjusted by activity
    annual_ratio = 0.15 * activity_factor
    annual_ratio = max(0.10, min(annual_ratio, 0.25))
    
    maint_hours_per_year = base_hours * annual_ratio * total_complexity
    return maint_hours_per_year * effective_years


def analyze_repo(
    owner: str,
    repo: str,
    analyze_deps: bool = False,
    years_of_use: Optional[float] = None,
    hourly_rate: float = DEFAULT_HOURLY_RATE,
    model: str = "linear",
) -> RepoStats:
    """Analyze a GitHub repository."""
    print(f"Fetching stats for {owner}/{repo}...")
    
    repo_data = github_api_get(f"https://api.github.com/repos/{owner}/{repo}")
    languages = github_api_get(f"https://api.github.com/repos/{owner}/{repo}/languages")
    contributors = get_contributor_count(owner, repo)
    top_contributors = get_top_contributors(owner, repo, limit=10)
    
    name = repo_data.get("name", repo)
    description = repo_data.get("description", "")
    topics = repo_data.get("topics", [])
    stars = repo_data.get("stargazers_count", 0)
    forks = repo_data.get("forks_count", 0)
    watchers = repo_data.get("subscribers_count", 0)
    created_at = repo_data.get("created_at", "")
    pushed_at = repo_data.get("pushed_at", "")
    archived = repo_data.get("archived", False)
    
    # LOC estimation with per-language accuracy
    raw_loc, core_loc = estimate_core_loc(languages)
    test_ratio = test_docs_ratio(topics, description)
    adjusted_loc = int(core_loc * (1 - test_ratio))
    eff_loc = effective_loc(adjusted_loc)
    
    # Complexity factors
    primary_category = determine_category(topics, description, languages, name)
    domain_weight = DOMAIN_COMPLEXITY[primary_category]
    perf_factor = calc_perf_factor(languages)
    safety_factor = calc_safety_factor(topics, description)
    contributor_factor = calc_contributor_factor(contributors)
    total_complexity = domain_weight * perf_factor * safety_factor * contributor_factor
    
    loc_per_hour = DOMAIN_LOC_PER_HOUR[primary_category]
    
    # Build savings - choose model
    if model == "cocomo":
        build_hours = estimate_build_hours_cocomo(eff_loc, primary_category, total_complexity)
    else:
        build_hours = estimate_build_hours_linear(eff_loc, loc_per_hour, total_complexity)
    
    build_dollars = build_hours * hourly_rate
    
    # Maintenance savings
    years_active = calc_years_active(created_at, pushed_at)
    usage_years = years_of_use if years_of_use is not None else min(years_active, 7.0)
    activity_factor = calc_activity_factor(owner, repo, stars, watchers, forks, archived)
    
    # Base hours for maintenance calculation
    base_hours = eff_loc / loc_per_hour
    maint_hours = estimate_maintenance_hours(base_hours, total_complexity, usage_years, activity_factor)
    maint_dollars = maint_hours * hourly_rate
    
    total_hours = build_hours + maint_hours
    total_dollars = build_dollars + maint_dollars
    
    # Risk assessment
    risk = assess_risk(repo_data, contributors, top_contributors)
    
    # Dependency analysis
    dep_tree = None
    dep_savings = None
    if analyze_deps:
        pm = detect_package_manager(languages)
        if pm:
            print(f"Analyzing {pm} dependencies...")
            candidates = [repo, repo.lower(), name, name.lower()]
            for pkg_name in candidates:
                dep_tree = fetch_dependencies(pm, pkg_name)
                if dep_tree:
                    break
            
            if dep_tree and dep_tree.direct_deps:
                dep_count = len(dep_tree.direct_deps)
                avg_hours_per_dep = 30
                dep_savings = {
                    "count": dep_count,
                    "estimated_hours": dep_count * avg_hours_per_dep,
                    "estimated_dollars": dep_count * avg_hours_per_dep * hourly_rate,
                }
    
    return RepoStats(
        name=name, description=description, topics=topics, languages=languages,
        stars=stars, forks=forks, watchers=watchers, contributors=contributors,
        created_at=created_at, pushed_at=pushed_at,
        raw_loc=raw_loc, core_loc=core_loc, effective_loc=eff_loc,
        primary_category=primary_category,
        domain_weight=domain_weight, perf_factor=perf_factor,
        safety_factor=safety_factor, contributor_factor=contributor_factor,
        total_complexity=total_complexity, loc_per_hour=loc_per_hour,
        build_hours=build_hours, build_dollars=build_dollars,
        years_active=years_active, usage_years=usage_years,
        activity_factor=activity_factor,
        maint_hours=maint_hours, maint_dollars=maint_dollars,
        total_hours=total_hours, total_dollars=total_dollars,
        model_used=model, hourly_rate=hourly_rate,
        risk=risk, dep_tree=dep_tree, dep_savings=dep_savings,
    )


def fmt_currency(amount: float) -> str:
    if amount >= 1_000_000_000:
        return f"${amount / 1_000_000_000:.2f}B"
    elif amount >= 1_000_000:
        return f"${amount / 1_000_000:.2f}M"
    elif amount >= 1_000:
        return f"${amount / 1_000:.1f}K"
    return f"${amount:.0f}"


def fmt_num(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def print_report(s: RepoStats):
    print("\n" + "=" * 65)
    print(f"  OSS SAVINGS REPORT: {s.name}")
    print("=" * 65)
    
    if s.description:
        print(f"\n{s.description[:80]}{'...' if len(s.description) > 80 else ''}")
    
    print(f"\n⭐ {fmt_num(s.stars)} stars  |  🍴 {fmt_num(s.forks)} forks  |  👥 {fmt_num(s.contributors)} contributors")
    print(f"📅 Active for {s.years_active:.1f} years (using {s.usage_years:.1f} years for calculations)")
    
    # Languages
    print("\n💻 Languages (code only):")
    sorted_langs = sorted(s.languages.items(), key=lambda x: -x[1])[:5]
    total = sum(s.languages.values())
    for lang, bytes_count in sorted_langs:
        if lang.lower() not in DOC_CONFIG_LANGS:
            pct = (bytes_count / total) * 100 if total > 0 else 0
            print(f"   • {lang}: {pct:.1f}%")
    
    if s.topics:
        print(f"\n🏷️  Topics: {', '.join(s.topics[:6])}")
    
    # LOC breakdown
    print(f"\n📝 Lines of Code:")
    print(f"   Raw estimate:      {s.raw_loc:,}")
    print(f"   Core code only:    {s.core_loc:,}")
    print(f"   Effective (capped): {s.effective_loc:,}")
    
    # Complexity
    print(f"\n🎯 Complexity Analysis:")
    print(f"   Category:          {s.primary_category.replace('_', ' ').title()}")
    print(f"   Domain weight:     {s.domain_weight:.2f}x")
    print(f"   Perf-lang boost:   {s.perf_factor:.2f}x")
    print(f"   Safety/critical:   {s.safety_factor:.2f}x")
    print(f"   Contributor boost: {s.contributor_factor:.2f}x")
    print(f"   Combined:          {s.total_complexity:.2f}x")
    print(f"   Model:             {s.model_used.upper()}")
    if s.model_used == "linear":
        print(f"   LOC/hour assumed:  {s.loc_per_hour}")
    
    # Savings breakdown
    print(f"\n💰 SAVINGS BREAKDOWN:")
    print(f"   ┌─────────────────────────────────────────────┐")
    print(f"   │ Build savings:        {s.build_hours:>10,.0f} hrs  {fmt_currency(s.build_dollars):>10} │")
    print(f"   │ Maintenance savings:  {s.maint_hours:>10,.0f} hrs  {fmt_currency(s.maint_dollars):>10} │")
    print(f"   ├─────────────────────────────────────────────┤")
    print(f"   │ TOTAL:                {s.total_hours:>10,.0f} hrs  {fmt_currency(s.total_dollars):>10} │")
    print(f"   └─────────────────────────────────────────────┘")
    print(f"   (at ${s.hourly_rate:.0f}/hr loaded rate)")
    
    # Equivalents
    print(f"\n📈 That's equivalent to:")
    years = s.total_hours / (160 * 12)
    print(f"   • {years:.1f} engineer-years of work")
    eng_salaries = s.total_dollars / DEFAULT_YEARLY_SALARY
    if eng_salaries >= 1:
        print(f"   • {eng_salaries:.1f} senior engineer annual salaries")
    
    # Dependency analysis
    if s.dep_tree:
        print(f"\n📦 DEPENDENCIES ({s.dep_tree.package_manager}):")
        print(f"   Direct dependencies: {len(s.dep_tree.direct_deps)}")
        if s.dep_savings:
            print(f"   Dep savings (est):   {s.dep_savings['estimated_hours']:,} hrs / {fmt_currency(s.dep_savings['estimated_dollars'])}")
        if s.dep_tree.direct_deps:
            print(f"   Top deps: {', '.join(d.name for d in s.dep_tree.direct_deps[:6])}")
    
    # Risk assessment
    if s.risk:
        risk_icons = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}
        icon = risk_icons.get(s.risk.level, "⚪")
        print(f"\n⚠️  RISK ASSESSMENT: {icon} {s.risk.level.upper()} ({s.risk.score:.0f}/100)")
        
        risky_factors = [(k, v) for k, v in s.risk.factors.items() if v["score"] > 0]
        if risky_factors:
            risky_factors.sort(key=lambda x: -x[1]["score"])
            for factor, data in risky_factors[:4]:
                print(f"   • {factor.replace('_', ' ').title()}: {data['detail']}")
        else:
            print("   • No significant risk factors detected")
    
    print("=" * 65 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Calculate OSS savings - how much money you saved by using an open-source library",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python oss_savings.py pytorch/pytorch
  python oss_savings.py https://github.com/facebook/react
  python oss_savings.py expressjs/express --deps
  python oss_savings.py rails/rails --model cocomo --years-of-use 5
  python oss_savings.py django/django --hourly-rate 150
        """
    )
    parser.add_argument("repo", help="GitHub repo (owner/repo or full URL)")
    parser.add_argument("--deps", action="store_true", help="Analyze dependencies")
    parser.add_argument(
        "--years-of-use",
        type=float,
        default=None,
        help="Years your project will rely on this library (default: min(repo age, 7))",
    )
    parser.add_argument(
        "--hourly-rate",
        type=float,
        default=DEFAULT_HOURLY_RATE,
        help=f"Loaded hourly rate for engineers (default: {DEFAULT_HOURLY_RATE})",
    )
    parser.add_argument(
        "--model",
        choices=["linear", "cocomo"],
        default="linear",
        help="Estimation model: linear (LOC/hour) or cocomo (industry-standard)",
    )
    
    args = parser.parse_args()
    
    owner, repo = parse_repo_url(args.repo)
    stats = analyze_repo(
        owner, repo,
        analyze_deps=args.deps,
        years_of_use=args.years_of_use,
        hourly_rate=args.hourly_rate,
        model=args.model,
    )
    print_report(stats)


if __name__ == "__main__":
    main()
