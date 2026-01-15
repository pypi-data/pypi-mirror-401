"""Tests for the release notes generation tool."""

import asyncio
import subprocess
from unittest.mock import Mock, patch

import pytest

from utility_mcp_server.src.tools.release_notes_tool import (
    _categorize_commit,
    _extract_commit_hash,
    _extract_pr_number,
    _format_commit_link,
    _format_pr_link,
    _generate_breaking_changes_section,
    _generate_bug_fixes_section,
    _generate_release_notes_section,
    _get_commits_between_tags,
    _run_git_command,
    generate_release_notes,
)


class TestRunGitCommand:
    """Tests for _run_git_command function."""

    @patch("utility_mcp_server.src.tools.release_notes_tool.subprocess.run")
    def test_run_git_command_success(self, mock_run):
        """Test successful git command execution."""
        mock_run.return_value = Mock(stdout="output\n", returncode=0)

        result = _run_git_command(["git", "status"])

        assert result == "output"
        mock_run.assert_called_once()

    @patch("utility_mcp_server.src.tools.release_notes_tool.subprocess.run")
    def test_run_git_command_with_cwd(self, mock_run):
        """Test git command with working directory."""
        mock_run.return_value = Mock(stdout="output\n", returncode=0)

        result = _run_git_command(["git", "log"], cwd="/path/to/repo")

        mock_run.assert_called_once()
        call_kwargs = mock_run.call_args[1]
        assert call_kwargs["cwd"] == "/path/to/repo"

    @patch("utility_mcp_server.src.tools.release_notes_tool.subprocess.run")
    def test_run_git_command_failure(self, mock_run):
        """Test git command failure."""
        mock_run.side_effect = subprocess.CalledProcessError(
            1, "git", stderr="error message"
        )

        with pytest.raises(subprocess.CalledProcessError):
            _run_git_command(["git", "invalid"])


class TestGetCommitsBetweenTags:
    """Tests for _get_commits_between_tags function."""

    @patch("utility_mcp_server.src.tools.release_notes_tool._run_git_command")
    def test_get_commits_with_both_tags(self, mock_run):
        """Test getting commits between two tags."""
        mock_run.return_value = "abc123|feat: add feature|Author|2024-01-01"

        commits = _get_commits_between_tags("v0.1.0", "v0.2.0")

        assert len(commits) == 1
        assert commits[0]["hash"] == "abc123"
        assert commits[0]["message"] == "feat: add feature"
        assert commits[0]["author"] == "Author"
        assert commits[0]["date"] == "2024-01-01"

    @patch("utility_mcp_server.src.tools.release_notes_tool._run_git_command")
    def test_get_commits_without_from_tag(self, mock_run):
        """Test getting commits up to a tag."""
        mock_run.return_value = "abc123|initial commit|Author|2024-01-01"

        commits = _get_commits_between_tags(None, "v0.1.0")

        assert len(commits) == 1

    @patch("utility_mcp_server.src.tools.release_notes_tool._run_git_command")
    def test_get_commits_multiple(self, mock_run):
        """Test getting multiple commits."""
        mock_run.return_value = (
            "abc123|feat: feature 1|Author1|2024-01-01\n"
            "def456|fix: bug fix|Author2|2024-01-02\n"
            "ghi789|docs: update readme|Author3|2024-01-03"
        )

        commits = _get_commits_between_tags("v0.1.0", "v0.2.0")

        assert len(commits) == 3
        assert commits[0]["message"] == "feat: feature 1"
        assert commits[1]["message"] == "fix: bug fix"
        assert commits[2]["message"] == "docs: update readme"

    @patch("utility_mcp_server.src.tools.release_notes_tool._run_git_command")
    def test_get_commits_empty(self, mock_run):
        """Test when no commits found."""
        mock_run.return_value = ""

        commits = _get_commits_between_tags("v0.1.0", "v0.2.0")

        assert commits == []

    @patch("utility_mcp_server.src.tools.release_notes_tool._run_git_command")
    def test_get_commits_error(self, mock_run):
        """Test error handling when git command fails."""
        mock_run.side_effect = Exception("Git error")

        commits = _get_commits_between_tags("v0.1.0", "v0.2.0")

        assert commits == []


class TestExtractPrNumber:
    """Tests for _extract_pr_number function."""

    def test_extract_pr_hash_format(self):
        """Test extracting PR number with # format."""
        assert _extract_pr_number("feat: add feature #123") == "123"

    def test_extract_pr_parenthesis_format(self):
        """Test extracting PR number with (#num) format."""
        assert _extract_pr_number("feat: add feature (#456)") == "456"

    def test_extract_pr_pr_prefix(self):
        """Test extracting PR number with PR# prefix."""
        assert _extract_pr_number("feat: add feature PR#789") == "789"
        assert _extract_pr_number("feat: add feature PR #789") == "789"

    def test_extract_pr_pull_format(self):
        """Test extracting PR number from pull/num format."""
        assert _extract_pr_number("Merge pull/123 from branch") == "123"

    def test_extract_pr_no_match(self):
        """Test when no PR number found."""
        assert _extract_pr_number("feat: add feature") is None

    def test_extract_pr_multiple_numbers(self):
        """Test that first PR number is extracted."""
        assert _extract_pr_number("feat: #123 and #456") == "123"


class TestExtractCommitHash:
    """Tests for _extract_commit_hash function."""

    def test_extract_hash_bracket_format(self):
        """Test extracting hash from [hash] format."""
        assert (
            _extract_commit_hash("[abc1234] commit message", "full_hash") == "abc1234"
        )

    def test_extract_hash_commit_keyword(self):
        """Test extracting hash with commit keyword."""
        assert (
            _extract_commit_hash("commit abc1234def message", "full_hash")
            == "abc1234def"
        )

    def test_extract_hash_fallback(self):
        """Test fallback to provided hash."""
        result = _extract_commit_hash("no hash here", "abc1234567890")
        assert result == "abc1234"

    def test_extract_hash_empty_hash(self):
        """Test with empty hash string."""
        result = _extract_commit_hash("no hash here", "")
        assert result is None


class TestCategorizeCommit:
    """Tests for _categorize_commit function."""

    def test_categorize_feature(self):
        """Test categorizing feature commits."""
        commit_type, _ = _categorize_commit("feat: add new feature")
        assert commit_type == "feature"

        commit_type, _ = _categorize_commit("Add new functionality")
        assert commit_type == "feature"

    def test_categorize_fix(self):
        """Test categorizing fix commits."""
        commit_type, _ = _categorize_commit("fix: resolve bug")
        assert commit_type == "fix"

        commit_type, _ = _categorize_commit("Bug fix for issue")
        assert commit_type == "fix"

    def test_categorize_breaking(self):
        """Test categorizing breaking changes."""
        commit_type, _ = _categorize_commit("breaking: remove deprecated api")
        assert commit_type == "breaking"

    def test_categorize_enhancement(self):
        """Test categorizing enhancements."""
        commit_type, _ = _categorize_commit("improve performance")
        assert commit_type == "enhancement"

        commit_type, _ = _categorize_commit("refactor code structure")
        assert commit_type == "enhancement"

    def test_categorize_docs(self):
        """Test categorizing documentation commits."""
        commit_type, _ = _categorize_commit("documentation changes")
        assert commit_type == "docs"

        commit_type, _ = _categorize_commit("readme edits")
        assert commit_type == "docs"

    def test_categorize_category_api(self):
        """Test categorizing api-related commits."""
        _, category = _categorize_commit("feat: add api endpoint")
        assert category == "api"

    def test_categorize_category_database(self):
        """Test categorizing database-related commits."""
        _, category = _categorize_commit("fix: database connection issue")
        assert category == "database"

    def test_categorize_category_kubernetes(self):
        """Test categorizing kubernetes-related commits."""
        _, category = _categorize_commit("feat: add k8s operator")
        assert category == "kubernetes"

    def test_categorize_default(self):
        """Test default categorization."""
        commit_type, category = _categorize_commit("random commit message")
        assert commit_type == "enhancement"
        assert category == "general"


class TestFormatLinks:
    """Tests for link formatting functions."""

    def test_format_pr_link(self):
        """Test PR link formatting."""
        link = _format_pr_link("123", "https://github.com/org/repo")
        assert link == "[#123](https://github.com/org/repo/pull/123)"

    def test_format_commit_link(self):
        """Test commit link formatting."""
        link = _format_commit_link("abc1234", "https://github.com/org/repo")
        assert link == "[abc1234](https://github.com/org/repo/commit/abc1234)"


class TestGenerateSections:
    """Tests for section generation functions."""

    def test_generate_release_notes_section(self):
        """Test release notes section generation."""
        items = [
            {
                "title": "Feature 1",
                "description": "Description 1",
                "pr": "123",
                "commit": "abc1234",
            }
        ]

        section = _generate_release_notes_section(
            "New Features",
            "New features in this release.",
            items,
            "https://github.com/org/repo",
        )

        assert "### New Features" in section
        assert "New features in this release." in section
        assert "| Feature | Description | PR |" in section
        assert "Feature 1" in section
        assert "[#123]" in section

    def test_generate_release_notes_section_empty(self):
        """Test section generation with empty items."""
        section = _generate_release_notes_section(
            "Empty", "No items.", [], "https://github.com/org/repo"
        )

        assert section == ""

    def test_generate_release_notes_section_commit_fallback(self):
        """Test section uses commit link when no PR."""
        items = [
            {"title": "Feature", "description": "Desc", "pr": None, "commit": "abc1234"}
        ]

        section = _generate_release_notes_section(
            "Features", "Desc.", items, "https://github.com/org/repo"
        )

        assert "[abc1234]" in section

    def test_generate_bug_fixes_section(self):
        """Test bug fixes section generation."""
        items = [
            {"title": "Fix 1", "description": "Fixed bug", "pr": "456", "commit": None}
        ]

        section = _generate_bug_fixes_section(
            "Bug Fixes",
            "Bug fixes in this release.",
            items,
            "https://github.com/org/repo",
        )

        assert "### Bug Fixes" in section
        assert "| Fix | Description | PR |" in section
        assert "Fix 1" in section

    def test_generate_bug_fixes_section_empty(self):
        """Test bug fixes section with empty items."""
        section = _generate_bug_fixes_section(
            "Bug Fixes", "No fixes.", [], "https://github.com/org/repo"
        )

        assert section == ""

    def test_generate_breaking_changes_section(self):
        """Test breaking changes section generation."""
        items = [
            {
                "title": "Breaking Change",
                "description": "Removed API",
                "pr": "789",
                "impact": "HIGH",
            }
        ]

        section = _generate_breaking_changes_section(
            items, "https://github.com/org/repo"
        )

        assert "### Breaking Changes" in section
        assert "| Change | Description | PR | Impact |" in section
        assert "Breaking Change" in section
        assert "HIGH" in section

    def test_generate_breaking_changes_section_empty(self):
        """Test breaking changes section with empty items."""
        section = _generate_breaking_changes_section([], "https://github.com/org/repo")

        assert section == ""


class TestGenerateReleaseNotes:
    """Tests for the main generate_release_notes function."""

    @patch("utility_mcp_server.src.tools.release_notes_tool._get_commits_between_tags")
    def test_generate_release_notes_success(self, mock_get_commits):
        """Test successful release notes generation."""
        mock_get_commits.return_value = [
            {
                "hash": "abc1234567890",
                "message": "feat: add new feature (#123)",
                "author": "Author",
                "date": "2024-01-01",
            },
            {
                "hash": "def4567890123",
                "message": "fix: bug fix (#456)",
                "author": "Author2",
                "date": "2024-01-02",
            },
        ]

        result = asyncio.run(
            generate_release_notes(
                version="v0.2.0",
                previous_version="v0.1.0",
                repo_url="https://github.com/org/repo",
                release_date="January 15, 2024",
            )
        )

        assert result["status"] == "success"
        assert result["operation"] == "generate_release_notes"
        assert result["version"] == "v0.2.0"
        assert result["previous_version"] == "v0.1.0"
        assert "release_notes" in result
        assert "statistics" in result
        assert "# v0.2.0 Release Notes" in result["release_notes"]
        assert "January 15, 2024" in result["release_notes"]

    @patch("utility_mcp_server.src.tools.release_notes_tool._get_commits_between_tags")
    def test_generate_release_notes_no_previous(self, mock_get_commits):
        """Test release notes without previous version."""
        mock_get_commits.return_value = []

        result = asyncio.run(generate_release_notes(version="v0.1.0"))

        assert result["status"] == "success"
        assert result["previous_version"] is None

    def test_generate_release_notes_no_version(self):
        """Test error when no version provided."""
        result = asyncio.run(generate_release_notes(version=""))

        assert result["status"] == "error"
        assert "Version is required" in result["error"]

    @patch("utility_mcp_server.src.tools.release_notes_tool._get_commits_between_tags")
    def test_generate_release_notes_empty_commits(self, mock_get_commits):
        """Test release notes with no commits."""
        mock_get_commits.return_value = []

        result = asyncio.run(
            generate_release_notes(version="v0.2.0", previous_version="v0.1.0")
        )

        assert result["status"] == "success"
        assert result["statistics"]["total_commits"] == 0

    @patch("utility_mcp_server.src.tools.release_notes_tool._get_commits_between_tags")
    def test_generate_release_notes_with_breaking_changes(self, mock_get_commits):
        """Test release notes with breaking changes."""
        mock_get_commits.return_value = [
            {
                "hash": "abc1234567890",
                "message": "breaking: remove deprecated API (#123)",
                "author": "Author",
                "date": "2024-01-01",
            }
        ]

        result = asyncio.run(
            generate_release_notes(
                version="v1.0.0",
                previous_version="v0.9.0",
                repo_url="https://github.com/org/repo",
            )
        )

        assert result["status"] == "success"
        assert result["statistics"]["breaking_changes"] == 1
        assert "Breaking Changes" in result["release_notes"]

    @patch("utility_mcp_server.src.tools.release_notes_tool._get_commits_between_tags")
    def test_generate_release_notes_default_date(self, mock_get_commits):
        """Test release notes uses current date when not provided."""
        mock_get_commits.return_value = []

        result = asyncio.run(generate_release_notes(version="v0.1.0"))

        assert result["status"] == "success"
        assert "Release Date:" in result["release_notes"]

    @patch("utility_mcp_server.src.tools.release_notes_tool._get_commits_between_tags")
    def test_generate_release_notes_statistics(self, mock_get_commits):
        """Test release notes statistics calculation."""
        mock_get_commits.return_value = [
            {
                "hash": "a" * 40,
                "message": "feat: feature",
                "author": "A",
                "date": "2024-01-01",
            },
            {
                "hash": "b" * 40,
                "message": "fix: bug",
                "author": "B",
                "date": "2024-01-02",
            },
            {
                "hash": "c" * 40,
                "message": "improve: enhance",
                "author": "C",
                "date": "2024-01-03",
            },
        ]

        result = asyncio.run(
            generate_release_notes(version="v0.2.0", previous_version="v0.1.0")
        )

        assert result["status"] == "success"
        assert result["statistics"]["total_commits"] == 3

    @patch("utility_mcp_server.src.tools.release_notes_tool._get_commits_between_tags")
    def test_generate_release_notes_with_repo_url(self, mock_get_commits):
        """Test release notes includes repo URL."""
        mock_get_commits.return_value = []

        result = asyncio.run(
            generate_release_notes(
                version="v0.2.0",
                previous_version="v0.1.0",
                repo_url="https://github.com/org/repo",
            )
        )

        assert result["status"] == "success"
        assert "https://github.com/org/repo" in result["release_notes"]
        assert "Full Changelog" in result["release_notes"]

    @patch("utility_mcp_server.src.tools.release_notes_tool._get_commits_between_tags")
    def test_generate_release_notes_long_commit_message(self, mock_get_commits):
        """Test handling of long commit messages."""
        long_message = "feat: " + "a" * 100 + " (#123)"
        mock_get_commits.return_value = [
            {
                "hash": "abc1234567890",
                "message": long_message,
                "author": "Author",
                "date": "2024-01-01",
            }
        ]

        result = asyncio.run(generate_release_notes(version="v0.2.0"))

        assert result["status"] == "success"

    @patch("utility_mcp_server.src.tools.release_notes_tool._get_commits_between_tags")
    def test_generate_release_notes_exception_handling(self, mock_get_commits):
        """Test exception handling in release notes generation."""
        mock_get_commits.side_effect = Exception("Unexpected error")

        result = asyncio.run(
            generate_release_notes(version="v0.2.0", previous_version="v0.1.0")
        )

        assert result["status"] == "error"
        assert "Failed to generate release notes" in result["message"]
