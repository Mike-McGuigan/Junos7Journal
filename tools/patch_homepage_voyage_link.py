#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "site" / "index.html"

CTA = '''
<div class="voyage-dashboard-cta">
  <p class="kicker">Voyage Dashboard</p>
  <h3>Voyage So Far has moved</h3>
  <p>The live voyage dashboard now contains the interactive map, latest known position, tracker status and route timeline.</p>
  <a href="voyage.html">Open the Voyage Dashboard</a>
</div>
'''

def main():
    if not INDEX.exists():
        raise SystemExit("site/index.html not found")
    text = INDEX.read_text(encoding="utf-8")
    backup = INDEX.with_suffix(".html.bak-0-7-1")
    backup.write_text(text, encoding="utf-8")
    text = text.replace('href="#voyage"', 'href="voyage.html"')
    text = text.replace("href='#voyage'", "href='voyage.html'")
    if "voyage-dashboard-cta" not in text:
        markers = ['<section id="voyage"', "<section id='voyage'", 'id="voyage"', "id='voyage'"]
        inserted = False
        for marker in markers:
            pos = text.find(marker)
            if pos != -1:
                close = text.find(">", pos)
                if close != -1:
                    text = text[:close+1] + "\n" + CTA + "\n" + text[close+1:]
                    inserted = True
                    break
        if not inserted:
            text = text.replace("</body>", CTA + "\n</body>")
    INDEX.write_text(text, encoding="utf-8")
    print("Patched site/index.html")
    print(f"Backup written to {backup}")

if __name__ == "__main__":
    main()