#!/bin/bash
# sync-skills-from-agentpad.sh
# Pulls all skills from AgentPad repo using parallel curl downloads
# Skills are gitignored - AgentPad remains source of truth

set -e

AGENTPAD_REPO="barnymurt/AgentPad"
SKILLS_DIR="skills"
BRANCHES=(
    "claude/skillbatch-p0fNB"
    "data-source-validation"
)

echo "=== AgentPad Skill Sync Script ==="
echo "Pulling skills from branches: ${BRANCHES[*]}"
echo ""

# Function to download a single file
download_file() {
    local branch="$1"
    local file_path="$2"
    local dest_path="$3"
    
    mkdir -p "$(dirname "$dest_path")"
    curl -sL "https://raw.githubusercontent.com/$AGENTPAD_REPO/$branch/$file_path" -o "$dest_path" 2>/dev/null
}

export -f download_file
export AGENTPAD_REPO

for branch in "${BRANCHES[@]}"; do
    echo "--- Fetching from branch: $branch ---"
    
    # Get branch SHA for tree API
    branch_sha=$(gh api "repos/$AGENTPAD_REPO/branches/$branch" --jq '.commit.sha')
    
    # Get all skill files (SKILL.md and examples.json only, skip references)
    files=$(gh api "repos/$AGENTPAD_REPO/git/trees/$branch_sha?recursive=1" --jq '.tree[].path' 2>/dev/null | grep -E "^skills/[^/]+/(SKILL\.md|examples\.json)$")
    
    count=$(echo "$files" | wc -l)
    echo "  Found $count skill files to download"
    
    # Download files in parallel (10 at a time)
    echo "$files" | xargs -P 10 -I {} bash -c '
        branch="'"$branch"'"
        file_path="{}"
        skill_name=$(echo "$file_path" | cut -d/ -f2)
        filename=$(basename "$file_path")
        dest_path="skills/$skill_name/$filename"
        download_file "$branch" "$file_path" "$dest_path"
        echo "  Downloaded: $skill_name/$filename"
    '
    
    echo "  Done with branch: $branch"
done

echo ""
echo "=== Sync Complete ==="
echo "Skills stored in: $SKILLS_DIR/"
echo ""
echo "To update: run this script again"