#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "site" / "index.html"

def main():
    if not INDEX.exists():
        raise SystemExit("site/index.html not found")

    text = INDEX.read_text(encoding="utf-8")
    INDEX.with_suffix(".html.bak-1-0-0-nav").write_text(text, encoding="utf-8")

    if 'href="about.html"' not in text:
        if '<a href="voyage.html">Voyage So Far</a>' in text:
            text = text.replace(
                '<a href="voyage.html">Voyage So Far</a>',
                '<a href="voyage.html">Voyage So Far</a><a href="about.html">About Juno\\\'s 7</a><a href="crew.html">Meet the Crew</a>'
            )
        else:
            text = text.replace('</nav>', '<a href="about.html">About Juno\\\'s 7</a><a href="crew.html">Meet the Crew</a></nav>')

    INDEX.write_text(text, encoding="utf-8")
    print("Homepage navigation patched with About and Crew links.")

if __name__ == "__main__":
    main()
