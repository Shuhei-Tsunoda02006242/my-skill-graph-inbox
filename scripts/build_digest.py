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

import html
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

# ソース別アクセントカラー（HTMLメールのヘッダー帯・リンク色に使用）。
# 未知ソースは「その他」にフォールバック。
SOURCE_COLORS = {
    "TechCrunch": "#0a7d33",
    "Techmeme": "#1a73e8",
    "STAT News": "#c5221f",
    "IEEE Spectrum Neuro": "#7627bb",
    "Quantum Computing Report": "#0b8043",
    "FierceBiotech": "#e37400",
    "The Quantum Insider": "#00695c",
    "Electrek": "#188038",
    "その他": "#5f6368",
}

# シグナル強度バッジの配色（背景色, 文字色）
SIGNAL_BADGE_COLORS = {
    "strong": ("#d93025", "#ffffff"),
    "moderate": ("#f9ab00", "#000000"),
    "weak": ("#9aa0a6", "#ffffff"),
    "none": ("#e8eaed", "#5f6368"),
}


def load_sources() -> dict[str, str]:
    """CLAUDE.mdのソーステーブルから prefix→ソース名 を読む。
    ソースは自動追加されるため、固定のSOURCESは読めなかった場合のフォールバック。"""
    sources = dict(SOURCES)
    try:
        text = open(os.path.join(os.path.dirname(__file__), "..", "CLAUDE.md")).read()
        for m in re.finditer(r"^\|\s*`([a-z]+)-`\s*\|\s*([^|]+?)\s*\|",
                             text, re.MULTILINE):
            sources[m.group(1)] = m.group(2).strip()
    except OSError:
        pass
    return sources


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


def parse_note(path: str, sources: dict[str, str]) -> dict:
    text = open(path).read()
    m = re.match(r"\d{4}-\d{2}-\d{2}-([a-z]+)-", os.path.basename(path))
    prefix = m.group(1) if m else ""
    return {
        "source_name": sources.get(prefix, "その他"),
        "title": frontmatter_field("title", text),
        "url": frontmatter_field("source", text),
        "signal": frontmatter_field("signal-strength", text),
        "implication": frontmatter_field("investment-implication", text),
        "position": frontmatter_field("landscape-position", text),
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
        ]
        if a["position"]:
            lines += [f"📍 {a['position']}"]
        lines += [
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


def _esc(text: str) -> str:
    """HTMLエスケープ後、改行を<br>に変換する。"""
    return html.escape(text).replace("\n", "<br>")


def build_html_body(source_name: str, articles: list[dict], commentary: str,
                     commentary_label: str, today: str) -> str:
    """NewsPicks風カードのHTMLメール本文を組み立てる。Gmail対応のためインラインstyleのみ使用。"""
    accent = SOURCE_COLORS.get(source_name, SOURCE_COLORS["その他"])

    parts = [
        '<div style="max-width:600px;margin:0 auto;'
        "font-family:-apple-system,'Hiragino Sans',sans-serif;"
        'background-color:#f1f3f4;padding:16px;">',
        # ヘッダー: ソース別アクセントカラーの帯
        f'<div style="background-color:{accent};border-radius:8px 8px 0 0;'
        'padding:16px;color:#ffffff;">'
        f'<div style="font-size:20px;font-weight:bold;">{html.escape(source_name)}</div>'
        f'<div style="font-size:13px;opacity:0.9;margin-top:4px;">'
        f'{html.escape(today)}（{len(articles)}件）</div>'
        "</div>",
    ]

    for a in articles:
        badge_bg, badge_fg = SIGNAL_BADGE_COLORS.get(
            a["signal"], SIGNAL_BADGE_COLORS["none"]
        )
        card = [
            '<div style="background-color:#ffffff;border:1px solid #dadce0;'
            "border-radius:8px;padding:16px;margin-bottom:12px;margin-top:12px;\">",
            f'<div style="font-size:18px;font-weight:bold;line-height:1.4;">'
            f'<a href="{html.escape(a["url"], quote=True)}" '
            f'style="color:{accent};text-decoration:none;">'
            f'{html.escape(a["title"])}</a></div>',
        ]
        if a["position"]:
            card.append(
                '<div style="font-size:12px;color:#5f6368;margin-top:4px;">'
                f'📍 {html.escape(a["position"])}</div>'
            )
        card.append(
            f'<div style="display:inline-block;background-color:{badge_bg};'
            f"color:{badge_fg};font-size:12px;font-weight:bold;border-radius:12px;"
            f'padding:2px 10px;margin-top:8px;">'
            f'{html.escape(a["signal"] or "none")}</div>'
        )
        card.append(
            '<div style="font-size:14px;font-weight:bold;color:#202124;margin-top:12px;">'
            "【主な主張】</div>"
            f'<div style="font-size:14px;color:#3c4043;line-height:1.6;margin-top:4px;">'
            f'{_esc(a["claim"] or "（なし）")}</div>'
        )
        card.append(
            '<div style="background-color:#fef7e0;border-left:4px solid #f9ab00;'
            'padding:8px 12px;margin-top:12px;">'
            '<div style="font-size:14px;font-weight:bold;color:#202124;">【投資含意】</div>'
            f'<div style="font-size:14px;color:#3c4043;line-height:1.6;margin-top:4px;">'
            f'{_esc(a["implication"] or "（なし）")}</div>'
            "</div>"
        )
        if a["my_take"]:
            card.append(
                '<div style="font-size:14px;font-weight:bold;color:#202124;margin-top:12px;">'
                "【My Take】</div>"
                f'<div style="font-size:14px;color:#3c4043;line-height:1.6;'
                f'font-style:italic;margin-top:4px;">{_esc(a["my_take"])}</div>'
            )
        card.append("</div>")
        parts.append("".join(card))

    if commentary:
        parts.append(
            '<div style="background-color:#f8f9fa;border-radius:8px;padding:16px;'
            'margin-top:4px;">'
            f'<div style="font-size:13px;font-weight:bold;color:#5f6368;">'
            f'🗒 批評コメント（{html.escape(commentary_label)}）</div>'
            f'<div style="font-size:14px;color:#3c4043;line-height:1.6;margin-top:8px;">'
            f'{_esc(commentary)}</div>'
            "</div>"
        )

    parts.append("</div>")
    return "".join(parts)


def send_emails(groups: dict[str, list[dict]], claude_comments: dict[str, str]) -> None:
    dry_run = os.environ.get("DRY_RUN") == "1"
    # シークレット値に末尾改行が入っているとメールヘッダーが弾かれるため必ずstrip
    username = os.environ["GMAIL_USERNAME"].strip()
    password = os.environ.get("GMAIL_APP_PASSWORD", "").strip()
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
        html_body = build_html_body(source_name, articles, commentary, label, today)
        messages.append((subject, body, html_body, source_name))

    if dry_run:
        preview_dir = os.environ.get("TMPDIR", "/tmp")
        sources = load_sources()
        for subject, body, html_body, source_name in messages:
            print("=" * 60)
            print(f"Subject: {subject}")
            print("-" * 60)
            print(body)
            prefix = next(
                (p for p, n in sources.items() if n == source_name), "other"
            )
            preview_path = os.path.join(preview_dir, f"digest_preview_{prefix}.html")
            with open(preview_path, "w", encoding="utf-8") as f:
                f.write(html_body)
            print(f"[DRY_RUN] HTML preview saved: {preview_path}")
        return

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(username, password)
        for subject, body, html_body, source_name in messages:
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = f"Skill Graph Inbox <{username}>"
            msg["To"] = username
            msg.set_content(body, charset="utf-8")
            msg.add_alternative(html_body, subtype="html")
            smtp.send_message(msg)
            print(f"Sent: {subject}")


def dedup_by_url(paths: list[str], sources: dict[str, str]) -> list[dict]:
    """URL重複を除外してパース済みノートを返す。
    複数のキャプチャ経路（クラウドルーチン/ローカル/手動）が同一記事を
    別ファイル名で拾う事故が繰り返し起きているため、送信直前に機械的に弾く。"""
    import glob
    pending = set(paths)
    past_urls = set()
    for p in glob.glob("00-Inbox/*.md"):
        if p in pending:
            continue
        try:
            u = frontmatter_field("source", open(p, errors="ignore").read()).strip()
        except OSError:
            continue
        if u:
            past_urls.add(u)
    notes, seen = [], set()
    for p in sorted(paths):
        note = parse_note(p, sources)
        u = note["url"].strip()
        if u and (u in past_urls or u in seen):
            print(f"Skipped duplicate: {p}")
            continue
        if u:
            seen.add(u)
        notes.append(note)
    return notes


def main() -> None:
    paths = [p for p in sys.argv[1:] if os.path.isfile(p)]
    sources = load_sources()
    notes = dedup_by_url(paths, sources)

    groups: dict[str, list[dict]] = {}
    for name in list(dict.fromkeys(sources.values())) + ["その他"]:
        matched = [n for n in notes if n["source_name"] == name]
        if matched:
            groups[name] = matched

    claude_comments = load_claude_commentary()

    if not notes:
        print("No unique articles to send")
    else:
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
