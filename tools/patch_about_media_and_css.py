#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "site" / "index.html"

def main():
    if INDEX.exists():
        text = INDEX.read_text(encoding="utf-8")
        INDEX.with_suffix(".html.bak-1-0-4").write_text(text, encoding="utf-8")
        text = text.replace("About Juno\\'s 7", "About Juno's 7")
        text = text.replace("About Juno&amp;#x27;s 7", "About Juno's 7")
        text = text.replace("About Juno&#x27;s 7", "About Juno's 7")
        text = text.replace("About Juno&#39;s 7", "About Juno's 7")
        INDEX.write_text(text, encoding="utf-8")
        print("Fixed homepage nav apostrophe escaping where present.")
    print("About page and companion CSS supplied by this release.")
if __name__ == "__main__":
    main()