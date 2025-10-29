#!/usr/bin/env python3
"""
Simple Notion database analyzer using requests library.
"""

import os
import sys
import io
import json
import requests
from datetime import datetime
from collections import defaultdict

# Force UTF-8 encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# API Configuration
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
if not NOTION_API_KEY:
    print("ERROR: NOTION_API_KEY not found in environment")
    print("Set it with: export NOTION_API_KEY='your_key_here'")
    sys.exit(1)

NOTION_VERSION = "2022-06-28"

HEADERS = {
    'Authorization': f'Bearer {NOTION_API_KEY}',
    'Notion-Version': NOTION_VERSION,
    'Content-Type': 'application/json'
}

# Database IDs
DATABASES = {
    "SLL": {
        "id": "84da6cbd09d640fb868e41444b941991",
        "name": "SLL - Shared Learning Library",
        "purpose": "Centralized repository of all agent Learning Points"
    },
    "ARF": {
        "id": "da4a5c2e7028492f91bfec7c88b7efce",
        "name": "ARF - Agent Reflection Forum",
        "purpose": "Deep reflections and cross-agent dialogue"
    },
    "SMK": {
        "id": "ba1d4a4407a5425fafd81d27dc02cc1c",
        "name": "SMK - Strategic Macro-Coordination",
        "purpose": "High-level strategic decisions and coordination"
    },
    "LK": {
        "id": "784556781fc14a14afc733f4eb51e0bc",
        "name": "LK - Living Compendiums",
        "purpose": "Agent knowledge bases and documentation"
    },
    "EM": {
        "id": "2988fec9293180509658e93447b3b259",
        "name": "EM - Emergent Patterns",
        "purpose": "Cross-cutting patterns and insights"
    }
}

def search_all_databases():
    """Search for all databases in the workspace."""
    url = 'https://api.notion.com/v1/search'
    data = {
        'filter': {
            'value': 'database',
            'property': 'object'
        }
    }

    response = requests.post(url, headers=HEADERS, json=data)

    if response.status_code == 200:
        results = response.json().get('results', [])
        print(f"\n{'='*70}")
        print(f"ALL DATABASES IN WORKSPACE ({len(results)} total)")
        print(f"{'='*70}\n")

        databases = []
        for db in results:
            title_parts = db.get('title', [])
            title = title_parts[0].get('plain_text', 'Untitled') if title_parts else 'Untitled'
            db_id = db.get('id', '').replace('-', '')
            created = db.get('created_time', 'N/A')

            databases.append({
                'id': db_id,
                'title': title,
                'created': created,
                'url': db.get('url', '')
            })

            print(f"📊 {title}")
            print(f"   ID: {db_id}")
            print(f"   Created: {created}")
            print()

        return databases
    else:
        print(f"ERROR: {response.status_code} - {response.text}")
        return []

def query_database(db_id, db_name):
    """Query a database for its entries."""
    url = f'https://api.notion.com/v1/databases/{db_id}/query'
    data = {
        'page_size': 100
    }

    response = requests.post(url, headers=HEADERS, json=data)

    if response.status_code == 200:
        results = response.json().get('results', [])
        print(f"\n{'='*70}")
        print(f"{db_name}: {len(results)} entries")
        print(f"{'='*70}")

        # Analyze property types from entries
        property_types = defaultdict(set)
        sample_values = defaultdict(list)

        for entry in results:
            props = entry.get('properties', {})
            for prop_name, prop_data in props.items():
                prop_type = prop_data.get('type')
                property_types[prop_name].add(prop_type)

                # Extract sample value
                value = extract_property_value(prop_data)
                if value and len(sample_values[prop_name]) < 3:
                    sample_values[prop_name].append(value)

        # Print schema
        print(f"\nPROPERTIES ({len(property_types)}):")
        for prop_name, types in sorted(property_types.items()):
            type_str = ', '.join(types)
            print(f"  • {prop_name}: {type_str}")

            # Show sample values
            if sample_values[prop_name]:
                for val in sample_values[prop_name][:2]:
                    val_str = str(val)
                    if len(val_str) > 50:
                        val_str = val_str[:50] + "..."
                    print(f"      ↳ {val_str}")

        return {
            'id': db_id,
            'name': db_name,
            'total_entries': len(results),
            'properties': dict(property_types),
            'sample_values': dict(sample_values)
        }

    else:
        print(f"\nERROR querying {db_name}: {response.status_code}")
        print(f"Response: {response.text[:200]}")
        return None

def extract_property_value(prop_data):
    """Extract value from property based on its type."""
    prop_type = prop_data.get('type')

    if prop_type == 'title':
        texts = prop_data.get('title', [])
        return ''.join([t.get('plain_text', '') for t in texts])
    elif prop_type == 'rich_text':
        texts = prop_data.get('rich_text', [])
        return ''.join([t.get('plain_text', '') for t in texts])
    elif prop_type == 'select':
        select = prop_data.get('select')
        return select.get('name', None) if select else None
    elif prop_type == 'multi_select':
        options = prop_data.get('multi_select', [])
        return [opt.get('name') for opt in options]
    elif prop_type == 'date':
        date = prop_data.get('date')
        return date.get('start', None) if date else None
    elif prop_type == 'relation':
        relations = prop_data.get('relation', [])
        return f"{len(relations)} relation(s)"
    elif prop_type == 'url':
        return prop_data.get('url', None)
    elif prop_type == 'number':
        return prop_data.get('number', None)
    elif prop_type == 'checkbox':
        return prop_data.get('checkbox', None)
    elif prop_type == 'people':
        people = prop_data.get('people', [])
        return f"{len(people)} person/people"
    elif prop_type == 'files':
        files = prop_data.get('files', [])
        return f"{len(files)} file(s)"
    elif prop_type == 'created_time':
        return prop_data.get('created_time', None)
    elif prop_type == 'last_edited_time':
        return prop_data.get('last_edited_time', None)
    else:
        return None

def analyze_relationships(databases_data):
    """Analyze relationships between databases."""
    print(f"\n{'='*70}")
    print("RELATIONSHIP ANALYSIS")
    print(f"{'='*70}\n")

    relationships = []

    # Check for relation properties
    for db_key, db_data in databases_data.items():
        if not db_data:
            continue

        properties = db_data.get('properties', {})
        for prop_name, types in properties.items():
            if 'relation' in types:
                print(f"✓ {db_key} has relation property: '{prop_name}'")
                relationships.append({
                    'from': db_key,
                    'property': prop_name,
                    'type': 'relation'
                })

    # Check for common properties
    print(f"\nCOMMON PROPERTIES ACROSS DATABASES:")
    all_props = defaultdict(list)

    for db_key, db_data in databases_data.items():
        if not db_data:
            continue
        properties = db_data.get('properties', {})
        for prop_name in properties.keys():
            all_props[prop_name].append(db_key)

    for prop_name, db_list in sorted(all_props.items()):
        if len(db_list) > 1:
            print(f"  • '{prop_name}': {', '.join(db_list)}")

    return relationships

def create_integration_plan():
    """Create comprehensive integration plan."""
    plan = f"""
# Notion Database Integration Plan

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview

This plan outlines how to integrate all 5 Notion databases (SLL, ARF, SMK, LK, EM)
into a unified knowledge system for the Homo Lumen Resonans project.

## Database Purposes

"""

    for key, info in DATABASES.items():
        plan += f"### {key} - {info['name']}\n\n"
        plan += f"**Purpose**: {info['purpose']}\n\n"
        plan += f"**ID**: `{info['id']}`\n\n"

    plan += """
## Integration Architecture

### Phase 1: Core Learning Loop (SLL ↔ ARF)

**Objective**: Establish bidirectional flow between Learning Points and Reflections

**Data Flows**:
- SLL → ARF: Learning points trigger reflections when threshold reached
- ARF → SLL: Reflections generate new learning points
- Cross-linking: Both databases reference each other

**Implementation**:
1. Add "Related Learning Points" relation property in ARF
2. Add "Related Reflections" relation property in SLL
3. Create GitHub Action to sync LP → ARF when LP count reaches threshold
4. Create webhook to notify when new reflection is created

### Phase 2: Strategic Coordination (SMK ↔ ARF + LK)

**Objective**: Connect strategic decisions to their source reflections and impact on knowledge

**Data Flows**:
- ARF → SMK: Reflections that require strategic decisions create SMK entries
- SMK → LK: Strategic decisions trigger LK updates
- SMK → ARF: Decisions link back to source reflections

**Implementation**:
1. Add "Source Reflection" relation property in SMK
2. Add "Affected Compendiums" relation property in SMK
3. Add "Strategic Decisions" relation property in LK
4. Create automation to link SMK ← → ARF ← → LK

### Phase 3: Living Knowledge (LK ↔ GitHub ↔ All)

**Objective**: Keep Living Compendiums synced with GitHub and linked to all other databases

**Data Flows**:
- GitHub → LK: Markdown files sync to Notion
- LK → GitHub: Notion updates push to GitHub
- SLL/ARF/SMK → LK: All learning feeds into compendiums
- LK → EM: Compendium updates trigger pattern detection

**Implementation**:
1. Enhance sync-lk-to-notion.yml workflow
2. Add bidirectional sync (Notion → GitHub)
3. Create "Source Learning Points" relation in LK
4. Create "Source Reflections" relation in LK

### Phase 4: Emergent Patterns (EM ← All databases)

**Objective**: Extract and track emergent patterns across all knowledge

**Data Flows**:
- LK → EM: Compendium analysis reveals patterns
- SLL → EM: Learning point clustering shows patterns
- ARF → EM: Reflection themes indicate patterns
- EM → All: Patterns inform future learning/decisions

**Implementation**:
1. Add "Source Compendium" relation property in EM
2. Add "Related Learning Points" relation property in EM
3. Add "Related Reflections" relation property in EM
4. Create pattern detection algorithm
5. Create GitHub Action to auto-generate EM entries

## Required Properties (To Add)

### SLL
- [ ] Related Reflections (relation to ARF)
- [ ] Related Patterns (relation to EM)
- [ ] Compendium Reference (relation to LK)

### ARF
- [ ] Related Learning Points (relation to SLL)
- [ ] Strategic Decisions (relation to SMK)
- [ ] Emergent Patterns (relation to EM)

### SMK
- [ ] Source Reflection (relation to ARF)
- [ ] Affected Compendiums (relation to LK)
- [ ] Learning Points (relation to SLL)

### LK
- [ ] Source Learning Points (relation to SLL)
- [ ] Source Reflections (relation to ARF)
- [ ] Strategic Decisions (relation to SMK)
- [ ] Patterns Identified (relation to EM)

### EM
- [ ] Source Compendium (relation to LK)
- [ ] Related Learning Points (relation to SLL)
- [ ] Related Reflections (relation to ARF)
- [ ] Strategic Impact (relation to SMK)

## API Endpoints Needed

```
GET  /api/databases/{db}/entries
POST /api/databases/{db}/entries
GET  /api/relationships/{from_db}/{to_db}
POST /api/sync/github-to-notion/{db}
POST /api/sync/notion-to-github/{db}
GET  /api/patterns/detect?source_lk={id}
POST /api/workflows/lp-to-reflection
POST /api/workflows/reflection-to-smk
POST /api/workflows/lk-to-pattern
```

## GitHub Actions Workflows

### 1. sync-lp-to-sll.yml (✓ Exists)
- Trigger: Commits with "LP #XXX"
- Action: Create SLL entry
- Status: Active

### 2. sync-lk-to-notion.yml (✓ Exists)
- Trigger: Changes to *_LK_*.md
- Action: Create/update LK entry
- Status: Active

### 3. sync-smk-to-notion.yml (✓ Exists)
- Trigger: Changes to SMK/**/*.md
- Action: Create/update SMK entry
- Status: Active

### 4. sync-em-to-notion.yml (⚠ Needs creation)
- Trigger: LK updates or manual trigger
- Action: Analyze and create EM entries
- Status: Pending

### 5. bidirectional-sync.yml (⚠ Needs creation)
- Trigger: Notion webhook or schedule
- Action: Pull Notion changes to GitHub
- Status: Pending

## Automation Workflows

### Workflow 1: Learning → Reflection
**Trigger**: SLL reaches X learning points for agent
**Action**: Create ARF reflection entry

### Workflow 2: Reflection → Decision
**Trigger**: ARF entry marked "action_required"
**Action**: Create SMK draft entry

### Workflow 3: Decision → Knowledge
**Trigger**: SMK entry status → "implemented"
**Action**: Update related LK entry

### Workflow 4: Knowledge → Pattern
**Trigger**: LK version update
**Action**: Run pattern detection, create EM entries

### Workflow 5: Pattern → Learning
**Trigger**: New EM pattern identified
**Action**: Create SLL learning point

## Implementation Timeline

### Week 1: Foundation
- [ ] Add all relation properties to databases
- [ ] Test manual linking between databases
- [ ] Document linking conventions

### Week 2: GitHub Sync
- [ ] Create bidirectional sync workflow
- [ ] Test LK ↔ GitHub sync
- [ ] Implement sync-em-to-notion.yml

### Week 3: Automation
- [ ] Build API endpoints
- [ ] Create workflow triggers
- [ ] Test LP → ARF automation

### Week 4: Pattern Detection
- [ ] Implement pattern detection algorithm
- [ ] Test LK → EM pipeline
- [ ] Create pattern notification system

### Week 5: Integration Testing
- [ ] End-to-end testing of all workflows
- [ ] Performance optimization
- [ ] Documentation updates

## Success Metrics

1. **Data Flow**: All 5 databases actively linked
2. **Automation**: 80%+ of connections automated
3. **Sync**: GitHub ↔ Notion bidirectional sync working
4. **Patterns**: EM database auto-populating from LK analysis
5. **Learning**: Closed loop from SLL → ARF → SMK → LK → EM → SLL

## Next Steps

1. **IMMEDIATE**: Review this plan with Osvald
2. **TODAY**: Add relation properties to all databases
3. **THIS WEEK**: Implement Phase 1 (SLL ↔ ARF)
4. **NEXT WEEK**: Build API endpoints
5. **MONTH 1**: Complete all 4 phases

---

*Generated by Claude Code for Homo Lumen Resonans*
"""

    return plan

def main():
    """Main execution."""
    print("="*70)
    print("HOMO LUMEN NOTION DATABASE INTEGRATION ANALYZER")
    print("="*70)

    # Search all databases
    all_databases = search_all_databases()

    # Query our 5 main databases
    databases_data = {}
    for key, info in DATABASES.items():
        db_data = query_database(info['id'], info['name'])
        databases_data[key] = db_data

    # Analyze relationships
    relationships = analyze_relationships(databases_data)

    # Create integration plan
    plan = create_integration_plan()

    # Save plan
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"NOTION_INTEGRATION_PLAN_{timestamp}.md"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(plan)

    print(f"\n{'='*70}")
    print(f"✓ INTEGRATION PLAN SAVED: {filename}")
    print(f"{'='*70}\n")

    # Print summary
    print("SUMMARY:")
    print(f"  • Total databases in workspace: {len(all_databases)}")
    print(f"  • Main databases analyzed: {len(databases_data)}")
    print(f"  • Total entries across main DBs: {sum(d.get('total_entries', 0) for d in databases_data.values() if d)}")
    print(f"  • Relationships found: {len(relationships)}")
    print()

if __name__ == "__main__":
    main()
