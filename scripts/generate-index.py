#!/usr/bin/env python3
"""Regenerate index.html navigation page from all *.html files in repo root."""
import re
import html
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
EXCLUDE = {"index.html"}


def extract_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"<title[^>]*>(.*?)</title>", text, re.IGNORECASE | re.DOTALL)
    if m:
        title = re.sub(r"\s+", " ", m.group(1)).strip()
        if title:
            return title
    return path.stem


def extract_desc(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(
        r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
        text,
        re.IGNORECASE,
    )
    return m.group(1).strip() if m else ""


def main():
    files = sorted(p for p in ROOT.glob("*.html") if p.name not in EXCLUDE)
    cards = []
    for p in files:
        title = html.escape(extract_title(p))
        desc = html.escape(extract_desc(p))
        href = quote(p.name)
        desc_html = f'\n      <div class="desc">{desc}</div>' if desc else ""
        cards.append(
            f'    <a class="card" href="{href}">\n'
            f'      <div class="title">{title}</div>{desc_html}\n'
            f'    </a>'
        )
    cards_html = "\n\n".join(cards)

    index = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Reports · zhangwenwei</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;background:#0d1117;color:#e6edf3;min-height:100vh;padding:24px 16px;line-height:1.6}}
  .wrap{{max-width:760px;margin:0 auto}}
  header{{padding:24px 8px 32px;border-bottom:1px solid #30363d;margin-bottom:24px}}
  h1{{font-size:28px;font-weight:700;margin-bottom:8px}}
  .sub{{color:#7d8590;font-size:14px}}
  .grid{{display:grid;gap:14px}}
  a.card{{display:block;padding:18px 20px;background:#161b22;border:1px solid #30363d;border-radius:12px;text-decoration:none;color:inherit;transition:all .15s ease}}
  a.card:hover,a.card:active{{border-color:#58a6ff;background:#1c2128;transform:translateY(-1px)}}
  .title{{font-size:17px;font-weight:600;color:#e6edf3;margin-bottom:4px}}
  .desc{{font-size:13px;color:#7d8590}}
  footer{{margin-top:40px;padding:20px 8px;text-align:center;color:#7d8590;font-size:12px;border-top:1px solid #30363d}}
  footer a{{color:#58a6ff;text-decoration:none}}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>📚 Reports</h1>
    <div class="sub">个人 HTML 报告与资料合集 · 共 {len(files)} 篇</div>
  </header>

  <div class="grid">
{cards_html}
  </div>

  <footer>
    Hosted on GitHub Pages · <a href="https://github.com/zhangwenwei/report">View Repository</a>
  </footer>
</div>
</body>
</html>
"""

    (ROOT / "index.html").write_text(index, encoding="utf-8")
    print(f"Generated index.html with {len(files)} entries")


if __name__ == "__main__":
    main()
