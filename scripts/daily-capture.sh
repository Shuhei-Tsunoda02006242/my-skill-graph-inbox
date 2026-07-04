#!/bin/bash
# デイリーキャプチャループ自動実行スクリプト
# LaunchAgent から毎朝呼ばれる
#
# Claude がノート作成に成功しても --print モード内で git が実行できない
# ことがあるため、コミット & push はこのスクリプト側で確実に行う。

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INBOX_DIR="$(dirname "$SCRIPT_DIR")"
PROMPT_FILE="$SCRIPT_DIR/capture-prompt.txt"
LOG_DIR="$INBOX_DIR/logs"
LOG_FILE="$LOG_DIR/capture-$(date +%Y-%m-%d).log"
CLAUDE_BIN="/Users/rena/.local/bin/claude"

echo "=== $(date '+%Y-%m-%d %H:%M:%S') キャプチャ開始 ===" >> "$LOG_FILE"

cd "$INBOX_DIR"

# クラウド側ルーチンの朝キャプチャを取り込んでから開始（重複キャプチャ防止）
git pull --rebase --quiet origin main >> "$LOG_FILE" 2>&1 || true

"$CLAUDE_BIN" \
  --dangerously-skip-permissions \
  --print \
  "$(cat "$PROMPT_FILE")" \
  >> "$LOG_FILE" 2>&1 \
  || echo "claude exited with non-zero status" >> "$LOG_FILE"

# --- フォールバック: Claude がコミットできなかった当日ノートを拾って commit & push ---

source_name() {
  case "$1" in
    tc)  echo "TechCrunch";;
    tm)  echo "Techmeme";;
    sn)  echo "STAT News";;
    is)  echo "IEEE Spectrum";;
    qcr) echo "Quantum Computing Report";;
    fb)  echo "FierceBiotech";;
    ek)  echo "Electrek";;
    *)   echo "Skill Graph";;
  esac
}

TODAY=$(date +%Y-%m-%d)
COMMITTED=0

for prefix in tc tm sn is qcr fb ek; do
  FILES=$(git ls-files --others --exclude-standard "00-Inbox/${TODAY}-${prefix}-*.md")
  [ -z "$FILES" ] && continue
  N=$(echo "$FILES" | wc -l | tr -d ' ')
  WORD="articles"; [ "$N" = "1" ] && WORD="article"
  git add $FILES
  GIT_AUTHOR_NAME="Claude" GIT_AUTHOR_EMAIL="noreply@anthropic.com" \
    git commit --quiet -m "daily: $(source_name "$prefix") capture ${TODAY} (${N} ${WORD})" >> "$LOG_FILE" 2>&1
  echo "fallback commit: $(source_name "$prefix") ${N}件" >> "$LOG_FILE"
  COMMITTED=1
done

if [ "$COMMITTED" = "1" ]; then
  git push origin main >> "$LOG_FILE" 2>&1 \
    || { git pull --rebase --quiet origin main >> "$LOG_FILE" 2>&1 && git push origin main >> "$LOG_FILE" 2>&1; } \
    || echo "git push failed" >> "$LOG_FILE"
fi

echo "=== $(date '+%Y-%m-%d %H:%M:%S') キャプチャ完了 ===" >> "$LOG_FILE"

# 30日以上古いログを削除
find "$LOG_DIR" -name "capture-*.log" -mtime +30 -delete 2>/dev/null || true
