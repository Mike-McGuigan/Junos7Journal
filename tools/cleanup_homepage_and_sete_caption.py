#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "site" / "index.html"

SAFE_CAPTION = "Juno's 7 in the marina shortly after Cameron and Sophie joined."
TEXT_EXTS = {".html", ".json", ".md", ".js", ".txt", ".css"}

def clean_sete_captions():
    changed = []
    for base in [ROOT / "site", ROOT / "content", ROOT / "docs"]:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in TEXT_EXTS:
                continue

            text = path.read_text(encoding="utf-8")
            original = text

            direct_replacements = [
                "Juno’s 7 with her chase boat SETE nearby.",
                "Juno's 7 with her chase boat SETE nearby.",
                "Juno’s 7 with SETE nearby.",
                "Juno's 7 with SETE nearby.",
                "Juno’s 7 and her chase boat SETE.",
                "Juno's 7 and her chase boat SETE.",
                "Juno’s 7 with her chase boat SETE.",
                "Juno's 7 with her chase boat SETE.",
            ]
            for phrase in direct_replacements:
                text = text.replace(phrase, SAFE_CAPTION)

            text = re.sub(
                r'("caption"\s*:\s*")([^"]*Juno[^"]*SETE[^"]*)(")',
                lambda m: m.group(1) + SAFE_CAPTION.replace('"', '\\"') + m.group(3),
                text,
                flags=re.I
            )
            text = re.sub(
                r'("title"\s*:\s*")([^"]*Juno[^"]*SETE[^"]*)(")',
                lambda m: m.group(1) + "Juno's 7 in the marina" + m.group(3),
                text,
                flags=re.I
            )
            text = re.sub(
                r'("alt"\s*:\s*")([^"]*Juno[^"]*SETE[^"]*)(")',
                lambda m: m.group(1) + "Juno's 7 in the marina" + m.group(3),
                text,
                flags=re.I
            )
            text = re.sub(
                r'Juno[’\']s 7[^.]{0,90}\bSETE\b[^.]{0,90}\.',
                SAFE_CAPTION,
                text,
                flags=re.I
            )

            if text != original:
                path.with_suffix(path.suffix + ".bak-0-7-5").write_text(original, encoding="utf-8")
                path.write_text(text, encoding="utf-8")
                changed.append(path.relative_to(ROOT).as_posix())
    return changed

def replace_homepage_voyage_area():
    if not INDEX.exists():
        raise SystemExit("site/index.html not found")

    html = INDEX.read_text(encoding="utf-8")
    original = html
    INDEX.with_suffix(".html.bak-0-7-5").write_text(original, encoding="utf-8")

    html = html.replace('href="#voyage"', 'href="voyage.html"')
    html = html.replace("href='#voyage'", "href='voyage.html'")

    replacement = '''
<section id="voyage" class="section">
  <div class="wrap">
    <p class="kicker">Voyage So Far</p>
    <h2>The live voyage dashboard</h2>
    <p class="lead">The interactive route map now lives on its own dashboard page, with satellite mapping, latest known position, tracker status and route timeline.</p>
    <p><a class="button" href="voyage.html">Open Voyage Dashboard</a></p>
  </div>
</section>
'''

    html = re.sub(
        r'<div\s+class=["\']voyage-dashboard-cta["\'][\s\S]*?</div>',
        '',
        html,
        flags=re.I
    )

    section_re = re.compile(
        r'<section\b[^>]*>[\s\S]*?(?:Voyage\s+So\s+Far|voyage-map|route-map|svg-route|timeline-grid)[\s\S]*?</section>',
        re.I
    )
    matches = list(section_re.finditer(html))

    if matches:
        match = max(matches, key=lambda m: m.end() - m.start())
        html = html[:match.start()] + replacement + html[match.end():]
        mode = "Replaced likely old Voyage So Far section."
    else:
        if "The live voyage dashboard" not in html:
            html = html.replace("</body>", replacement + "\n</body>")
        mode = "Could not identify old map section; inserted clean dashboard link."

    INDEX.write_text(html, encoding="utf-8")
    return mode

def main():
    caption_files = clean_sete_captions()
    homepage_result = replace_homepage_voyage_area()

    print(homepage_result)
    if caption_files:
        print("Corrected likely SETE photo-caption references in:")
        for f in caption_files:
            print(f"- {f}")
    else:
        print("No likely SETE photo-caption references found by the cleanup script.")
        print("Run this to see remaining SETE references:")
        print("  grep -R \"SETE\" site content docs")

if __name__ == "__main__":
    main()
