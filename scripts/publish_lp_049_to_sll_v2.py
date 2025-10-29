#!/usr/bin/env python3
"""
Publish LP #049A-G to Notion SLL Database (Schema V2)
Fixed to match actual SLL database schema
"""

import os
import requests
from datetime import datetime

# Notion Configuration
NOTION_TOKEN = os.getenv("NOTION_API_KEY", "***REMOVED***")
SLL_DATABASE_ID = "84da6cbd09d640fb868e41444b941991"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Learning Points from SMK #049
LEARNING_POINTS = [
    {
        "lp_id": "LP-2025-10-29-049A",
        "title": "Emoji Crashes Hide Daemon Thread Failures",
        "content": "On Windows with cp1252 encoding, emoji characters in print() statements cause UnicodeEncodeError. When this happens in daemon background threads, the thread silently fails without logging to stderr - making it appear as if the thread never started. Replace all emojis with ASCII text ([PASS], [FAIL], etc.) to prevent crashes.",
        "agent": "Code",
        "tags": ["windows", "python", "threading", "emoji", "encoding"],
        "category": ["Technical", "Platform-Specific"],
        "half_life_days": 180,
        "source_smk": "SMK_049"
    },
    {
        "lp_id": "LP-2025-10-29-049B",
        "title": "Test Infrastructure Before Testing Features",
        "content": "When running validation tests on complex systems, test the testing infrastructure first. All 3 of Orion's tests initially failed not because features were broken, but because the testing infrastructure had bugs (emoji encoding, array unwrapping, missing integrations). Meta-testing checklist: (1) Servers running? (2) Background threads started? (3) API keys valid? (4) File paths accessible? (5) Encoding correct?",
        "agent": "Code",
        "tags": ["testing", "infrastructure", "validation", "meta-testing"],
        "category": ["Testing", "Systems"],
        "half_life_days": 365,
        "source_smk": "SMK_049"
    },
    {
        "lp_id": "LP-2025-10-29-049C",
        "title": "Triadiske Portvokter Validation Pattern",
        "content": "To comprehensively test the 3-layer Triadiske Portvokter system: (1) BiofeltGate with HRV<40 (should block with recommendations), (2) ThalosFilter with SQL injection (should block with ethical reasoning), (3) MutationLog with normal write (should approve and log). Verify GENOMOS logging for all 3 outcomes. This pattern validates: Consciousness (BiofeltGate) → Conscience (ThalosFilter) → Memory (MutationLog).",
        "agent": "Code",
        "tags": ["portvokter", "triadisk-etikk", "validation", "testing-pattern"],
        "category": ["Testing", "Ethics", "Architecture"],
        "half_life_days": 730,
        "source_smk": "SMK_049"
    },
    {
        "lp_id": "LP-2025-10-29-049D",
        "title": "SMK V2.0 Provenance Formula Syntax",
        "content": "Notion API formula syntax is complex and error-prone. When adding 8+ properties to a database, use hybrid approach: API for simple properties (text, number, select, checkbox, date), manual UI for formula properties. This saves debugging time and reduces API error complexity. Example: temporal_weight formula had to be added manually after schema migration.",
        "agent": "Code",
        "tags": ["notion", "api", "formula", "schema-migration"],
        "category": ["Tooling", "API"],
        "half_life_days": 180,
        "source_smk": "SMK_049"
    },
    {
        "lp_id": "LP-2025-10-29-049E",
        "title": "Session Continuity Protocol",
        "content": "When continuing from previous session with summary: (1) Verify infrastructure state (servers running, ports available), (2) Run validation tests (health endpoints, auth), (3) Document findings before proceeding. Don't assume previous state is still valid after restart. Multiple issues (port conflicts, emoji crashes) only appeared after PC restart in this session.",
        "agent": "Code",
        "tags": ["session-continuity", "validation", "infrastructure"],
        "category": ["Systems", "Reliability"],
        "half_life_days": 365,
        "source_smk": "SMK_049"
    },
    {
        "lp_id": "LP-2025-10-29-049F",
        "title": "GENOMOS as Living Audit Trail",
        "content": "Blockchain growth (16→19 blocks) during testing session provides retrospective validation. Consultation + mutation genes create permanent record of infrastructure validation. GENOMOS serves as living audit trail where each validation test leaves permanent DNA trace. This architectural pattern enables temporal queries like 'show me all validation events from Oct 29'.",
        "agent": "Code",
        "tags": ["genomos", "blockchain", "audit-trail", "validation"],
        "category": ["Architecture", "Validation"],
        "half_life_days": 1095,
        "source_smk": "SMK_049"
    },
    {
        "lp_id": "LP-2025-10-29-049G",
        "title": "Notion Schema Migration Strategy",
        "content": "When adding 9+ properties to Notion database: (1) Dry-run first (verify database access), (2) Add non-formula properties via API (text, number, select, checkbox, date), (3) Add formulas manually via UI (complex syntax). Reduces API error complexity and allows for iterative debugging. Successfully migrated 8/9 properties programmatically, 1/9 manually.",
        "agent": "Code",
        "tags": ["notion", "migration", "schema", "api-strategy"],
        "category": ["Database", "Migration"],
        "half_life_days": 180,
        "source_smk": "SMK_049"
    }
]


def create_lp_entry(lp: dict):
    """Create a new LP entry in Notion SLL database"""

    url = "https://api.notion.com/v1/pages"

    # Build Content block with title + content
    content_parts = [
        f"**{lp['title']}**",
        "",
        lp['content'],
        "",
        f"**Source:** SMK #{lp['source_smk']}",
        f"**Half-life:** {lp['half_life_days']} days",
        f"**Created:** {datetime.now().strftime('%Y-%m-%d')}"
    ]
    full_content = "\n".join(content_parts)

    # Build properties matching SLL schema
    properties = {
        "LP_ID": {
            "title": [{"text": {"content": lp['lp_id']}}]
        },
        "Content": {
            "rich_text": [{"text": {"content": full_content}}]
        },
        "Agent": {
            "select": {"name": lp['agent']}
        },
        "half_life_days": {
            "number": lp['half_life_days']
        },
        "temporal_weight_raw": {
            "number": 1.0  # Initial weight = 1.0 for new LPs
        },
        "reactivation_count": {
            "number": 0  # No reactivations yet
        },
        "freshness_status": {
            "select": {"name": "fresh"}  # New LPs are fresh
        },
        "shadow_flags": {
            "checkbox": False  # Not flagged initially
        },
        "provenance_block": {
            "rich_text": [{"text": {"content": f"Source: SMK #049 - Session: 2025-10-29 - Orion's Test Tasks + SMK V2.0 Week 1"}}]
        },
        "Date": {
            "date": {"start": datetime.now().strftime("%Y-%m-%d")}
        }
    }

    # Add tags (multi-select)
    if lp.get('tags'):
        properties["Tags"] = {
            "multi_select": [{"name": tag} for tag in lp['tags']]
        }

    # Add categories (multi-select)
    if lp.get('category'):
        properties["Category"] = {
            "multi_select": [{"name": cat} for cat in lp['category']]
        }

    payload = {
        "parent": {"database_id": SLL_DATABASE_ID},
        "properties": properties
    }

    try:
        response = requests.post(url, json=payload, headers=HEADERS)
        response.raise_for_status()

        print(f"[SUCCESS] Created: {lp['lp_id']}")
        return response.json()

    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] Failed to create {lp['lp_id']}: {e}")
        print(f"Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error for {lp['lp_id']}: {e}")
        return None


def main():
    print("="*80)
    print("Publishing LP #049A-G to Notion SLL Database")
    print(f"Database ID: {SLL_DATABASE_ID}")
    print(f"LP Count: {len(LEARNING_POINTS)}")
    print("="*80)

    success_count = 0
    failed_count = 0

    for lp in LEARNING_POINTS:
        print(f"\nPublishing {lp['lp_id']}: {lp['title']}...")
        result = create_lp_entry(lp)

        if result:
            success_count += 1
        else:
            failed_count += 1

    print("\n" + "="*80)
    print(f"SUMMARY: {success_count} successful, {failed_count} failed")
    print("="*80)

    if failed_count > 0:
        print("\n[WARNING] Some LPs failed to publish. Check errors above.")
        return 1
    else:
        print("\n[SUCCESS] All 7 LPs published to SLL database!")
        return 0


if __name__ == "__main__":
    exit(main())
