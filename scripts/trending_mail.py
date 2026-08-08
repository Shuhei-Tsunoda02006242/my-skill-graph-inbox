#!/usr/bin/env python3
"""はてなブックマーク・Qiita・Zenn・Hacker News・Product Hunt の人気記事を取得し、
モバイルで読みやすいHTMLメール1通として送信する（トレンドダイジェスト）。

仕様の出所: dotfiles/claude/commands/trending.md（取得先URL・抽出ルール・除外ルール）。
Xトレンド・YouTubeはローカル専用の取得手段（opencli／ブラウザ拡張、YouTube APIキー）に
依存するため対象外（Actions環境では取得不可能）。

取得ソース（すべて認証不要の公開エンドポイント。opencliは使わない）:
- はてなブックマーク: https://b.hatena.ne.jp/hotentry.rss (RSS/RDF) 上位15件
- Qiita: https://qiita.com/popular-items/feed.atom (Atom) 上位15件
  author が sumomoo/prumnn の記事は除外（ユーザー指定。除外分は繰り上げない）
- Zenn: https://zenn.dev/feed (RSS) 上位15件
- Hacker News: topstories.json → item/{id}.json を個別取得 上位10件
- Product Hunt: https://www.producthunt.com/feed (Atom。RSSで返る可能性にも両対応) 上位10件

あるソースの取得に失敗しても他は続行し、メール本文に「〇〇: 取得失敗」と明記する。
全ソース失敗時は送信せず非ゼロ終了する。

環境変数:
- GMAIL_USERNAME / GMAIL_APP_PASSWORD  SMTP認証情報（build_digest.pyと同じ扱い。末尾改行はstrip）
- DRY_RUN=1                            SMTP送信せず、件名・本文を標準出力するのみ

出力:
- $GITHUB_OUTPUT (あれば)  count（送信したセクションの記事合計数）
"""

import html
import json
import os
import re
import smtplib
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage

JST = timezone(timedelta(hours=9))
UA = "Mozilla/5.0 (compatible; TrendingMailBot/1.0; +https://github.com/Shuhei-Tsunoda02006242/my-skill-graph-inbox)"

NS_RSS1 = "http://purl.org/rss/1.0/"
NS_HATENA = "http://www.hatena.ne.jp/info/xmlns#"
NS_ATOM = "http://www.w3.org/2005/Atom"

def load_exclusions() -> set[str]:
    """除外authorを trending-exclusions.json から読む（このファイルが唯一の正）。

    デスクトップの /trending も同じJSONを読む。dotfilesはremoteが無く
    GitHub Actionsから見えないため、GitHub上にあるこちら側を正とする。
    読めない場合は除外なしで続行する（メールが止まるより混ざるほうがマシ）。
    """
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trending-exclusions.json")
    try:
        with open(path, encoding="utf-8") as f:
            return set(json.load(f).get("qiita_authors", []))
    except (OSError, ValueError) as e:
        print(f"warning: 除外リストを読めませんでした（除外なしで続行）: {e}", file=sys.stderr)
        return set()


EXCLUDE_QIITA_AUTHORS = load_exclusions()


def fetch_bytes(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return res.read()


def strip_html(text: str, max_len: int = 120) -> str:
    """HTMLタグを除去してプレーンテキストに変換し、長すぎる場合は省略する。"""
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_len:
        text = text[:max_len].rstrip() + "…"
    return text


def fetch_hatena(limit: int = 15) -> list[dict]:
    """はてなブックマーク ホットエントリー。RSS 1.0(RDF)形式。"""
    data = fetch_bytes("https://b.hatena.ne.jp/hotentry.rss")
    root = ET.fromstring(data)
    results = []
    for item in root.findall(f"{{{NS_RSS1}}}item")[:limit]:
        title = (item.findtext(f"{{{NS_RSS1}}}title") or "").strip()
        url = (item.findtext(f"{{{NS_RSS1}}}link") or "").strip()
        if not (title and url):
            continue
        count_text = item.findtext(f"{{{NS_HATENA}}}bookmarkcount")
        count = int(count_text) if count_text and count_text.isdigit() else None
        description = strip_html(item.findtext(f"{{{NS_RSS1}}}description") or "")
        results.append({"title": title, "url": url, "count": count, "description": description})
    return results


def fetch_qiita(limit: int = 15) -> list[dict]:
    """Qiita 人気の記事。Atomフィード。指定author（sumomoo/prumnn）の記事は抽出後に除外（繰り上げなし）。"""
    data = fetch_bytes("https://qiita.com/popular-items/feed.atom")
    root = ET.fromstring(data)
    results = []
    for entry in root.findall(f"{{{NS_ATOM}}}entry")[:limit]:
        title = (entry.findtext(f"{{{NS_ATOM}}}title") or "").strip()
        link_el = entry.find(f"{{{NS_ATOM}}}link")
        url = link_el.get("href", "").strip() if link_el is not None else ""
        author_el = entry.find(f"{{{NS_ATOM}}}author/{{{NS_ATOM}}}name")
        author = (author_el.text or "").strip() if author_el is not None and author_el.text else ""
        if not (title and url):
            continue
        results.append({"title": title, "url": url, "author": author})
    return [r for r in results if r["author"] not in EXCLUDE_QIITA_AUTHORS]


def fetch_zenn(limit: int = 15) -> list[dict]:
    """Zennのトレンド。RSS 2.0形式。"""
    data = fetch_bytes("https://zenn.dev/feed")
    root = ET.fromstring(data)
    channel = root.find("channel")
    items = channel.findall("item") if channel is not None else []
    results = []
    for item in items[:limit]:
        title = (item.findtext("title") or "").strip()
        url = (item.findtext("link") or "").strip()
        if not (title and url):
            continue
        description = strip_html(item.findtext("description") or "")
        results.append({"title": title, "url": url, "description": description})
    return results


def fetch_hn(limit: int = 10) -> list[dict]:
    """Hacker News トップストーリー。ID配列取得後、個別取得（計 limit+1 リクエスト）。"""
    ids = json.loads(fetch_bytes("https://hacker-news.firebaseio.com/v0/topstories.json"))[:limit]
    results = []
    for hid in ids:
        item = json.loads(
            fetch_bytes(f"https://hacker-news.firebaseio.com/v0/item/{hid}.json")
        )
        title = (item.get("title") or "").strip()
        if not title:
            continue
        url = item.get("url") or f"https://news.ycombinator.com/item?id={hid}"
        results.append({
            "title": title,
            "url": url,
            "score": item.get("score"),
            "comments": item.get("descendants"),
        })
    return results


def first_paragraph(html_content: str) -> str:
    """<p>タグ区切りのHTML断片から最初の段落だけを抽出する。
    Product Huntのcontentは2段落目に「Discussion | Link」のアンカーテキストが
    続くため、タグを外すだけだとそれが本文に混入してしまう。"""
    m = re.search(r"<p[^>]*>(.*?)</p>", html_content, re.S)
    return strip_html(m.group(1)) if m else strip_html(html_content)


def fetch_producthunt(limit: int = 10) -> list[dict]:
    """Product Hunt フィード。現状はAtom形式で返るが、RSS 2.0で返る可能性にも両対応する。"""
    data = fetch_bytes("https://www.producthunt.com/feed")
    root = ET.fromstring(data)
    results = []
    if root.tag == f"{{{NS_ATOM}}}feed":
        for entry in root.findall(f"{{{NS_ATOM}}}entry")[:limit]:
            title = (entry.findtext(f"{{{NS_ATOM}}}title") or "").strip()
            link_el = entry.find(f"{{{NS_ATOM}}}link")
            url = link_el.get("href", "").strip() if link_el is not None else ""
            content_el = entry.find(f"{{{NS_ATOM}}}content")
            description = first_paragraph(content_el.text) if content_el is not None and content_el.text else ""
            if title and url:
                results.append({"title": title, "url": url, "description": description})
    else:
        channel = root.find("channel")
        items = channel.findall("item") if channel is not None else []
        for item in items[:limit]:
            title = (item.findtext("title") or "").strip()
            url = (item.findtext("link") or "").strip()
            if not (title and url):
                continue
            description = strip_html(item.findtext("description") or "")
            results.append({"title": title, "url": url, "description": description})
    return results


# 表示順・見出し・取得関数（このタプルの順にセクションを組み立てる）
SOURCE_DEFS = [
    ("hatena", "📰 はてなブックマーク", fetch_hatena),
    ("qiita", "💻 Qiita", fetch_qiita),
    ("zenn", "📝 Zenn", fetch_zenn),
    ("hackernews", "🔥 Hacker News", fetch_hn),
    ("producthunt", "🚀 Product Hunt", fetch_producthunt),
]


def fetch_all() -> tuple[dict[str, list[dict]], dict[str, str]]:
    """全ソースを取得する。失敗したソースは results から欠落し、errors に理由が入る。"""
    results: dict[str, list[dict]] = {}
    errors: dict[str, str] = {}
    for key, label, fetch_fn in SOURCE_DEFS:
        try:
            results[key] = fetch_fn()
        except (urllib.error.URLError, urllib.error.HTTPError, ET.ParseError,
                json.JSONDecodeError, TimeoutError, OSError) as e:
            errors[key] = f"{type(e).__name__}: {e}"
            print(f"{label}: 取得失敗 ({errors[key]})", file=sys.stderr)
    return results, errors


def fmt_meta(key: str, article: dict) -> str:
    """ソースごとのメタ情報（はてブ数/HNスコア・コメント数/Qiitaのauthor）を1行に整形する。"""
    if key == "hatena":
        return f"{article['count']}users" if article.get("count") is not None else ""
    if key == "qiita":
        return f"by @{article['author']}" if article.get("author") else ""
    if key == "hackernews":
        bits = []
        if article.get("score") is not None:
            bits.append(f"▲{article['score']}")
        if article.get("comments") is not None:
            bits.append(f"{article['comments']}コメント")
        return " · ".join(bits)
    return ""


def build_text_body(results: dict[str, list[dict]], errors: dict[str, str], fetched_at: str) -> str:
    lines = [f"📈 トレンドダイジェスト", ""]
    for key, label, _ in SOURCE_DEFS:
        lines.append(f"## {label}")
        if key in errors:
            lines.append("（取得失敗）")
            lines.append("")
            continue
        articles = results.get(key, [])
        if not articles:
            lines.append("（該当記事なし）")
            lines.append("")
            continue
        for i, a in enumerate(articles, 1):
            meta = fmt_meta(key, a)
            lines.append(f"{i}. {a['title']}" + (f" — {meta}" if meta else ""))
            lines.append(f"   {a['url']}")
            desc = a.get("description")
            if desc:
                lines.append(f"   {desc}")
        lines.append("")
    lines.append(f"取得時刻: {fetched_at}")
    return "\n".join(lines) + "\n"


def _esc(text: str) -> str:
    return html.escape(text)


def build_article_html(key: str, article: dict) -> str:
    meta = fmt_meta(key, article)
    parts = [
        '<div style="padding:14px 0;border-bottom:1px solid #e8eaed;">',
        f'<a href="{_esc(article["url"])}" '
        'style="display:block;font-size:16px;font-weight:600;line-height:1.5;'
        'color:#1a73e8;text-decoration:none;">'
        f'{_esc(article["title"])}</a>',
    ]
    if meta:
        parts.append(
            f'<div style="font-size:14px;color:#5f6368;margin-top:6px;">{_esc(meta)}</div>'
        )
    description = article.get("description")
    if description:
        parts.append(
            '<div style="font-size:14px;color:#3c4043;line-height:1.6;margin-top:6px;">'
            f'{_esc(description)}</div>'
        )
    parts.append("</div>")
    return "".join(parts)


def build_section_html(key: str, label: str, results: dict[str, list[dict]], errors: dict[str, str]) -> str:
    parts = [
        '<div style="background-color:#ffffff;border-radius:8px;padding:16px;margin-bottom:14px;">',
        f'<div style="font-size:17px;font-weight:bold;color:#202124;margin-bottom:4px;">'
        f'{_esc(label)}</div>',
    ]
    if key in errors:
        parts.append(
            '<div style="background-color:#fef7e0;color:#856404;border-radius:6px;'
            'padding:10px 12px;margin-top:8px;font-size:14px;">'
            f'⚠️ {_esc(label)}: 取得失敗</div>'
        )
    else:
        articles = results.get(key, [])
        if not articles:
            parts.append(
                '<div style="font-size:14px;color:#5f6368;margin-top:8px;">該当記事なし</div>'
            )
        else:
            rows = "".join(build_article_html(key, a) for a in articles)
            parts.append(f'<div style="margin-top:4px;">{rows}</div>')
    parts.append("</div>")
    return "".join(parts)


def build_html_body(results: dict[str, list[dict]], errors: dict[str, str], today: str, fetched_at: str) -> str:
    """モバイル閲覧を主目的にした1カラムHTML本文。Gmail対応のためインラインstyleのみ使用。"""
    parts = [
        '<div style="max-width:600px;margin:0 auto;'
        "font-family:-apple-system,'Hiragino Sans',sans-serif;"
        'background-color:#f1f3f4;padding:12px;">',
        '<div style="background-color:#1a73e8;border-radius:8px;padding:16px;'
        'color:#ffffff;margin-bottom:14px;">'
        '<div style="font-size:20px;font-weight:bold;">📈 トレンドダイジェスト</div>'
        f'<div style="font-size:13px;opacity:0.9;margin-top:4px;">{_esc(today)}</div>'
        "</div>",
    ]
    for key, label, _ in SOURCE_DEFS:
        parts.append(build_section_html(key, label, results, errors))
    parts.append(
        '<div style="text-align:center;color:#9aa0a6;font-size:12px;margin-top:8px;">'
        f'取得時刻: {_esc(fetched_at)}</div>'
    )
    parts.append("</div>")
    return "".join(parts)


def send_email(results: dict[str, list[dict]], errors: dict[str, str]) -> int:
    dry_run = os.environ.get("DRY_RUN") == "1"
    # シークレット値に末尾改行が入っているとメールヘッダーが弾かれるため必ずstrip（build_digest.pyと同様）
    username = os.environ["GMAIL_USERNAME"].strip()
    password = os.environ.get("GMAIL_APP_PASSWORD", "").strip()

    now_jst = datetime.now(JST)
    today = now_jst.strftime("%Y-%m-%d")
    fetched_at = now_jst.strftime("%Y-%m-%d %H:%M JST")

    total = sum(len(v) for v in results.values())
    subject = f"📈 トレンドダイジェスト {today}"
    body = build_text_body(results, errors, fetched_at)
    html_body = build_html_body(results, errors, today, fetched_at)

    if dry_run:
        print("=" * 60)
        print(f"Subject: {subject}")
        print("-" * 60)
        print(body)
        preview_dir = os.environ.get("TMPDIR", "/tmp")
        preview_path = os.path.join(preview_dir, "trending_mail_preview.html")
        with open(preview_path, "w", encoding="utf-8") as f:
            f.write(html_body)
        print(f"[DRY_RUN] HTML preview saved: {preview_path}")
        return total

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"Skill Graph Inbox <{username}>"
    msg["To"] = username
    msg.set_content(body, charset="utf-8")
    msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(username, password)
        smtp.send_message(msg)
    print(f"Sent: {subject}")
    return total


def main() -> None:
    results, errors = fetch_all()

    if len(errors) == len(SOURCE_DEFS):
        print("All sources failed to fetch. Aborting without sending.", file=sys.stderr)
        sys.exit(1)

    for key, _, _ in SOURCE_DEFS:
        count = len(results.get(key, []))
        print(f"{key}: {count} articles" if key not in errors else f"{key}: failed")

    total = send_email(results, errors)

    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as f:
            f.write(f"count={total}\n")
    print(f"Built trending digest: {total} articles across {len(results)} sources"
          f" ({len(errors)} failed)")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"trending_mail failed: {e}", file=sys.stderr)
        sys.exit(1)
