#!/usr/bin/env python3
"""キャプチャが0件だった日に通知メールを送る。

daily-digest.yml から、検出ファイル数が0件だったときだけ呼ばれる。
「0件＝異常」ではない点に注意が必要で、保険cron（8:20 JST）は本命cronが
送信に成功した後も必ず0件になる。そのため呼び出し側が巡回ログ
（digests/YYYY-MM-DD-sources.md）を見て理由を判定し、本当に異常なときだけ
このスクリプトを呼ぶ。ここでは理由を受け取って本文を組み立てるだけ。

環境変数:
- GMAIL_USERNAME / GMAIL_APP_PASSWORD  SMTP認証情報（送受信とも同一アドレス）
- DRY_RUN=1                            SMTP送信せず標準出力するのみ

使い方: python3 scripts/notify_capture_failure.py <YYYY-MM-DD> <reason>
  reason: all-failed（巡回ログの全ソースが失敗）/ no-log（巡回ログ自体が無い）
"""
import os
import smtplib
import sys
from email.message import EmailMessage

REASON_LABEL = {
    "all-failed": "全ソース取得失敗",
    "no-log": "キャプチャ未実行（巡回ログなし）",
}

REASON_DETAIL = {
    "all-failed": (
        "クラウドキャプチャルーチンは動きましたが、巡回ログの全ソースが取得失敗でした。\n"
        "過去の同種障害はいずれもegressポリシーの間欠障害で、環境設定側では直せません\n"
        "（2026-09-08に設定の保存し直し・apex追加とも効果なしを確認済み）。"
    ),
    "no-log": (
        "巡回ログ自体が作られていません。ルーチンが起動しなかったか、\n"
        "ログを書く前に落ちた可能性があります。claude.ai の実行履歴を確認してください。"
    ),
}


def build_body(date_str: str, reason: str, log_text: str | None) -> str:
    lines = [
        f"{date_str} のキャプチャが0件でした。理由: {REASON_LABEL.get(reason, reason)}",
        "",
        REASON_DETAIL.get(reason, ""),
        "",
        "■ この後どうなるか",
        "翌朝の実行で、この日は「障害日」と判定されてさかのぼり取得の対象になります",
        "（CLAUDE.md「障害日のさかのぼり取得」。各ソース最大2件、直近1日分のみ）。",
        "翌朝も0件だった場合はさかのぼりも効かないため、その日の記事は失われます。",
        "",
        "■ 確認する場所",
        f"- 巡回ログ: digests/{date_str}-sources.md",
        "- ルーチンの実行履歴: https://claude.ai/code",
        "",
    ]
    if log_text:
        lines += ["■ 巡回ログ", "", log_text.strip(), ""]
    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit("usage: notify_capture_failure.py <YYYY-MM-DD> <reason>")
    date_str, reason = sys.argv[1], sys.argv[2]

    log_path = f"digests/{date_str}-sources.md"
    log_text = None
    if os.path.isfile(log_path):
        log_text = open(log_path, encoding="utf-8").read()

    subject = f"⚠️ キャプチャ0件 {date_str}（{REASON_LABEL.get(reason, reason)}）"
    body = build_body(date_str, reason, log_text)

    if os.environ.get("DRY_RUN") == "1":
        print("=" * 60)
        print(f"Subject: {subject}")
        print("-" * 60)
        print(body)
        return

    username = os.environ["GMAIL_USERNAME"].strip()
    password = os.environ["GMAIL_APP_PASSWORD"].strip()
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"Skill Graph Inbox <{username}>"
    msg["To"] = username
    msg.set_content(body, charset="utf-8")
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(username, password)
        smtp.send_message(msg)
    print(f"Sent capture-failure notification for {date_str} ({reason})")


if __name__ == "__main__":
    main()
