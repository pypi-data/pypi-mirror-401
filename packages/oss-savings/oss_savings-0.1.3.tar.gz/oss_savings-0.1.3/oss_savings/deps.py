#!/usr/bin/env python3
"""
Dependency analysis for OSS Savings Calculator.
Detects package manager and fetches dependency tree.
"""

import json
import re
import urllib.request
from dataclasses import dataclass
from typing import Optional


@dataclass
class Dependency:
    name: str
    version: str
    registry: str  # npm, pypi, crates, etc.
    github_repo: Optional[str] = None  # owner/repo if detected


@dataclass 
class DependencyTree:
    package_manager: str
    package_name: str
    direct_deps: list  # List[Dependency]
    total_dep_count: int


def detect_package_manager(languages: dict, repo_files: list = None) -> Optional[str]:
    """
    Detect package manager from languages and common files.
    Returns: npm, pypi, crates, go, rubygems, or None
    """
    if not languages:
        return None
    
    primary_lang = max(languages, key=languages.get).lower()
    
    lang_to_pm = {
        "javascript": "npm",
        "typescript": "npm",
        "python": "pypi",
        "rust": "crates",
        "go": "go",
        "ruby": "rubygems",
    }
    
    return lang_to_pm.get(primary_lang)


def fetch_npm_deps(package_name: str) -> Optional[DependencyTree]:
    """Fetch dependencies from npm registry."""
    url = f"https://registry.npmjs.org/{package_name}/latest"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "oss-savings"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        
        deps = data.get("dependencies", {})
        dev_deps = data.get("devDependencies", {})
        
        direct_deps = []
        for name, version in deps.items():
            # Try to extract GitHub repo from package
            github_repo = extract_github_from_npm(name)
            direct_deps.append(Dependency(
                name=name,
                version=version,
                registry="npm",
                github_repo=github_repo
            ))
        
        return DependencyTree(
            package_manager="npm",
            package_name=package_name,
            direct_deps=direct_deps,
            total_dep_count=len(deps) + len(dev_deps)
        )
    except Exception as e:
        return None


def extract_github_from_npm(package_name: str) -> Optional[str]:
    """Try to get GitHub repo from npm package metadata."""
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
        
        # Parse GitHub URL
        match = re.search(r"github\.com[/:]([^/]+)/([^/.]+)", repo_url)
        if match:
            return f"{match.group(1)}/{match.group(2)}"
    except:
        pass
    return None


def fetch_pypi_deps(package_name: str) -> Optional[DependencyTree]:
    """Fetch dependencies from PyPI."""
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "oss-savings"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        
        info = data.get("info", {})
        requires = info.get("requires_dist", []) or []
        
        direct_deps = []
        for req_str in requires:
            # Parse requirement string like "requests>=2.0"
            match = re.match(r"^([a-zA-Z0-9_-]+)", req_str)
            if match:
                dep_name = match.group(1)
                # Skip extras and markers
                if "extra ==" in req_str:
                    continue
                direct_deps.append(Dependency(
                    name=dep_name,
                    version="*",
                    registry="pypi",
                    github_repo=None  # Would need another lookup
                ))
        
        # Get GitHub repo from project URLs
        github_repo = None
        urls = info.get("project_urls", {}) or {}
        for key, url in urls.items():
            if "github.com" in url.lower():
                match = re.search(r"github\.com/([^/]+)/([^/]+)", url)
                if match:
                    github_repo = f"{match.group(1)}/{match.group(2)}"
                    break
        
        return DependencyTree(
            package_manager="pypi",
            package_name=package_name,
            direct_deps=direct_deps,
            total_dep_count=len(direct_deps)
        )
    except Exception as e:
        return None


def fetch_crates_deps(package_name: str) -> Optional[DependencyTree]:
    """Fetch dependencies from crates.io."""
    url = f"https://crates.io/api/v1/crates/{package_name}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "oss-savings"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        
        crate = data.get("crate", {})
        
        # Get dependencies from versions endpoint
        latest = crate.get("newest_version", "")
        deps_url = f"https://crates.io/api/v1/crates/{package_name}/{latest}/dependencies"
        
        req = urllib.request.Request(deps_url, headers={"User-Agent": "oss-savings"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            deps_data = json.loads(resp.read().decode())
        
        deps = deps_data.get("dependencies", [])
        direct_deps = []
        for dep in deps:
            if dep.get("kind") == "normal":
                direct_deps.append(Dependency(
                    name=dep.get("crate_id", ""),
                    version=dep.get("req", "*"),
                    registry="crates",
                    github_repo=None
                ))
        
        # Get GitHub repo
        github_repo = None
        repo_url = crate.get("repository", "")
        if "github.com" in repo_url:
            match = re.search(r"github\.com/([^/]+)/([^/]+)", repo_url)
            if match:
                github_repo = f"{match.group(1)}/{match.group(2)}"
        
        return DependencyTree(
            package_manager="crates",
            package_name=package_name,
            direct_deps=direct_deps,
            total_dep_count=len(direct_deps)
        )
    except Exception as e:
        return None


def fetch_rubygems_deps(package_name: str) -> Optional[DependencyTree]:
    """Fetch dependencies from RubyGems."""
    url = f"https://rubygems.org/api/v1/gems/{package_name}.json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "oss-savings"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        
        deps = data.get("dependencies", {})
        runtime_deps = deps.get("runtime", [])
        
        direct_deps = []
        for dep in runtime_deps:
            direct_deps.append(Dependency(
                name=dep.get("name", ""),
                version=dep.get("requirements", "*"),
                registry="rubygems",
                github_repo=None
            ))
        
        # Get GitHub repo from source_code_uri or homepage_uri
        github_repo = None
        for key in ["source_code_uri", "homepage_uri"]:
            uri = data.get(key, "")
            if uri and "github.com" in uri:
                match = re.search(r"github\.com/([^/]+)/([^/]+)", uri)
                if match:
                    github_repo = f"{match.group(1)}/{match.group(2)}"
                    break
        
        return DependencyTree(
            package_manager="rubygems",
            package_name=package_name,
            direct_deps=direct_deps,
            total_dep_count=len(direct_deps)
        )
    except Exception as e:
        return None


def fetch_dependencies(package_manager: str, package_name: str) -> Optional[DependencyTree]:
    """Fetch dependencies based on package manager."""
    fetchers = {
        "npm": fetch_npm_deps,
        "pypi": fetch_pypi_deps,
        "crates": fetch_crates_deps,
        "rubygems": fetch_rubygems_deps,
    }
    
    fetcher = fetchers.get(package_manager)
    if fetcher:
        return fetcher(package_name)
    return None


# Known repo -> package name mappings
REPO_TO_PACKAGE = {
    # PyPI
    "pytorch": "torch",
    "scikit-learn": "scikit-learn",
    "tensorflow": "tensorflow",
    "numpy": "numpy",
    "pandas": "pandas",
    "requests": "requests",
    "flask": "flask",
    "django": "django",
    "fastapi": "fastapi",
    # npm
    "node": "node",
    # crates
    "rust": "rustc",
    # rubygems
    "rails": "rails",
}


def get_package_name_from_repo(owner: str, repo: str, languages: dict) -> Optional[str]:
    """
    Guess package name from repo.
    Often the repo name IS the package name.
    """
    pm = detect_package_manager(languages)
    if not pm:
        return None
    
    # Check known mappings first
    if repo.lower() in REPO_TO_PACKAGE:
        return REPO_TO_PACKAGE[repo.lower()]
    
    # Most common: package name = repo name
    # Try lowercase version too
    candidates = [repo, repo.lower(), repo.replace("-", "_")]
    
    for candidate in candidates:
        tree = fetch_dependencies(pm, candidate)
        if tree:
            return candidate
    
    return None
