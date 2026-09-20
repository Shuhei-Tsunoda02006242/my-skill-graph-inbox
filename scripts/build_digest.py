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

# 量子週次ダイジェスト「実現までの距離」ダッシュボード用データ（週次パス専用）
MILESTONES_PATH = "docs/quantum-milestones.json"
GLOSSARY_PATH = "docs/quantum-glossary.json"

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
    ソースは自動追加されるため、固定のSOURCESは読めなかった場合のフォールバック。

    `| prefix |` 見出しで始まるソーステーブルの中だけを読む。CLAUDE.md には
    同じ `| `tc-` | ... |` 形の行が巡回ログの記入例にもあり、ファイル全体を走査すると
    ソース名が「OK」「失敗」で上書きされる（2026-09-08〜17の配信で実際に発生）。"""
    sources = dict(SOURCES)
    try:
        text = open(os.path.join(os.path.dirname(__file__), "..", "CLAUDE.md")).read()
    except OSError:
        return sources
    lines = text.split("\n")
    start = next((i for i, l in enumerate(lines) if l.startswith("| prefix |")), None)
    if start is None:
        return sources
    for line in lines[start + 2:]:
        if not line.startswith("|"):
            break
        m = re.match(r"^\|\s*`([a-z]+)-`\s*\|\s*([^|]+?)\s*\|", line)
        if m:
            sources[m.group(1)] = m.group(2).strip()
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
        # 週次量子パス（指標更新検出・初出用語検出・お金/政策判定）専用。日次パスは未使用
        "path": path,
        "raw_text": text,
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
        "(1) 記事に欠けている文脈 (2) 記事間に共通するトレンドがあれば指摘。"
        "**「ハイプ/誇張かもしれない」「投資家として注意が必要だ」といった一般的な"
        "注意喚起は書かないこと。**毎回同じ定型になり読み飛ばされるため。"
        "断定を避けるための保険的な但し書きも不要。"
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
        "日本語で3〜5文で書いてください。"
        "**「ハイプ/誇張かもしれない」「注意すべき」といった一般的な注意喚起は書かないこと。**"
        "毎回同じ定型になり読み飛ばされるため。"
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


def load_json(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, data: dict, trailing_newline: bool = True) -> None:
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if trailing_newline:
        text += "\n"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def _sentence_containing(text: str, pos: int) -> str:
    """text内、posを含む一文を『。』か改行で区切って取り出す（前後の区切り文字は含めない）。"""
    start = 0
    for m in re.finditer(r"[。\n]", text):
        if m.end() > pos:
            return text[start:m.end()].strip()
        start = m.end()
    return text[start:].strip()


def _parse_number(s: str) -> float:
    return float(s.replace(",", ""))


def _body_after_frontmatter(text: str) -> str:
    """frontmatter（先頭の `---` 〜 `---`）を落とした本文を返す。"""
    m = re.match(r"^---\n.*?\n---\n", text, re.DOTALL)
    return text[m.end():] if m else text


def format_indicator_value(unit: str, value: float) -> str:
    """指標の value を unit に合わせて display 文字列に整形する。"""
    is_int = abs(value - round(value)) < 1e-9
    if unit == "%":
        return f"{value:g}%"
    num = f"{int(round(value)):,}" if is_int else f"{value:g}"
    if unit == "個":
        return f"{num}個"
    if unit == "分の1":
        return f"{num}分の1"
    return f"{num}{unit}"


def detect_milestone_update(indicator: dict, notes: list[dict]) -> dict | None:
    """1指標について、今週のノート群から最良の更新候補を1つ返す（無ければNone）。
    patterns が空の指標（手動更新のみ）は None を返す。"""
    patterns = indicator.get("patterns") or []
    if not patterns:
        return None
    direction = indicator.get("direction")
    current = float(indicator["value"])
    exclude_pattern = indicator.get("exclude_context") or ""
    exclude_re = re.compile(exclude_pattern) if exclude_pattern else None

    best = None
    for note in notes:
        # frontmatter は走査しない。title 行は1文が短く exclude_context の語（「コンペ」等）が
        # 入らないため、本文なら除外できる将来目標・賞金条件の数字が素通りする
        # （2026-09-18 のDOEコンペ記事が論理量子ビット48→100の更新候補として誤検出された）
        text = _body_after_frontmatter(note.get("raw_text", ""))
        for pat in patterns:
            for m in re.finditer(pat, text):
                if not m.groups():
                    continue
                try:
                    value = _parse_number(m.group(1))
                except (ValueError, IndexError):
                    continue
                if direction == "up" and not (value > current):
                    continue
                if direction == "down" and not (value < current):
                    continue
                sentence = _sentence_containing(text, m.start())
                if exclude_re and exclude_re.search(sentence):
                    continue
                if best is None:
                    better = True
                elif direction == "up":
                    better = value > best["value"]
                else:
                    better = value < best["value"]
                if better:
                    best = {"value": value, "sentence": sentence, "note": note}
    return best


def apply_milestone_updates(milestones: dict, quantum_notes: list[dict], today: str) -> list[dict]:
    """今週のノート群から各指標の更新を検出し、milestones（メモリ上の辞書）を書き換える。
    ファイルへの保存は行わない（呼び出し側がDRY_RUN次第で判断する）。
    返り値はメール本文組み立て用の採用済み更新リスト。"""
    updates = []
    for indicator in milestones["indicators"]:
        best = detect_milestone_update(indicator, quantum_notes)
        if best is None:
            continue
        note = best["note"]
        old_display = indicator["display"]
        new_value = best["value"]
        new_display = format_indicator_value(indicator["unit"], new_value)
        filename = os.path.splitext(os.path.basename(note["path"]))[0]
        date_m = re.match(r"(\d{4}-\d{2}-\d{2})-", filename)
        as_of = date_m.group(1) if date_m else today

        indicator["value"] = new_value
        indicator["display"] = new_display
        indicator["as_of"] = as_of
        indicator["source_note"] = filename
        indicator["source_detail"] = best["sentence"][:120]
        milestones.setdefault("history", []).append({
            "date": today,
            "id": indicator["id"],
            "from": old_display,
            "to": new_display,
            "note": filename,
        })
        updates.append({
            "id": indicator["id"],
            "label": indicator["label"],
            "old_display": old_display,
            "new_display": new_display,
            "note": note,
        })
    return updates


def detect_new_terms(glossary: dict, notes: list[dict], today: str, max_terms: int = 2) -> list[dict]:
    """今週のノート本文に aliases が出てくる用語のうち、last_shown が未設定か180日以上前の
    ものをJSON順で最大 max_terms 件選ぶ。選んだ用語の last_shown を today に書き換える
    （メモリ上のみ。保存は呼び出し側がDRY_RUN次第で判断する）。"""
    combined_text = "\n".join(n.get("raw_text", "") for n in notes)
    today_date = datetime.strptime(today, "%Y-%m-%d").date()
    selected = []
    for term in glossary["terms"]:
        if len(selected) >= max_terms:
            break
        last_shown = term.get("last_shown")
        if last_shown:
            try:
                last_date = datetime.strptime(last_shown, "%Y-%m-%d").date()
                if (today_date - last_date).days < 180:
                    continue
            except ValueError:
                pass
        if any(alias in combined_text for alias in term["aliases"]):
            selected.append(term)
    for term in selected:
        term["last_shown"] = today
    return selected


_MONEY_RE = re.compile(r"\$\d|億円|CHIPS")


def is_money_policy(note: dict) -> bool:
    """landscape-positionに『資本』を含む、または本文・投資含意に金額表現を含む記事か判定する。"""
    if "資本" in (note.get("position") or ""):
        return True
    return bool(_MONEY_RE.search(note.get("raw_text", "")))


def classify_weekly_articles(quantum_notes: list[dict], updates: list[dict]) -> tuple[list[dict], list[dict]]:
    """週次記事を「お金と政策」「その他」に振り分ける。指標更新の根拠になった記事
    （距離を縮めた動きセクションで既に列挙済み）は両方から除く。"""
    updated_urls = {u["note"]["url"] for u in updates}
    remaining = [n for n in quantum_notes if n["url"] not in updated_urls]
    money = [n for n in remaining if is_money_policy(n)]
    money_urls = {n["url"] for n in money}
    other = [n for n in remaining if n["url"] not in money_urls]
    return money, other


def weeks_since(as_of: str, today_date) -> str:
    """as_of と今日の差÷7の週数文字列（0なら「今週更新」）。"""
    try:
        as_of_date = datetime.strptime(as_of, "%Y-%m-%d").date()
    except ValueError:
        return ""
    weeks = (today_date - as_of_date).days // 7
    return "今週更新" if weeks <= 0 else f"{weeks}週間"


def min_weeks_number(indicators: list[dict], today_date) -> int:
    weeks_list = []
    for ind in indicators:
        try:
            as_of_date = datetime.strptime(ind["as_of"], "%Y-%m-%d").date()
        except ValueError:
            continue
        weeks_list.append((today_date - as_of_date).days // 7)
    return min(weeks_list) if weeks_list else 0


def no_progress_line(indicators: list[dict], today_date) -> str:
    """指標更新が0件だった週に出す1行。

    「最短N週間」だけだと、直近更新がその週のうちだったときに『材料なし・0週間』と
    並んで意味が通らない。最後に動いた指標とその日付を名指しする。"""
    latest = None
    for ind in indicators:
        try:
            as_of_date = datetime.strptime(ind["as_of"], "%Y-%m-%d").date()
        except ValueError:
            continue
        if latest is None or as_of_date > latest[0]:
            latest = (as_of_date, ind)
    if latest is None:
        return "今週は指標を動かした記事なし"
    as_of_date, ind = latest
    weeks = (today_date - as_of_date).days // 7
    span = "今週" if weeks == 0 else f"{weeks}週間前"
    return (f"今週は指標を動かした記事なし（最後に動いたのは「{ind['label']}」"
            f"／{ind['as_of']}・{span}）")


def build_target_line(indicators: list[dict]) -> str:
    """logical_qubits の targets[0] から『目標線：…まで、あと約N倍』の1行を組み立てる。"""
    indicator = next((i for i in indicators if i["id"] == "logical_qubits"), None)
    if not indicator or not indicator.get("targets"):
        return ""
    target = indicator["targets"][0]
    current = indicator["value"]
    if not current:
        return ""
    label = re.sub(r"（[^）]*）", "", target["label"]).strip()
    n = target["value"] / current
    return f"目標線：{label}（{target['value']}{indicator['unit']}）まで、あと約{n:.1f}倍"


def build_weekly_body(quantum_notes: list[dict], milestones: dict, updates: list[dict],
                       glossary_terms: list[dict], summary: str, today: str,
                       heatmap_available: bool = False) -> str:
    """量子週次ダイジェストのplain本文（実現までの距離ダッシュボード形式）を組み立てる。"""
    today_date = datetime.strptime(today, "%Y-%m-%d").date()
    indicators = milestones["indicators"]
    updates_by_id = {u["id"]: u for u in updates}

    lines = [
        f"Frontier（量子） 週次ダイジェスト {today}"
        f"（今週{len(quantum_notes)}件・指標更新{len(updates)}件）",
        "",
        "■ 実現までの距離",
    ]
    for ind in indicators:
        upd = updates_by_id.get(ind["id"])
        bits = [ind["label"], ind["display"]]
        if upd:
            bits.append(f'{upd["old_display"]}→{upd["new_display"]}')
        bits.append(weeks_since(ind["as_of"], today_date))
        lines.append("・" + "｜".join(bits))
    target_line = build_target_line(indicators)
    if target_line:
        lines.append(target_line)
    lines.append("")

    if summary:
        lines += ["今週の総括", summary, ""]

    lines.append(f"■ 距離を縮めた動き（{len(updates)}件）" if updates else "■ 距離を縮めた動き")
    if not updates:
        lines.append(
            no_progress_line(indicators, today_date)
        )
    else:
        for u in updates:
            note = u["note"]
            lines.append(f"・{note['title']}")
            if note["claim"]:
                lines.append(f"  {note['claim']}")
            lines.append(f'  → {u["label"]}を{u["old_display"]}から{u["new_display"]}に更新')
            lines.append(f"  🔗 {note['url']}")
    lines.append("")

    money, other = classify_weekly_articles(quantum_notes, updates)
    lines.append(f"■ お金と政策（{len(money)}件）")
    for n in money:
        lines.append(f"・{n['title']}")
        lines.append(f"  🔗 {n['url']}")
    lines.append("")

    lines.append("■ その他の動き")
    for n in other:
        lines.append(f"・{n['title']}")
        lines.append(f"  🔗 {n['url']}")
    lines.append("")

    if glossary_terms:
        lines.append("■ 今週の初出用語")
        for t in glossary_terms:
            lines.append(f"・{t['term']}: {t['definition']}")
        lines.append("")

    if heatmap_available:
        lines += ["🗺 市場規模ヒートマップは HTML表示で確認", ""]
    return "\n".join(lines) + "\n"


def build_weekly_html_body(quantum_notes: list[dict], milestones: dict, updates: list[dict],
                            glossary_terms: list[dict], summary: str, today: str,
                            heatmap_html: str = "") -> str:
    """量子週次ダイジェストのHTML本文（実現までの距離ダッシュボード形式）を組み立てる。"""
    accent = CATEGORIES["Frontier（量子）"]["accent"]
    today_date = datetime.strptime(today, "%Y-%m-%d").date()
    indicators = milestones["indicators"]
    updates_by_id = {u["id"]: u for u in updates}

    parts = [
        '<div style="max-width:600px;margin:0 auto;'
        "font-family:-apple-system,'Hiragino Sans',sans-serif;"
        'background-color:#f1f3f4;padding:16px;">',
        f'<div style="background-color:{accent};border-radius:8px 8px 0 0;'
        'padding:16px;color:#ffffff;">'
        '<div style="font-size:20px;font-weight:bold;">Frontier（量子） 週次ダイジェスト</div>'
        f'<div style="font-size:13px;opacity:0.9;margin-top:4px;">'
        f'{html.escape(today)}（今週{len(quantum_notes)}件・指標更新{len(updates)}件）</div>'
        "</div>",
    ]

    # ■ 実現までの距離
    ind_rows = []
    for ind in indicators:
        upd = updates_by_id.get(ind["id"])
        arrow = (
            f'{html.escape(upd["old_display"])}→<strong>{html.escape(upd["new_display"])}</strong>'
            if upd else "—"
        )
        ind_rows.append(
            "<tr>"
            f'<td style="padding:6px 8px;border-bottom:1px solid #dadce0;font-size:13px;'
            f'color:#202124;">{html.escape(ind["label"])}</td>'
            f'<td style="padding:6px 8px;border-bottom:1px solid #dadce0;font-size:13px;'
            f'text-align:right;color:#202124;white-space:nowrap;">{html.escape(ind["display"])}</td>'
            f'<td style="padding:6px 8px;border-bottom:1px solid #dadce0;font-size:12px;'
            f'text-align:right;color:#188038;white-space:nowrap;">{arrow}</td>'
            f'<td style="padding:6px 8px;border-bottom:1px solid #dadce0;font-size:12px;'
            f'text-align:right;color:#5f6368;white-space:nowrap;">'
            f'{html.escape(weeks_since(ind["as_of"], today_date))}</td>'
            "</tr>"
        )
    target_line = build_target_line(indicators)
    parts.append(
        '<div style="background-color:#ffffff;border-radius:8px;padding:16px;margin-top:12px;">'
        '<div style="font-size:16px;font-weight:bold;color:#202124;">■ 実現までの距離</div>'
        '<table style="width:100%;border-collapse:collapse;margin-top:8px;">'
        '<tr style="background-color:#f8f9fa;">'
        '<th style="padding:6px 8px;font-size:12px;color:#5f6368;text-align:left;">指標</th>'
        '<th style="padding:6px 8px;font-size:12px;color:#5f6368;text-align:right;">現在値</th>'
        '<th style="padding:6px 8px;font-size:12px;color:#5f6368;text-align:right;">前回→今週</th>'
        '<th style="padding:6px 8px;font-size:12px;color:#5f6368;text-align:right;">最終更新</th>'
        "</tr>" + "".join(ind_rows) + "</table>"
        + (
            f'<div style="font-size:12px;color:#5f6368;margin-top:8px;">{html.escape(target_line)}</div>'
            if target_line else ""
        )
        + "</div>"
    )

    # 今週の総括
    if summary:
        parts.append(
            '<div style="background-color:#f8f9fa;border-radius:8px;padding:16px;'
            'margin-top:12px;">'
            '<div style="font-size:13px;font-weight:bold;color:#5f6368;">今週の総括</div>'
            f'<div style="font-size:14px;color:#3c4043;line-height:1.6;margin-top:8px;">'
            f'{_esc_rich(summary)}</div>'
            "</div>"
        )

    # ■ 距離を縮めた動き
    heading = f"■ 距離を縮めた動き（{len(updates)}件）" if updates else "■ 距離を縮めた動き"
    section = [
        '<div style="background-color:#ffffff;border-radius:8px;padding:16px;margin-top:12px;">'
        f'<div style="font-size:16px;font-weight:bold;color:#202124;">{html.escape(heading)}</div>'
    ]
    if not updates:
        min_weeks = min_weeks_number(indicators, today_date)
        section.append(
            '<div style="font-size:14px;color:#5f6368;margin-top:8px;">'
            f'{html.escape(no_progress_line(indicators, today_date))}</div>'
        )
    else:
        for u in updates:
            note = u["note"]
            section.append(
                '<div style="margin-top:12px;padding-top:12px;border-top:1px solid #dadce0;">'
                f'<a href="{html.escape(note["url"], quote=True)}" '
                f'style="color:{accent};text-decoration:none;font-size:15px;font-weight:bold;">'
                f'{html.escape(note["title"])}</a>'
                + (
                    f'<div style="font-size:13px;color:#3c4043;margin-top:4px;">'
                    f'{html.escape(note["claim"])}</div>' if note["claim"] else ""
                )
                + '<div style="font-size:13px;color:#188038;margin-top:4px;">'
                f'→ {html.escape(u["label"])}を{html.escape(u["old_display"])}から'
                f'{html.escape(u["new_display"])}に更新</div>'
                "</div>"
            )
    section.append("</div>")
    parts.append("".join(section))

    # ■ お金と政策 / ■ その他の動き
    money, other = classify_weekly_articles(quantum_notes, updates)

    def build_link_list(title: str, notes_list: list[dict]) -> str:
        rows_html = "".join(
            '<div style="padding:8px 0;border-bottom:1px solid #dadce0;">'
            f'<a href="{html.escape(n["url"], quote=True)}" '
            f'style="color:{accent};text-decoration:none;font-size:14px;">'
            f'{html.escape(n["title"])}</a></div>'
            for n in notes_list
        )
        return (
            '<div style="background-color:#ffffff;border-radius:8px;padding:16px;margin-top:12px;">'
            f'<div style="font-size:16px;font-weight:bold;color:#202124;">{html.escape(title)}</div>'
            f'<div style="margin-top:4px;">{rows_html}</div>'
            "</div>"
        )

    parts.append(build_link_list(f"■ お金と政策（{len(money)}件）", money))
    parts.append(build_link_list("■ その他の動き", other))

    # ■ 今週の初出用語
    if glossary_terms:
        terms_html = "".join(
            '<div style="margin-top:8px;">'
            f'<div style="font-size:14px;font-weight:bold;color:#202124;">{html.escape(t["term"])}</div>'
            f'<div style="font-size:13px;color:#3c4043;margin-top:2px;">{html.escape(t["definition"])}</div>'
            "</div>"
            for t in glossary_terms
        )
        parts.append(
            '<div style="background-color:#f8f9fa;border-radius:8px;padding:16px;margin-top:12px;">'
            '<div style="font-size:16px;font-weight:bold;color:#202124;">■ 今週の初出用語</div>'
            + terms_html + "</div>"
        )

    if heatmap_html:
        parts.append(heatmap_html)

    parts.append("</div>")
    return "".join(parts)


def send_weekly_quantum_email(quantum_notes: list[dict], milestones: dict, updates: list[dict],
                               glossary_terms: list[dict], today: str) -> None:
    """量子週次ダイジェストを1通だけ送信する。"""
    dry_run = os.environ.get("DRY_RUN") == "1"
    # シークレット値に末尾改行が入っているとメールヘッダーが弾かれるため必ずstrip
    username = os.environ["GMAIL_USERNAME"].strip()
    password = os.environ.get("GMAIL_APP_PASSWORD", "").strip()

    market_data = load_market_data()
    include_heatmaps = os.environ.get("INCLUDE_HEATMAPS", "1") != "0"

    summary = gemini_weekly_summary(quantum_notes)

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

    subject = (
        f"🔭 [Frontier（量子）] 週次ダイジェスト {today}"
        f"（今週{len(quantum_notes)}件・指標更新{len(updates)}件）"
    )
    body = build_weekly_body(
        quantum_notes, milestones, updates, glossary_terms, summary, today, bool(heatmap_html)
    )
    html_body = build_weekly_html_body(
        quantum_notes, milestones, updates, glossary_terms, summary, today, heatmap_html
    )

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
    # 相対/絶対パスの取り違えで自分自身を「過去ノート」と誤認しないよう正規化して比較する。
    # （絶対パスで呼ぶと全記事が無言で重複判定され、0件配信になる事故があった）
    pending = {os.path.realpath(p) for p in paths}
    past_urls = set()
    for p in glob.glob("00-Inbox/*.md"):
        if os.path.realpath(p) in pending:
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

    updates = []
    if not quantum_notes:
        print("No quantum articles this week")
    else:
        dry_run = os.environ.get("DRY_RUN") == "1"
        today = datetime.now(JST).strftime("%Y-%m-%d")

        milestones = load_json(MILESTONES_PATH)
        updates = apply_milestone_updates(milestones, quantum_notes, today)
        if updates:
            print(f"Milestone updates detected: {len(updates)}")
            for u in updates:
                print(f"  {u['id']}: {u['old_display']} -> {u['new_display']} ({u['note']['url']})")
            if not dry_run:
                save_json(MILESTONES_PATH, milestones, trailing_newline=True)
        else:
            print("Milestone updates detected: 0")

        glossary = load_json(GLOSSARY_PATH)
        glossary_terms = detect_new_terms(glossary, quantum_notes, today)
        print(f"New glossary terms: {len(glossary_terms)}")
        if glossary_terms and not dry_run:
            save_json(GLOSSARY_PATH, glossary, trailing_newline=False)

        send_weekly_quantum_email(quantum_notes, milestones, updates, glossary_terms, today)

    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as f:
            f.write(f"count={len(quantum_notes)}\n")
    print(f"Built weekly quantum digest: {len(quantum_notes)} articles, "
          f"{len(updates)} milestone updates")


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
