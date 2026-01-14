This file is a merged representation of a subset of the codebase, containing specifically included files, combined into a single document by Repomix.

# File Summary

## Purpose
This file contains a packed representation of a subset of the repository's contents that is considered the most important context.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Only files matching these patterns are included: **/**
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
src/
  specbook/
    core/
      __init__.py
      finder.py
      models.py
      server.py
    ui/
      web/
        templates/
          index.html
        __init__.py
        app.py
      __init__.py
      console.py
    __init__.py
    __main__.py
    cli.py
tests/
  integration/
    __init__.py
    test_cli.py
    test_web.py
  unit/
    __init__.py
    test_finder.py
    test_server.py
  __init__.py
  conftest.py
.gitignore
LICENSE
pyproject.toml
README.md
```

# Files

## File: src/specbook/core/__init__.py
````python
"""Core business logic for specbook."""
````

## File: src/specbook/core/finder.py
````python
"""project root finder implementation"""

from pathlib import Path

from specbook.core.models import ProjectRoot, SearchResult


def find_project_root(start_path: Path) -> SearchResult:
    """Find the Specbook project root by searching upward from start_path:
    Looks for directories containing .specify/ or specs/ markers.

    Args:
        start_path: directory to start searching from.

    Returns:
        SearchResult with found=True if a project root was discovered
    """
    current = start_path.resolve()
    searched_from = current

    while True:
        has_specify = (current / ".specify").is_dir()
        has_specs = (current / "specs").is_dir()

        if has_specify or has_specs:
            return SearchResult(
                found=True,
                project_root=ProjectRoot(
                    path=current,
                    has_specify_dir=has_specify,
                    has_specs_dir=has_specs,
                ),
                searched_from=searched_from,
                searched_to=current,
            )

        # check if we've reached the filesystem root
        parent = current.parent
        if parent == current:
            # at root, one final check 
            return SearchResult(
                found=False,
                project_root=None,
                searched_from=searched_from,
                searched_to=current,
            )

        current = parent
````

## File: src/specbook/core/server.py
````python
"""Server management utilities for specbook web server."""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

import psutil

from specbook.core.models import ServerConfig, ServerState, ServerStatus


def find_process_on_port(port: int) -> psutil.Process | None:
    """find process listening on the given port; returns the Process object if found (else None)"""
    for proc in psutil.process_iter():
        try:
            for conn in proc.net_connections(kind="inet"):
                if conn.laddr and hasattr(conn.laddr, "port"):
                    if conn.laddr.port == port and conn.status == "LISTEN":
                        return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # skip processes we can't read (e.g. other users' processes)
            continue
    return None


def is_specbook_process(proc: psutil.Process) -> bool:
    """check if process is a specbook server"""
    try:
        cmdline = " ".join(proc.cmdline())
        return "specbook" in cmdline  # look for 'specbook' in the argument
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False


def get_project_root_from_process(proc: psutil.Process) -> Path | None:
    """extract project root from specbook server process command line"""
    try:
        cmdline = proc.cmdline()
        # look for the project root path argument (last argument after port)
        for i, arg in enumerate(cmdline):
            if arg == "--project-root" and i + 1 < len(cmdline):
                return Path(cmdline[i + 1])
        # fallback: check if last arg is a valid path
        if cmdline and Path(cmdline[-1]).is_dir():
            return Path(cmdline[-1])
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass
    return None


def get_server_status(port: int) -> ServerStatus:
    """Get the status of a server on a specific port.

    Returns ServerStatus with appropriate state:
        - RUNNING: specbook server is active on the port
        - STOPPED: no process is listening on the port
        - PORT_CONFLICT: non-specbook process is using the port
    """
    proc = find_process_on_port(port)

    if proc is None:
        return ServerStatus(
            port=port,
            state=ServerState.STOPPED,
            pid=None,
            project_root=None,
        )

    if is_specbook_process(proc):
        project_root = get_project_root_from_process(proc)
        return ServerStatus(
            port=port,
            state=ServerState.RUNNING,
            pid=proc.pid,
            project_root=project_root,
        )

    # some other process is using the port
    return ServerStatus(
        port=port,
        state=ServerState.PORT_CONFLICT,
        pid=proc.pid,
        project_root=None,
    )


def start_server(config: ServerConfig) -> int:
    """Start the specbook web server detached/in the background.

    Args:
        config: server configuration with port and project root

    Returns:
        PID of the spawned server process
    """
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "specbook.ui.web.app",
            str(config.port),
            str(config.project_root),
        ],
        start_new_session=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    # give the server a moment to start
    time.sleep(0.5)
    return proc.pid


def stop_server(port: int) -> bool:
    """Stop a specbook server running on the given port.

    Args:
        port: Port the server is listening on.

    Returns:
        True if server was stopped, False if no server was running
    """
    proc = find_process_on_port(port)
    if proc is None:
        return False

    if not is_specbook_process(proc):
        return False

    try:
        proc.terminate()
        proc.wait(timeout=5)
        return True
    except (psutil.NoSuchProcess, psutil.TimeoutExpired):
        # try again, this time harder
        try:
            proc.kill()
            return True
        except psutil.NoSuchProcess:
            return True


def open_browser(url: str) -> bool:
    """Open URL in the default browser.

    Args:
        url: URL to open

    Returns:
        True if browser was launched successfully
    """
    try:
        return webbrowser.open(url)
    except Exception:
        return False
````

## File: src/specbook/ui/web/templates/index.html
````html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Specbook</title>
    <style>

        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
       
        :root {

            /* fonts */
            --font-sans: 'Plus Jakarta Sans', -apple-system, sans-serif;
            --font-mono: 'JetBrains Mono', monospace;

            /* font sizes */
            --text-xs: 0.75rem;    /* ~12px for timestamps, labels, chips */
            --text-sm: 0.875rem;   /* ~14px for secondary text */
            --text-base: 1rem;     /* ~16px for body text */
            --text-lg: 1.125rem;   /* ~18px for emphasis and h4 rendering */
            --text-xl: 1.25rem;    /* ~20px for h3 and section headers */
            --text-2xl: 1.5rem;    /* ~24px for h2 and section/page titles */
            --text-3xl: 1.875rem;  /* ~30px for h1 */
            
            /* Font weights */
            --font-normal: 400;
            --font-medium: 500;
            --font-semibold: 600;
            --font-bold: 700;
            
            /* Line heights */
            --leading-tight: 1.25;
            --leading-normal: 1.5;
            --leading-relaxed: 1.625;
            
            /* primary (teal) */
            --color-primary: #0d9488;
            --color-primary-light: #5eead4;
            --color-primary-dim: #134e4a;

            /* secondary (lavender) */
            --color-secondary: #8a86a3;
            --color-secondary-light: #c4c1d4;
            --color-secondary-dim: #6e6a82;

            /* darks */
            --color-bg: #1a1f2e;
            --color-surface: #262c3a;
            --color-surface-raised: #323a4a;

            /* whites */
            --color-text: #eef0f4;
            --color-text-muted: #8b92a8;

            /* borders */
            --color-border: #3b4252;
            --color-border-light: #4a5568;
        }
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: var(--font-sans);
            font-size: var(--text-base);
            line-height: var(--leading-normal);
            color: var(--color-text);
            background-color: var(--color-bg);
            padding: 2rem;
            letter-spacing: 0.01em; /* improves readability a bit */
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: var(--color-surface);
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }
        header {
            background: var(--color-primary-dim);
            color: var(--color-text);
            padding: 1.0rem 1.5rem;
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.75rem;
        }
        header img {
            height: 1.75rem;
            width: auto;
        }
        header h1 {
            font-size: var(--text-xl);
            font-weight: var(--font-semibold);
            margin: 0;
        }
        .layout {
            display: flex;
            height: calc(100vh - 200px);
        }
        .sidebar {
            width: 280px;
            background: var(--color-surface-raised);
            border-right: 1px solid var(--color-border);
            overflow-y: auto;
            display: flex;
            flex-direction: column;
        }
        .sidebar-header {
            padding: 1rem;
            border-bottom: 1px solid var(--color-border);
            flex-shrink: 0;
        }
        .sidebar-header h2 {
            font-size: var(--text-sm);
            font-weight: var(--font-semibold);
            margin: 0;
        }
        .main-content {
            flex: 1;
            overflow-y: auto;
            padding: 1.5rem 2rem;
        }
        .spec-list {
            list-style: none;
            padding: 0.5rem 0;
        }
        .spec-list li {
            font-size: var(--text-sm);
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--color-border);
            cursor: pointer;
            transition: background-color 0.2s ease;
        }
        .spec-list li:hover {
            background-color: var(--color-surface);
        }
        .spec-list li:last-child {
            border-bottom: none;
        }
        .spec-list li::before {
            content: "\2022";
            color: var(--color-primary-light);
            font-weight: bold;
            display: inline-block;
            width: 1em;
            margin-right: 0.5rem;
        }
        .spec-list > li {
            font-weight: var(--font-medium);
        }
        .spec-list > li + ul {
            display: none;
        }
        .spec-list > li.expanded + ul {
            display: block;
        }
        .spec-list li[data-level="1"] {
            padding-left: 2rem;
            font-size: var(--text-xs);
            color: var(--color-text-muted);
            border-bottom: none;
        }
        .empty-state {
            text-align: center;
            padding: 2rem;
            color: var(--color-text-muted);
        }
        .empty-state p {
            margin-bottom: 1rem;
        }
        .empty-state code {
            background: var(--color-surface-raised);
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-family: var(--font-mono);
            font-size: var(--text-xs);
        }
        h1 {
            font-size: var(--text-3xl);
            font-weight: var(--font-bold);
            line-height: var(--leading-tight);
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            color: var(--color-text);
        }
        h2 {
            font-size: var(--text-2xl);
            font-weight: var(--font-bold);
            line-height: var(--leading-tight);
            margin-top: 1.25rem;
            margin-bottom: 0.875rem;
            color: var(--color-text);
        }
        h3 {
            font-size: var(--text-xl);
            font-weight: var(--font-semibold);
            line-height: var(--leading-tight);
            margin-top: 1rem;
            margin-bottom: 0.75rem;
            color: var(--color-text);
        }
        h4 {
            font-size: var(--text-lg);
            font-weight: var(--font-semibold);
            line-height: var(--leading-tight);
            margin-top: 0.875rem;
            margin-bottom: 0.625rem;
            color: var(--color-text);
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <img src="/static/specbook_leaf_white.png" alt="Specbook logo">
            <h1>Specbook</h1>
        </header>
        <div class="layout">
            <aside class="sidebar" id="sidebar">
                <div class="sidebar-header">
                    <h2>Documements</h2>
                </div>
                <div class="sidebar-content">
                    {% if specs %}
                    <ul class="spec-list">
                        {% for spec in specs %}
                        <li>{{ spec.name }}</li>
                            <ul>
                                <!-- placeholder / example -->
                                <li data-level="1">one</li>
                                <li data-level="1">two</li>
                                <li data-level="1">three</li>
                            </ul>
                        {% endfor %}
                    </ul>
                    {% else %}
                    <div style="padding: 1rem; color: var(--color-text-muted); text-align: center;">
                        <p>No specifications found</p>
                    </div>
                    {% endif %}
                </div>
            </aside>
            <main class="main-content">
                <div class="empty-state">
                    <p>Select a specification to view details</p>
                </div>
            </main>
        </div>
    </div>
    <script>
        // expand/collapse spec list items
        document.querySelectorAll('.spec-list > li').forEach(item => {
            item.addEventListener('click', (e) => {
                e.stopPropagation();
                const sibling = item.nextElementSibling;
                if (sibling && sibling.tagName === 'UL') {
                    // close any other open lists
                    document.querySelectorAll('.spec-list > li.expanded').forEach(other => {
                        if (other !== item) other.classList.remove('expanded');
                    });
                    // toggle current
                    item.classList.toggle('expanded');
                }
            });
        });
    </script>
</body>
</html>
````

## File: src/specbook/ui/web/__init__.py
````python
"""web UI components for specbook"""
````

## File: src/specbook/ui/web/app.py
````python
"""Starlette web application for specbook spec viewer"""

import sys
from pathlib import Path

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from specbook.core.models import SpecListing

# templates and static dir relative to this file
TEMPLATES_DIR = Path(__file__).parent / "templates"
STATIC_DIR = Path(__file__).parent / "static"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# global project root (set by create_app or main)
_project_root: Path | None = None


async def index(request: Request) -> HTMLResponse:
    """render the spec listing page"""
    if _project_root is None:
        return HTMLResponse("Server not configured", status_code=500)

    listing = SpecListing.from_project(_project_root)
    return templates.TemplateResponse(
        request,
        "index.html",
        {"specs": listing.specs},
    )


def create_app(project_root: Path) -> Starlette:
    """Create a Starlette application for the given project.

    Args:
        project_root: path to the project root directory

    Returns:
        configured Starlette application
    """
    global _project_root
    _project_root = project_root

    routes = [
        Route("/", index),
        Mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static"),
    ]
    return Starlette(routes=routes)


def run_server(port: int, project_root: Path) -> None:
    """run the uvicorn server (called when the module is run directly as a subprocess)"""
    import uvicorn

    global _project_root
    _project_root = project_root

    app = create_app(project_root)
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        # show usage
        print("Usage: python -m specbook.ui.web.app <port> <project_root>")
        sys.exit(1)

    port = int(sys.argv[1])
    project_root = Path(sys.argv[2])
    run_server(port, project_root)
````

## File: src/specbook/ui/__init__.py
````python
"""UI components and console helpers for specbook."""
````

## File: src/specbook/__init__.py
````python
"""Specbook CLI - specification-driven development tool."""

__version__ = "0.1.0"
````

## File: tests/integration/__init__.py
````python
"""Integration tests for specbook."""
````

## File: tests/integration/test_web.py
````python
"""Integration tests for the web server."""

from pathlib import Path

import pytest
from starlette.testclient import TestClient


class TestWebApp:
    """integration tests for the Starlette web app"""

    def test_index_returns_html_with_header(self, project_with_specs: Path) -> None:
        """web app returns HTML with Specbook header"""
        # avoid import errors if app not yet created
        from specbook.ui.web.app import create_app

        app = create_app(project_with_specs)
        client = TestClient(app)

        response = client.get("/")

        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "Specbook" in response.text

    def test_index_lists_spec_directories(self, project_with_specs: Path) -> None:
        """web app lists spec directories from project"""
        from specbook.ui.web.app import create_app

        # create some spec directories
        (project_with_specs / "specs" / "001-feature-a").mkdir()
        (project_with_specs / "specs" / "002-feature-b").mkdir()

        app = create_app(project_with_specs)
        client = TestClient(app)

        response = client.get("/")

        assert response.status_code == 200
        assert "001-feature-a" in response.text
        assert "002-feature-b" in response.text

    def test_index_shows_empty_state(self, project_with_specs: Path) -> None:
        """Web app shows empty state when no specs exist."""
        from specbook.ui.web.app import create_app

        app = create_app(project_with_specs)
        client = TestClient(app)

        response = client.get("/")

        assert response.status_code == 200
        assert "No specifications found" in response.text
````

## File: tests/unit/__init__.py
````python
"""Unit tests for specbook."""
````

## File: tests/unit/test_finder.py
````python
"""Unit tests for project root finder."""

from pathlib import Path

import pytest

from specbook.core.finder import find_project_root


class TestFindProjectRootHappyPath:
    """tests for successful project root discovery."""

    def test_finds_project_from_root(self, project_with_both: Path) -> None:
        """should find project when searching from project root"""
        result = find_project_root(project_with_both)

        assert result.found is True
        assert result.project_root is not None
        # resolve both paths to handle macOS /var -> /private/var symlink
        assert result.project_root.path.resolve() == project_with_both.resolve()
        assert result.project_root.has_specify_dir is True
        assert result.project_root.has_specs_dir is True

    def test_finds_project_from_subdirectory(self, nested_subdir: Path) -> None:
        """should find project when searching from nested subdirectory"""
        result = find_project_root(nested_subdir)

        assert result.found is True
        assert result.project_root is not None
        # project root is the parent, not the nested subdir
        # resolve both paths to handle macOS /var -> /private/var symlink
        expected_root = nested_subdir.parent.parent.parent.resolve()
        assert result.project_root.path.resolve() == expected_root
        assert result.searched_from.resolve() == nested_subdir.resolve()


class TestFindProjectRootNotFound:
    """Tests for when no project root exists."""

    def test_not_found_returns_false(self, temp_dir: Path) -> None:
        """Should return found=False when no markers exist."""
        result = find_project_root(temp_dir)

        assert result.found is False
        assert result.project_root is None
        # resolve to handle macOS /var -> /private/var symlink
        assert result.searched_from.resolve() == temp_dir.resolve()
        # searched_to should be filesystem root
        assert result.searched_to == Path("/")

    def test_error_message_when_not_found(self, temp_dir: Path) -> None:
        """should provide helpful error message when not found"""
        result = find_project_root(temp_dir)

        assert result.error_message is not None
        assert "No spec-driven development project" in result.error_message
        assert str(temp_dir) in result.error_message
        assert ".specify/ or specs/" in result.error_message


class TestFindProjectRootOnlySpecify:
    """tests for projects with only .specify/ dir"""

    def test_finds_with_only_specify_dir(self, project_with_specify: Path) -> None:
        """should find project with only .specify/ marker."""
        result = find_project_root(project_with_specify)

        assert result.found is True
        assert result.project_root is not None
        assert result.project_root.has_specify_dir is True
        assert result.project_root.has_specs_dir is False
        assert result.project_root.markers == [".specify/"]


class TestFindProjectRootOnlySpecs:
    """tests for projects with only specs/ directory"""

    def test_finds_with_only_specs_dir(self, project_with_specs: Path) -> None:
        """should find project with only specs/ marker"""
        result = find_project_root(project_with_specs)

        assert result.found is True
        assert result.project_root is not None
        assert result.project_root.has_specify_dir is False
        assert result.project_root.has_specs_dir is True
        assert result.project_root.markers == ["specs/"]


class TestProjectRootMarkers:
    """tests for ProjectRoot marker properties"""

    def test_markers_display_both(self, project_with_both: Path) -> None:
        """should display both markers when both exist"""
        result = find_project_root(project_with_both)

        assert result.project_root is not None
        assert result.project_root.markers_display == ".specify/, specs/"

    def test_markers_display_single(self, project_with_specs: Path) -> None:
        """should display single marker when only one exists"""
        result = find_project_root(project_with_specs)

        assert result.project_root is not None
        assert result.project_root.markers_display == "specs/"
````

## File: tests/unit/test_server.py
````python
"""unit tests for server management utilities"""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from specbook.core.models import ServerState, SpecDirectory, SpecListing
from specbook.core.server import get_server_status


class TestSpecListing:
    """tests for SpecListing.from_project()"""

    def test_from_project_happy_path(self, temp_dir: Path) -> None:
        """SpecListing.from_project() returns specs sorted by name"""
        # create specs directory with subdirectories
        specs_dir = temp_dir / "specs"
        specs_dir.mkdir()
        (specs_dir / "002-feature-b").mkdir()
        (specs_dir / "001-feature-a").mkdir()
        (specs_dir / "003-feature-c").mkdir()

        listing = SpecListing.from_project(temp_dir)

        assert listing.project_root == temp_dir
        assert len(listing.specs) == 3
        assert listing.specs[0].name == "001-feature-a"
        assert listing.specs[1].name == "002-feature-b"
        assert listing.specs[2].name == "003-feature-c"
        assert not listing.is_empty

    def test_from_project_empty_specs(self, temp_dir: Path) -> None:
        """SpecListing.from_project() returns empty list when no subdirs"""
        specs_dir = temp_dir / "specs"
        specs_dir.mkdir()

        listing = SpecListing.from_project(temp_dir)

        assert listing.project_root == temp_dir
        assert len(listing.specs) == 0
        assert listing.is_empty

    def test_from_project_no_specs_dir(self, temp_dir: Path) -> None:
        """SpecListing.from_project() returns empty list when no specs/ dir"""
        listing = SpecListing.from_project(temp_dir)

        assert listing.project_root == temp_dir
        assert len(listing.specs) == 0
        assert listing.is_empty

    def test_from_project_excludes_hidden(self, temp_dir: Path) -> None:
        """SpecListing excludes hidden directories (starting with .)"""
        specs_dir = temp_dir / "specs"
        specs_dir.mkdir()
        (specs_dir / "001-visible").mkdir()
        (specs_dir / ".hidden").mkdir()
        (specs_dir / "002-also-visible").mkdir()

        listing = SpecListing.from_project(temp_dir)

        assert len(listing.specs) == 2
        spec_names = [s.name for s in listing.specs]
        assert "001-visible" in spec_names
        assert "002-also-visible" in spec_names
        assert ".hidden" not in spec_names

    def test_from_project_excludes_files(self, temp_dir: Path) -> None:
        """SpecListing excludes files, only lists directories"""
        specs_dir = temp_dir / "specs"
        specs_dir.mkdir()
        (specs_dir / "001-spec-dir").mkdir()
        (specs_dir / "README.md").write_text("readme")

        listing = SpecListing.from_project(temp_dir)

        assert len(listing.specs) == 1
        assert listing.specs[0].name == "001-spec-dir"


class TestSpecDirectory:
    """tests for SpecDirectory model"""

    def test_from_path(self, temp_dir: Path) -> None:
        """SpecDirectory.from_path() creates instance from path"""
        spec_path = temp_dir / "001-my-feature"
        spec_path.mkdir()

        spec_dir = SpecDirectory.from_path(spec_path)

        assert spec_dir.name == "001-my-feature"
        assert spec_dir.path == spec_path


class TestGetServerStatus:
    """tests for get_server_status() (RUNNING, STOPPED, etc) function"""

    def test_returns_stopped_when_no_process(self) -> None:
        """get_server_status() returns STOPPED when no process on port"""
        with patch("specbook.core.server.find_process_on_port") as mock_find:
            mock_find.return_value = None

            status = get_server_status(7732)

            assert status.state == ServerState.STOPPED
            assert status.port == 7732
            assert status.pid is None
            assert status.project_root is None

    def test_returns_running_for_specbook_process(self) -> None:
        """get_server_status() returns RUNNING for specbook process"""
        mock_proc = MagicMock()
        mock_proc.pid = 12345
        mock_proc.cmdline.return_value = [
            "/usr/bin/python",
            "-m",
            "specbook.ui.web.app",
            "7732",
            "/path/to/project",
        ]

        with (
            patch("specbook.core.server.find_process_on_port") as mock_find,
            patch("specbook.core.server.is_specbook_process") as mock_is_specbook,
            patch(
                "specbook.core.server.get_project_root_from_process"
            ) as mock_get_root,
        ):
            mock_find.return_value = mock_proc
            mock_is_specbook.return_value = True
            mock_get_root.return_value = Path("/path/to/project")

            status = get_server_status(7732)

            assert status.state == ServerState.RUNNING
            assert status.port == 7732
            assert status.pid == 12345
            assert status.project_root == Path("/path/to/project")

    def test_returns_port_conflict_for_other_process(self) -> None:
        """get_server_status() returns PORT_CONFLICT for non-specbook"""
        mock_proc = MagicMock()
        mock_proc.pid = 99999

        with (
            patch("specbook.core.server.find_process_on_port") as mock_find,
            patch("specbook.core.server.is_specbook_process") as mock_is_specbook,
        ):
            mock_find.return_value = mock_proc
            mock_is_specbook.return_value = False

            status = get_server_status(7732)

            assert status.state == ServerState.PORT_CONFLICT
            assert status.port == 7732
            assert status.pid == 99999
            assert status.project_root is None
````

## File: tests/__init__.py
````python
"""Test suite for specbook."""
````

## File: tests/conftest.py
````python
"""Pytest fixtures for specbook tests."""

import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    """create temp directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def project_with_specify(temp_dir: Path) -> Path:
    """create project with just a .specify/ directory"""
    (temp_dir / ".specify").mkdir()
    return temp_dir


@pytest.fixture
def project_with_specs(temp_dir: Path) -> Path:
    """create project with just a specs/ directory"""
    (temp_dir / "specs").mkdir()
    return temp_dir


@pytest.fixture
def project_with_both(temp_dir: Path) -> Path:
    """create typical spec-kit project with both .specify/ and specs/ directories"""
    (temp_dir / ".specify").mkdir()
    (temp_dir / "specs").mkdir()
    return temp_dir


@pytest.fixture
def nested_subdir(project_with_both: Path) -> Path:
    """create a nested subdirectory structure within a project"""
    nested = project_with_both / "src" / "components" / "deep"
    nested.mkdir(parents=True)
    return nested
````

## File: src/specbook/core/models.py
````python
"""Data models for specbook project root detection and server management."""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


@dataclass
class ProjectRoot:
    """discovered Specbook project root"""

    path: Path
    """absolute path to the project root directory"""

    has_specify_dir: bool
    """true if .specify/ directory exists at root"""

    has_specs_dir: bool
    """true if specs/ directory exists at root"""

    @property
    def markers(self) -> list[str]:
        """list of marker directories found"""
        result = []
        if self.has_specify_dir:
            result.append(".specify/")
        if self.has_specs_dir:
            result.append("specs/")
        return result

    @property
    def markers_display(self) -> str:
        """formatted string of markers for display"""
        return ", ".join(self.markers)


@dataclass
class SearchContext:
    """configuration for project root search"""

    start_path: Path
    """directory to start searching from"""

    @classmethod
    def from_cwd(cls) -> "SearchContext":
        """create context starting from current working directory"""
        return cls(start_path=Path.cwd())

    @classmethod
    def from_path(cls, path: str | Path) -> "SearchContext":
        """create context starting from specified path"""
        return cls(start_path=Path(path).resolve())


@dataclass
class SearchResult:
    """result of searching for project root"""

    found: bool
    """true if a project root was found"""

    project_root: ProjectRoot | None
    """discovered project root (or None if not found)"""

    searched_from: Path
    """starting directory of the search"""

    searched_to: Path
    """last directory checked (filesystem root if not found)"""

    @property
    def error_message(self) -> str | None:
        """user-friendly error message if not found"""
        if self.found:
            return None
        return (
            f"No spec-driven development project found.\n\n"
            f"Did not find .specify/ or specs/ at \033[1m{self.searched_from}\033[0m\n"
            #f"Reached: {self.searched_to}\n\n"
            #f"Specbook works in a project with .specify/ or specs/"
        )


# server management models

@dataclass
class ServerConfig:
    """config for a specbook web server"""

    port: int
    """port to bind server to"""

    project_root: Path
    """absolute path to the project root being served"""

    host: str = "127.0.0.1"
    """host to bind to—always localhost"""

    @property
    def url(self) -> str:
        """full URL for the server."""
        return f"http://{self.host}:{self.port}"


class ServerState(Enum):
    """possible states for a server port"""

    RUNNING = "running"
    STOPPED = "stopped"
    PORT_CONFLICT = "conflict"


@dataclass
class ServerStatus:
    """status of a server on a specific port"""

    port: int
    """port number being checked"""

    state: ServerState
    """current state of the port"""

    pid: int | None
    """process ID if running (else None)"""

    project_root: Path | None
    """project being served if running (else None)"""

    @property
    def url(self) -> str | None:
        """URL if server is running"""
        if self.state == ServerState.RUNNING:
            return f"http://127.0.0.1:{self.port}"
        return None

    @property
    def is_running(self) -> bool:
        """True if a specbook server is running on this port"""
        return self.state == ServerState.RUNNING

    @property
    def has_conflict(self) -> bool:
        """True if port is occupied by a non-specbook process"""
        return self.state == ServerState.PORT_CONFLICT


@dataclass
class SpecDirectory:
    """specification directory for display"""

    name: str
    """directory name (e.g., '001-spec-a')"""

    path: Path
    """absolute path to the directory"""

    @classmethod
    def from_path(cls, path: Path) -> "SpecDirectory":
        """create from a directory path"""
        return cls(name=path.name, path=path)


@dataclass
class SpecListing:
    """all spec directories in a project"""

    project_root: Path
    """path to the project root"""

    specs: list[SpecDirectory]
    """list of spec directories, sorted by name"""

    @property
    def is_empty(self) -> bool:
        """True if no specs found"""
        return len(self.specs) == 0

    @classmethod
    def from_project(cls, project_root: Path) -> "SpecListing":
        """scan project and build spec listing"""
        specs_dir = project_root / "specs"
        if not specs_dir.is_dir():
            return cls(project_root=project_root, specs=[])

        specs = [
            SpecDirectory.from_path(p)
            for p in sorted(specs_dir.iterdir())
            if p.is_dir() and not p.name.startswith(".")
        ]
        return cls(project_root=project_root, specs=specs)
````

## File: src/specbook/ui/console.py
````python
"""Rich console helpers for specbook CLI output."""

from contextlib import contextmanager
from typing import Generator

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# shared console instance
console = Console()


def error_panel(message: str, title: str = "Error") -> None:
    """display an error message in a red Rich panel"""
    console.print(Panel(message, title=title, border_style="red"))


def success_output(path: str, markers: str) -> None:
    """display successful project root discovery in green"""
    console.print(f"[green]✓[/green] Project root: {path}")
    console.print(f"  Found: {markers}")


def server_message(message: str, url: str | None = None, path: str | None = None) -> None:
    """display a server status message with optional details"""
    console.print(f"[green]✓[/green] {message}")
    if url:
        console.print(f"  URL: {url}")
    if path:
        console.print(f"  Serving: {path}")


def server_info(message: str) -> None:
    """display an informational server message"""
    console.print(f"[blue]ℹ[/blue] {message}")


def server_error(message: str, suggestion: str | None = None) -> None:
    """display a server error message in a red panel with optional suggestion"""
    full_message = message
    if suggestion:
        full_message = f"{message}\n\n{suggestion}"
    console.print(Panel(full_message, title="Error", border_style="red"))


@contextmanager
def search_progress() -> Generator[None, None, None]:
    """context manager for displaying progress spinner"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,  # remove after complete
        console=console,
    ) as progress:
        progress.add_task("Searching for project root...", total=None)
        yield
````

## File: src/specbook/__main__.py
````python
"""entry point for python -m specbook"""

from specbook.cli import app

if __name__ == "__main__":
    app()
````

## File: src/specbook/cli.py
````python
"""Specbook CLI application."""

from pathlib import Path

import typer

from specbook.core.finder import find_project_root
from specbook.core.models import SearchContext, ServerConfig, ServerState
from specbook.core.server import (
    get_server_status,
    open_browser,
    start_server,
    stop_server,
)
from specbook.ui.console import (
    error_panel,
    search_progress,
    server_error,
    server_info,
    server_message,
    success_output,
)

# 📞 SPEC
DEFAULT_PORT = 7732

app = typer.Typer(
    help="CLI tool to view spec-driven development docs",
    no_args_is_help=False,
    invoke_without_command=True,
)


def _start_server_impl(port: int, path: str | None) -> None:
    """implementation of server start logic"""
    # validate provided path argument
    if path is not None:
        target = Path(path)
        if not target.exists():
            error_panel(f"Directory does not exist: {path}")
            raise typer.Exit(code=2)
        if not target.is_dir():
            error_panel(f"Path is not a directory: {path}")
            raise typer.Exit(code=2)
        search_ctx = SearchContext.from_path(path)
    else:
        search_ctx = SearchContext.from_cwd()

    # search for project root
    with search_progress():
        result = find_project_root(search_ctx.start_path)

    # display results
    if not result.found or not result.project_root:
        error_panel(result.error_message or "Unknown error")
        raise typer.Exit(code=1)

    project_root = result.project_root.path

    # check current port status
    current_status = get_server_status(port)

    if current_status.state == ServerState.PORT_CONFLICT:
        # another (non-specbook) process is using the port
        server_error(
            f"Port {port} is already in use by another application",
            f"Try a different port with: specbook -p {port + 1}",
        )
        raise typer.Exit(code=1)

    if current_status.state == ServerState.RUNNING:
        # existing specbook server - auto-restart
        stop_server(port)

    # start the server
    config = ServerConfig(port=port, project_root=project_root)
    start_server(config)

    # open browser and show message
    open_browser(config.url)
    server_message(
        f"Server started at {config.url}",
        path=str(project_root),
    )
    typer.echo("  Press Ctrl+C or run 'specbook stop' to stop")
    raise typer.Exit(code=0)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    port: int = typer.Option(
        DEFAULT_PORT,
        "--port",
        "-p",
        help="Port to run the server on",
    ),
) -> None:
    """Start the spec viewer web server (or use a subcommand).

    Without arguments, finds the project root from current directory,
    starts a web server, *and* launches the browser.
    """
    # if a subcommand was invoked, don't run the default
    if ctx.invoked_subcommand is not None:
        return

    # default behavior: start the server
    _start_server_impl(port, None)


@app.command()
def serve(
    port: int = typer.Option(
        DEFAULT_PORT,
        "--port",
        "-p",
        help="Port to run the server on",
    ),
    path: str | None = typer.Argument(
        None,
        help="Directory to search from (defaults to current directory)",
    ),
) -> None:
    """start the spec viewer web server *with* explicit path"""
    _start_server_impl(port, path)


@app.command()
def stop(
    port: int = typer.Option(
        DEFAULT_PORT,
        "--port",
        "-p",
        help="Port of the server to stop",
    ),
) -> None:
    """stop a running specbook server."""
    status = get_server_status(port)

    if status.state == ServerState.STOPPED:
        server_info(f"No server running on port {port}")
        raise typer.Exit(code=0)

    if status.state == ServerState.PORT_CONFLICT:
        server_error(
            f"Port {port} is in use by another application"
        )
        raise typer.Exit(code=1)

    # stop the specbook server
    if stop_server(port):
        server_message("Server stopped")
        raise typer.Exit(code=0)
    else:
        server_error("Failed to stop server")
        raise typer.Exit(code=1)


@app.command()
def status(
    port: int = typer.Option(
        DEFAULT_PORT,
        "--port",
        "-p",
        help="Port to check server status on",
    ),
) -> None:
    """show the status of a specbook server"""
    server_status = get_server_status(port)

    if server_status.state == ServerState.STOPPED:
        server_info(f"No server running on port {port}")
        raise typer.Exit(code=0)

    if server_status.state == ServerState.PORT_CONFLICT:
        server_info(f"Port {port} is in use by another application (not specbook)")
        raise typer.Exit(code=0)

    # server is running
    server_message(
        "Server running",
        url=server_status.url,
        path=str(server_status.project_root) if server_status.project_root else None,
    )
    if server_status.pid:
        typer.echo(f"  PID: {server_status.pid}")
    raise typer.Exit(code=0)


@app.command()
def restart(
    port: int = typer.Option(
        DEFAULT_PORT,
        "--port",
        "-p",
        help="Port to restart the server on",
    ),
    path: str | None = typer.Argument(
        None,
        help="Directory to search from (defaults to current directory)",
    ),
) -> None:
    """restart the specbook server."""
    # validate provided path argument
    if path is not None:
        target = Path(path)
        if not target.exists():
            error_panel(f"Directory does not exist: {path}")
            raise typer.Exit(code=2)
        if not target.is_dir():
            error_panel(f"Path is not a directory: {path}")
            raise typer.Exit(code=2)
        search_ctx = SearchContext.from_path(path)
    else:
        search_ctx = SearchContext.from_cwd()

    # search for project root
    with search_progress():
        result = find_project_root(search_ctx.start_path)

    if not result.found or not result.project_root:
        error_panel(result.error_message or "Unknown error")
        raise typer.Exit(code=1)

    project_root = result.project_root.path

    # stop existing server if running
    current_status = get_server_status(port)
    if current_status.state == ServerState.RUNNING:
        stop_server(port)
    elif current_status.state == ServerState.PORT_CONFLICT:
        server_error(
            f"Port {port} is already in use by another application",
            f"Try a different port with: specbook restart -p {port + 1}",
        )
        raise typer.Exit(code=1)

    # start the server
    config = ServerConfig(port=port, project_root=project_root)
    start_server(config)

    # open browser and show message
    open_browser(config.url)
    server_message(
        f"Server restarted at {config.url}",
        path=str(project_root),
    )
    raise typer.Exit(code=0)


if __name__ == "__main__":
    app()
````

## File: tests/integration/test_cli.py
````python
"""Integration tests for specbook CLI."""

import os
from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from specbook.cli import DEFAULT_PORT, app

runner = CliRunner()


class TestCLIServerStart:
    """tests for the serve command that starts the web server"""

    def test_starts_server_from_project(self, project_with_both: Path) -> None:
        """CLI starts server and returns prompt"""
        # mock the server start and browser open to avoid actual side effects
        with (
            patch("specbook.cli.start_server") as mock_start,
            patch("specbook.cli.open_browser") as mock_browser,
            patch("specbook.cli.get_server_status") as mock_status,
        ):
            from specbook.core.models import ServerState, ServerStatus

            mock_status.return_value = ServerStatus(
                port=DEFAULT_PORT,
                state=ServerState.STOPPED,
                pid=None,
                project_root=None,
            )

            result = runner.invoke(app, ["serve", str(project_with_both)])

            assert result.exit_code == 0
            assert "Server started" in result.output
            assert f"http://127.0.0.1:{DEFAULT_PORT}" in result.output
            mock_start.assert_called_once()
            mock_browser.assert_called_once()

    def test_starts_server_with_custom_port(self, project_with_both: Path) -> None:
        """CLI starts server on custom port with -p flag."""
        with (
            patch("specbook.cli.start_server") as mock_start,
            patch("specbook.cli.open_browser"),
            patch("specbook.cli.get_server_status") as mock_status,
        ):
            from specbook.core.models import ServerState, ServerStatus

            mock_status.return_value = ServerStatus(
                port=3627,
                state=ServerState.STOPPED,
                pid=None,
                project_root=None,
            )

            result = runner.invoke(app, ["serve", "-p", "3627", str(project_with_both)])

            assert result.exit_code == 0
            assert "3627" in result.output  
            # verify start_server was called with custom port
            call_args = mock_start.call_args[0][0]
            assert call_args.port == 3627 # Dial D-O-C-S

    def test_auto_restarts_existing_specbook_server(
        self, project_with_both: Path
    ) -> None:
        """CLI auto-restarts existing specbook server on same port"""
        with (
            patch("specbook.cli.start_server"),
            patch("specbook.cli.open_browser"),
            patch("specbook.cli.stop_server") as mock_stop,
            patch("specbook.cli.get_server_status") as mock_status,
        ):
            from specbook.core.models import ServerState, ServerStatus

            mock_status.return_value = ServerStatus(
                port=DEFAULT_PORT,
                state=ServerState.RUNNING,
                pid=12345,
                project_root=project_with_both,
            )

            result = runner.invoke(app, ["serve", str(project_with_both)])

            assert result.exit_code == 0
            mock_stop.assert_called_once_with(DEFAULT_PORT)

    def test_shows_error_for_port_conflict(self, project_with_both: Path) -> None:
        """CLI shows error when port is used by non-specbook process"""
        with patch("specbook.cli.get_server_status") as mock_status:
            from specbook.core.models import ServerState, ServerStatus

            mock_status.return_value = ServerStatus(
                port=DEFAULT_PORT,
                state=ServerState.PORT_CONFLICT,
                pid=99999,
                project_root=None,
            )

            result = runner.invoke(app, ["serve", str(project_with_both)])

            assert result.exit_code == 1
            assert "already in use" in result.output


class TestCLIErrorCases:
    """Tests for CLI error handling"""

    def test_nonexistent_path_error(self) -> None:
        """should show error for non-existent path"""
        result = runner.invoke(app, ["serve", "/nonexistent/path/that/does/not/exist"])

        assert result.exit_code == 2
        assert "does not exist" in result.output

    def test_file_instead_of_directory_error(self, temp_dir: Path) -> None:
        """should show error when path is a file, not directory"""
        test_file = temp_dir / "test_file.txt"
        test_file.write_text("test content")

        result = runner.invoke(app, ["serve", str(test_file)])

        assert result.exit_code == 2
        assert "not a directory" in result.output

    def test_no_project_found_error(self, temp_dir: Path) -> None:
        """Should show error when no project markers are found."""
        result = runner.invoke(app, ["serve", str(temp_dir)])

        assert result.exit_code == 1
        assert "No spec-driven development project" in result.output


class TestCLIHelp:
    """Tests for CLI help output."""

    def test_help_flag(self) -> None:
        """Should display help with --help flag."""
        result = runner.invoke(app, ["--help"])

        assert result.exit_code == 0
        # verify help shows tool description
        assert "spec" in result.output.lower()


class TestCLIStop:
    """Tests for the stop command."""

    def test_stop_running_server(self) -> None:
        """T036: specbook stop stops running server."""
        with (
            patch("specbook.cli.get_server_status") as mock_status,
            patch("specbook.cli.stop_server") as mock_stop,
        ):
            from specbook.core.models import ServerState, ServerStatus

            mock_status.return_value = ServerStatus(
                port=DEFAULT_PORT,
                state=ServerState.RUNNING,
                pid=12345,
                project_root=Path("/path/to/project"),
            )
            mock_stop.return_value = True

            result = runner.invoke(app, ["stop"])

            assert result.exit_code == 0
            assert "stopped" in result.output.lower()
            mock_stop.assert_called_once_with(DEFAULT_PORT)

    def test_stop_no_server_running(self) -> None:
        """Stop shows info when no server running."""
        with patch("specbook.cli.get_server_status") as mock_status:
            from specbook.core.models import ServerState, ServerStatus

            mock_status.return_value = ServerStatus(
                port=DEFAULT_PORT,
                state=ServerState.STOPPED,
                pid=None,
                project_root=None,
            )

            result = runner.invoke(app, ["stop"])

            assert result.exit_code == 0
            assert "No server running" in result.output

    def test_stop_with_custom_port(self) -> None:
        """Stop uses custom port with -p flag."""
        with (
            patch("specbook.cli.get_server_status") as mock_status,
            patch("specbook.cli.stop_server") as mock_stop,
        ):
            from specbook.core.models import ServerState, ServerStatus

            mock_status.return_value = ServerStatus(
                port=8080,
                state=ServerState.RUNNING,
                pid=12345,
                project_root=Path("/path/to/project"),
            )
            mock_stop.return_value = True

            result = runner.invoke(app, ["stop", "-p", "8080"])

            assert result.exit_code == 0
            mock_stop.assert_called_once_with(8080)


class TestCLIStatus:
    """tests the status command"""

    def test_status_shows_running_server(self) -> None:
        """specbook status shows correct state for running server"""
        with patch("specbook.cli.get_server_status") as mock_status:
            from specbook.core.models import ServerState, ServerStatus

            mock_status.return_value = ServerStatus(
                port=DEFAULT_PORT,
                state=ServerState.RUNNING,
                pid=12345,
                project_root=Path("/path/to/project"),
            )

            result = runner.invoke(app, ["status"])

            assert result.exit_code == 0
            assert "running" in result.output.lower()
            assert "12345" in result.output
            assert "7732" in result.output

    def test_status_shows_stopped(self) -> None:
        """status shows info even when no server running"""
        with patch("specbook.cli.get_server_status") as mock_status:
            from specbook.core.models import ServerState, ServerStatus

            mock_status.return_value = ServerStatus(
                port=DEFAULT_PORT,
                state=ServerState.STOPPED,
                pid=None,
                project_root=None,
            )

            result = runner.invoke(app, ["status"])

            assert result.exit_code == 0
            assert "No server running" in result.output

    def test_status_with_custom_port(self) -> None:
        """status uses custom port with -p flag"""
        with patch("specbook.cli.get_server_status") as mock_status:
            from specbook.core.models import ServerState, ServerStatus

            mock_status.return_value = ServerStatus(
                port=8080,
                state=ServerState.STOPPED,
                pid=None,
                project_root=None,
            )

            result = runner.invoke(app, ["status", "-p", "8080"])

            assert result.exit_code == 0
            assert "8080" in result.output


class TestCLIRestart:
    """tests the restart command"""

    def test_restart_server(self, project_with_both: Path) -> None:
        """Restart stops and starts the server."""
        with (
            patch("specbook.cli.get_server_status") as mock_status,
            patch("specbook.cli.stop_server") as mock_stop,
            patch("specbook.cli.start_server"),
            patch("specbook.cli.open_browser"),
        ):
            from specbook.core.models import ServerState, ServerStatus

            mock_status.return_value = ServerStatus(
                port=DEFAULT_PORT,
                state=ServerState.RUNNING,
                pid=12345,
                project_root=project_with_both,
            )

            result = runner.invoke(app, ["restart", str(project_with_both)])

            assert result.exit_code == 0
            assert "restarted" in result.output.lower()
            mock_stop.assert_called_once_with(DEFAULT_PORT)
````

## File: .gitignore
````
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store
*.tmp

# Project cruft
*.log
.env
.env.local
*.lock
.specify/
.claude/
CLAUDE.md
/specs
.coverage

# Application-Specific files
*.zip
````

## File: LICENSE
````
BSD 3-Clause License

Copyright (c) 2026, Christopher Correa

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
````

## File: pyproject.toml
````toml
[project]
name = "specbook"
version = "0.1.0"
description = "CLI tool to collaborate on spec-driven development (SDD) project artifacts"
readme = "README.md"
requires-python = ">=3.11"
license = { file = "LICENSE" }
authors = [
    { name = "Christopher Correa" }
]
dependencies = [
    "typer>=0.9",
    "rich>=13",
    "starlette>=0.40",
    "uvicorn>=0.30",
    "jinja2>=3.1",
    "psutil>=5.9",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4",
    "pytest-cov>=4.1",
    "pyright>=1.1",
]

[project.scripts]
specbook = "specbook.cli:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/specbook"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]

[tool.pyright]
pythonVersion = "3.11"
typeCheckingMode = "basic"
include = ["src"]

[tool.coverage.run]
source = ["src/specbook"]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
]
````

## File: README.md
````markdown
<img src="src/specbook/ui/web/static/specbook_leaf.png" alt="Specbook" width="64">

# Specbook

A browser-based viewer and editor for spec-driven development (SDD) projects. Specbook facilitates review, collaboration on specs, plans, and task lists.

## How Does It Work?

Specbook launches a local web server that renders your `specs/` directory in a clean, readable format.

## Install

```bash
uv tool install specbook --from git+https://github.com/chriscorrea/specbook.git
```

## Usage

From any directory in your project:

```bash
specbook
```

The server runs in the background—use `specbook stop` when you're done.

## Development

```bash
git clone https://github.com/chriscorrea/specbook.git
cd specbook
uv sync
uv run specbook
```

## License

This project is licensed under the [BSD-3 License](LICENSE).
````
