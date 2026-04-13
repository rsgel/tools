# Claude Instructions for tools repo

Read TOOLS_GUIDE.md before making any changes to understand the repository structure and conventions.

## Creating Tools

Each tool is a single, self-contained HTML file. Follow these rules:

- Never use React or heavy frameworks — always plain HTML, vanilla JavaScript, and CSS
- CSS should be indented with two spaces and start with `* { box-sizing: border-box; }`
- Inputs and textareas should be font-size 16px
- Font stack: `-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif`
- JavaScript should use two-space indents
- Every tool must be mobile-responsive (test at 600px width)
- Use `<meta name="viewport" content="width=device-width, initial-scale=1.0">`

## File Naming

- Tool HTML: `{tool-name}.html` (kebab-case)
- Tool docs: `{tool-name}.docs.md`
- Tests: `tests/test_{tool_name}.py`

## When Adding a Tool

1. Create the `.html` file
2. Create the `.docs.md` file (see format below)
3. Add a line to `README.md` in the Tools section
4. Optionally add Playwright tests in `tests/`

## Docs File Format (`*.docs.md`)

Each tool's docs file starts with a 2-3 sentence description, then optionally includes
a lightweight spec and a backlog of future ideas:

```markdown
Brief 2-3 sentence description of what the tool does.

## Spec

Essential spec notes: core data model, key behaviors, technical decisions.
Keep it concise — just enough for an agent to understand intent without
reading all the source code.

## Backlog

- Future idea one
- Future idea two
```

The Spec and Backlog sections are optional but encouraged for non-trivial tools.

## Code Style

- No trailing whitespace
- Use semantic HTML elements
- Prefer `const` over `let`, never use `var`
- Use template literals for string interpolation
- Event listeners over inline handlers
- Copy-to-clipboard buttons should show "Copied!" feedback for 2 seconds
