"""Tests that every tool is properly listed on the homepage and has required files."""
import pathlib
import re

import pytest

root = pathlib.Path(__file__).parent.parent.absolute()


def get_tool_files():
    """Return list of tool HTML files (everything except index.html)."""
    return sorted(f.stem for f in root.glob("*.html") if f.name != "index.html")


def get_readme_links():
    """Extract tool slugs linked in README.md's Tools section."""
    readme = (root / "README.md").read_text()
    # Only look at content before the HTML comment marker
    marker = "<!-- New tools should be added"
    if marker in readme:
        readme = readme[:readme.index(marker)]
    # Match markdown links like [Tool Name](tool-slug)
    return re.findall(r"\[.*?\]\(([a-z0-9-]+)\)", readme)


@pytest.fixture(scope="module")
def tool_files():
    return get_tool_files()


@pytest.fixture(scope="module")
def readme_links():
    return get_readme_links()


@pytest.mark.parametrize("tool", get_tool_files())
def test_tool_listed_in_readme(tool, readme_links):
    """Every tool HTML file must have a corresponding link in README.md."""
    assert tool in readme_links, (
        f"{tool}.html exists but is not listed in README.md. "
        f"Add a line like: - [{tool}]({tool}) short description"
    )


@pytest.mark.parametrize("tool", get_tool_files())
def test_tool_has_docs(tool):
    """Every tool must have a .docs.md file."""
    docs_file = root / f"{tool}.docs.md"
    assert docs_file.exists(), (
        f"{tool}.html exists but {tool}.docs.md is missing."
    )


def test_no_dead_readme_links(tool_files, readme_links):
    """Every tool linked in README.md must have a corresponding HTML file."""
    for link in readme_links:
        assert link in tool_files, (
            f"README.md links to ({link}) but {link}.html does not exist."
        )
