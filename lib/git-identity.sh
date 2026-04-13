#!/usr/bin/env bash
# git-identity.sh — auto-pick the correct gh account + git user for the current repo.
#
# Logic:
#   1. Read `origin` remote, parse the owner (user or org).
#   2. List accounts known to `gh auth status`.
#   3. If the owner matches one of those accounts, `gh auth switch` to it.
#   4. Set *local* git user.name/user.email from that gh account (never touches --global).
#   5. If no owner match, fall back to the currently active gh account.
#
# Invoked automatically by the PreToolUse hook in global-settings.json before any
# `git commit`, and callable directly by agents (see agents/research/*.md).
#
# Safe to run anywhere: exits 0 silently when not in a git repo or gh is unavailable.

set -u
command -v gh  >/dev/null 2>&1 || exit 0
command -v git >/dev/null 2>&1 || exit 0
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

remote=$(git remote get-url origin 2>/dev/null || true)
[ -z "$remote" ] && exit 0

# Parse owner from git@github.com:owner/repo(.git)? or https://github.com/owner/repo(.git)?
owner=$(printf '%s\n' "$remote" \
  | sed -E 's#\.git$##' \
  | sed -E 's#^(git@|https?://)[^/:]+[:/]##' \
  | awk -F/ '{print $1}')
[ -z "$owner" ] && exit 0

# Gather known gh accounts (one per line).
accounts=$(gh auth status 2>&1 | awk '/account / {for(i=1;i<=NF;i++) if ($i=="account") print $(i+1)}' | sort -u)

target=""
if printf '%s\n' "$accounts" | grep -qx "$owner"; then
  target="$owner"
fi

# Switch if we found a matching account and it isn't already active.
if [ -n "$target" ]; then
  active=$(gh auth status 2>&1 | awk '/Active account: true/{found=1} found && /account /{for(i=1;i<=NF;i++) if ($i=="account") print $(i+1); exit}')
  if [ "$active" != "$target" ]; then
    gh auth switch --hostname github.com --user "$target" >/dev/null 2>&1 || true
  fi
fi

# Pull identity from whichever account is now active.
name=$(gh api user --jq .name  2>/dev/null || true)
login=$(gh api user --jq .login 2>/dev/null || true)
email=$(gh api user --jq .email 2>/dev/null || true)
if [ -z "$email" ] || [ "$email" = "null" ]; then
  # noreply fallback derived from the login — works even when the user hides their email.
  if [ -n "$login" ]; then
    id=$(gh api user --jq .id 2>/dev/null || true)
    if [ -n "$id" ]; then
      email="${id}+${login}@users.noreply.github.com"
    fi
  fi
fi
[ -z "$name" ] || [ "$name" = "null" ] && name="$login"

[ -n "$name"  ] && git config --local user.name  "$name"  2>/dev/null || true
[ -n "$email" ] && git config --local user.email "$email" 2>/dev/null || true

# Log what we did (pre-commit hook reads stdout, so keep it to stderr).
printf '[git-identity] repo owner=%s  active=%s  user=%s <%s>\n' \
  "$owner" "${target:-$(gh api user --jq .login 2>/dev/null)}" "${name}" "${email}" >&2
exit 0
