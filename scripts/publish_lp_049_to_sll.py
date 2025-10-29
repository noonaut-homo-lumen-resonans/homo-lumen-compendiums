#!/usr/bin/env python3
"""
Publish LP #047A-G (from SMK #049) to Notion SLL Database
Session: 2025-10-29 - Orion's Test Tasks + SMK V2.0 Week 1
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
        "domain": "Technical Debugging, Platform-Specific",
        "confidence": 0.95,
        "tags": ["windows", "python", "threading", "emoji", "encoding"],
        "description": "On Windows with cp1252 encoding, emoji characters in print() statements cause UnicodeEncodeError. When this happens in daemon background threads, the thread silently fails without logging to stderr - making it appear as if the thread never started.",
        "phase": "published",
        "source_smk": "SMK_049",
        "half_life_days": 180,  # Technical patterns decay slower
        "falsification": "Would be falsified by Windows configuration that handles UTF-8 in terminal without crashes"
    },
    {
        "lp_id": "LP-2025-10-29-049B",
        "title": "Test Infrastructure Before Testing Features",
        "domain": "Testing Strategy, Systems Thinking",
        "confidence": 0.90,
        "tags": ["testing", "infrastructure", "validation", "meta-testing"],
        "description": "When running validation tests on complex systems, test the testing infrastructure first. All 3 of Orion's tests initially failed not because features were broken, but because the testing infrastructure had bugs (emoji encoding, array unwrapping, missing integrations).",
        "phase": "published",
        "source_smk": "SMK_049",
        "half_life_days": 365,  # Testing strategy has long relevance
        "falsification": "Would be falsified by scenario where testing features first reveals infrastructure bugs faster"
    },
    {
        "lp_id": "LP-2025-10-29-049C",
        "title": "Triadiske Portvokter Validation Pattern",
        "domain": "Testing, Ethics, Validation Architecture",
        "confidence": 0.92,
        "tags": ["portvokter", "triadisk-etikk", "validation", "testing-pattern"],
        "description": "To comprehensively test the 3-layer Triadiske Portvokter system: (1) BiofeltGate with HRV<40 (should block), (2) ThalosFilter with SQL injection (should block), (3) MutationLog with normal write (should approve). Verify GENOMOS logging for all 3 outcomes.",
        "phase": "published",
        "source_smk": "SMK_049",
        "half_life_days": 730,  # Architectural patterns decay very slowly
        "falsification": "Would be falsified by finding edge cases that this pattern doesn't cover"
    },
    {
        "lp_id": "LP-2025-10-29-049D",
        "title": "SMK V2.0 Provenance Formula Syntax",
        "domain": "Tooling, Notion API, Schema Design",
        "confidence": 0.85,
        "tags": ["notion", "api", "formula", "schema-migration"],
        "description": "Notion API formula syntax is complex and error-prone. When adding 8+ properties to a database, use hybrid approach: API for simple properties (text, number, select), manual UI for formula properties. This saves debugging time and reduces API error complexity.",
        "phase": "published",
        "source_smk": "SMK_049",
        "half_life_days": 180,  # API patterns change with platform updates
        "falsification": "Would be falsified by finding reliable formula syntax for temporal_weight computation"
    },
    {
        "lp_id": "LP-2025-10-29-049E",
        "title": "Session Continuity Protocol",
        "domain": "Systems Reliability, Session Management",
        "confidence": 0.88,
        "tags": ["session-continuity", "validation", "infrastructure"],
        "description": "When continuing from previous session with summary: (1) Verify infrastructure state (servers running, ports available), (2) Run validation tests (health endpoints, auth), (3) Document findings before proceeding. Don't assume previous state is still valid after restart - multiple issues (port conflicts, emoji crashes) only appeared after PC restart.",
        "phase": "published",
        "source_smk": "SMK_049",
        "half_life_days": 365,  # Session management patterns are long-lived
        "falsification": "Would be falsified by infrastructure that guarantees state persistence across restarts"
    },
    {
        "lp_id": "LP-2025-10-29-049F",
        "title": "GENOMOS as Living Audit Trail",
        "domain": "Architecture, Epistemology, Validation",
        "confidence": 0.93,
        "tags": ["genomos", "blockchain", "audit-trail", "validation"],
        "description": "Blockchain growth (16→19 blocks) during testing session provides retrospective validation. Consultation + mutation genes create permanent record of infrastructure validation. GENOMOS serves as living audit trail where each validation test leaves permanent DNA trace.",
        "phase": "published",
        "source_smk": "SMK_049",
        "half_life_days": 1095,  # Architectural insights decay very slowly (3 years)
        "falsification": "Would be falsified by GENOMOS scalability issues at 1000+ blocks"
    },
    {
        "lp_id": "LP-2025-10-29-049G",
        "title": "Notion Schema Migration Strategy",
        "domain": "Database Migration, API Design",
        "confidence": 0.87,
        "tags": ["notion", "migration", "schema", "api-strategy"],
        "description": "When adding 9+ properties to Notion database: (1) Dry-run first (verify database access), (2) Add non-formula properties via API (text, number, select, checkbox, date), (3) Add formulas manually via UI (complex syntax). Reduces API error complexity and allows for iterative debugging.",
        "phase": "published",
        "source_smk": "SMK_049",
        "half_life_days": 180,  # Migration patterns may change with Notion updates
        "falsification": "Would be falsified by successful programmatic formula property creation"
    }
]


def create_lp_entry(lp: dict):
    """Create a new LP entry in Notion SLL database"""

    url = "https://api.notion.com/v1/pages"

    # Build properties
    properties = {
        "Name": {
            "title": [{"text": {"content": f"{lp['lp_id']}: {lp['title']}"}}]
        },
        "LP_ID": {
            "rich_text": [{"text": {"content": lp['lp_id']}}]
        },
        "Domain": {
            "rich_text": [{"text": {"content": lp['domain']}}]
        },
        "Confidence": {
            "number": lp['confidence']
        },
        "Description": {
            "rich_text": [{"text": {"content": lp['description']}}]
        },
        "Phase": {
            "select": {"name": lp['phase']}
        },
        "Source_SMK": {
            "rich_text": [{"text": {"content": lp['source_smk']}}]
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
        }
    }

    # Add tags if the database has a Tags property (multi-select)
    if lp.get('tags'):
        properties["Tags"] = {
            "multi_select": [{"name": tag} for tag in lp['tags']]
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
    print("Publishing LP #047A-G to Notion SLL Database")
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
        print("\n[SUCCESS] All LPs published to SLL database!")
        return 0


if __name__ == "__main__":
    exit(main())
