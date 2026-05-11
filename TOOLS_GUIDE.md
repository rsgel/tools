# Tools Repository — Guide for Coding Agents

## Repository Overview

**Type**: Static HTML/JavaScript web tools  
**Hosting**: GitHub Pages (rsgel.github.io/tools/)  
**Build**: Python scripts generate the index page  
**Testing**: Playwright + pytest for automated testing  

---

## 1. Repository Structure

```
tools/
├── *.html                    # Individual tool files (one per tool)
├── *.docs.md                 # Documentation/descriptions for each tool
├── tests/
│   └── test_*.py             # Pytest + Playwright test files
├── .github/workflows/
│   ├── test.yml              # Runs pytest/playwright on push/PR
│   ├── pages.yml             # Builds and deploys to GitHub Pages
│   └── claude.yml            # Claude Code action for @claude mentions
├── build_index.py            # Generates index.html from README.md
├── build.sh                  # Build script
├── README.md                 # Main listing of all tools
├── TOOLS_GUIDE.md            # This file — agent reference
├── pyproject.toml            # Python project config and test dependencies
├── _config.yml               # GitHub Pages / Jekyll config
└── .gitignore
```

---

## 2. Tool File Naming Convention

- **HTML file**: `{tool-name}.html` (e.g., `json-formatter.html`)
- **Docs file**: `{tool-name}.docs.md` (e.g., `json-formatter.docs.md`)
- **Docs format**: Description first, then optional Spec and Backlog sections

### Example docs.md:
```markdown
A JSON formatting and validation tool. Paste or type JSON into the input area 
and see it pretty-printed with syntax highlighting. Invalid JSON is flagged 
with a clear error message showing the line and position of the problem.

## Spec

Core behaviors: paste/type JSON in left panel, formatted output in right panel.
Uses native JSON.parse for validation. Error messages extract line/position from
SyntaxError. Supports compact vs. pretty output (2-space indent).

## Backlog

- JSON diff mode (compare two JSON blobs)
- JSON-to-YAML conversion
- Collapsible tree view
```

The **Spec** and **Backlog** sections are optional but encouraged for non-trivial tools.
Keep the spec concise — essential data model, key behaviors, and technical decisions.

---

## 3. Common HTML Structure

Each tool is a **single, self-contained HTML file**. Follow this pattern:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tool Name</title>
    <style>
    * {
      box-sizing: border-box;
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      max-width: 800px;
      margin: 0 auto;
      padding: 20px;
      line-height: 1.6;
    }
    /* Mobile-friendly */
    @media (max-width: 600px) {
      body { padding: 10px; }
      h1 { font-size: 24px; }
    }
    </style>
</head>
<body>
    <h1>Tool Name</h1>
    <p>Brief description of what this tool does.</p>
    
    <!-- Tool UI here -->
    
    <script>
    // JavaScript logic here — vanilla JS, no frameworks
    </script>
</body>
</html>
```

**Key rules:**
- Never use React or heavy frameworks — always plain HTML, vanilla JavaScript, and CSS
- CSS indented with two spaces, starting with `* { box-sizing: border-box; }`
- Inputs and textareas should use `font-size: 16px` (prevents iOS zoom)
- Font stack should prefer system fonts
- JavaScript uses two-space indents
- Responsive design with max-width centered container
- Mobile media query at ~600px breakpoint

---

## 4. UI Patterns

### Copy to Clipboard
```javascript
navigator.clipboard.writeText(text).then(() => {
  button.textContent = 'Copied!';
  setTimeout(() => { button.textContent = 'Copy'; }, 2000);
});
```

### Error Display
```html
<div id="error" class="error" style="display:none"></div>
```
```css
.error {
  color: #e74c3c;
  padding: 12px;
  background: #fef5f5;
  border-radius: 4px;
  margin-top: 10px;
}
```

### Loading States
```javascript
button.disabled = true;
button.textContent = 'Loading...';
try {
  const result = await doWork();
  displayResult(result);
} finally {
  button.disabled = false;
  button.textContent = 'Process';
}
```

### File Input + Drag & Drop
```javascript
dropzone.addEventListener('dragover', e => { e.preventDefault(); });
dropzone.addEventListener('drop', e => {
  e.preventDefault();
  handleFiles(e.dataTransfer.files);
});
```

---

## 5. Tool Architecture Patterns

### Pattern 1: Simple Stateless (most common)
Input → Process → Output. Real-time event listeners, no external APIs.
Examples: text formatters, encoders, calculators.

### Pattern 2: External Libraries via CDN
```html
<script src="https://cdn.jsdelivr.net/npm/library@version/dist/lib.min.js"></script>
```
Use jsdelivr or cdnjs for external dependencies.

### Pattern 3: WebAssembly
For tools using SQLite WASM, Pyodide, etc.

---

## 6. Adding a New Tool — Checklist

1. Create `{tool-name}.html` following the HTML template above
2. Create `{tool-name}.docs.md` with a brief description
3. Add a bullet point to `README.md` under the appropriate section:
   ```
   - [Tool Name](tool-name) short description
   ```
4. Create `tests/test_{tool_name}.py` with Playwright tests
5. Test locally: `python -m http.server 8000` then visit `localhost:8000/tool-name.html`

---

## 7. Test Structure

```python
import pathlib
from playwright.sync_api import Page, expect
import pytest
from subprocess import Popen, PIPE
from http.client import HTTPConnection
import time

test_dir = pathlib.Path(__file__).parent.absolute()
root = test_dir.parent.absolute()

@pytest.fixture(scope="module")
def static_server():
    process = Popen(
        ["python", "-m", "http.server", "8123", "--directory", root],
        stdout=PIPE
    )
    retries = 5
    while retries > 0:
        conn = HTTPConnection("127.0.0.1:8123")
        try:
            conn.request("HEAD", "/")
            conn.getresponse()
            yield process
            break
        except ConnectionRefusedError:
            time.sleep(1)
            retries -= 1
    process.terminate()
    process.wait()

def test_initial_state(page: Page, static_server):
    page.goto("http://127.0.0.1:8123/tool-name.html")
    expect(page.locator("h1")).to_have_text("Tool Name")
```

---

## 8. Local Development

```bash
# Serve locally
python -m http.server 8000

# Run tests
pip install -e .
playwright install
pytest

# Build index
python build_index.py
```

---

## Summary

1. Each tool is a **single, self-contained HTML file**
2. Tools are **mobile-responsive** with minimal CSS
3. **Real-time processing** via vanilla JavaScript event listeners
4. **External resources** loaded from CDNs (jsdelivr, cdnjs)
5. **No build step** required for individual tools
6. **Tests** use Playwright + pytest
7. **GitHub Pages** deploys automatically on push to main
