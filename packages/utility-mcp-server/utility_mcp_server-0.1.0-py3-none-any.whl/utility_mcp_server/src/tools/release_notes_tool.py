"""Release notes generation tool for the Utility MCP Server.

This tool provides functionality to generate release notes from git commits
or tags in a structured markdown format similar to Feast release notes.
"""

import re
import subprocess
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from utility_mcp_server.utils.pylogger import get_python_logger

logger = get_python_logger()


def _run_git_command(cmd: List[str], cwd: Optional[str] = None) -> str:
    """Run a git command and return the output.

    Args:
        cmd: List of command arguments starting with 'git'
        cwd: Working directory for the command

    Returns:
        Command output as string

    Raises:
        subprocess.CalledProcessError: If command fails
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            cwd=cwd,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to run git command: {e.stderr}")
        raise


def _get_commits_between_tags(
    from_tag: Optional[str],
    to_tag: str,
    repo_path: Optional[str] = None,
) -> List[Dict[str, str]]:
    """Get commits between two git tags.

    Args:
        from_tag: Starting tag (None for all commits up to to_tag)
        to_tag: Ending tag
        repo_path: Path to git repository (None for current directory)

    Returns:
        List of commit dictionaries with hash, message, author, date
    """
    try:
        if from_tag:
            range_spec = f"{from_tag}..{to_tag}"
        else:
            range_spec = f"..{to_tag}"

        format_str = "%H|%s|%an|%ad"
        date_format = "%Y-%m-%d"
        cmd = [
            "git",
            "log",
            f"--format={format_str}",
            f"--date=format:{date_format}",
            range_spec,
        ]

        output = _run_git_command(cmd, cwd=repo_path)
        commits = []

        for line in output.split("\n"):
            if not line.strip():
                continue
            parts = line.split("|", 3)
            if len(parts) >= 4:
                commits.append(
                    {
                        "hash": parts[0],
                        "message": parts[1],
                        "author": parts[2],
                        "date": parts[3],
                    },
                )

        return commits
    except Exception as e:
        logger.error(f"Failed to get commits: {e}")
        return []


def _extract_pr_number(message: str) -> Optional[str]:
    """Extract PR number from commit message.

    Args:
        message: Commit message

    Returns:
        PR number as string or None
    """
    patterns = [
        r"#(\d+)",
        r"\(#(\d+)\)",
        r"PR\s*#(\d+)",
        r"pull/(\d+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, message)
        if match:
            return match.group(1)

    return None


def _extract_commit_hash(message: str, hash_str: str) -> Optional[str]:
    """Extract commit hash reference from message or use provided hash.

    Args:
        message: Commit message
        hash_str: Full commit hash

    Returns:
        Short commit hash or None
    """
    patterns = [
        r"\[([a-f0-9]{7,})\]",
        r"commit\s+([a-f0-9]{7,})",
    ]

    for pattern in patterns:
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            return match.group(1)

    return hash_str[:7] if hash_str else None


def _categorize_commit(message: str) -> Tuple[str, str]:
    """Categorize commit into type and category.

    Args:
        message: Commit message

    Returns:
        Tuple of (type, category) where type is 'feature', 'fix', 'breaking', etc.
    """
    message_lower = message.lower()

    type_keywords = {
        "feature": ["feat", "add", "new", "implement", "support"],
        "fix": ["fix", "bug", "resolve", "correct", "repair"],
        "breaking": ["breaking", "remove", "deprecate", "drop"],
        "enhancement": ["improve", "enhance", "update", "refactor", "optimize"],
        "docs": ["doc", "readme", "documentation"],
        "test": ["test", "spec"],
        "chore": ["chore", "ci", "build", "deps"],
    }

    category_keywords = {
        "ui/ux": ["ui", "ux", "interface", "dark mode", "theme", "visual"],
        "api": ["api", "endpoint", "route", "rest", "grpc"],
        "database": [
            "database",
            "db",
            "sql",
            "store",
            "storage",
            "dynamodb",
            "snowflake",
            "trino",
            "clickhouse",
        ],
        "cli": ["cli", "command", "cmd"],
        "kubernetes": ["k8s", "kubernetes", "operator", "pod", "deployment"],
        "integration": ["integration", "test", "ci/cd"],
        "configuration": ["config", "setting", "environment", "variable"],
        "materialization": ["materialization", "materialize"],
        "compute": ["compute", "spark", "dask", "engine"],
        "rag": ["rag", "retrieval", "ai", "mcp"],
        "architecture": ["architecture", "store", "registry", "server"],
    }

    commit_type = "enhancement"
    for type_name, keywords in type_keywords.items():
        if any(keyword in message_lower for keyword in keywords):
            commit_type = type_name
            break

    category = "general"
    for cat_name, keywords in category_keywords.items():
        if any(keyword in message_lower for keyword in keywords):
            category = cat_name
            break

    return commit_type, category


def _format_pr_link(pr_number: str, repo_url: str) -> str:
    """Format PR link in markdown.

    Args:
        pr_number: PR number
        repo_url: Repository URL

    Returns:
        Formatted PR link
    """
    return f"[#{pr_number}]({repo_url}/pull/{pr_number})"


def _format_commit_link(commit_hash: str, repo_url: str) -> str:
    """Format commit link in markdown.

    Args:
        commit_hash: Commit hash
        repo_url: Repository URL

    Returns:
        Formatted commit link
    """
    return f"[{commit_hash}]({repo_url}/commit/{commit_hash})"


def _generate_release_notes_section(
    title: str,
    description: str,
    items: List[Dict[str, str]],
    repo_url: Optional[str] = None,
) -> str:
    """Generate a release notes section.

    Args:
        title: Section title
        description: Section description
        items: List of items with 'title', 'description', 'pr', 'commit' keys
        repo_url: Repository URL for links

    Returns:
        Formatted markdown section
    """
    if not items:
        return ""

    section = f"### {title}\n{description}\n\n"
    section += "| Feature | Description | PR |\n"
    section += "|---------|-------------|-----|\n"

    for item in items:
        title_text = item.get("title", "")
        desc_text = item.get("description", "")
        pr_ref = item.get("pr")
        commit_ref = item.get("commit")

        pr_link = ""
        if pr_ref and repo_url:
            pr_link = _format_pr_link(pr_ref, repo_url)
        elif commit_ref and repo_url:
            pr_link = _format_commit_link(commit_ref, repo_url)

        section += f"| **{title_text}** | {desc_text} | {pr_link} |\n"

    return section + "\n"


def _generate_bug_fixes_section(
    title: str,
    description: str,
    items: List[Dict[str, str]],
    repo_url: Optional[str] = None,
) -> str:
    """Generate a bug fixes section.

    Args:
        title: Section title
        description: Section description
        items: List of items with 'title', 'description', 'pr', 'commit' keys
        repo_url: Repository URL for links

    Returns:
        Formatted markdown section
    """
    if not items:
        return ""

    section = f"### {title}\n{description}\n\n"
    section += "| Fix | Description | PR |\n"
    section += "|-----|-------------|-----|\n"

    for item in items:
        title_text = item.get("title", "")
        desc_text = item.get("description", "")
        pr_ref = item.get("pr")
        commit_ref = item.get("commit")

        pr_link = ""
        if pr_ref and repo_url:
            pr_link = _format_pr_link(pr_ref, repo_url)
        elif commit_ref and repo_url:
            pr_link = _format_commit_link(commit_ref, repo_url)

        section += f"| **{title_text}** | {desc_text} | {pr_link} |\n"

    return section + "\n"


def _generate_breaking_changes_section(
    items: List[Dict[str, str]],
    repo_url: Optional[str] = None,
) -> str:
    """Generate breaking changes section.

    Args:
        items: List of items with 'title', 'description', 'pr', 'impact' keys
        repo_url: Repository URL for links

    Returns:
        Formatted markdown section
    """
    if not items:
        return ""

    section = "### Breaking Changes\n"
    section += "| Change | Description | PR | Impact |\n"
    section += "|--------|-------------|-----|--------|\n"

    for item in items:
        title_text = item.get("title", "")
        desc_text = item.get("description", "")
        pr_ref = item.get("pr")
        impact = item.get("impact", "")

        pr_link = ""
        if pr_ref and repo_url:
            pr_link = _format_pr_link(pr_ref, repo_url)

        section += f"| **{title_text}** | {desc_text} | {pr_link} | {impact} |\n"

    return section + "\n"


async def generate_release_notes(
    version: str,
    previous_version: Optional[str] = None,
    repo_path: Optional[str] = None,
    repo_url: Optional[str] = None,
    release_date: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate release notes from git commits between tags.

    TOOL_NAME=generate_release_notes
    DISPLAY_NAME=Release Notes Generator
    USECASE=Generate structured release notes from git commits or tags
    INSTRUCTIONS=1. Provide version tag, 2. Optionally provide previous version tag, 3. Receive formatted release notes
    INPUT_DESCRIPTION=version (string): current version tag, previous_version (string, optional): previous version tag, repo_path (string, optional): path to git repo, repo_url (string, optional): repository URL for links, release_date (string, optional): release date in YYYY-MM-DD format
    OUTPUT_DESCRIPTION=Dictionary with status, release_notes markdown content, and statistics
    EXAMPLES=generate_release_notes("v0.50.0", "v0.49.0", repo_url="https://github.com/org/repo")
    PREREQUISITES=Git repository with tags
    RELATED_TOOLS=None - standalone release notes generation

    I/O-bound operation - uses async def for potential future API calls.

    Generates structured release notes in markdown format from git commits
    between two tags, categorizing them into features, bug fixes, breaking
    changes, etc.

    Args:
        version: Current version tag (e.g., "v0.50.0")
        previous_version: Previous version tag (e.g., "v0.49.0")
        repo_path: Path to git repository (None for current directory)
        repo_url: Repository URL for generating PR/commit links
        release_date: Release date in YYYY-MM-DD format (None for today)

    Returns:
        Dict[str, Any]: Dictionary containing release notes markdown and metadata
    """
    try:
        if not version:
            raise ValueError("Version is required")

        if not release_date:
            release_date = datetime.now().strftime("%B %d, %Y")

        logger.info(f"Generating release notes for version {version}")

        commits = _get_commits_between_tags(previous_version, version, repo_path)

        if not commits:
            logger.warning(f"No commits found between {previous_version} and {version}")

        features: List[Dict[str, str]] = []
        breaking_changes: List[Dict[str, str]] = []

        feature_categories: Dict[str, List[Dict[str, str]]] = {}
        enhancement_categories: Dict[str, List[Dict[str, str]]] = {}
        bug_fix_categories: Dict[str, List[Dict[str, str]]] = {}

        for commit in commits:
            message = commit["message"]
            pr_number = _extract_pr_number(message)
            commit_hash = _extract_commit_hash(message, commit["hash"])

            commit_type, category = _categorize_commit(message)

            title = message.split("\n")[0]
            if len(title) > 80:
                title = title[:77] + "..."

            item: dict[str, str] = {
                "title": title,
                "description": message.split("\n")[0],
                "pr": pr_number or "",
                "commit": commit_hash or "",
            }

            if commit_type == "breaking":
                item["impact"] = "**HIGH**: Review breaking changes before upgrading"
                breaking_changes.append(item)
            elif commit_type == "feature":
                if category not in feature_categories:
                    feature_categories[category] = []
                feature_categories[category].append(item)
            elif commit_type == "fix":
                if category not in bug_fix_categories:
                    bug_fix_categories[category] = []
                bug_fix_categories[category].append(item)
            else:
                if category not in enhancement_categories:
                    enhancement_categories[category] = []
                enhancement_categories[category].append(item)

        release_notes = f"# {version} Release Notes\n\n"
        release_notes += f"**Release Date:** {release_date}  \n"

        if previous_version:
            release_notes += f"**Previous Version:** {previous_version}  \n"

        if repo_url:
            release_notes += f"**Repository:** [{repo_url}]({repo_url})\n"

        release_notes += "\n---\n\n"

        if feature_categories or features:
            release_notes += "## 🎉 Major Features\n\n"

            category_descriptions = {
                "ui/ux": "Comprehensive user interface improvements bringing modern design and enhanced functionality.",
                "api": "API enhancements and new endpoints.",
                "database": "Database and storage improvements.",
                "cli": "Command-line interface enhancements.",
                "kubernetes": "Kubernetes and operator improvements.",
                "integration": "Integration and testing improvements.",
                "configuration": "Configuration and settings enhancements.",
                "materialization": "Materialization engine improvements.",
                "compute": "Compute engine updates.",
                "rag": "RAG and AI integration enhancements.",
                "architecture": "Architecture and infrastructure improvements.",
            }

            for category, items in sorted(feature_categories.items()):
                title = category.replace("_", " ").title()
                description = category_descriptions.get(
                    category, f"{title} improvements."
                )
                release_notes += _generate_release_notes_section(
                    title,
                    description,
                    items,
                    repo_url,
                )

        if enhancement_categories:
            release_notes += "## 🚀 Additional Enhancements\n\n"

            category_descriptions = {
                "cli": "Enhanced command-line interface and improved capabilities.",
                "configuration": "Enhanced configuration options for improved deployment flexibility.",
                "kubernetes": "Improved Kubernetes integration with enhanced operator capabilities.",
                "database": "Enhanced support for various database systems and storage engines.",
                "compute": "Improved compute capabilities for data processing.",
            }

            for category, items in sorted(enhancement_categories.items()):
                title = category.replace("_", " ").title()
                description = category_descriptions.get(
                    category, f"{title} enhancements."
                )
                release_notes += _generate_release_notes_section(
                    title,
                    description,
                    items,
                    repo_url,
                )

        if bug_fix_categories:
            release_notes += "## 🐛 Key Bug Fixes\n\n"

            category_descriptions = {
                "database": "Critical fixes for various database integrations.",
                "integration": "Test stability and integration improvements.",
                "api": "Fixes for API endpoints and configuration handling.",
                "ui": "User interface and dependency fixes.",
            }

            for category, items in sorted(bug_fix_categories.items()):
                title = category.replace("_", " ").title()
                description = category_descriptions.get(category, f"{title} fixes.")
                release_notes += _generate_bug_fixes_section(
                    title,
                    description,
                    items,
                    repo_url,
                )

        if breaking_changes:
            release_notes += "## 🔄 Breaking Changes\n\n"
            release_notes += _generate_breaking_changes_section(
                breaking_changes, repo_url
            )

        if previous_version and repo_url:
            release_notes += "## 🔗 Links and Resources\n\n"
            release_notes += f"- **Full Changelog**: [{previous_version}...{version}]({repo_url}/compare/{previous_version}...{version})\n"

        stats = {
            "total_commits": len(commits),
            "features": sum(len(items) for items in feature_categories.values()),
            "enhancements": sum(
                len(items) for items in enhancement_categories.values()
            ),
            "bug_fixes": sum(len(items) for items in bug_fix_categories.values()),
            "breaking_changes": len(breaking_changes),
        }

        release_notes += "\n## 📊 Release Statistics\n\n"
        release_notes += f"- **Total Commits**: {stats['total_commits']}\n"
        release_notes += f"- **New Features**: {stats['features']}\n"
        release_notes += f"- **Enhancements**: {stats['enhancements']}\n"
        release_notes += f"- **Bug Fixes**: {stats['bug_fixes']}\n"
        release_notes += f"- **Breaking Changes**: {stats['breaking_changes']}\n"

        return {
            "status": "success",
            "operation": "generate_release_notes",
            "version": version,
            "previous_version": previous_version,
            "release_notes": release_notes,
            "statistics": stats,
            "message": f"Successfully generated release notes for {version}",
        }

    except Exception as e:
        logger.error(f"Error in release notes tool: {e}")
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to generate release notes",
        }
