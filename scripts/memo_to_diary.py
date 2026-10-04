#!/usr/bin/env python3
"""iPhoneメモ（00-Inbox/YYYY-MM-DD-HHMMSS-memo.md）をローカル日記へ追記する。

Usage:
    memo_to_diary.py <memo.md> <diary_entries_dir>

日記 <dir>/YYYY-MM-DD.md の `## タグ` 見出しの直前に `## iPhoneメモ HH:MM` セクションを
挿入する（`## タグ` が無ければ末尾に追記、日付ファイルが無ければ新規作成）。
同一の見出し+本文が既にあれば何もしない（冪等）。成功時は exit 0、失敗時は非0。
システムの /usr/bin/python3（3.9）で動くよう新しい構文は使わない。
"""

import os
import re
import sys


def memo_body(text: str) -> str:
    """frontmatterと `## Memo` 見出しを除いた本文を返す。"""
    text = re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.DOTALL)
    text = re.sub(r"^## Memo[ \t]*\n", "", text.lstrip("\n"), count=1)
    return text.strip()


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: memo_to_diary.py <memo.md> <diary_entries_dir>", file=sys.stderr)
        return 2
    memo_path, diary_dir = sys.argv[1], sys.argv[2]
    m = re.match(r"(\d{4}-\d{2}-\d{2})-(\d{2})(\d{2})\d{2}-memo\.md$", os.path.basename(memo_path))
    if not m:
        print("memoファイル名が想定形式ではありません: %s" % memo_path, file=sys.stderr)
        return 2
    date, hh, mm = m.group(1), m.group(2), m.group(3)

    with open(memo_path, encoding="utf-8") as f:
        body = memo_body(f.read())
    if not body:
        print("本文が空のためスキップ: %s" % memo_path, file=sys.stderr)
        return 0

    block = "## iPhoneメモ %s:%s\n%s\n" % (hh, mm, body)
    day_file = os.path.join(diary_dir, date + ".md")

    if os.path.exists(day_file):
        with open(day_file, encoding="utf-8") as f:
            text = f.read()
        if block in text:
            return 0
        tags = list(re.finditer(r"^## タグ[ \t]*$", text, re.MULTILINE))
        if tags:
            pos = tags[-1].start()
            head = text[:pos].rstrip("\n")
            new = head + "\n\n" + block + "\n" + text[pos:]
        else:
            new = text.rstrip("\n") + "\n\n" + block
    else:
        os.makedirs(diary_dir, exist_ok=True)
        new = "# %s\n\n%s\n## タグ\n" % (date, block)

    tmp = day_file + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(new)
    os.replace(tmp, day_file)
    return 0


if __name__ == "__main__":
    sys.exit(main())
