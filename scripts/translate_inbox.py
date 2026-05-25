#!/usr/bin/env python3
"""
新着 .md ファイルを deep-translator (Google Translate) で日本語翻訳する。
APIキー不要・完全無料。
"""

import os
import sys
import re
from deep_translator import GoogleTranslator

translator = GoogleTranslator(source="en", target="ja")

SECTION_MAP = {
    "## Key Claim": "## 主な主張",
    "## Evidence / Context": "## 根拠・背景",
    "## My Take": "## 私の見解",
    "## Links": "## リンク",
}


def translate_text(text: str) -> str:
    """4500文字ごとにチャンクして翻訳（Google上限対応）。"""
    if not text.strip():
        return text
    chunks = [text[i:i+4500] for i in range(0, len(text), 4500)]
    return "".join(translator.translate(c) for c in chunks)


def needs_translation(path: str) -> bool:
    content = open(path).read()
    return "主な主張" not in content and "根拠・背景" not in content


def translate_frontmatter_field(field: str, content: str) -> str:
    pattern = rf'^({re.escape(field)}:\s*")([^"]+)(")'
    m = re.search(pattern, content, re.MULTILINE)
    if m:
        translated = translate_text(m.group(2))
        content = content[:m.start()] + f'{m.group(1)}{translated}{m.group(3)}' + content[m.end():]
    return content


def translate_section_body(header_ja: str, content: str) -> str:
    """セクション本文（コメント以外）を翻訳する。"""
    pattern = rf"(^{re.escape(header_ja)}\n)(.*?)(?=\n## |\Z)"
    m = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    if m:
        body = m.group(2).strip()
        if body and not body.startswith("<!--"):
            translated_body = translate_text(body)
            content = content[:m.start(2)] + translated_body + "\n" + content[m.end(2):]
    return content


def process_file(path: str) -> None:
    content = open(path).read()

    # フロントマター翻訳
    content = translate_frontmatter_field("title", content)
    content = translate_frontmatter_field("investment-implication", content)

    # セクションヘッダー置換
    for en, ja in SECTION_MAP.items():
        content = content.replace(en, ja)

    # 本文翻訳
    content = translate_section_body("## 主な主張", content)
    content = translate_section_body("## 根拠・背景", content)

    open(path, "w").write(content)
    print(f"  ✓ {os.path.basename(path)}")


if __name__ == "__main__":
    files = sys.argv[1:]
    if not files:
        print("Usage: translate_inbox.py <file1.md> [file2.md ...]")
        sys.exit(1)

    to_translate = [f for f in files if needs_translation(f)]

    if not to_translate:
        print("All files already translated.")
        sys.exit(0)

    print(f"Translating {len(to_translate)} file(s)...")
    for path in to_translate:
        process_file(path)
