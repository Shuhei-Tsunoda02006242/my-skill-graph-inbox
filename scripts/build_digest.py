#!/usr/bin/env python3
"""キャプチャノートからソース別ダイジェスト（+ Gemini批評コメント）を組み立てて、
ソースごとに1通ずつメール送信する。

Usage: build_digest.py <file1.md> [file2.md ...]

環境変数:
- GMAIL_USERNAME / GMAIL_APP_PASSWORD  SMTP認証情報（送受信とも同一アドレス）
- GEMINI_API_KEY                       批評コメント生成用（無くても継続）
- DRY_RUN=1                            SMTP送信せず、件名・本文を標準出力するのみ

出力:
- $GITHUB_OUTPUT (あれば)  count
"""

import os
import re
import smtplib
import sys
import json
import urllib.request
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage

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


def load_claude_commentary() -> dict[str, str]:
    """キャプチャループ（Claude）が書いた本日の批評コメントをソース別に読む。"""
    today = datetime.now(JST).strftime("%Y-%m-%d")
    path = f"digests/{today}-commentary.md"
    if not os.path.isfile(path):
        return {}
    text = open(path).read()
    result = {}
    for m in re.finditer(r"^## (.+?)\s*\n(.*?)(?=^## |\Z)",
                         text, re.MULTILINE | re.DOTALL):
        body = m.group(2).strip()
        if body:
            result[m.group(1).strip()] = body
    return result


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


def build_body(source_name: str, articles: list[dict], commentary: str, commentary_label: str) -> str:
    lines = [
        f"{source_name}（{len(articles)}件）",
        "",
    ]
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
    if commentary:
        lines += [f"🗒 批評コメント（{commentary_label}）:", commentary, ""]
    return "\n".join(lines) + "\n"


def send_emails(groups: dict[str, list[dict]], claude_comments: dict[str, str]) -> None:
    dry_run = os.environ.get("DRY_RUN") == "1"
    username = os.environ["GMAIL_USERNAME"]
    password = os.environ.get("GMAIL_APP_PASSWORD", "")
    today = datetime.now(JST).strftime("%Y-%m-%d")

    messages = []
    for source_name, articles in groups.items():
        commentary = claude_comments.get(source_name)
        if commentary:
            label = "Claude"
        else:
            commentary = gemini_commentary(source_name, articles)
            label = "Gemini生成"

        subject = f"📥 [{source_name}] デイリーキャプチャ {today}（{len(articles)}件）"
        body = build_body(source_name, articles, commentary, label)
        messages.append((subject, body))

    if dry_run:
        for subject, body in messages:
            print("=" * 60)
            print(f"Subject: {subject}")
            print("-" * 60)
            print(body)
        return

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(username, password)
        for subject, body in messages:
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = f"Skill Graph Inbox <{username}>"
            msg["To"] = username
            msg.set_content(body, charset="utf-8")
            smtp.send_message(msg)
            print(f"Sent: {subject}")


def main() -> None:
    paths = [p for p in sys.argv[1:] if os.path.isfile(p)]
    notes = [parse_note(p) for p in paths]

    groups: dict[str, list[dict]] = {}
    for name in list(SOURCES.values()) + ["その他"]:
        matched = [n for n in notes if n["source_name"] == name]
        if matched:
            groups[name] = matched

    claude_comments = load_claude_commentary()

    send_emails(groups, claude_comments)

    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as f:
            f.write(f"count={len(notes)}\n")
    print(f"Built digest: {len(notes)} articles, {len(groups)} sources")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"build_digest failed: {e}", file=sys.stderr)
        sys.exit(1)
