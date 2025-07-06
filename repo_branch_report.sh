#!/usr/bin/env bash
# repo_branch_report.sh
# Generates Markdown report of all branches in your GitHub repos, ordered by last update, and marks obsolete (> AGE_LIMIT_DAYS days).
# Requirements:
#  - Either GitHub CLI (`gh`) authenticated OR `curl` with environment variable GITHUB_TOKEN set.
#  - `jq` command-line JSON processor.
#  - Environment variable GITHUB_OWNER set to your GitHub username or org.
#
# Usage:
#  AGE_LIMIT_DAYS=15 GITHUB_OWNER=myuser ./repo_branch_report.sh

set -euo pipefail

AGE_LIMIT_DAYS=${AGE_LIMIT_DAYS:-15}
OWNER=${GITHUB_OWNER:-}
OUTPUT=${OUTPUT_FILE:-repos_branches_report.md}

if [[ -z "$OWNER" ]]; then
  echo "ERROR: Environment variable GITHUB_OWNER not set.\nSet it to your GitHub username or organization, e.g.:\n  export GITHUB_OWNER=youruser" >&2
  exit 1
fi

# Detect available GitHub interface: gh or curl
if command -v gh >/dev/null 2>&1; then
  GH_TOOL="gh"
# Fall back to curl; if no GITHUB_TOKEN we will make unauthenticated requests (rate-limited)
elif command -v curl >/dev/null 2>&1; then
  GH_TOOL="curl"
else
  echo "ERROR: Neither GitHub CLI nor curl found." >&2
  exit 1
fi

# Helper functions ----------------------------------------------------------
function gh_api() {
  # Wrapper around gh api (CLI) or curl
  local endpoint="$1" # Example: /user/repos
  if [[ "$GH_TOOL" == "gh" ]]; then
    gh api "$endpoint"
  else
    if [[ -n "${GITHUB_TOKEN:-}" ]]; then
      curl -sSL -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github+json" "https://api.github.com$endpoint"
    else
      curl -sSL -H "Accept: application/vnd.github+json" "https://api.github.com$endpoint"
    fi
  fi
}

function get_repos() {
  # Returns JSON array of repositories for the owner (user or org)
  # Use pagination (100 per page)
  local page=1
  local per_page=100
  local repos="[]"
  while true; do
    local resp=$(gh_api "/users/$OWNER/repos?per_page=$per_page&page=$page")
    # If org: /orgs/:org/repos
    if echo "$resp" | jq 'type' | grep -q 'array'; then
      :
    else
      resp=$(gh_api "/orgs/$OWNER/repos?per_page=$per_page&page=$page")
    fi
    local count=$(echo "$resp" | jq 'length')
    repos=$(jq -s 'add' <(echo "$repos") <(echo "$resp"))
    if (( count < per_page )); then break; fi
    ((page++))
  done
  echo "$repos"
}

function list_branches() {
  local repo_full="$1" # owner/name
  gh_api "/repos/$repo_full/branches?per_page=100"
}

function get_commit() {
  local repo_full="$1"
  local branch="$2"
  gh_api "/repos/$repo_full/commits/$branch"
}

# --------------------------------------------------------------------------

echo "| Repository | Branch | Last commit date | Message | Default | Obsolete |" > "$OUTPUT"
echo "|------------|--------|------------------|---------|---------|----------|" >> "$OUTPUT"

# Collect repositories
repos_json=$(get_repos)
repo_count=$(echo "$repos_json" | jq 'length')

for ((i=0; i<repo_count; i++)); do
  repo=$(echo "$repos_json" | jq -r ".[$i].full_name")
  default_branch=$(echo "$repos_json" | jq -r ".[$i].default_branch")

  branches_json=$(list_branches "$repo")
  branch_count=$(echo "$branches_json" | jq 'length')

  for ((j=0; j<branch_count; j++)); do
    br=$(echo "$branches_json" | jq -r ".[$j].name")
    commit_json=$(get_commit "$repo" "$br")
    commit_date=$(echo "$commit_json" | jq -r '.commit.author.date')
    commit_msg=$(echo "$commit_json" | jq -r '.commit.message' | head -c 60 | tr '\n' ' ')
    days_old=$(( ( $(date +%s) - $(date -d "$commit_date" +%s) ) / 86400 ))
    obsolete=""
    [[ $days_old -gt $AGE_LIMIT_DAYS ]] && obsolete="⚠️"
    is_default=""
    [[ "$br" == "$default_branch" ]] && is_default="✅"
    echo "| $repo | $br | $commit_date | $commit_msg | $is_default | $obsolete |" >> "$OUTPUT"
  done

done

echo "Report saved to $OUTPUT"