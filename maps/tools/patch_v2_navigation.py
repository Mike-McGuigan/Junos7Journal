#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [ROOT/'site'/'index.html', ROOT/'site'/'voyage.html', ROOT/'site'/'about.html', ROOT/'site'/'crew.html']

def patch(path):
    if not path.exists(): return False
    text = path.read_text(encoding='utf-8')
    original = text
    path.with_suffix(path.suffix + '.bak-2-0-0-nav').write_text(text, encoding='utf-8')
    text = text.replace("About Juno\\'s 7", "About Juno's 7").replace("Manual Location", "Captain's Dashboard")
    if 'href="admin.html"' not in text and '</nav>' in text:
        text = text.replace('</nav>', '<a href="admin.html">Captain\'s Dashboard</a></nav>', 1)
    if text != original:
        path.write_text(text, encoding='utf-8')
        return True
    return False

def main():
    changed=[p.relative_to(ROOT).as_posix() for p in FILES if patch(p)]
    print('v2 navigation patched:')
    for item in changed: print(f'- {item}')

if __name__ == '__main__':
    main()
