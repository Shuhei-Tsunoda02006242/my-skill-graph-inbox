#!/usr/bin/env python3
"""キャプチャノートからソース別ダイジェスト（+ Gemini批評コメント）を組み立てる。

Usage: build_digest.py <file1.md> [file2.md ...]

出力:
- digest_body.txt          メール本文
- $GITHUB_OUTPUT (あれば)  subject / count
"""

import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

SOURCES = {
    "tc": "TechCrunch",
    "tm": "Techmeme",
    "sn": "STAT News",
    "is": "IEEE Spectrum Neuro",
    "qcr": "Quantum Computing Report",
    "fb": "FierceBiotech",
    "ek": "Electrek",
}
GEMINI_MODELS = ["gemini-2.5-flash", "gemini-2.0-flash"]
JST = timezone(timedelta(hours=9))


def frontmatter_field(field: str, text: str) -> str:
    m = re.search(rf'^{re.escape(field)}:\s*"?(.*?)"?\s*$', text, re.MULTILINE)
    return m.group(1).strip() if m else ""


def section(names: list[str], text: str) -> str:
    """指定見出し（日英どちらか）の本文をコメント除去して返す。"""
    for name in names:
        m = re.search(rf"^## {re.escape(name)}\s*\n(.*?)(?=^## |\Z)",
                      text, re.MULTILINE | re.DOTALL)
        if m:
            body = re.sub(r"<!--.*?-->", "", m.group(1), flags=re.DOTALL).strip()
            if body:
                return body
    return ""


def parse_note(path: str) -> dict:
    text = open(path).read()
    m = re.match(r"\d{4}-\d{2}-\d{2}-([a-z]+)-", os.path.basename(path))
    prefix = m.group(1) if m else ""
    return {
        "source_name": SOURCES.get(prefix, "その他"),
        "title": frontmatter_field("title", text),
        "url": frontmatter_field("source", text),
        "signal": frontmatter_field("signal-strength", text),
        "implication": frontmatter_field("investment-implication", text),
        "claim": section(["主な主張", "Key Claim"], text),
        "my_take": section(["私の見解", "My Take"], text),
    }


def gemini_commentary(source_name: str, articles: list[dict]) -> str:
    """ソース単位の批評コメントを生成。失敗したら空文字（メール送信は止めない）。"""
    key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        return ""
    summary = "\n\n".join(
        f"記事{i + 1}: {a['title']}\n主張: {a['claim']}\n投資含意: {a['implication']}"
        for i, a in enumerate(articles)
    )
    prompt = (
        f"あなたはDeepTech（AI・半導体・量子・バイオ・エネルギー）と投資のクロスドメインアナリストです。"
        f"以下は本日キャプチャした {source_name} の記事要約です。\n\n{summary}\n\n"
        "この記事群への批評コメントを日本語で3〜5文で書いてください。観点: "
        "(1) 誇張・ハイプの可能性 (2) 記事に欠けている文脈 "
        "(3) 投資家として注意すべき点 (4) 記事間に共通するトレンドがあれば指摘。"
        "前置き・見出し・箇条書きは不要で、コメント本文のみを出力してください。"
    )
    payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode()
    for model in GEMINI_MODELS:
        try:
            req = urllib.request.Request(
                "https://generativelanguage.googleapis.com/v1beta/models/"
                f"{model}:generateContent",
                data=payload,
                headers={"Content-Type": "application/json", "x-goog-api-key": key},
            )
            with urllib.request.urlopen(req, timeout=60) as res:
                data = json.load(res)
            text = "".join(
                p.get("text", "")
                for p in data["candidates"][0]["content"]["parts"]
            ).strip()
            if text:
                return text
        except Exception as e:
            print(f"Gemini ({model}) failed: {e}", file=sys.stderr)
    return ""


def main() -> None:
    paths = [p for p in sys.argv[1:] if os.path.isfile(p)]
    notes = [parse_note(p) for p in paths]

    groups: dict[str, list[dict]] = {}
    for name in list(SOURCES.values()) + ["その他"]:
        matched = [n for n in notes if n["source_name"] == name]
        if matched:
            groups[name] = matched

    today = datetime.now(JST).strftime("%Y-%m-%d")
    subject = (
        f"📥 [Skill Graph] デイリーダイジェスト {today}"
        f"（{len(notes)}件 / {len(groups)}ソース）"
    )

    lines = [
        f"📥 Skill Graph Inbox デイリーダイジェスト（{today}）",
        f"全{len(notes)}件 / {len(groups)}ソース",
        "",
    ]
    for source_name, articles in groups.items():
        lines += ["", f"━━━━━ {source_name}（{len(articles)}件）━━━━━", ""]
        for a in articles:
            lines += [
                f"📌 {a['title']}",
                f"シグナル強度: {a['signal']}",
                "",
                "【主な主張】",
                a["claim"] or "（なし）",
                "",
                "【投資含意】",
                a["implication"] or "（なし）",
            ]
            if a["my_take"]:
                lines += ["", "【My Take】", a["my_take"]]
            lines += [f"🔗 {a['url']}", ""]
        commentary = gemini_commentary(source_name, articles)
        if commentary:
            lines += ["🗒 批評コメント（AI生成）:", commentary, ""]

    with open("digest_body.txt", "w") as f:
        f.write("\n".join(lines) + "\n")

    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as f:
            f.write(f"subject={subject}\n")
            f.write(f"count={len(notes)}\n")
    print(f"Built digest: {len(notes)} articles, {len(groups)} sources")


if __name__ == "__main__":
    main()
