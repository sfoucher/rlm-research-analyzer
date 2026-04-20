#!/usr/bin/env python3
"""Convert an RLM synthesis markdown file to a styled PDF via weasyprint.

Usage:
    python make_pdf.py --collection "TMART" --date "2026-04-11" \
        --input /path/to/rlm_answer_tmart.md \
        --output /path/to/rlm_answer_tmart.pdf
"""
import argparse
from pathlib import Path
import markdown
from weasyprint import HTML


def main():
    parser = argparse.ArgumentParser(
        description="Render an RLM synthesis markdown file to a styled PDF."
    )
    parser.add_argument("--collection", required=True, help="Collection name (used in running header)")
    parser.add_argument("--date",       required=True, help="Synthesis date (used in running header)")
    parser.add_argument("--input",      required=True, help="Path to input .md file")
    parser.add_argument("--output",     required=True, help="Path to output .pdf file")
    args = parser.parse_args()

    _css_cname  = args.collection.replace('\\', '\\\\').replace('"', '\\"')
    _css_date   = args.date.replace('\\', '\\\\').replace('"', '\\"')
    _html_cname = args.collection.replace('{', '{{').replace('}', '}}')

    md_file  = Path(args.input)
    pdf_file = Path(args.output)

    md_text    = md_file.read_text(encoding="utf-8")
    md_engine  = markdown.Markdown(extensions=["tables", "fenced_code", "extra"])
    body_html  = md_engine.convert(md_text)

    CSS_TEMPLATE = """
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;0,700;1,400&family=Source+Sans+3:wght@400;600;700&family=Source+Code+Pro:wght@400&display=swap');

@page {
    size: A4;
    margin: 27mm 22mm 24mm 28mm;
    @top-left {
        content: "Synthesis: __CNAME__";
        font-family: 'Source Sans 3', 'Segoe UI', Calibri, sans-serif;
        font-size: 7.5pt; color: #7a8a9a;
        padding-bottom: 4pt; border-bottom: 0.5pt solid #c0ccd8;
        vertical-align: bottom;
    }
    @top-right {
        content: "__DATE__";
        font-family: 'Source Sans 3', 'Segoe UI', Calibri, sans-serif;
        font-size: 7.5pt; color: #7a8a9a;
        padding-bottom: 4pt; border-bottom: 0.5pt solid #c0ccd8;
        vertical-align: bottom;
    }
    @bottom-center {
        content: counter(page) " \2014 " counter(pages);
        font-family: 'Source Sans 3', 'Segoe UI', Calibri, sans-serif;
        font-size: 7.5pt; color: #7a8a9a;
    }
}
@page :first {
    @top-left  { content: ""; border: none; }
    @top-right { content: ""; border: none; }
}
body {
    font-family: 'Lora', Georgia, 'Times New Roman', serif;
    font-size: 10.5pt; line-height: 1.72; color: #1c1c1e;
}
h1 {
    font-family: 'Source Sans 3', 'Segoe UI', Calibri, sans-serif;
    font-size: 24pt; font-weight: 700; color: #0d2b4e;
    margin: 0 0 6pt 0; padding-bottom: 6pt;
    border-bottom: 2pt solid #0d2b4e; page-break-after: avoid;
}
h2 {
    font-family: 'Source Sans 3', 'Segoe UI', Calibri, sans-serif;
    font-size: 13pt; font-weight: 700; color: #0d2b4e;
    margin: 22pt 0 5pt 0; padding-bottom: 3pt;
    border-bottom: 1pt solid #b8cce0; page-break-after: avoid;
}
h3 {
    font-family: 'Source Sans 3', 'Segoe UI', Calibri, sans-serif;
    font-size: 10.5pt; font-weight: 600; color: #1e4a7a;
    margin: 16pt 0 3pt 0; page-break-after: avoid;
}
h4 {
    font-family: 'Source Sans 3', 'Segoe UI', Calibri, sans-serif;
    font-size: 10pt; font-weight: 600; color: #3a3a3a;
    margin: 10pt 0 2pt 0;
}
p { margin: 0 0 7pt 0; text-align: justify; }
ul, ol { margin: 3pt 0 7pt 0; padding-left: 1.6em; }
li { margin-bottom: 4pt; line-height: 1.65; text-align: justify; }
li > ul, li > ol { margin: 2pt 0 2pt 0; }
a { color: #1558a0; text-decoration: none; }
code {
    font-family: 'Source Code Pro', Consolas, 'Courier New', monospace;
    font-size: 8.5pt; background: #f1f4f7;
    border: 0.5pt solid #d4dbe2; border-radius: 2pt; padding: 0.5pt 3pt;
}
pre {
    background: #f1f4f7; border: 0.5pt solid #d4dbe2; border-radius: 3pt;
    padding: 8pt 10pt; font-size: 8.5pt; line-height: 1.5;
    page-break-inside: avoid;
}
pre code { background: none; border: none; padding: 0; }
table {
    width: 100%; border-collapse: collapse;
    font-family: 'Source Sans 3', 'Segoe UI', Calibri, sans-serif;
    font-size: 8.5pt; line-height: 1.5; margin: 10pt 0;
    page-break-inside: avoid;
}
thead tr { background: #0d2b4e; color: #ffffff; }
th { text-align: left; padding: 5pt 7pt; font-weight: 600; }
td { padding: 4pt 7pt; border-bottom: 0.5pt solid #d4dbe2; vertical-align: top; }
tbody tr:nth-child(even) td { background: #f5f8fb; }
hr { border: none; border-top: 0.75pt solid #d4dbe2; margin: 14pt 0; }
blockquote {
    margin: 8pt 0; padding: 4pt 12pt;
    border-left: 3pt solid #1558a0; background: #f5f8fb;
    color: #3a3a3a; font-style: italic;
}
blockquote p { margin: 0; }
strong { font-weight: 700; color: #0d1f33; }
h3 + ul, h3 + ol { page-break-before: avoid; }
"""
    CSS  = CSS_TEMPLATE.replace("__CNAME__", _css_cname).replace("__DATE__", _css_date)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Synthesis: {_html_cname}</title>
  <style>{CSS}</style>
</head>
<body>{body_html}</body>
</html>"""

    print(f"Rendering {md_file.name} -> {pdf_file.name} ...")
    HTML(string=html, base_url=str(md_file.parent)).write_pdf(str(pdf_file))
    print(f"Done. PDF written to: {pdf_file} ({pdf_file.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
