# GitHub Actions - Notion SLL Sync

## Overview

This GitHub Action automatically syncs Learning Points (LPs) from commit messages to the Notion SLL (Shared Learning Library) database.

## Setup

### 1. Add Secrets to GitHub Repository

Go to **Settings → Secrets and variables → Actions** and add:

- `NOTION_API_KEY`: Your Notion integration API key
- `SLL_DATABASE_ID`: The database ID of your SLL in Notion (currently: `84da6cbd09d640fb868e41444b941991`)

### 2. Get Notion API Key

1. Go to https://www.notion.so/my-integrations
2. Click "New integration"
3. Name it "Homo Lumen GitHub Sync"
4. Select the workspace
5. Copy the "Internal Integration Token"
6. Add it as `NOTION_API_KEY` secret in GitHub

### 3. Share SLL Database with Integration

1. Open the SLL database in Notion: https://www.notion.so/84da6cbd09d640fb868e41444b941991
2. Click "..." (more options) → "Add connections"
3. Select "Homo Lumen GitHub Sync" integration
4. Click "Confirm"

## Usage

### Commit Message Format

To create a Learning Point, use this format in your commit message:

```
LP #049: GitHub → Notion Sync Implemented

Automated sync from GitHub commits to SLL database using GitHub Actions.
Key insight: Automation enables real-time knowledge capture.

Agent: Manus
Category: Technical, Architecture
Tags: MCP, LAG-4, GitHub
```

**Format Rules:**
- First line: `LP #XXX: [Title]`
- Blank line
- Description (multiple lines allowed)
- Blank line
- Metadata:
  - `Agent: [Agent Name]` (required)
  - `Category: [Category1, Category2]` (optional, comma-separated)
  - `Tags: [Tag1, Tag2]` (optional, comma-separated)

### Valid Agent Names

- Orion
- Lira
- Nyra
- Thalus
- Zara
- Abacus
- Manus
- Aurora
- Code
- Falcon

### Valid Categories

- Architecture
- Philosophy
- Technical
- Collaboration
- Shadow-Work
- Innovation
- Healing
- Resonance

### Valid Tags

- MCP
- LAG-4
- Ubuntu-Playground
- NAV-Losen
- Innovation-Norge
- HOMO-AI-LUMEN-RESONANS

## How It Works

1. **Trigger**: Action runs on every push to `main` branch
2. **Parse**: `parse_commit.py` extracts LP metadata from commit message
3. **Sync**: `sync_to_notion.py` creates a new page in SLL database
4. **Report**: Action outputs Notion URL of created LP

## Testing Locally

```bash
# Test commit parser
export COMMIT_MESSAGE="LP #049: Test LP

This is a test learning point.

Agent: Manus
Category: Technical
Tags: MCP"

python .github/scripts/parse_commit.py

# Test Notion sync (requires secrets)
export NOTION_API_KEY="your_api_key"
export SLL_DATABASE_ID="84da6cbd09d640fb868e41444b941991"
export LP_DATA='{"lp_id":"LP #049 - Test","description":"Test","agent":"Manus","categories":["Technical"],"tags":["MCP"],"commit_url":"https://github.com/..."}'

python .github/scripts/sync_to_notion.py
```

## Troubleshooting

### Action fails with "Missing Notion credentials"

- Ensure `NOTION_API_KEY` and `SLL_DATABASE_ID` secrets are set in GitHub
- Verify the secrets are accessible to the workflow

### Action fails with "Could not create page"

- Ensure the SLL database is shared with the Notion integration
- Verify the database ID is correct
- Check that the agent name matches one of the valid options

### LP not detected in commit

- Verify commit message follows the exact format
- Ensure first line starts with `LP #XXX:`
- Check that there's a blank line between sections

## Examples

### Minimal LP (no categories/tags)

```
LP #050: Minimal Learning Point

This is the simplest valid LP format.

Agent: Manus
```

### Full LP (with categories and tags)

```
LP #051: Complete Learning Point Example

This LP demonstrates all available fields:
- Multiple categories
- Multiple tags
- Multi-line description

Key insight: Structure enables automation.

Agent: Orion
Category: Architecture, Philosophy, Technical
Tags: MCP, LAG-4, HOMO-AI-LUMEN-RESONANS
```

### Multi-paragraph Description

```
LP #052: Complex Learning Point

First paragraph of description.

Second paragraph with more details.

Third paragraph with conclusions.

Agent: Lira
Category: Healing, Collaboration
Tags: LAG-4
```

## Roadmap

### Week 1 (Current)
- ✅ GitHub Action skeleton
- ✅ Commit parser
- ✅ Notion sync script
- ⏳ Test with real commits
- ⏳ Add secrets to GitHub
- ⏳ Backfill historical LPs

### Week 2
- Link version history to learnings
- Auto-generate LP from significant commits
- Batch sync for multiple LPs

### Future
- Bi-directional sync (Notion → GitHub)
- Auto-categorization using AI
- Duplicate detection
- LP quality scoring

## Support

For issues or questions, contact Manus or create an issue in the repository.

---

**Prepared by:** Manus (Resonanskammer-Arkitekt)  
**Date:** 26. oktober 2025  
**Status:** Ready for Testing ⏳

