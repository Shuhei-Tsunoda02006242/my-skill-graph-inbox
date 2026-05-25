#!/usr/bin/env python3
"""
新着 .md ファイルを全件まとめて1回のGemini APIコールで日本語翻訳する。
"""

import os
import sys
import re
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL = "gemini-2.0-flash"

SEPARATOR = "===FILE==="


def needs_translation(path: str) -> bool:
    content = open(path).read()
    return "主な主張" not in content and "根拠・背景" not in content


def batch_translate(files: list[str]) -> dict[str, str]:
    """全ファイルを1リクエストで翻訳して {filename: translated_content} を返す。"""

    combined = ""
    for path in files:
        combined += f"{SEPARATOR} {os.path.basename(path)}\n"
        combined += open(path).read()
        combined += "\n"

    prompt = f"""以下は複数のMarkdownファイルです。各ファイルを日本語に翻訳してください。

翻訳ルール：
- フロントマターの title と investment-implication の値を日本語に翻訳する
- ## Key Claim → ## 主な主張 に変更し本文を翻訳
- ## Evidence / Context → ## 根拠・背景 に変更し本文を翻訳
- ## My Take → ## 私の見解（<!-- fill in later --> はそのまま）
- ## Links → ## リンク（<!-- fill in later --> はそのまま）
- フロントマターのキー名・tech-tags・companies-mentioned・数値・URLは変更しない
- 各ファイルの区切りは "{SEPARATOR} ファイル名" の形式をそのまま維持する
- ファイル全体（フロントマター含む）を出力すること

{combined}"""

    response = client.models.generate_content(model=MODEL, contents=prompt)
    text = response.text.strip()

    result = {}
    parts = re.split(rf"{re.escape(SEPARATOR)}\s+(\S+\.md)", text)
    for i in range(1, len(parts) - 1, 2):
        filename = parts[i].strip()
        content = parts[i + 1].strip()
        result[filename] = content

    return result


if __name__ == "__main__":
    files = sys.argv[1:]
    if not files:
        print("Usage: translate_inbox.py <file1.md> [file2.md ...]")
        sys.exit(1)

    to_translate = [f for f in files if needs_translation(f)]

    if not to_translate:
        print("All files already translated.")
        sys.exit(0)

    print(f"Translating {len(to_translate)} file(s) in 1 API call...")
    translated = batch_translate(to_translate)

    for path in to_translate:
        filename = os.path.basename(path)
        if filename in translated:
            open(path, "w").write(translated[filename])
            print(f"  ✓ {filename}")
        else:
            print(f"  ✗ {filename} (not found in response)")
