#!/bin/bash
# GitHub Token Helper Functions for Secret Manager
# Source this file: source scripts/github_token_helper.sh

# Funksjon for å hente GitHub token fra Secret Manager
get_github_token() {
    gcloud secrets versions access latest --secret=github-token --project=dotted-stage-476513-r4 2>/dev/null
}

# Funksjon for å teste GitHub token
test_github_token() {
    local token=$(get_github_token)
    if [ -z "$token" ]; then
        echo "❌ Kunne ikke hente token fra Secret Manager"
        return 1
    fi

    echo "🔍 Tester token..."
    local response=$(curl -s -H "Authorization: token $token" https://api.github.com/user)
    local login=$(echo "$response" | grep -o '"login":"[^"]*"' | cut -d'"' -f4)

    if [ -n "$login" ]; then
        echo "✅ Token fungerer!"
        echo "   Bruker: $login"
        return 0
    else
        echo "❌ Token fungerer ikke"
        return 1
    fi
}

# Funksjon for å pushe med token
git_push_with_token() {
    local token=$(get_github_token)
    if [ -z "$token" ]; then
        echo "❌ Kunne ikke hente token"
        return 1
    fi

    local branch=${1:-main}
    local remote=${2:-origin}

    echo "📤 Pusher til $remote/$branch..."
    git push https://$token@github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums.git $branch
}

# Funksjon for å pulle med token
git_pull_with_token() {
    local token=$(get_github_token)
    if [ -z "$token" ]; then
        echo "❌ Kunne ikke hente token"
        return 1
    fi

    local branch=${1:-main}
    local remote=${2:-origin}

    echo "📥 Puller fra $remote/$branch..."
    git pull https://$token@github.com/noonaut-homo-lumen-resonans/homo-lumen-compendiums.git $branch
}

# Vis hjelp
github_token_help() {
    echo "GitHub Token Helper Functions"
    echo ""
    echo "Bruk: source scripts/github_token_helper.sh"
    echo ""
    echo "Tilgjengelige funksjoner:"
    echo "  get_github_token          - Henter token fra Secret Manager"
    echo "  test_github_token         - Tester om token fungerer"
    echo "  git_push_with_token       - Pusher til GitHub med token"
    echo "  git_pull_with_token       - Puller fra GitHub med token"
    echo "  github_token_help         - Viser denne hjelpen"
    echo ""
    echo "Eksempel:"
    echo "  source scripts/github_token_helper.sh"
    echo "  test_github_token"
    echo "  git_push_with_token main"
}

