#!/usr/bin/env python3
"""各ソースのフィードと記事本文を取得し、sources-raw/ 配下に書き出す。

なぜ必要か: クラウドキャプチャルーチンの実行環境は2026-09-07以降、外部ドメインへの
egress が全て403で拒否されている（環境側の問題で、利用者が触れる設定は存在しない）。
一方 GitHub Actions のegressは制限されておらず、github.com は遮断日でも到達できる。
そこで「外部サイトを取りに行く役」をActionsへ移し、ルーチンはリポジトリ内の
ファイルを読むだけにする。これでルーチンが必要とする外部通信は github.com だけになる。

ソース一覧は CLAUDE.md の「キャプチャ対象ソース」テーブルが唯一の正。
このスクリプトは同テーブルの prefix / フィードURL 列を読む（ここには書き写さない）。

出力:
  sources-raw/<YYYY-MM-DD>/<prefix>/<slug>.md   記事1本（frontmatter + 本文抽出）
  sources-raw/<YYYY-MM-DD>/index.md             当日分の一覧
  sources-raw/fetch-log.md                      ソース別の取得結果（成功/失敗と件数）

使い方: python3 scripts/fetch_sources.py [--date YYYY-MM-DD] [--out sources-raw]
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import os
import re
import sys
import traceback

import feedparser
import requests
import trafilatura

UA = "Mozilla/5.0 (compatible; SkillGraphInbox/1.0; +https://github.com/Shuhei-Tsunoda02006242/my-skill-graph-inbox)"

# 1ソースあたりの取得上限。ルーチン側は最大3件しか採らないが、
# 重複スキップで候補が尽きると0件になるため余裕を持たせる。
MAX_PER_SOURCE = 6
# 何日前までの記事を候補にするか。障害日のさかのぼり取得（CLAUDE.md参照）が
# 前日分を拾えるよう、1日では足りない。
LOOKBACK_DAYS = 3
# 1記事あたりの本文の上限文字数。ルーチンが読むのに十分で、かつリポジトリが膨らまない量。
MAX_BODY_CHARS = 12000

TIMEOUT = 30


def log(msg: str) -> None:
    print(msg, flush=True)


def parse_source_table(claude_md: str) -> list[dict]:
    """CLAUDE.md の「キャプチャ対象ソース」テーブルを読む。

    期待する列: | prefix | ソース | URL | フィード | ドメイン |
    フィード列が空、または `-` の行はスキップする（取得手段がないため）。
    """
    lines = claude_md.split("\n")
    try:
        start = next(i for i, l in enumerate(lines) if l.startswith("| prefix |"))
    except StopIteration:
        raise SystemExit("CLAUDE.md にソーステーブルが見つかりません（| prefix | で始まる行）")

    header = [c.strip() for c in lines[start].strip().strip("|").split("|")]
    try:
        i_prefix = header.index("prefix")
        i_name = header.index("ソース")
        i_feed = header.index("フィード")
    except ValueError:
        raise SystemExit(f"ソーステーブルに必要な列がありません: {header}")

    sources = []
    for l in lines[start + 2:]:
        if not l.startswith("|"):
            break
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(cells) <= max(i_prefix, i_name, i_feed):
            continue
        feed = cells[i_feed].strip("`").strip()
        if not feed or feed == "-":
            continue
        sources.append({
            "prefix": cells[i_prefix].strip("`"),
            "name": cells[i_name],
            "feed": feed,
        })
    return sources


def clean_title(raw: str) -> str:
    """RSSのtitleからHTMLを取り除く。

    FierceBiotech は title を <a href="...">実際のタイトル</a> の形で返すため、
    そのまま使うとfrontmatterにもslugにもURLが混入する（2026-09-10に実測）。
    """
    t = re.sub(r"<[^>]+>", "", raw)
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t).strip()


def slugify(text: str, maxlen: int = 60) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return s[:maxlen].rstrip("-") or "untitled"


def entry_summary(entry) -> str:
    """フィードの要約テキスト（HTML除去済み）を返す。

    本文抽出が効かないソースのフォールバック。Techmeme は集約サイトで
    ページ本文がほぼ無く、trafilatura が200字未満しか取れない（GitHub Actions の
    ランナーからだと特に顕著。2026-09-10に実測）。一方 RSS の description には
    出典・見出し・リード文が300字前後入っており、これが実質的な本文にあたる。
    """
    raw = entry.get("summary") or entry.get("description") or ""
    if not isinstance(raw, str):
        raw = str(raw)
    t = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    return re.sub(r"\s+", " ", t).strip()


def entry_date(entry) -> dt.date | None:
    for key in ("published_parsed", "updated_parsed"):
        t = entry.get(key)
        if t:
            return dt.date(t.tm_year, t.tm_mon, t.tm_mday)
    return None


def fetch_feed(url: str) -> list:
    """フィードを取得して entries を返す。

    quantumcomputingreport.com は Accept-Encoding: gzip を送っても brotli で返すため、
    requests 経由で取得する（urllib3 は brotli パッケージがあれば自動で解く）。
    feedparser に URL を直接渡すと brotli を解けず 0 件になる。
    """
    r = requests.get(url, headers={"User-Agent": UA}, timeout=TIMEOUT)
    r.raise_for_status()
    parsed = feedparser.parse(r.content)
    return parsed.entries or []


def fetch_article_text(url: str) -> str:
    r = requests.get(url, headers={"User-Agent": UA}, timeout=TIMEOUT)
    r.raise_for_status()
    text = trafilatura.extract(
        r.text, include_comments=False, include_tables=True, favor_precision=True
    )
    return (text or "").strip()


def yaml_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d"))
    ap.add_argument("--out", default="sources-raw")
    ap.add_argument("--claude-md", default="CLAUDE.md")
    args = ap.parse_args()

    today = dt.date.fromisoformat(args.date)
    cutoff = today - dt.timedelta(days=LOOKBACK_DAYS)
    day_dir = os.path.join(args.out, args.date)

    sources = parse_source_table(open(args.claude_md, encoding="utf-8").read())
    log(f"ソース {len(sources)}件 / 対象日 {args.date} / {cutoff} 以降の記事を候補にする")

    results = []
    index_rows = []

    for src in sources:
        prefix, name, feed = src["prefix"], src["name"], src["feed"]
        row = {"prefix": prefix, "name": name, "status": "OK", "candidates": 0,
               "saved": 0, "note": ""}
        try:
            entries = fetch_feed(feed)
            log(f"[{prefix}] フィード {len(entries)}件")
        except Exception as e:
            row["status"] = "失敗"
            row["note"] = f"フィード取得失敗: {type(e).__name__}: {e}"[:150]
            log(f"[{prefix}] フィード取得失敗: {e}")
            results.append(row)
            continue

        recent = []
        for e in entries:
            d = entry_date(e)
            if d is None or d >= cutoff:
                recent.append((d, e))
        row["candidates"] = len(recent)

        saved = 0
        for d, e in recent:
            if saved >= MAX_PER_SOURCE:
                break
            url = e.get("link")
            title = clean_title(e.get("title") or "")
            if not url or not title:
                continue
            extraction = "full"
            try:
                body = fetch_article_text(url)
            except Exception as ex:
                log(f"[{prefix}] 本文取得失敗 {url}: {ex}")
                body = ""
            if len(body) < 200:
                # ページ本文が取れない（集約サイト・ペイウォール・JS描画等）。
                # フィードの要約で代替する。要約すら短ければ諦める。
                fallback = entry_summary(e)
                if len(fallback) >= 200:
                    body, extraction = fallback, "summary"
                    log(f"[{prefix}] 本文が薄いため要約で代替 ({len(fallback)}字): {url}")
                else:
                    log(f"[{prefix}] 本文も要約も短すぎるため除外 "
                        f"(本文{len(body)}字/要約{len(fallback)}字): {url}")
                    continue

            truncated = len(body) > MAX_BODY_CHARS
            body = body[:MAX_BODY_CHARS]
            slug = slugify(title)
            rel = os.path.join(args.date, prefix, f"{slug}.md")
            path = os.path.join(args.out, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write("---\n")
                f.write(f'source: "{yaml_escape(name)}"\n')
                f.write(f"prefix: {prefix}\n")
                f.write(f'title: "{yaml_escape(title)}"\n')
                f.write(f'url: "{yaml_escape(url)}"\n')
                f.write(f"published: {d.isoformat() if d else 'unknown'}\n")
                f.write(f"chars: {len(body)}\n")
                f.write(f"truncated: {str(truncated).lower()}\n")
                f.write(f"extraction: {extraction}\n")
                f.write("---\n\n")
                f.write(body)
                f.write("\n")
            saved += 1
            index_rows.append((prefix, d.isoformat() if d else "?", title, url, rel))
            log(f"[{prefix}] 保存 {rel} ({len(body)}字)")

        row["saved"] = saved
        if saved == 0 and row["candidates"] > 0:
            row["note"] = "候補はあったが本文も要約も取れず0件"
        results.append(row)

    os.makedirs(day_dir, exist_ok=True)
    with open(os.path.join(day_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(f"# 取得済みソース {args.date}\n\n")
        f.write(f"{cutoff} 以降に公開された記事の本文を取得済み。"
                f"ファイルパスは `sources-raw/` からの相対。\n\n")
        f.write("| prefix | 公開日 | タイトル | ファイル | URL |\n")
        f.write("|--------|--------|----------|----------|-----|\n")
        for prefix, d, title, url, rel in index_rows:
            t = title.replace("|", "\\|")[:110]
            f.write(f"| `{prefix}` | {d} | {t} | `{rel}` | {url} |\n")
        if not index_rows:
            f.write("| - | - | （取得0件） | - | - |\n")

    with open(os.path.join(args.out, "fetch-log.md"), "w", encoding="utf-8") as f:
        f.write(f"# 取得ログ {args.date}\n\n")
        f.write("GitHub Actions（`fetch-sources.yml`）による取得結果。"
                "巡回ログの「取得」列はこの表をそのまま使ってよい。\n\n")
        f.write("| prefix | ソース | 取得 | 候補 | 保存 | 備考 |\n")
        f.write("|--------|--------|------|------|------|------|\n")
        for r in results:
            f.write(f"| `{r['prefix']}` | {r['name']} | {r['status']} | "
                    f"{r['candidates']} | {r['saved']} | {r['note']} |\n")
        total = sum(r["saved"] for r in results)
        failed = [r["prefix"] for r in results if r["status"] == "失敗"]
        f.write(f"\n合計 {total}件を保存。")
        f.write(f"取得失敗ソース: {', '.join(failed) if failed else 'なし'}\n")

    total = sum(r["saved"] for r in results)
    log(f"完了: {total}件を保存 / 失敗ソース {len([r for r in results if r['status']=='失敗'])}件")
    # 1件も取れなければ異常。ワークフロー側で気づけるよう非0で終える。
    return 0 if total > 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(2)
