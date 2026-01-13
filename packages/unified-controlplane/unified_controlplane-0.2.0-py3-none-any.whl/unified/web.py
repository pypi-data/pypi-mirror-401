"""Minimal web dashboard for unified control plane.

Uses Python's built-in http.server - no external dependencies.
Binds to localhost only (127.0.0.1) for security.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

from unified.services import (
    get_status,
    route_task,
    add_memory,
    list_memory,
)
from unified.paths import detect_project_name


# HTML Templates
BASE_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Unified Control Plane</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        h1 {{ color: #333; }}
        h2 {{ color: #555; border-bottom: 1px solid #ddd; padding-bottom: 5px; }}
        nav {{ background: #333; padding: 10px; margin-bottom: 20px; border-radius: 5px; }}
        nav a {{ color: white; margin-right: 15px; text-decoration: none; }}
        nav a:hover {{ text-decoration: underline; }}
        .card {{
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .stat {{ font-size: 24px; font-weight: bold; color: #007bff; }}
        form {{ margin: 15px 0; }}
        label {{ display: block; margin: 10px 0 5px; font-weight: bold; }}
        input[type="text"], textarea, select {{
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }}
        textarea {{ min-height: 100px; }}
        button {{
            background: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin-top: 10px;
        }}
        button:hover {{ background: #0056b3; }}
        .entry {{
            border-left: 3px solid #007bff;
            padding-left: 10px;
            margin: 10px 0;
        }}
        .entry-type {{
            display: inline-block;
            background: #e9ecef;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 12px;
        }}
        .success {{ background: #d4edda; padding: 10px; border-radius: 4px; margin: 10px 0; }}
        .result {{ background: #e7f3ff; padding: 15px; border-radius: 4px; margin: 10px 0; }}
        pre {{ background: #f8f9fa; padding: 10px; overflow-x: auto; }}
    </style>
</head>
<body>
    <nav>
        <a href="/">Home</a>
        <a href="/memory">Memory</a>
        <a href="/route">Route Task</a>
    </nav>
    {content}
</body>
</html>
"""


def home_page() -> str:
    """Generate home page HTML."""
    status = get_status()

    models_html = ""
    for m in status.models:
        adapter = f"[{m.adapter}]" if m.adapter else "[no adapter]"
        models_html += f"<li>{m.name} ({m.provider}) {adapter}</li>"

    tools_html = "".join(f"<li>{t.name}: {t.description}</li>" for t in status.tools)
    skills_html = "".join(f"<li>{s.name}: {s.description}</li>" for s in status.skills)

    memory_total = sum(status.memory_counts.values())
    memory_html = ""
    if status.memory_counts:
        for t, count in status.memory_counts.items():
            memory_html += f"<li>{t}: {count}</li>"
    else:
        memory_html = "<li>No entries yet</li>"

    content = f"""
    <h1>Unified Control Plane</h1>

    <div class="card">
        <h2>Project: {status.project}</h2>
        <p>Home: <code>{status.home}</code></p>
    </div>

    <div class="card">
        <h2>Registry</h2>
        <p><span class="stat">{len(status.models)}</span> Models</p>
        <ul>{models_html or '<li>None</li>'}</ul>

        <p><span class="stat">{len(status.tools)}</span> Tools</p>
        <ul>{tools_html or '<li>None</li>'}</ul>

        <p><span class="stat">{len(status.skills)}</span> Skills</p>
        <ul>{skills_html or '<li>None</li>'}</ul>
    </div>

    <div class="card">
        <h2>Memory</h2>
        <p><span class="stat">{memory_total}</span> Total Entries</p>
        <ul>{memory_html}</ul>
        <p><a href="/memory">Manage Memory</a></p>
    </div>

    <div class="card">
        <h2>Audit Log</h2>
        <p><span class="stat">{status.audit_entries}</span> Entries</p>
    </div>
    """
    return BASE_TEMPLATE.format(content=content)


def memory_page(success_msg: str = "") -> str:
    """Generate memory page HTML."""
    project = detect_project_name() or "default"
    entries = list_memory()

    success_html = f'<div class="success">{success_msg}</div>' if success_msg else ""

    entries_html = ""
    for entry_type, items in entries.items():
        entries_html += f"<h3>{entry_type.upper()}S ({len(items)})</h3>"
        for entry in items:
            preview = entry.content[:100].replace("\n", " ")
            entries_html += f"""
            <div class="entry">
                <span class="entry-type">{entry.type}</span>
                <strong>{entry.id[:12]}</strong>
                <p>{preview}...</p>
            </div>
            """

    if not entries_html:
        entries_html = "<p>No memory entries yet. Add one below!</p>"

    content = f"""
    <h1>Memory - {project}</h1>

    {success_html}

    <div class="card">
        <h2>Add Memory Entry</h2>
        <form method="POST" action="/memory/add">
            <label for="type">Type</label>
            <select name="type" id="type" required>
                <option value="decision">Decision</option>
                <option value="context">Context</option>
                <option value="pattern">Pattern</option>
                <option value="finding">Finding</option>
            </select>

            <label for="content">Content</label>
            <textarea name="content" id="content" required placeholder="Enter memory content..."></textarea>

            <label for="tags">Tags (comma-separated, optional)</label>
            <input type="text" name="tags" id="tags" placeholder="tag1, tag2">

            <button type="submit">Add Entry</button>
        </form>
    </div>

    <div class="card">
        <h2>Existing Entries</h2>
        {entries_html}
    </div>
    """
    return BASE_TEMPLATE.format(content=content)


def route_page(result: dict | None = None) -> str:
    """Generate route task page HTML."""
    result_html = ""
    if result:
        result_html = f"""
        <div class="result">
            <h3>Routing Result</h3>
            <p><strong>Task:</strong> {result['task_intent']}</p>
            <p><strong>Model:</strong> {result['model']}</p>
            <p><strong>Reason:</strong> {result['reason']}</p>
            <p><strong>Fallback:</strong> {result['fallback'] or 'None'}</p>
        </div>
        """

    content = f"""
    <h1>Route Task</h1>

    {result_html}

    <div class="card">
        <h2>Route a Task</h2>
        <form method="POST" action="/route">
            <label for="intent">Task Description</label>
            <textarea name="intent" id="intent" required placeholder="Describe what you want to do..."></textarea>

            <label for="type">Task Type</label>
            <select name="type" id="type">
                <option value="code">Code</option>
                <option value="review">Review</option>
                <option value="documentation">Documentation</option>
                <option value="research">Research</option>
            </select>

            <label for="role">Role</label>
            <select name="role" id="role">
                <option value="lead">Lead</option>
                <option value="reviewer">Reviewer</option>
                <option value="advisor">Advisor</option>
            </select>

            <button type="submit">Route Task</button>
        </form>
    </div>
    """
    return BASE_TEMPLATE.format(content=content)


class UnifiedHandler(BaseHTTPRequestHandler):
    """HTTP request handler for unified dashboard."""

    def log_message(self, format, *args):
        """Suppress default logging to keep terminal clean."""
        pass

    def _send_html(self, html: str, status: int = 200):
        """Send HTML response."""
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def _redirect(self, location: str):
        """Send redirect response."""
        self.send_response(303)
        self.send_header("Location", location)
        self.end_headers()

    def _parse_post_data(self) -> dict:
        """Parse POST form data."""
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        parsed = urllib.parse.parse_qs(post_data)
        # parse_qs returns lists, extract single values
        return {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}

    def do_GET(self):
        """Handle GET requests."""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/":
            self._send_html(home_page())
        elif path == "/memory":
            # Check for success message from redirect
            added_id = query.get("added", [None])[0]
            success_msg = f"Added memory entry: {added_id}" if added_id else ""
            self._send_html(memory_page(success_msg))
        elif path == "/route":
            self._send_html(route_page())
        else:
            self._send_html("<h1>404 Not Found</h1>", 404)

    def do_POST(self):
        """Handle POST requests."""
        path = urllib.parse.urlparse(self.path).path
        data = self._parse_post_data()

        if path == "/memory/add":
            entry_type = data.get("type", "context")
            content = data.get("content", "")
            tags_str = data.get("tags", "")
            tags = [t.strip() for t in tags_str.split(",") if t.strip()]

            # Validate entry_type
            valid_types = ["decision", "context", "pattern", "finding"]
            if entry_type not in valid_types:
                entry_type = "context"  # Default to context if invalid

            if content:
                entry_id = add_memory(entry_type, content, tags=tags)
                # Redirect with success message via query param
                self._redirect(f"/memory?added={entry_id[:12]}")
            else:
                self._redirect("/memory")

        elif path == "/route":
            intent = data.get("intent", "")
            task_type = data.get("type", "code")
            role = data.get("role", "lead")

            if intent:
                try:
                    result = route_task(intent, task_type, role)
                    result_dict = {
                        "task_intent": result.task_intent,
                        "model": result.model,
                        "reason": result.reason,
                        "fallback": result.fallback,
                    }
                    self._send_html(route_page(result_dict))
                except Exception as e:
                    self._send_html(f"<h1>Error</h1><p>{e}</p>", 500)
            else:
                self._redirect("/route")
        else:
            self._send_html("<h1>404 Not Found</h1>", 404)


def run_server(port: int = 8765):
    """Run the web dashboard server.

    Args:
        port: Port to bind to (default 8765)
    """
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, UnifiedHandler)
    print(f"Unified Dashboard running at http://127.0.0.1:{port}")
    print("Press Ctrl+C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        httpd.shutdown()
