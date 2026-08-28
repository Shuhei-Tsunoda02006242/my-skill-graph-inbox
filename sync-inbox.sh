#!/bin/bash
# Pulls inbox repo, reconciles vault against a ledger of already-synced
# files, copies missing notes, and notifies.
#
# Modes:
#   (no args)              normal run — pull, diff against ledger, copy, notify
#   --seed                 write current 00-Inbox/*.md basenames to the ledger and exit
#   --backfill [--since D] [--yes]
#                           copy any *.md whose basename is missing anywhere in
#                           the vault, regardless of ledger state

set -euo pipefail

INBOX_DIR="/Users/rena/projects/skill-graph/My-Skill-Graph-Inbox"
VAULT="/Users/rena/projects/skill-graph/My-Skill-Graph"
VAULT_INBOX="$VAULT/00-Inbox"
LEDGER="$INBOX_DIR/.sync-ledger"
GIT="/usr/bin/git"
NOTIFIER="/opt/homebrew/bin/terminal-notifier"

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') $*"
}

# Prints sorted basenames of *.md in $INBOX_DIR/00-Inbox, excluding README.md.
list_inbox_basenames() {
    local f bn
    for f in "$INBOX_DIR"/00-Inbox/*.md; do
        [ -e "$f" ] || continue
        bn=$(basename "$f")
        [ "$bn" = "README.md" ] && continue
        printf '%s\n' "$bn"
    done | sort
}

do_seed() {
    local tmp
    tmp=$(mktemp)
    list_inbox_basenames > "$tmp"
    mv "$tmp" "$LEDGER"
    local count
    count=$(wc -l < "$LEDGER" | tr -d ' ')
    echo "台帳を作成しました: ${count}件 (${LEDGER})"
}

do_backfill() {
    local since="" yes=0
    while [ $# -gt 0 ]; do
        case "$1" in
            --since)
                if [ $# -lt 2 ]; then
                    echo "--since には日付(YYYY-MM-DD)を指定してください" >&2
                    exit 1
                fi
                since="$2"
                shift 2
                ;;
            --yes)
                yes=1
                shift
                ;;
            *)
                echo "不明な引数: $1" >&2
                exit 1
                ;;
        esac
    done

    local tmp_vault tmp_cand tmp_targets
    tmp_vault=$(mktemp)
    tmp_cand=$(mktemp)
    tmp_targets=$(mktemp)
    trap 'rm -f "$tmp_vault" "$tmp_cand" "$tmp_targets"' RETURN

    find "$VAULT" -path "$VAULT/.git" -prune -o -type f -print \
        | xargs -I{} basename {} \
        | sort -u > "$tmp_vault"

    list_inbox_basenames > "$tmp_cand"

    if [ -n "$since" ]; then
        awk -v since="$since" 'substr($0,1,10) >= since' "$tmp_cand" > "${tmp_cand}.filtered"
        mv "${tmp_cand}.filtered" "$tmp_cand"
    fi

    comm -23 "$tmp_cand" "$tmp_vault" > "$tmp_targets" || true

    local total
    total=$(wc -l < "$tmp_targets" | tr -d ' ')

    echo "対象件数: ${total}件"
    if [ "$total" -gt 0 ]; then
        echo "日付別内訳:"
        sed 's/^\(.\{10\}\).*/\1/' "$tmp_targets" | sort | uniq -c | while read -r cnt date; do
            echo "  ${date}: ${cnt}件"
        done
    fi

    if [ "$total" -eq 0 ]; then
        echo "対象なし。終了します。"
        return 0
    fi

    if [ "$yes" -ne 1 ]; then
        read -r -p "上記 ${total}件 を vault にコピーします。よろしいですか？ (y/N) " ans
        case "$ans" in
            y|Y) ;;
            *)
                echo "中断しました。"
                return 0
                ;;
        esac
    fi

    local copied=0 bn
    while IFS= read -r bn; do
        [ -z "$bn" ] && continue
        cp "$INBOX_DIR/00-Inbox/$bn" "$VAULT_INBOX/$bn"
        printf '%s\n' "$bn" >> "$LEDGER"
        copied=$((copied + 1))
    done < "$tmp_targets"

    sort -u -o "$LEDGER" "$LEDGER"

    echo "コピー完了: ${copied}件"
}

do_normal() {
    # pull が失敗しても処理は続ける。前回までにローカルへ降りてきていて
    # まだ台帳に載っていないノートは、ネットワークが落ちていても Vault へ
    # 反映できるため。ここで exit すると「取得済みなのに同期されない」
    # 取りこぼしが再発する（2026-08-26に8/24〜8/25分16件で実際に発生）。
    local pull_failed=0
    if ! "$GIT" -C "$INBOX_DIR" pull origin main; then
        log "WARN: git pull に失敗しました（ローカルにある分だけ同期します）"
        pull_failed=1
    fi

    if [ ! -f "$LEDGER" ]; then
        log "台帳が存在しないため seed します"
        do_seed
        return 0
    fi

    local tmp_inbox tmp_new
    tmp_inbox=$(mktemp)
    tmp_new=$(mktemp)
    trap 'rm -f "$tmp_inbox" "$tmp_new"' RETURN

    list_inbox_basenames > "$tmp_inbox"
    comm -23 "$tmp_inbox" "$LEDGER" > "$tmp_new" || true

    local count=0 bn
    while IFS= read -r bn; do
        [ -z "$bn" ] && continue
        if cp "$INBOX_DIR/00-Inbox/$bn" "$VAULT_INBOX/$bn"; then
            printf '%s\n' "$bn" >> "$LEDGER"
            count=$((count + 1))
        fi
    done < "$tmp_new"

    if [ "$count" -gt 0 ]; then
        sort -u -o "$LEDGER" "$LEDGER"
        if [ -x "$NOTIFIER" ]; then
            "$NOTIFIER" \
                -title "Skill Graph Inbox" \
                -message "新着記事 ${count}件 → Vaultに追加済み" \
                -sound default \
                -open "obsidian://open?vault=My-Skill-Graph"
        fi
    fi

    log "新着 ${count}件"

    if [ "$pull_failed" -eq 1 ]; then
        log "ERROR: git pull に失敗したままです（次回実行で再取得します）"
        return 1
    fi
}

case "${1:-}" in
    --seed)
        do_seed
        ;;
    --backfill)
        shift
        do_backfill "$@"
        ;;
    "")
        do_normal
        ;;
    *)
        echo "不明な引数: $1" >&2
        exit 1
        ;;
esac
