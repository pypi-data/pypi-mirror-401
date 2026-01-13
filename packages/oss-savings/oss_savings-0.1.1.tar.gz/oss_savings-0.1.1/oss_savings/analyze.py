#!/usr/bin/env python3
"""
Analyze a dependency file and calculate total OSS savings.
Supports: package.json, requirements.txt, Gemfile, Cargo.toml, go.mod
"""

import argparse
import json
import re
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from oss_savings.calculator import (
    analyze_repo,
    fmt_currency,
    fmt_num,
    DEFAULT_HOURLY_RATE,
    RepoStats,
)


@dataclass
class DepAnalysis:
    name: str
    github_repo: Optional[str]
    stats: Optional[RepoStats]
    error: Optional[str] = None


def parse_package_json(path: Path) -> list[tuple[str, str]]:
    """Parse dependencies from package.json."""
    with open(path) as f:
        data = json.load(f)
    
    deps = {}
    deps.update(data.get("dependencies", {}))
    deps.update(data.get("devDependencies", {}))
    
    return [(name, version) for name, version in deps.items()]


def parse_requirements_txt(path: Path) -> list[tuple[str, str]]:
    """Parse dependencies from requirements.txt."""
    deps = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("-"):
                continue
            match = re.match(r"^([a-zA-Z0-9_-]+)", line)
            if match:
                deps.append((match.group(1), "*"))
    return deps


def parse_gemfile(path: Path) -> list[tuple[str, str]]:
    """Parse dependencies from Gemfile."""
    deps = []
    with open(path) as f:
        for line in f:
            match = re.match(r"^\s*gem\s+['\"]([^'\"]+)['\"]", line)
            if match:
                deps.append((match.group(1), "*"))
    return deps


def parse_cargo_toml(path: Path) -> list[tuple[str, str]]:
    """Parse dependencies from Cargo.toml."""
    deps = []
    in_deps = False
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("[dependencies]") or line.startswith("[dev-dependencies]"):
                in_deps = True
                continue
            if line.startswith("[") and in_deps:
                in_deps = False
                continue
            if in_deps and "=" in line:
                name = line.split("=")[0].strip()
                if name and not name.startswith("#"):
                    deps.append((name, "*"))
    return deps


def parse_go_mod(path: Path) -> list[tuple[str, str]]:
    """Parse dependencies from go.mod."""
    deps = []
    in_require = False
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("require ("):
                in_require = True
                continue
            if line == ")" and in_require:
                in_require = False
                continue
            if in_require or line.startswith("require "):
                match = re.search(r"(github\.com/[^\s]+)", line)
                if match:
                    repo_path = match.group(1)
                    parts = repo_path.replace("github.com/", "").split("/")
                    if len(parts) >= 2:
                        deps.append((f"{parts[0]}/{parts[1]}", "*"))
    return deps


def detect_and_parse(path: Path) -> tuple[str, list[tuple[str, str]]]:
    """Detect file type and parse dependencies."""
    name = path.name.lower()
    
    if name == "package.json":
        return "npm", parse_package_json(path)
    elif name == "requirements.txt" or name.endswith(".txt"):
        return "pypi", parse_requirements_txt(path)
    elif name == "gemfile" or name == "gemfile.lock":
        return "rubygems", parse_gemfile(path)
    elif name == "cargo.toml":
        return "crates", parse_cargo_toml(path)
    elif name == "go.mod":
        return "go", parse_go_mod(path)
    else:
        print(f"Error: Unsupported file type: {path.name}")
        sys.exit(1)


def lookup_npm_github(package_name: str) -> Optional[str]:
    """Look up GitHub repo for an npm package."""
    url = f"https://registry.npmjs.org/{package_name}/latest"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "oss-savings"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        
        repo = data.get("repository", {})
        if isinstance(repo, dict):
            repo_url = repo.get("url", "")
        else:
            repo_url = str(repo)
        
        match = re.search(r"github\.com[/:]([^/]+)/([^/.]+)", repo_url)
        if match:
            return f"{match.group(1)}/{match.group(2)}"
    except:
        pass
    return None


def lookup_pypi_github(package_name: str) -> Optional[str]:
    """Look up GitHub repo for a PyPI package."""
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "oss-savings"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        
        info = data.get("info", {})
        urls = info.get("project_urls", {}) or {}
        
        for key, url in urls.items():
            if "github.com" in url.lower():
                match = re.search(r"github\.com/([^/]+)/([^/]+)", url)
                if match:
                    return f"{match.group(1)}/{match.group(2)}"
        
        # Try homepage
        homepage = info.get("home_page", "") or ""
        if "github.com" in homepage:
            match = re.search(r"github\.com/([^/]+)/([^/]+)", homepage)
            if match:
                return f"{match.group(1)}/{match.group(2)}"
    except:
        pass
    return None


def lookup_rubygems_github(package_name: str) -> Optional[str]:
    """Look up GitHub repo for a RubyGems package."""
    url = f"https://rubygems.org/api/v1/gems/{package_name}.json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "oss-savings"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        
        for key in ["source_code_uri", "homepage_uri"]:
            uri = data.get(key, "")
            if uri and "github.com" in uri:
                match = re.search(r"github\.com/([^/]+)/([^/]+)", uri)
                if match:
                    return f"{match.group(1)}/{match.group(2)}"
    except:
        pass
    return None


def lookup_crates_github(package_name: str) -> Optional[str]:
    """Look up GitHub repo for a crates.io package."""
    url = f"https://crates.io/api/v1/crates/{package_name}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "oss-savings"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        
        crate = data.get("crate", {})
        repo_url = crate.get("repository", "")
        if "github.com" in repo_url:
            match = re.search(r"github\.com/([^/]+)/([^/]+)", repo_url)
            if match:
                return f"{match.group(1)}/{match.group(2)}"
    except:
        pass
    return None


def lookup_github_repo(registry: str, package_name: str) -> Optional[str]:
    """Look up GitHub repo for a package."""
    # For go.mod, the package name is already the repo
    if registry == "go":
        return package_name
    
    lookups = {
        "npm": lookup_npm_github,
        "pypi": lookup_pypi_github,
        "rubygems": lookup_rubygems_github,
        "crates": lookup_crates_github,
    }
    
    lookup_fn = lookups.get(registry)
    if lookup_fn:
        return lookup_fn(package_name)
    return None


def calculate_funding_score(stats: RepoStats) -> float:
    """
    Calculate a funding priority score.
    High score = should fund (high savings + high risk + low popularity).
    """
    savings_score = min(stats.total_dollars / 1_000_000, 10)  # Cap at 10M
    risk_score = stats.risk.score / 20 if stats.risk else 0  # 0-5 range
    
    # Inverse popularity - smaller projects need more help
    popularity_factor = 1.0
    if stats.stars < 1000:
        popularity_factor = 2.0
    elif stats.stars < 10000:
        popularity_factor = 1.5
    
    return (savings_score + risk_score) * popularity_factor


def analyze_dependency_file(
    path: Path,
    hourly_rate: float = DEFAULT_HOURLY_RATE,
    model: str = "linear",
    limit: Optional[int] = None,
) -> list[DepAnalysis]:
    """Analyze all dependencies in a file."""
    registry, deps = detect_and_parse(path)
    print(f"Found {len(deps)} dependencies in {path.name} ({registry})")
    
    if limit:
        deps = deps[:limit]
        print(f"Analyzing first {limit} dependencies...")
    
    results = []
    seen_repos = set()
    
    for i, (name, version) in enumerate(deps):
        print(f"[{i+1}/{len(deps)}] Looking up {name}...", end=" ", flush=True)
        
        github_repo = lookup_github_repo(registry, name)
        
        if not github_repo:
            print("(no GitHub repo found)")
            results.append(DepAnalysis(name=name, github_repo=None, stats=None, error="No GitHub repo found"))
            continue
        
        # Dedupe repos (e.g., @types/node and node)
        repo_key = github_repo.lower()
        if repo_key in seen_repos:
            print(f"(duplicate: {github_repo})")
            continue
        seen_repos.add(repo_key)
        
        print(f"-> {github_repo}")
        
        try:
            owner, repo = github_repo.split("/")
            stats = analyze_repo(
                owner, repo,
                analyze_deps=False,
                hourly_rate=hourly_rate,
                model=model,
            )
            results.append(DepAnalysis(name=name, github_repo=github_repo, stats=stats))
        except SystemExit:
            raise
        except Exception as e:
            results.append(DepAnalysis(name=name, github_repo=github_repo, stats=None, error=str(e)))
    
    return results


def print_summary(results: list[DepAnalysis], hourly_rate: float):
    """Print summary report with funding recommendations."""
    successful = [r for r in results if r.stats]
    failed = [r for r in results if not r.stats]
    
    if not successful:
        print("\nNo dependencies could be analyzed.")
        return
    
    total_build = sum(r.stats.build_dollars for r in successful)
    total_maint = sum(r.stats.maint_dollars for r in successful)
    total_hours = sum(r.stats.total_hours for r in successful)
    total_dollars = sum(r.stats.total_dollars for r in successful)
    
    print("\n" + "=" * 70)
    print("  DEPENDENCY ANALYSIS SUMMARY")
    print("=" * 70)
    
    print(f"\n📊 Analyzed: {len(successful)} dependencies ({len(failed)} failed)")
    
    print(f"\n💰 TOTAL SAVINGS:")
    print(f"   Build:       {fmt_currency(total_build)}")
    print(f"   Maintenance: {fmt_currency(total_maint)}")
    print(f"   ─────────────────────")
    print(f"   TOTAL:       {fmt_currency(total_dollars)} ({total_hours:,.0f} hours)")
    
    # Top dependencies by savings
    print(f"\n📈 TOP DEPENDENCIES BY SAVINGS:")
    sorted_by_savings = sorted(successful, key=lambda r: r.stats.total_dollars, reverse=True)[:10]
    for i, r in enumerate(sorted_by_savings, 1):
        risk_icon = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}.get(r.stats.risk.level, "⚪")
        print(f"   {i:2}. {r.github_repo:<35} {fmt_currency(r.stats.total_dollars):>10}  {risk_icon}")
    
    # Funding recommendations
    print(f"\n🎯 FUNDING RECOMMENDATIONS:")
    print("   (High savings + high risk + lower popularity = fund this!)\n")
    
    scored = [(r, calculate_funding_score(r.stats)) for r in successful]
    scored.sort(key=lambda x: x[1], reverse=True)
    
    for i, (r, score) in enumerate(scored[:10], 1):
        risk_icon = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}.get(r.stats.risk.level, "⚪")
        stars = fmt_num(r.stats.stars)
        print(f"   {i:2}. {r.github_repo:<35} {fmt_currency(r.stats.total_dollars):>10}  {risk_icon}  ⭐{stars}")
        
        # Show why
        reasons = []
        if r.stats.risk.score >= 20:
            reasons.append(f"risk: {r.stats.risk.score:.0f}/100")
        if r.stats.stars < 1000:
            reasons.append("low visibility")
        if r.stats.total_dollars >= 1_000_000:
            reasons.append("high value")
        if reasons:
            print(f"       └─ {', '.join(reasons)}")
    
    # High risk warnings
    high_risk = [r for r in successful if r.stats.risk and r.stats.risk.score >= 40]
    if high_risk:
        print(f"\n⚠️  HIGH RISK DEPENDENCIES:")
        for r in sorted(high_risk, key=lambda x: x.stats.risk.score, reverse=True)[:5]:
            factors = [f"{k}: {v['detail']}" for k, v in r.stats.risk.factors.items() if v["score"] > 0]
            print(f"   • {r.github_repo} (risk: {r.stats.risk.score:.0f}/100)")
            for f in factors[:2]:
                print(f"     - {f}")
    
    if failed:
        print(f"\n❌ FAILED TO ANALYZE ({len(failed)}):")
        for r in failed[:10]:
            print(f"   • {r.name}: {r.error}")
    
    print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze a dependency file and calculate total OSS savings",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Supported files:
  - package.json (npm)
  - requirements.txt (pip)
  - Gemfile (bundler)
  - Cargo.toml (cargo)
  - go.mod (go)

Examples:
  python3 analyze_deps.py package.json
  python3 analyze_deps.py requirements.txt --limit 20
  python3 analyze_deps.py Cargo.toml --model cocomo
        """
    )
    parser.add_argument("file", help="Path to dependency file")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of dependencies to analyze (useful for testing)",
    )
    parser.add_argument(
        "--hourly-rate",
        type=float,
        default=DEFAULT_HOURLY_RATE,
        help=f"Loaded hourly rate in USD (default: {DEFAULT_HOURLY_RATE})",
    )
    parser.add_argument(
        "--model",
        choices=["linear", "cocomo"],
        default="linear",
        help="Estimation model (default: linear)",
    )
    
    args = parser.parse_args()
    
    path = Path(args.file)
    if not path.exists():
        print(f"Error: File not found: {args.file}")
        sys.exit(1)
    
    results = analyze_dependency_file(
        path,
        hourly_rate=args.hourly_rate,
        model=args.model,
        limit=args.limit,
    )
    
    print_summary(results, args.hourly_rate)


if __name__ == "__main__":
    main()
