#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "site" / "index.html"

REPLACEMENT = """
<section id="voyage" class="section">
  <div class="wrap">
    <p class="kicker">Voyage So Far</p>
    <h2>The live voyage dashboard</h2>
    <p class="lead">The interactive route map has moved to its own dashboard page, with satellite mapping, latest known position, tracker status and the route timeline.</p>
    <div class="voyage-dashboard-cta">
      <p class="kicker">Live Map</p>
      <h3>Open the Voyage Dashboard</h3>
      <p>View the current route, latest AIS summary and the growing Mediterranean track.</p>
      <a href="voyage.html">Open Voyage Dashboard</a>
    </div>
  </div>
</section>
"""

def find_section_bounds(text):
    m = re.search(r'<section\b[^>]*\bid=["\']voyage["\'][^>]*>', text, flags=re.I)
    if not m:
        return None
    start = m.start()
    pos = m.end()
    depth = 1
    tag_re = re.compile(r'</?section\b[^>]*>', flags=re.I)
    for tag in tag_re.finditer(text, pos):
        token = tag.group(0).lower()
        if token.startswith("</section"):
            depth -= 1
            if depth == 0:
                return start, tag.end()
        else:
            depth += 1
    return None

def main():
    if not INDEX.exists():
        raise SystemExit("site/index.html not found")
    text = INDEX.read_text(encoding="utf-8")
    INDEX.with_suffix(".html.bak-0-7-2").write_text(text, encoding="utf-8")
    text = text.replace('href="#voyage"', 'href="voyage.html"').replace("href='#voyage'", "href='voyage.html'")
    bounds = find_section_bounds(text)
    if bounds:
        start, end = bounds
        text = text[:start] + REPLACEMENT + text[end:]
        print("Replaced old homepage voyage section.")
    else:
        text = text.replace("</body>", REPLACEMENT + "\n</body>")
        print("Could not find section id=voyage; inserted dashboard CTA before </body>.")
    INDEX.write_text(text, encoding="utf-8")
    print("Backup written beside site/index.html")

if __name__ == "__main__":
    main()
