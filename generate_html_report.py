
"""Generate HTML reports from Pylint JSON results."""

import html
import json
import sys
from pathlib import Path


def read_json_report(input_path):
    """Read a JSON file using compatible text encodings."""
    raw_data = Path(input_path).read_bytes()

    encodings = ["utf-8-sig", "utf-16", "utf-16-le", "utf-16-be"]

    for encoding in encodings:
        try:
            content = raw_data.decode(encoding)
            return json.loads(content)
        except (UnicodeError, json.JSONDecodeError):
            continue

    raise ValueError(
        f"Unable to read {input_path}. "
        "The file is not valid JSON or uses an unsupported encoding."
    )


def generate_report(input_path, output_path):
    """Convert a Pylint JSON report into an HTML document."""
    issues = read_json_report(input_path)

    if not isinstance(issues, list):
        raise ValueError("Expected a list of Pylint issues.")

    rows = []

    for issue in issues:
        cells = [
            issue["type"],
            issue["symbol"],
            issue["message"],
            str(issue["line"]),
        ]

        columns = "".join(
            f"<td>{html.escape(str(value))}</td>"
            for value in cells
        )

        rows.append(f"<tr>{columns}</tr>")

    table_rows = "\n".join(rows)

    if not table_rows:
        table_rows = (
            '<tr><td colspan="4">No issues found</td></tr>'
        )

    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pylint Analysis Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f8f9fa;
        }}

        h1 {{
            color: #253858;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            background-color: white;
        }}

        th, td {{
            border: 1px solid #ccc;
            padding: 10px;
            text-align: left;
        }}

        th {{
            background-color: #253858;
            color: white;
        }}

        tr:nth-child(even) {{
            background-color: #f2f2f2;
        }}
    </style>
</head>
<body>
    <h1>Pylint Analysis Report</h1>

    <p><strong>Source:</strong>
        {html.escape(str(input_path))}
    </p>

    <p><strong>Total issues detected:</strong> {len(issues)}</p>

    <table>
        <tr>
            <th>Type</th>
            <th>Rule</th>
            <th>Message</th>
            <th>Line</th>
        </tr>
        {table_rows}
    </table>
</body>
</html>"""

    Path(output_path).write_text(document, encoding="utf-8")
    print(f"HTML report generated: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python generate_html_report.py "
            "INPUT.json OUTPUT.html"
        )
        sys.exit(1)

    try:
        generate_report(sys.argv[1], sys.argv[2])
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Error: {error}")
        sys.exit(1)
