#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = {
    "Juno’s 7 with her chase boat SETE nearby.": "Juno’s 7 in the marina shortly after Cameron and Sophie joined.",
    "Juno's 7 with her chase boat SETE nearby.": "Juno's 7 in the marina shortly after Cameron and Sophie joined.",
    "Juno’s 7 with SETE nearby.": "Juno’s 7 in the marina shortly after Cameron and Sophie joined.",
    "Juno's 7 with SETE nearby.": "Juno's 7 in the marina shortly after Cameron and Sophie joined.",
    "Juno’s 7 and her chase boat SETE.": "Juno’s 7 in the marina shortly after Cameron and Sophie joined.",
    "Juno's 7 and her chase boat SETE.": "Juno's 7 in the marina shortly after Cameron and Sophie joined.",
    "with her chase boat SETE nearby": "in the marina shortly after Cameron and Sophie joined",
    "with SETE nearby": "in the marina shortly after Cameron and Sophie joined"
}

SEARCH_DIRS = [
    ROOT / "site",
    ROOT / "content",
    ROOT / "docs"
]

FILE_EXTENSIONS = {".json", ".html", ".md", ".js", ".txt"}

def main():
    changed_files = []

    for base in SEARCH_DIRS:
        if not base.exists():
            continue

        for path in base.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in FILE_EXTENSIONS:
                continue

            text = path.read_text(encoding="utf-8")
            new_text = text

            for old, new in REPLACEMENTS.items():
                new_text = new_text.replace(old, new)

            if new_text != text:
                backup = path.with_suffix(path.suffix + ".bak-0-7-4")
                backup.write_text(text, encoding="utf-8")
                path.write_text(new_text, encoding="utf-8")
                changed_files.append(path.relative_to(ROOT).as_posix())

    if changed_files:
        print("Corrected SETE caption references in:")
        for item in changed_files:
            print(f"- {item}")
    else:
        print("No matching SETE photo captions found.")
        print("This is safe. The caption may already have been corrected, or the wording is slightly different.")
        print("Search your repo for SETE to verify remaining references are only in vessel/tracker context.")

if __name__ == "__main__":
    main()
