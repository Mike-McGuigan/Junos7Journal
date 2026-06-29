#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
index = ROOT / "site" / "index.html"

text = index.read_text(encoding="utf-8")

css_line = '<link rel="stylesheet" href="assets/css/version.css">'
js_line = '<script src="assets/js/version.js"></script>'

if css_line not in text:
    text = text.replace('</head>', f'  {css_line}\n</head>')

if js_line not in text:
    text = text.replace('</body>', f'{js_line}\n</body>')

index.write_text(text, encoding="utf-8")
print("Patched site/index.html for version display.")
