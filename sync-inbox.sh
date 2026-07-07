#!/bin/bash
# Pulls inbox repo, copies new notes to vault, and notifies

INBOX_DIR="$HOME/projects/skill-graph/My-Skill-Graph-Inbox"
VAULT_INBOX="$HOME/projects/skill-graph/My-Skill-Graph/00-Inbox"
NOTIFIER="/opt/homebrew/bin/terminal-notifier"
GIT="/usr/bin/git"

cd "$INBOX_DIR" || exit 1

BEFORE=$($GIT rev-parse HEAD)
$GIT pull --quiet origin main 2>/dev/null
AFTER=$($GIT rev-parse HEAD)

if [ "$BEFORE" != "$AFTER" ]; then
    NEW_FILES=$($GIT diff --name-only "$BEFORE" "$AFTER" | grep '\.md$' | grep -v 'README')
    COUNT=$(echo "$NEW_FILES" | grep -c '\.md$')

    # Copy new files to vault inbox
    while IFS= read -r file; do
        [ -z "$file" ] && continue
        cp "$INBOX_DIR/$file" "$VAULT_INBOX/$(basename "$file")"
    done <<< "$NEW_FILES"

    $NOTIFIER \
        -title "Skill Graph Inbox" \
        -message "新着記事 ${COUNT}件 → Vaultに追加済み" \
        -sound default \
        -open "obsidian://open?vault=My-Skill-Graph"
fi
