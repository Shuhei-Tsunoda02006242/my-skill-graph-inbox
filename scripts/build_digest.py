#!/usr/bin/env python3
"""キャプチャノートからカテゴリ別ダイジェスト（+ Gemini批評コメント）を組み立てて、
カテゴリ（Sequoia Capital風アレンジ5分類: AI/Hardware（半導体）/Climate & Energy/
Healthcare/Frontier（量子）/その他）ごとに1通ずつメール送信する（2026-07-18〜、
以前はソース別グルーピングだった）。

Frontier（量子）は日次配信の対象外。WEEKLY_QUANTUM=1 で起動すると、日次処理の代わりに
過去7日以内の量子ノートをスキャンして週次サマリー1通（1行ヘッドライン形式＋Gemini総括＋
量子ヒートマップ）を送信する専用モードに切り替わる。

Usage:
    build_digest.py <file1.md> [file2.md ...]              通常の日次カテゴリダイジェスト
    WEEKLY_QUANTUM=1 build_digest.py [file1.md ...]         週次量子ダイジェスト
        （パスを渡せばそれを対象にする＝テスト用。渡さなければ 00-Inbox/*.md を
        ファイル名の日付でスキャンし、過去7日以内かつFrontier（量子）カテゴリの
        ノートを対象にする。.digest-state には依存しない）

環境変数:
- GMAIL_USERNAME / GMAIL_APP_PASSWORD  SMTP認証情報（送受信とも同一アドレス）
- GEMINI_API_KEY                       批評コメント/週次総括生成用（無くても継続）
- WEEKLY_QUANTUM=1                     週次量子ダイジェストモードに切り替え
- DRY_RUN=1                            SMTP送信せず、件名・本文を標準出力するのみ
- INCLUDE_HEATMAPS=0                   末尾ヒートマップ画像の埋め込みのみを無効化（📍市場規模
                                        注記は独立して継続。デフォルト有効。
                                        assets/market/market-sizes.json が無い場合は
                                        両機能とも自動的に無効）

出力:
- $GITHUB_OUTPUT (あれば)  count
"""

import base64
import html
import os
import re
import smtplib
import subprocess
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

# 配信カテゴリ（Sequoia Capital風アレンジ5分類 + その他）。
# アクセントカラーはHTMLメールのヘッダー帯・リンク色に、domainはヒートマップ画像
# （assets/market/market-{domain}-treemap.svg）の選択に使う。「その他」はdomain無し。
CATEGORIES = {
    "AI": {"accent": "#1a73e8", "domain": "ai"},
    "Hardware（半導体）": {"accent": "#0a7d33", "domain": "semiconductor"},
    "Climate & Energy": {"accent": "#e37400", "domain": "energy"},
    "Healthcare": {"accent": "#c5221f", "domain": "biotech"},
    "Frontier（量子）": {"accent": "#7627bb", "domain": "quantum"},
    "その他": {"accent": "#5f6368", "domain": None},
}
CATEGORY_ORDER = list(CATEGORIES.keys())

# DRY_RUNプレビューファイル名用のカテゴリ→スラグ変換
CATEGORY_SLUG = {
    "AI": "ai",
    "Hardware（半導体）": "hardware",
    "Climate & Energy": "climate-energy",
    "Healthcare": "healthcare",
    "Frontier（量子）": "quantum",
    "その他": "other",
}

# landscape-position 第1セグメント → 配信カテゴリ
SEGMENT_TO_CATEGORY = {
    "AI": "AI",
    "Semiconductor": "Hardware（半導体）",
    "Energy": "Climate & Energy",
    "Biotech": "Healthcare",
    "Quantum": "Frontier（量子）",
}

# landscape-position が空のノート向け、ソースprefix→配信カテゴリのフォールバック
PREFIX_FALLBACK_CATEGORY = {
    "tc": "AI",
    "tm": "AI",
    "sn": "Healthcare",
    "is": "Healthcare",
    "fb": "Healthcare",
    "ek": "Climate & Energy",
    "qcr": "Frontier（量子）",
    "tqi": "Frontier（量子）",
}

# シグナル強度バッジの配色（背景色, 文字色）
SIGNAL_BADGE_COLORS = {
    "strong": ("#d93025", "#ffffff"),
    "moderate": ("#f9ab00", "#000000"),
    "weak": ("#9aa0a6", "#ffffff"),
    "none": ("#e8eaed", "#5f6368"),
}

# 市場規模データ（vault側 scripts/generate_market_treemaps.py 実行時に自動同期される）
MARKET_DATA_PATH = "assets/market/market-sizes.json"

# landscape-position 先頭セグメント → market-sizes.json の domains キー
DOMAIN_SEGMENT_TO_KEY = {
    "AI": "ai",
    "Semiconductor": "semiconductor",
    "Quantum": "quantum",
    "Biotech": "biotech",
    "Energy": "energy",
}

# ヒートマップ埋め込み時の見出しラベル
DOMAIN_KEY_TO_LABEL = {
    "ai": "AI",
    "semiconductor": "半導体",
    "quantum": "量子",
    "biotech": "バイオテック",
    "energy": "エネルギー",
}

# cagrが「%」を含まない語彙表現の変換（市場規模注記用）
CAGR_WORD_MAP = {
    "高い": "急成長",
    "非常に高い": "急成長",
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
        "prefix": prefix,
        "source_name": sources.get(prefix, "その他"),
        "title": frontmatter_field("title", text),
        "url": frontmatter_field("source", text),
        "signal": frontmatter_field("signal-strength", text),
        "implication": frontmatter_field("investment-implication", text),
        "position": frontmatter_field("landscape-position", text),
        "claim": section(["主な主張", "Key Claim"], text),
        "my_take": section(["私の見解", "My Take"], text),
    }


def categorize(note: dict) -> str:
    """ノートを配信カテゴリに振り分ける。
    landscape-position の第1セグメントを優先し、無ければソースprefixでフォールバック、
    どちらも該当しなければ「その他」。"""
    position = note.get("position", "")
    if position:
        top = position.split(">")[0].strip()
        category = SEGMENT_TO_CATEGORY.get(top)
        if category:
            return category
    return PREFIX_FALLBACK_CATEGORY.get(note.get("prefix", ""), "その他")


def load_claude_commentary() -> dict[str, str]:
    """キャプチャループ（Claude）が書いた本日の批評コメントをソース別に読む。
    クラウドキャプチャルーチンはUTC日付でファイルを書くが、メール送信はJST日付基準で
    動いているため、日付ズレを吸収するため複数の候補日付を順に試す
    （UTC今日 → JST今日 → JST昨日）。"""
    now_utc = datetime.now(timezone.utc)
    now_jst = datetime.now(JST)
    candidates = [
        now_utc.strftime("%Y-%m-%d"),
        now_jst.strftime("%Y-%m-%d"),
        (now_jst - timedelta(days=1)).strftime("%Y-%m-%d"),
    ]
    path = None
    for date_str in candidates:
        candidate_path = f"digests/{date_str}-commentary.md"
        if os.path.isfile(candidate_path):
            path = candidate_path
            break
    if path is None:
        print("No Claude commentary found; will fall back to Gemini")
        return {}
    print(f"Loaded Claude commentary: {path}")
    text = open(path).read()
    result = {}
    for m in re.finditer(r"^## (.+?)\s*\n(.*?)(?=^## |\Z)",
                         text, re.MULTILINE | re.DOTALL):
        body = m.group(2).strip()
        if body:
            result[m.group(1).strip()] = body
    return result


def load_market_data() -> dict | None:
    """assets/market/market-sizes.json を読み込む。無ければ機能を静かに無効化する
    （vault側 generate_market_treemaps.py が未実行のセットアップ初期等を想定）。
    INCLUDE_HEATMAPS=0 はヒートマップ画像埋め込みのみを止める（📍市場規模注記は継続）ため、
    ここでは判定しない（send_emails側でヒートマップ生成のみをスキップする）。"""
    if not os.path.isfile(MARKET_DATA_PATH):
        return None
    try:
        with open(MARKET_DATA_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"market-sizes.json 読み込み失敗: {e}", file=sys.stderr)
        return None


def find_market_tile(position: str, market_data: dict) -> dict | None:
    """landscape-position のパンくずを breadcrumb-map で最長プレフィックス一致させ、
    該当する domains 配下のタイル（item dict）を返す。ヒットしなければNone。
    まず完全一致、無ければ末尾セグメントを1つずつ削って再照合する。"""
    if not position:
        return None
    breadcrumb_map = market_data.get("breadcrumb-map", {})
    segments = [s.strip() for s in position.split(">") if s.strip()]
    if not segments:
        return None

    for n in range(len(segments), 0, -1):
        key = " > ".join(segments[:n])
        if key not in breadcrumb_map:
            continue
        tile_name = breadcrumb_map[key]
        if tile_name is None:
            return None
        domain_key = DOMAIN_SEGMENT_TO_KEY.get(segments[0])
        if not domain_key:
            return None
        for item in market_data.get("domains", {}).get(domain_key, []):
            if item["name"] == tile_name:
                return item
        return None
    return None


def fmt_market_annotation(item: dict) -> str:
    """タイル情報から📍行に付ける市場規模注記を組み立てる。"""
    size_str = "${:g}B".format(item["size"])
    if "★" in item.get("note", ""):
        return f"（★投資額{size_str}/年ベース）"
    cagr = item.get("cagr", "")
    if "%" in cagr:
        return f"（市場{size_str}・CAGR {cagr}）"
    cagr_disp = CAGR_WORD_MAP.get(cagr, cagr)
    return f"（市場{size_str}・{cagr_disp}）"


def annotate_position(position: str, market_data: dict | None) -> str:
    """📍 位置文字列に市場規模注記を付記する。マップ不一致・データ無しならそのまま返す。"""
    if not position or not market_data:
        return position
    tile = find_market_tile(position, market_data)
    if not tile:
        return position
    return position + fmt_market_annotation(tile)


def render_domain_heatmap_png(domain_key: str, width: int = 1200) -> bytes | None:
    """market-{domain}-treemap.svg を rsvg-convert でPNG化する。
    rsvg-convertが無い/失敗した場合はNoneを返し、stderrに警告する
    （画像なしで送信を継続するためのフォールバック）。"""
    svg_path = os.path.join("assets", "market", f"market-{domain_key}-treemap.svg")
    if not os.path.isfile(svg_path):
        print(f"ヒートマップSVGが見つかりません: {svg_path}", file=sys.stderr)
        return None
    try:
        result = subprocess.run(
            ["rsvg-convert", "-w", str(width), svg_path],
            capture_output=True,
            check=True,
        )
        return result.stdout
    except FileNotFoundError:
        print(
            "rsvg-convert が見つかりません。ヒートマップ画像埋め込みをスキップします。",
            file=sys.stderr,
        )
        return None
    except subprocess.CalledProcessError as e:
        stderr_text = e.stderr.decode(errors="ignore") if e.stderr else ""
        print(f"rsvg-convert 失敗（{domain_key}）: {stderr_text}", file=sys.stderr)
        return None


def build_heatmap_html(domain_keys: list[str], src_map: dict[str, str]) -> str:
    """ヒートマップ画像セクションのHTML断片を組み立てる。
    src_map に無い（＝変換不可だった）domainはスキップする。"""
    available = [dk for dk in domain_keys if dk in src_map]
    if not available:
        return ""
    parts = [
        '<div style="margin-top:16px;">',
        '<div style="font-size:16px;font-weight:bold;color:#202124;margin-bottom:8px;">'
        "🗺 市場規模ヒートマップ</div>",
    ]
    for dk in available:
        label = DOMAIN_KEY_TO_LABEL.get(dk, dk)
        parts.append(
            '<div style="margin-bottom:12px;">'
            f'<div style="font-size:13px;font-weight:bold;color:#5f6368;margin-bottom:4px;">'
            f"{html.escape(label)}</div>"
            f'<img src="{src_map[dk]}" style="width:100%;max-width:600px;border-radius:8px;">'
            "</div>"
        )
    parts.append("</div>")
    return "".join(parts)


def _gemini_generate(prompt: str, label: str) -> str:
    """Gemini API呼び出しの共通処理。失敗したら空文字（呼び出し元の送信は止めない）。"""
    key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        return ""
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
            print(f"Gemini {label} ({model}) failed: {e}", file=sys.stderr)
    return ""


def gemini_commentary(category_name: str, articles: list[dict]) -> str:
    """カテゴリ単位の批評コメントを生成。失敗したら空文字（メール送信は止めない）。"""
    summary = "\n\n".join(
        f"記事{i + 1}: {a['title']}\n主張: {a['claim']}\n投資含意: {a['implication']}"
        for i, a in enumerate(articles)
    )
    prompt = (
        f"あなたはDeepTech（AI・半導体・量子・バイオ・エネルギー）と投資のクロスドメインアナリストです。"
        f"以下は本日キャプチャした {category_name} カテゴリの記事要約です。\n\n{summary}\n\n"
        "この記事群への批評コメントを日本語で3〜5文で書いてください。観点: "
        "(1) 誇張・ハイプの可能性 (2) 記事に欠けている文脈 "
        "(3) 投資家として注意すべき点 (4) 記事間に共通するトレンドがあれば指摘。"
        "前置き・見出し・箇条書きは不要で、コメント本文のみを出力してください。"
    )
    return _gemini_generate(prompt, category_name)


def gemini_weekly_summary(articles: list[dict]) -> str:
    """量子週次ダイジェストの総括コメントを生成。失敗したら空文字（総括なしで継続）。"""
    summary = "\n\n".join(
        f"記事{i + 1}: {a['title']}\n主張: {a['claim']}\n投資含意: {a['implication']}"
        for i, a in enumerate(articles)
    )
    prompt = (
        "あなたはDeepTech（AI・半導体・量子・バイオ・エネルギー）と投資のクロスドメインアナリストです。"
        f"以下は今週キャプチャした量子分野の記事群の要約です。\n\n{summary}\n\n"
        "個別記事の詳細ではなく、記事群全体から見える潮流・地形の変化がわかる総括を"
        "日本語で3〜5文で書いてください。ハイプ（誇張）に注意すべき点があれば添えてください。"
        "前置き・見出し・箇条書きは不要で、総括本文のみを出力してください。"
    )
    return _gemini_generate(prompt, "weekly-quantum")


def build_body(category: str, articles: list[dict], commentary: str, commentary_label: str,
                market_data: dict | None = None, heatmap_available: bool = False) -> str:
    lines = [
        f"{category}（{len(articles)}件）",
        "",
    ]
    for a in articles:
        lines += [
            f"📌 {a['title']}",
        ]
        if a["position"]:
            lines += [f"📍 {annotate_position(a['position'], market_data)}"]
        lines += [
            f"ソース: {a['source_name']}",
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
    if heatmap_available:
        lines += ["🗺 市場規模ヒートマップは HTML表示で確認", ""]
    return "\n".join(lines) + "\n"


def _esc(text: str) -> str:
    """HTMLエスケープ後、改行を<br>に変換する。"""
    return html.escape(text).replace("\n", "<br>")


# **強調**マークアップ（キャプチャ時にClaudeが本文に埋め込む）を<strong>に変換する
_BOLD_MARKUP_RE = re.compile(r"\*\*(.+?)\*\*", re.DOTALL)
# 既存の<strong>...</strong>区間を切り出すためのスプリッタ（数値太字化の二重適用を避ける）
_STRONG_SPLIT_RE = re.compile(r"(<strong>.*?</strong>)", re.DOTALL)

# 太字化する数値パターン（過剰適用を避けるため下記に限定。年号・四半期等は対象外）
_CURRENCY_RE = r"[$€£]\d[\d,]*(?:\.\d+)?(?:兆|億|万|[BMK])?"          # $400M / $3.8B / $1.5兆 / €91M / £50M
_YEN_CONVERSION_RE = r"約\d[\d,]*(?:\.\d+)?(?:兆|億|万)円"             # 約600億円 / 約1.1兆円
_POWER_RE = r"\d[\d,]*(?:\.\d+)?(?:TWh|GWh|MWh|KWh|TW|GW|MW|KW)"      # 2.5GW / 509MW / 1,440MWh / 1.1TWh
_QUBIT_RE = r"\d[\d,]*(?:\.\d+)?万?量子ビット"                         # 2万量子ビット / 98量子ビット
_MULTIPLIER_RE = r"\d[\d,]*(?:\.\d+)?倍"                              # 20倍 / 3倍
_PERCENT_RE = r"[+-]?\d[\d,]*(?:\.\d+)?%\+?"                          # 76% / +143% / -55% / 30%+

_NUMBER_PATTERN = re.compile("|".join([
    _YEN_CONVERSION_RE, _CURRENCY_RE, _POWER_RE, _QUBIT_RE, _MULTIPLIER_RE, _PERCENT_RE,
]))


def _bold_numbers(text: str) -> str:
    """数値パターンを<strong>で囲む。既に<strong>...</strong>で囲まれた区間はスキップし、
    二重の太字化ネストを避ける。"""
    parts = _STRONG_SPLIT_RE.split(text)
    for i, part in enumerate(parts):
        if i % 2 == 0:  # 偶数インデックス=<strong>タグの外側（分割元テキスト）
            parts[i] = _NUMBER_PATTERN.sub(lambda m: f"<strong>{m.group(0)}</strong>", part)
    return "".join(parts)


def _esc_rich(text: str) -> str:
    """本文用のエスケープ。HTMLエスケープ後に **強調** と数値の太字化を適用し、改行を<br>にする。
    処理順序はセキュリティ上重要（この順を変えないこと）:
    1. html.escape でユーザー由来テキストのHTML注入を防ぐ
    2. **〜** を <strong>〜</strong> に変換（キャプチャ時にClaudeが埋め込む要点マークアップ用）
    3. 数値パターンを <strong> で囲む
    4. 改行を <br> に変換
    """
    escaped = html.escape(text)
    with_markup = _BOLD_MARKUP_RE.sub(r"<strong>\1</strong>", escaped)
    with_numbers = _bold_numbers(with_markup)
    return with_numbers.replace("\n", "<br>")


def build_html_body(category: str, articles: list[dict], commentary: str,
                     commentary_label: str, today: str, market_data: dict | None = None,
                     heatmap_html: str = "") -> str:
    """NewsPicks風カードのHTMLメール本文を組み立てる。Gmail対応のためインラインstyleのみ使用。"""
    accent = CATEGORIES.get(category, CATEGORIES["その他"])["accent"]

    parts = [
        '<div style="max-width:600px;margin:0 auto;'
        "font-family:-apple-system,'Hiragino Sans',sans-serif;"
        'background-color:#f1f3f4;padding:16px;">',
        # ヘッダー: カテゴリ別アクセントカラーの帯
        f'<div style="background-color:{accent};border-radius:8px 8px 0 0;'
        'padding:16px;color:#ffffff;">'
        f'<div style="font-size:20px;font-weight:bold;">{html.escape(category)}</div>'
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
                f'📍 {html.escape(annotate_position(a["position"], market_data))}</div>'
            )
        card.append(
            f'<div style="display:inline-block;background-color:{badge_bg};'
            f"color:{badge_fg};font-size:12px;font-weight:bold;border-radius:12px;"
            f'padding:2px 10px;margin-top:8px;">'
            f'{html.escape(a["signal"] or "none")}</div>'
            # 複数ソースが混在するカテゴリメールのため、ソース名チップを併記
            f'<span style="font-size:12px;color:#5f6368;margin-left:8px;">'
            f'{html.escape(a["source_name"])}</span>'
        )
        card.append(
            '<div style="font-size:14px;font-weight:bold;color:#202124;margin-top:12px;">'
            "【主な主張】</div>"
            f'<div style="font-size:14px;color:#3c4043;line-height:1.6;margin-top:4px;">'
            f'{_esc_rich(a["claim"] or "（なし）")}</div>'
        )
        card.append(
            '<div style="background-color:#fef7e0;border-left:4px solid #f9ab00;'
            'padding:8px 12px;margin-top:12px;">'
            '<div style="font-size:14px;font-weight:bold;color:#202124;">【投資含意】</div>'
            f'<div style="font-size:14px;color:#3c4043;line-height:1.6;margin-top:4px;">'
            f'{_esc_rich(a["implication"] or "（なし）")}</div>'
            "</div>"
        )
        if a["my_take"]:
            card.append(
                '<div style="font-size:14px;font-weight:bold;color:#202124;margin-top:12px;">'
                "【My Take】</div>"
                f'<div style="font-size:14px;color:#3c4043;line-height:1.6;'
                f'font-style:italic;margin-top:4px;">{_esc_rich(a["my_take"])}</div>'
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
            f'{_esc_rich(commentary)}</div>'
            "</div>"
        )

    if heatmap_html:
        parts.append(heatmap_html)

    parts.append("</div>")
    return "".join(parts)


def send_emails(groups: dict[str, list[dict]], claude_comments: dict[str, str]) -> None:
    dry_run = os.environ.get("DRY_RUN") == "1"
    # シークレット値に末尾改行が入っているとメールヘッダーが弾かれるため必ずstrip
    username = os.environ["GMAIL_USERNAME"].strip()
    password = os.environ.get("GMAIL_APP_PASSWORD", "").strip()
    today = datetime.now(JST).strftime("%Y-%m-%d")

    market_data = load_market_data()
    # INCLUDE_HEATMAPS=0 は画像埋め込みのみを止める（📍市場規模注記は独立して継続する）
    include_heatmaps = os.environ.get("INCLUDE_HEATMAPS", "1") != "0"

    # ヒートマップPNGは領域単位（最大5枚）なので、複数ソースにまたがっても1回だけ変換する
    heatmap_cache: dict[str, bytes | None] = {}

    def get_heatmap_png(domain_key: str) -> bytes | None:
        if domain_key not in heatmap_cache:
            heatmap_cache[domain_key] = render_domain_heatmap_png(domain_key)
        return heatmap_cache[domain_key]

    messages = []
    for category, articles in groups.items():
        commentary = claude_comments.get(category)
        if commentary:
            label = "Claude"
        else:
            commentary = gemini_commentary(category, articles)
            label = "Gemini生成"

        # カテゴリメールでは対応する領域のヒートマップ1枚だけを埋め込む（その他はdomain無し）
        domain_key = CATEGORIES.get(category, CATEGORIES["その他"])["domain"]
        domain_keys = [domain_key] if (domain_key and market_data and include_heatmaps) else []
        images: dict[str, bytes] = {}
        for dk in domain_keys:
            png_bytes = get_heatmap_png(dk)
            if png_bytes:
                images[dk] = png_bytes

        if dry_run:
            # DRY_RUN時はEmailMessageを作らず、プレビューHTMLに直接data URIを埋め込む
            src_map = {
                dk: "data:image/png;base64," + base64.b64encode(data).decode()
                for dk, data in images.items()
            }
            if domain_keys and not images:
                print(f"[DRY_RUN] {category}: ヒートマップ画像は変換できませんでした（rsvg-convert未導入等）")
        else:
            # 実送信時はCID参照にし、あとでadd_relatedする
            src_map = {dk: f"cid:heatmap-{dk}" for dk in images}

        heatmap_html = build_heatmap_html(domain_keys, src_map)

        subject = f"📥 [{category}] デイリーダイジェスト {today}（{len(articles)}件）"
        body = build_body(category, articles, commentary, label, market_data, bool(heatmap_html))
        html_body = build_html_body(
            category, articles, commentary, label, today, market_data, heatmap_html
        )
        messages.append((subject, body, html_body, category, images))

    if dry_run:
        preview_dir = os.environ.get("TMPDIR", "/tmp")
        for subject, body, html_body, category, images in messages:
            print("=" * 60)
            print(f"Subject: {subject}")
            print("-" * 60)
            print(body)
            slug = CATEGORY_SLUG.get(category, "other")
            preview_path = os.path.join(preview_dir, f"digest_preview_{slug}.html")
            with open(preview_path, "w", encoding="utf-8") as f:
                f.write(html_body)
            print(f"[DRY_RUN] HTML preview saved: {preview_path}")
        return

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(username, password)
        for subject, body, html_body, category, images in messages:
            msg = EmailMessage()
            msg["Subject"] = subject
            msg["From"] = f"Skill Graph Inbox <{username}>"
            msg["To"] = username
            msg.set_content(body, charset="utf-8")
            msg.add_alternative(html_body, subtype="html")
            if images:
                html_part = msg.get_payload()[-1]
                for dk, data in images.items():
                    html_part.add_related(
                        data, maintype="image", subtype="png", cid=f"<heatmap-{dk}>"
                    )
            smtp.send_message(msg)
            print(f"Sent: {subject}")


def build_weekly_body(articles: list[dict], summary: str, today: str,
                       market_data: dict | None = None, heatmap_available: bool = False) -> str:
    """量子週次ダイジェストのplain本文（1行ヘッドライン形式）を組み立てる。"""
    lines = [f"Frontier（量子） 週次ダイジェスト {today}（今週{len(articles)}件）", ""]
    if summary:
        lines += ["🔭 今週の潮流", summary, ""]
    for a in articles:
        lines.append(f"・{a['title']}")
        meta_bits = []
        if a["position"]:
            meta_bits.append(f"📍 {annotate_position(a['position'], market_data)}")
        meta_bits.append(f"ソース: {a['source_name']}")
        lines.append("  " + "｜".join(meta_bits))
        lines.append(f"  🔗 {a['url']}")
        lines.append("")
    if heatmap_available:
        lines += ["🗺 市場規模ヒートマップは HTML表示で確認", ""]
    return "\n".join(lines) + "\n"


def build_weekly_html_body(articles: list[dict], summary: str, today: str,
                            market_data: dict | None = None, heatmap_html: str = "") -> str:
    """量子週次ダイジェストのHTML本文（1行ヘッドライン形式）を組み立てる。"""
    accent = CATEGORIES["Frontier（量子）"]["accent"]

    parts = [
        '<div style="max-width:600px;margin:0 auto;'
        "font-family:-apple-system,'Hiragino Sans',sans-serif;"
        'background-color:#f1f3f4;padding:16px;">',
        f'<div style="background-color:{accent};border-radius:8px 8px 0 0;'
        'padding:16px;color:#ffffff;">'
        '<div style="font-size:20px;font-weight:bold;">Frontier（量子） 週次ダイジェスト</div>'
        f'<div style="font-size:13px;opacity:0.9;margin-top:4px;">'
        f'{html.escape(today)}（今週{len(articles)}件）</div>'
        "</div>",
    ]

    if summary:
        parts.append(
            '<div style="background-color:#f8f9fa;border-radius:8px;padding:16px;'
            'margin-top:12px;">'
            '<div style="font-size:13px;font-weight:bold;color:#5f6368;">🔭 今週の潮流</div>'
            f'<div style="font-size:14px;color:#3c4043;line-height:1.6;margin-top:8px;">'
            f'{_esc_rich(summary)}</div>'
            "</div>"
        )

    rows = []
    for a in articles:
        meta_bits = []
        if a["position"]:
            meta_bits.append(
                f'📍 {html.escape(annotate_position(a["position"], market_data))}'
            )
        meta_bits.append(html.escape(a["source_name"]))
        rows.append(
            '<div style="background-color:#ffffff;border-bottom:1px solid #dadce0;'
            'padding:12px 4px;">'
            f'<a href="{html.escape(a["url"], quote=True)}" '
            f'style="color:{accent};text-decoration:none;font-size:15px;font-weight:bold;'
            'line-height:1.4;">'
            f'{html.escape(a["title"])}</a>'
            '<div style="font-size:12px;color:#5f6368;margin-top:4px;">'
            f'{"｜".join(meta_bits)}</div>'
            "</div>"
        )
    parts.append(
        '<div style="background-color:#ffffff;border:1px solid #dadce0;'
        'border-radius:8px;margin-top:12px;overflow:hidden;">' + "".join(rows) + "</div>"
    )

    if heatmap_html:
        parts.append(heatmap_html)

    parts.append("</div>")
    return "".join(parts)


def send_weekly_quantum_email(articles: list[dict]) -> None:
    """量子週次ダイジェストを1通だけ送信する。"""
    dry_run = os.environ.get("DRY_RUN") == "1"
    # シークレット値に末尾改行が入っているとメールヘッダーが弾かれるため必ずstrip
    username = os.environ["GMAIL_USERNAME"].strip()
    password = os.environ.get("GMAIL_APP_PASSWORD", "").strip()
    today = datetime.now(JST).strftime("%Y-%m-%d")

    market_data = load_market_data()
    include_heatmaps = os.environ.get("INCLUDE_HEATMAPS", "1") != "0"

    summary = gemini_weekly_summary(articles)

    domain_key = CATEGORIES["Frontier（量子）"]["domain"]
    images: dict[str, bytes] = {}
    if domain_key and market_data and include_heatmaps:
        png_bytes = render_domain_heatmap_png(domain_key)
        if png_bytes:
            images[domain_key] = png_bytes

    domain_keys = [domain_key] if (domain_key and market_data and include_heatmaps) else []

    if dry_run:
        src_map = {
            dk: "data:image/png;base64," + base64.b64encode(data).decode()
            for dk, data in images.items()
        }
        if domain_keys and not images:
            print("[DRY_RUN] Frontier（量子）: ヒートマップ画像は変換できませんでした（rsvg-convert未導入等）")
    else:
        src_map = {dk: f"cid:heatmap-{dk}" for dk in images}

    heatmap_html = build_heatmap_html(domain_keys, src_map)

    subject = f"🔭 [Frontier（量子）] 週次ダイジェスト {today}（今週{len(articles)}件）"
    body = build_weekly_body(articles, summary, today, market_data, bool(heatmap_html))
    html_body = build_weekly_html_body(articles, summary, today, market_data, heatmap_html)

    if dry_run:
        print("=" * 60)
        print(f"Subject: {subject}")
        print("-" * 60)
        print(body)
        preview_dir = os.environ.get("TMPDIR", "/tmp")
        preview_path = os.path.join(preview_dir, "digest_preview_weekly_quantum.html")
        with open(preview_path, "w", encoding="utf-8") as f:
            f.write(html_body)
        print(f"[DRY_RUN] HTML preview saved: {preview_path}")
        return

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(username, password)
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = f"Skill Graph Inbox <{username}>"
        msg["To"] = username
        msg.set_content(body, charset="utf-8")
        msg.add_alternative(html_body, subtype="html")
        if images:
            html_part = msg.get_payload()[-1]
            for dk, data in images.items():
                html_part.add_related(
                    data, maintype="image", subtype="png", cid=f"<heatmap-{dk}>"
                )
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


def run_weekly_quantum(paths: list[str], sources: dict[str, str]) -> None:
    """WEEKLY_QUANTUM=1 時のエントリーポイント。
    argvにパスが渡されればそれを対象にする（テスト用）。無ければ 00-Inbox/*.md を
    ファイル名の日付でスキャンし、過去7日以内かつFrontier（量子）カテゴリのノートを
    対象にする（.digest-state には依存しない）。対象0件なら送信せず正常終了する。"""
    import glob

    if paths:
        candidate_paths = paths
    else:
        cutoff = datetime.now(JST).date() - timedelta(days=7)
        candidate_paths = []
        for p in sorted(glob.glob("00-Inbox/*.md")):
            m = re.match(r"(\d{4}-\d{2}-\d{2})-", os.path.basename(p))
            if not m:
                continue
            try:
                file_date = datetime.strptime(m.group(1), "%Y-%m-%d").date()
            except ValueError:
                continue
            if file_date >= cutoff:
                candidate_paths.append(p)

    notes = dedup_by_url(candidate_paths, sources)
    quantum_notes = [n for n in notes if categorize(n) == "Frontier（量子）"]

    if not quantum_notes:
        print("No quantum articles this week")
    else:
        send_weekly_quantum_email(quantum_notes)

    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as f:
            f.write(f"count={len(quantum_notes)}\n")
    print(f"Built weekly quantum digest: {len(quantum_notes)} articles")


def main() -> None:
    paths = [p for p in sys.argv[1:] if os.path.isfile(p)]
    sources = load_sources()

    if os.environ.get("WEEKLY_QUANTUM") == "1":
        run_weekly_quantum(paths, sources)
        return

    notes = dedup_by_url(paths, sources)

    # Frontier（量子）は日次配信の対象外。週次サマリー（WEEKLY_QUANTUM=1）側で拾うため
    # ここでは除くだけで、ノート自体は消失しない
    quantum_notes = [n for n in notes if categorize(n) == "Frontier（量子）"]
    if quantum_notes:
        print(f"Skipped for weekly: {len(quantum_notes)} quantum articles")
    daily_notes = [n for n in notes if categorize(n) != "Frontier（量子）"]

    groups: dict[str, list[dict]] = {}
    for category in CATEGORY_ORDER:
        if category == "Frontier（量子）":
            continue
        matched = [n for n in daily_notes if categorize(n) == category]
        if matched:
            groups[category] = matched

    claude_comments = load_claude_commentary()

    if not daily_notes:
        print("No unique articles to send")
    else:
        send_emails(groups, claude_comments)

    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as f:
            f.write(f"count={len(notes)}\n")
    print(f"Built digest: {len(notes)} articles, {len(groups)} categories")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"build_digest failed: {e}", file=sys.stderr)
        sys.exit(1)
