"""
Build index.html from README.md

Converts the README into a styled HTML page that serves as the
homepage for the tools site on GitHub Pages.
"""
import markdown
import re
import glob

def get_tool_count():
    """Count the number of .html tool files in the root directory."""
    tools = [f for f in glob.glob("*.html") if f != "index.html"]
    return len(tools)

def build_index():
    with open("README.md") as f:
        readme_content = f.read()

    md = markdown.Markdown(extensions=["extra", "toc"])
    html_body = md.convert(readme_content)

    tool_count = get_tool_count()

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tools</title>
    <style>
    * {{
      box-sizing: border-box;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      max-width: 800px;
      margin: 0 auto;
      padding: 20px;
      line-height: 1.6;
      color: #333;
    }}
    a {{
      color: #0969da;
      text-decoration: none;
    }}
    a:hover {{
      text-decoration: underline;
    }}
    ul {{
      padding-left: 20px;
    }}
    li {{
      margin-bottom: 6px;
    }}
    h1 {{
      border-bottom: 1px solid #d0d7de;
      padding-bottom: 8px;
    }}
    h2 {{
      border-bottom: 1px solid #d0d7de;
      padding-bottom: 6px;
      margin-top: 24px;
    }}
    .meta {{
      color: #666;
      font-size: 14px;
      margin-bottom: 20px;
    }}
    @media (max-width: 600px) {{
      body {{
        padding: 12px;
      }}
      h1 {{
        font-size: 24px;
      }}
    }}
    </style>
</head>
<body>
    {html_body}
    <p class="meta">{tool_count} tool{"s" if tool_count != 1 else ""} and counting.</p>
</body>
</html>"""

    with open("index.html", "w") as f:
        f.write(index_html)

    print(f"Built index.html ({tool_count} tools)")

if __name__ == "__main__":
    build_index()
