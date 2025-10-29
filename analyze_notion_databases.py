#!/usr/bin/env python3
"""
Analyze all Notion databases and create an integration plan.
"""

import os
import sys
import io
import json
from datetime import datetime

# Force UTF-8 encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    from notion_client import Client
except ImportError:
    print("ERROR: notion-client not installed")
    print("Run: pip install notion-client")
    sys.exit(1)

# Database IDs
DATABASES = {
    "SLL": "84da6cbd09d640fb868e41444b941991",  # Learning Points
    "ARF": "da4a5c2e7028492f91bfec7c88b7efce",  # Agent Reflections
    "SMK": "ba1d4a4407a5425fafd81d27dc02cc1c",  # Strategic Macro-Coordination
    "LK": "784556781fc14a14afc733f4eb51e0bc",   # Living Compendiums
    "EM": "2988fec9293180509658e93447b3b259",   # Emergent Patterns
}

def get_notion_client():
    """Get Notion client with API key."""
    api_key = os.getenv("NOTION_API_KEY")
    if not api_key:
        print("ERROR: NOTION_API_KEY not found in environment")
        print("Set it with: export NOTION_API_KEY='your_key_here'")
        sys.exit(1)
    return Client(auth=api_key)

def analyze_database(notion, db_id, db_name):
    """Analyze a single database and return its schema and sample data."""
    print(f"\n{'='*70}")
    print(f"Analyzing {db_name}")
    print(f"{'='*70}")

    try:
        # Get database schema
        db = notion.databases.retrieve(database_id=db_id)

        print(f"\nDatabase Title: {db.get('title', [{}])[0].get('plain_text', 'N/A')}")
        print(f"Created: {db.get('created_time', 'N/A')}")
        print(f"Last Edited: {db.get('last_edited_time', 'N/A')}")

        # Analyze properties
        properties = db.get('properties', {})
        print(f"\nProperties ({len(properties)}):")

        schema = {}
        for prop_name, prop_data in properties.items():
            prop_type = prop_data.get('type', 'unknown')
            print(f"  - {prop_name}: {prop_type}")

            # Store detailed schema
            schema[prop_name] = {
                'type': prop_type,
                'id': prop_data.get('id', ''),
            }

            # Add type-specific details
            if prop_type == 'relation':
                schema[prop_name]['relation'] = {
                    'database_id': prop_data.get('relation', {}).get('database_id', ''),
                    'type': prop_data.get('relation', {}).get('type', ''),
                }
            elif prop_type == 'select':
                options = prop_data.get('select', {}).get('options', [])
                schema[prop_name]['options'] = [opt.get('name') for opt in options]
            elif prop_type == 'multi_select':
                options = prop_data.get('multi_select', {}).get('options', [])
                schema[prop_name]['options'] = [opt.get('name') for opt in options]

        # Get sample data (first 5 entries)
        print(f"\nQuerying entries...")
        results = notion.databases.query(
            database_id=db_id,
            page_size=5
        )

        entries = results.get('results', [])
        print(f"Total entries found: {len(entries)}")

        # Analyze sample entries
        sample_data = []
        for entry in entries[:3]:  # Show first 3 as examples
            entry_data = {
                'id': entry.get('id', ''),
                'created': entry.get('created_time', ''),
                'properties': {}
            }

            for prop_name, prop_value in entry.get('properties', {}).items():
                prop_type = prop_value.get('type')

                # Extract value based on type
                if prop_type == 'title':
                    texts = prop_value.get('title', [])
                    entry_data['properties'][prop_name] = ''.join([t.get('plain_text', '') for t in texts])
                elif prop_type == 'rich_text':
                    texts = prop_value.get('rich_text', [])
                    entry_data['properties'][prop_name] = ''.join([t.get('plain_text', '') for t in texts])
                elif prop_type == 'select':
                    select = prop_value.get('select', {})
                    entry_data['properties'][prop_name] = select.get('name', None)
                elif prop_type == 'multi_select':
                    options = prop_value.get('multi_select', [])
                    entry_data['properties'][prop_name] = [opt.get('name') for opt in options]
                elif prop_type == 'date':
                    date = prop_value.get('date', {})
                    entry_data['properties'][prop_name] = date.get('start', None)
                elif prop_type == 'relation':
                    relations = prop_value.get('relation', [])
                    entry_data['properties'][prop_name] = [rel.get('id') for rel in relations]
                elif prop_type == 'url':
                    entry_data['properties'][prop_name] = prop_value.get('url', None)
                elif prop_type == 'number':
                    entry_data['properties'][prop_name] = prop_value.get('number', None)

            sample_data.append(entry_data)

        # Print sample
        if sample_data:
            print(f"\nSample Entry:")
            sample = sample_data[0]
            for prop_name, prop_value in sample['properties'].items():
                if prop_value:
                    value_str = str(prop_value)
                    if len(value_str) > 60:
                        value_str = value_str[:60] + "..."
                    print(f"  {prop_name}: {value_str}")

        return {
            'name': db_name,
            'id': db_id,
            'title': db.get('title', [{}])[0].get('plain_text', 'N/A'),
            'created_time': db.get('created_time', 'N/A'),
            'last_edited_time': db.get('last_edited_time', 'N/A'),
            'schema': schema,
            'sample_data': sample_data,
            'total_entries': len(entries)
        }

    except Exception as e:
        print(f"ERROR analyzing {db_name}: {str(e)}")
        return None

def identify_relationships(databases_info):
    """Identify potential relationships between databases."""
    print(f"\n{'='*70}")
    print("RELATIONSHIP ANALYSIS")
    print(f"{'='*70}")

    relationships = []

    for db_name, db_info in databases_info.items():
        if not db_info:
            continue

        schema = db_info.get('schema', {})

        for prop_name, prop_data in schema.items():
            if prop_data.get('type') == 'relation':
                related_db_id = prop_data.get('relation', {}).get('database_id', '')

                # Find which database this relates to
                related_db_name = None
                for other_name, other_id in DATABASES.items():
                    if other_id == related_db_id:
                        related_db_name = other_name
                        break

                if related_db_name:
                    relationships.append({
                        'from': db_name,
                        'to': related_db_name,
                        'property': prop_name,
                        'type': 'relation'
                    })
                    print(f"  {db_name} -> {related_db_name} (via '{prop_name}')")

    # Look for implicit relationships (common properties)
    print(f"\nImplicit Relationships (common properties):")

    common_props = {}
    for db_name, db_info in databases_info.items():
        if not db_info:
            continue
        schema = db_info.get('schema', {})
        for prop_name in schema.keys():
            if prop_name not in common_props:
                common_props[prop_name] = []
            common_props[prop_name].append(db_name)

    # Show properties shared by multiple databases
    for prop_name, db_list in common_props.items():
        if len(db_list) > 1:
            print(f"  '{prop_name}' appears in: {', '.join(db_list)}")
            relationships.append({
                'property': prop_name,
                'databases': db_list,
                'type': 'common_property'
            })

    return relationships

def create_integration_plan(databases_info, relationships):
    """Create a comprehensive integration plan."""
    print(f"\n{'='*70}")
    print("INTEGRATION PLAN")
    print(f"{'='*70}")

    plan = {
        'overview': '',
        'phases': [],
        'data_flows': [],
        'api_endpoints': [],
        'automation_workflows': []
    }

    # Overview
    plan['overview'] = """
HOMO LUMEN COMPENDIUMS - NOTION DATABASE INTEGRATION PLAN

This plan connects all 5 Notion databases (SLL, ARF, SMK, LK, EM) into a
unified knowledge system that supports agent learning, reflection, and
emergent pattern recognition.
"""

    # Phase 1: Core Learning Loop (SLL + ARF)
    plan['phases'].append({
        'phase': 1,
        'name': 'Core Learning Loop',
        'databases': ['SLL', 'ARF'],
        'description': 'Establish bidirectional flow between Learning Points and Agent Reflections',
        'tasks': [
            'Create ARF entries from SLL learning points when threshold reached',
            'Link related SLL entries to ARF reflections',
            'Auto-tag ARF reflections based on SLL categories',
        ]
    })

    # Phase 2: Strategic Coordination (SMK)
    plan['phases'].append({
        'phase': 2,
        'name': 'Strategic Coordination',
        'databases': ['SMK', 'ARF', 'LK'],
        'description': 'Connect strategic decisions to reflections and compendiums',
        'tasks': [
            'Link SMK decisions to triggering ARF reflections',
            'Associate SMK entries with affected LK versions',
            'Track implementation status across databases',
        ]
    })

    # Phase 3: Living Knowledge (LK)
    plan['phases'].append({
        'phase': 3,
        'name': 'Living Knowledge Base',
        'databases': ['LK', 'SLL', 'ARF', 'SMK'],
        'description': 'Sync Living Compendiums with learning and decisions',
        'tasks': [
            'Auto-update LK when related SLL/ARF entries created',
            'Version tracking linked to SMK decisions',
            'GitHub sync for LK markdown files',
        ]
    })

    # Phase 4: Emergent Patterns (EM)
    plan['phases'].append({
        'phase': 4,
        'name': 'Emergent Pattern Recognition',
        'databases': ['EM', 'LK', 'SLL', 'ARF'],
        'description': 'Extract and track emergent patterns across all knowledge',
        'tasks': [
            'Analyze LK updates for emergent patterns',
            'Cross-reference patterns with SLL/ARF data',
            'Auto-generate EM entries from pattern detection',
        ]
    })

    # Data flows
    plan['data_flows'] = [
        'SLL -> ARF: Learning points trigger reflections',
        'ARF -> SMK: Reflections inform strategic decisions',
        'SMK -> LK: Decisions update compendiums',
        'LK -> EM: Compendiums reveal emergent patterns',
        'EM -> SLL: Patterns inform new learning points',
        'EM -> ARF: Patterns trigger deeper reflections'
    ]

    # API endpoints needed
    plan['api_endpoints'] = [
        'GET /databases/sll/entries?agent={agent}&category={category}',
        'POST /databases/arf/create-from-sll?lp_ids={ids}',
        'GET /databases/relationships?from={db}&to={db}',
        'POST /databases/em/detect-patterns?source={lk_id}',
        'GET /databases/timeline?start={date}&end={date}',
        'POST /databases/sync-github?database={db}',
    ]

    # Automation workflows
    plan['automation_workflows'] = [
        {
            'name': 'Learning Point -> Reflection',
            'trigger': 'New SLL entry with category="breakthrough"',
            'action': 'Create ARF reflection with linked SLL entries'
        },
        {
            'name': 'Reflection -> Strategic Decision',
            'trigger': 'ARF status changed to "action_required"',
            'action': 'Create SMK entry draft with linked ARF'
        },
        {
            'name': 'LK Update -> Pattern Detection',
            'trigger': 'LK version updated in GitHub',
            'action': 'Run pattern detection and create EM entries'
        },
        {
            'name': 'Pattern -> Notification',
            'trigger': 'New EM pattern identified',
            'action': 'Notify agents and create SLL learning point'
        }
    ]

    return plan

def save_plan_to_markdown(databases_info, relationships, plan):
    """Save the integration plan to a markdown file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"NOTION_INTEGRATION_PLAN_{timestamp}.md"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# Notion Database Integration Plan\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Database Overview
        f.write("## Database Overview\n\n")
        for db_name, db_info in databases_info.items():
            if not db_info:
                continue
            f.write(f"### {db_name} - {db_info['title']}\n\n")
            f.write(f"- **ID**: `{db_info['id']}`\n")
            f.write(f"- **Created**: {db_info['created_time']}\n")
            f.write(f"- **Last Edited**: {db_info['last_edited_time']}\n")
            f.write(f"- **Total Entries**: {db_info['total_entries']}\n\n")

            f.write("**Properties**:\n\n")
            for prop_name, prop_data in db_info['schema'].items():
                f.write(f"- `{prop_name}`: {prop_data['type']}\n")
            f.write("\n")

        # Relationships
        f.write("## Database Relationships\n\n")
        f.write("### Direct Relations\n\n")
        for rel in relationships:
            if rel.get('type') == 'relation':
                f.write(f"- **{rel['from']}** → **{rel['to']}** (via `{rel['property']}`)\n")

        f.write("\n### Common Properties\n\n")
        common_rels = {}
        for rel in relationships:
            if rel.get('type') == 'common_property':
                prop = rel['property']
                dbs = rel['databases']
                common_rels[prop] = dbs

        for prop, dbs in common_rels.items():
            f.write(f"- **`{prop}`**: {', '.join(dbs)}\n")

        # Integration Plan
        f.write("\n## Integration Plan\n\n")
        f.write(plan['overview'])

        f.write("\n### Implementation Phases\n\n")
        for phase in plan['phases']:
            f.write(f"#### Phase {phase['phase']}: {phase['name']}\n\n")
            f.write(f"**Databases**: {', '.join(phase['databases'])}\n\n")
            f.write(f"{phase['description']}\n\n")
            f.write("**Tasks**:\n\n")
            for task in phase['tasks']:
                f.write(f"- [ ] {task}\n")
            f.write("\n")

        f.write("### Data Flows\n\n")
        for flow in plan['data_flows']:
            f.write(f"- {flow}\n")

        f.write("\n### Required API Endpoints\n\n")
        for endpoint in plan['api_endpoints']:
            f.write(f"- `{endpoint}`\n")

        f.write("\n### Automation Workflows\n\n")
        for workflow in plan['automation_workflows']:
            f.write(f"#### {workflow['name']}\n\n")
            f.write(f"- **Trigger**: {workflow['trigger']}\n")
            f.write(f"- **Action**: {workflow['action']}\n\n")

        f.write("\n## Next Steps\n\n")
        f.write("1. [ ] Review and approve this integration plan\n")
        f.write("2. [ ] Set up GitHub secrets for all database IDs\n")
        f.write("3. [ ] Implement Phase 1: Core Learning Loop\n")
        f.write("4. [ ] Create API endpoints for database operations\n")
        f.write("5. [ ] Build automation workflows\n")
        f.write("6. [ ] Test integration with sample data\n")
        f.write("7. [ ] Deploy to production\n")

    return filename

def main():
    """Main execution function."""
    print("="*70)
    print("NOTION DATABASE INTEGRATION ANALYZER")
    print("="*70)

    # Get Notion client
    notion = get_notion_client()

    # Analyze all databases
    databases_info = {}
    for db_name, db_id in DATABASES.items():
        db_info = analyze_database(notion, db_id, db_name)
        databases_info[db_name] = db_info

    # Identify relationships
    relationships = identify_relationships(databases_info)

    # Create integration plan
    plan = create_integration_plan(databases_info, relationships)

    # Save to markdown
    filename = save_plan_to_markdown(databases_info, relationships, plan)

    print(f"\n{'='*70}")
    print(f"PLAN SAVED TO: {filename}")
    print(f"{'='*70}")

if __name__ == "__main__":
    main()
