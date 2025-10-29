#!/usr/bin/env python3
"""
Detect Voktere Citations in CS/EM Entries and Auto-Tag Them

This script scans CS (Case Studies) and EM (Emergent Patterns) entries in Notion
and automatically tags them with referenced Voktere (knowledge guardians).

Voktere = Wisdom teachers whose teachings inform the work (Bohm, Spira, Eisenstein, etc.)

Usage:
    python scripts/detect_citations.py

Environment Variables Required:
    NOTION_API_KEY: Notion integration API key
    CS_DATABASE_ID: Case Studies database ID (2988fec9293180bfa32ac404a311a07e)
    EM_DATABASE_ID: Emergent Patterns database ID (2988fec9293180509658e93447b3b259)

Author: Code (Claude Code Agent)
Date: 29. oktober 2025
"""

import os
import re
import sys
import io
from notion_client import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Force UTF-8 encoding for stdout (Windows compatibility)
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Configuration
NOTION_API_KEY = os.environ.get('NOTION_API_KEY')
if not NOTION_API_KEY:
    print("ERROR: NOTION_API_KEY not found in environment")
    print("Set it with: export NOTION_API_KEY=your_key_here")
    sys.exit(1)

CS_DATABASE_ID = os.environ.get('CS_DATABASE_ID', '2988fec9293180bfa32ac404a311a07e')
EM_DATABASE_ID = os.environ.get('EM_DATABASE_ID', '2988fec9293180509658e93447b3b259')

notion = Client(auth=NOTION_API_KEY)

# VOKTERE REGISTRY - 40 Knowledge Guardians
# Organized by domain for easier maintenance
VOKTERE = {
    # Filosofi & Etikk
    'Kant': ['Kant', 'Immanuel Kant', 'Categorical Imperative', 'autonomi som mål'],
    'Heidegger': ['Heidegger', 'Martin Heidegger', 'Dasein', 'Being-in-the-World', 'væren'],
    'Levinas': ['Levinas', 'Emmanuel Levinas', 'Face-to-Face', 'ansvar for den andre'],
    'Arendt': ['Arendt', 'Hannah Arendt', 'Banality of Evil', 'banal ondskap'],
    'Kierkegaard': ['Kierkegaard', 'Søren Kierkegaard', 'Subjective Truth', 'leap of faith'],
    'Lao Tzu': ['Lao Tzu', 'Laozi', 'Wu Wei', 'Tao', 'ikke-handling'],
    'Popper': ['Popper', 'Karl Popper', 'Falsifikasjon', 'falsification'],
    'Kuhn': ['Kuhn', 'Thomas Kuhn', 'Paradigm', 'paradigmeskift'],
    'Longino': ['Longino', 'Helen Longino', 'Social Epistemology'],
    'Haraway': ['Haraway', 'Donna Haraway', 'Situated Knowledge'],

    # Psykologi & Bevissthet
    'Jung': ['Jung', 'Carl Jung', 'Arketyp', 'archetype', 'Shadow', 'individuation', 'kollektivt ubevisst'],
    'Porges': ['Porges', 'Stephen Porges', 'Polyvagal', 'polyvagal theory', 'ventral vagal'],
    'Maté': ['Maté', 'Gabor Maté', 'Gabor Mate', 'trauma', 'compassion'],
    'Levine': ['Levine', 'Peter Levine', 'Somatic Experiencing'],
    'Hübl': ['Hübl', 'Thomas Hübl', 'Thomas Hubl', 'kollektivt trauma'],
    'Kahneman': ['Kahneman', 'Daniel Kahneman', 'Thinking Fast and Slow', 'System 1', 'System 2', 'kognitive bias'],
    'Csikszentmihalyi': ['Csikszentmihalyi', 'Mihaly Csikszentmihalyi', 'Flow'],
    'Rogers': ['Rogers', 'Carl Rogers', 'Unconditional Positive Regard'],
    'Frankl': ['Frankl', 'Viktor Frankl', "Man's Search for Meaning"],
    'Wilber': ['Wilber', 'Ken Wilber', 'Integral Theory', 'AQAL'],

    # Fysikk & Systems Thinking
    'Bohm': ['Bohm', 'David Bohm', 'Implicate Order', 'explicate order', 'implisitt orden', 'Holomovement', 'Dialogue'],
    'Capra': ['Capra', 'Fritjof Capra', 'Web of Life', 'Systems View'],
    'Prigogine': ['Prigogine', 'Ilya Prigogine', 'Dissipative Structures'],
    'Heisenberg': ['Heisenberg', 'Werner Heisenberg', 'Uncertainty Principle'],
    'Bohr': ['Bohr', 'Niels Bohr', 'Complementarity'],

    # Consciousness & Non-Duality
    'Spira': ['Spira', 'Rupert Spira', 'Non-dual Awareness', 'Direct Knowing', 'bevissthet'],
    'Tolle': ['Tolle', 'Eckhart Tolle', 'Power of Now', 'Presence'],
    'Rinpoche': ['Rinpoche', 'Lama Michel Rinpoche', 'Lama Michel', 'Buddhist wisdom'],

    # Social Systems & Economics
    'Eisenstein': ['Eisenstein', 'Charles Eisenstein', 'Sacred Economics', 'Interbeing', 'samhørighet'],
    'Meadows': ['Meadows', 'Donella Meadows', 'Leverage Points'],
    'Raworth': ['Raworth', 'Kate Raworth', 'Doughnut Economics'],

    # Technology & AI
    'Schneier': ['Schneier', 'Bruce Schneier', 'Security'],
    'Winner': ['Winner', 'Langdon Winner', 'Do Artifacts Have Politics'],
    'Harari': ['Harari', 'Yuval Noah Harari', 'Sapiens', 'Homo Deus'],

    # Neuroscience & Cognition
    'McGilchrist': ['McGilchrist', 'Iain McGilchrist', 'Master and His Emissary', 'Right Brain', 'Left Brain', 'hemispheric balance'],
    'Damasio': ['Damasio', 'Antonio Damasio', 'Somatic Markers'],
    'LeDoux': ['LeDoux', 'Joseph LeDoux', 'Emotional Brain'],

    # Anthropology & Culture
    'Bateson': ['Bateson', 'Gregory Bateson', 'Ecology of Mind'],
    'Geertz': ['Geertz', 'Clifford Geertz', 'Thick Description'],
    'Turner': ['Turner', 'Victor Turner', 'Liminal'],
}

def detect_voktere_in_text(text):
    """
    Detect which Voktere are referenced in text.

    Args:
        text: String to search for Vokter references

    Returns:
        List of detected Vokter names (canonical form)
    """
    if not text:
        return []

    detected = []
    text_lower = text.lower()

    for vokter_name, keywords in VOKTERE.items():
        for keyword in keywords:
            # Case-insensitive search with word boundaries
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            if re.search(pattern, text_lower):
                detected.append(vokter_name)
                break  # Found this Vokter, no need to check more keywords

    return list(set(detected))  # Remove duplicates

def get_text_content(rich_text_property):
    """Extract plain text from Notion rich_text property."""
    if not rich_text_property:
        return ""

    return " ".join([
        block.get('plain_text', '')
        for block in rich_text_property
    ])

def get_database_entries(database_id, database_name):
    """Fetch all entries from a database."""
    print(f"\n📚 Fetching entries from {database_name} database...")

    try:
        results = []
        has_more = True
        start_cursor = None

        while has_more:
            query_params = {'page_size': 100}
            if start_cursor:
                query_params['start_cursor'] = start_cursor

            response = notion.databases.query(database_id=database_id, **query_params)
            results.extend(response['results'])

            has_more = response.get('has_more', False)
            start_cursor = response.get('next_cursor')

        print(f"   Found {len(results)} entries")
        return results

    except Exception as e:
        print(f"   ❌ Error fetching entries: {e}")
        return []

def analyze_entry(entry, database_name):
    """
    Analyze an entry for Vokter citations.

    Returns:
        dict with:
            - page_id: str
            - title: str
            - detected_voktere: list
            - all_text: str (for debugging)
    """
    try:
        page_id = entry['id']
        props = entry.get('properties', {})

        # Extract title (different property names for CS vs EM)
        title = ""
        if database_name == "CS":
            # CS uses "Name" as title
            title_prop = props.get('Name', {})
            if title_prop.get('title'):
                title = get_text_content(title_prop['title'])
        elif database_name == "EM":
            # EM uses "Pattern ID" as title
            title_prop = props.get('Pattern ID', {})
            if title_prop.get('title'):
                title = get_text_content(title_prop['title'])

        # Extract all text content from the entry
        text_content = []

        for prop_name, prop_value in props.items():
            prop_type = prop_value.get('type')

            if prop_type == 'rich_text':
                if prop_value.get('rich_text'):
                    text_content.append(get_text_content(prop_value['rich_text']))
            elif prop_type == 'title':
                if prop_value.get('title'):
                    text_content.append(get_text_content(prop_value['title']))

        all_text = " ".join(text_content)

        # Detect Voktere
        detected = detect_voktere_in_text(all_text)

        return {
            'page_id': page_id,
            'title': title or page_id[:8],
            'detected_voktere': detected,
            'all_text': all_text[:200] + "..." if len(all_text) > 200 else all_text
        }

    except Exception as e:
        print(f"   ⚠️ Error analyzing entry: {e}")
        return None

def update_voktere_tags(page_id, voktere_list, entry_title):
    """
    Update Voktere tags for an entry.

    Note: This assumes a "Voktere" multi_select property exists in the database.
    If not, this will fail. Manual setup required in Notion UI first.
    """
    if not voktere_list:
        return False

    try:
        notion.pages.update(
            page_id=page_id,
            properties={
                'Voktere': {
                    'multi_select': [{'name': vokter} for vokter in voktere_list]
                }
            }
        )

        voktere_str = ", ".join(voktere_list)
        print(f"   ✅ Tagged '{entry_title}' with: {voktere_str}")
        return True

    except Exception as e:
        if "Voktere is not a property" in str(e):
            print(f"   ⚠️ 'Voktere' property not found in database. Please add it manually in Notion UI.")
            print(f"      Entry: '{entry_title}' - Detected: {', '.join(voktere_list)}")
            return False
        else:
            print(f"   ❌ Error updating tags for '{entry_title}': {e}")
            return False

def process_database(database_id, database_name, dry_run=False):
    """Process a database and tag entries with detected Voktere."""
    print(f"\n" + "="*70)
    print(f"PROCESSING {database_name} DATABASE")
    print("="*70)

    entries = get_database_entries(database_id, database_name)

    if not entries:
        print(f"   No entries found or error fetching")
        return 0, 0

    print(f"\n🔍 Analyzing entries for Vokter citations...")

    analyzed_entries = []
    for entry in entries:
        result = analyze_entry(entry, database_name)
        if result and result['detected_voktere']:
            analyzed_entries.append(result)

    print(f"\n📊 Found {len(analyzed_entries)} entries with Vokter citations")

    if not analyzed_entries:
        print("   No Vokter citations detected")
        return 0, 0

    # Show summary
    print(f"\n📋 Summary of detected citations:")
    for entry in analyzed_entries:
        voktere_str = ", ".join(entry['detected_voktere'])
        print(f"   • {entry['title']}: {voktere_str}")

    # Update tags (if not dry run)
    if dry_run:
        print(f"\n⚠️ DRY RUN MODE - Not updating tags")
        print(f"   Remove --dry-run flag to apply changes")
        return len(analyzed_entries), 0
    else:
        print(f"\n🏷️ Updating Notion tags...")
        success_count = 0

        for entry in analyzed_entries:
            if update_voktere_tags(entry['page_id'], entry['detected_voktere'], entry['title']):
                success_count += 1

        return len(analyzed_entries), success_count

def main():
    """Main execution function."""
    print("\n" + "="*70)
    print("VOKTERE AUTO-TAGGING SYSTEM")
    print("="*70)
    print(f"📚 Voktere Registry: {len(VOKTERE)} knowledge guardians tracked")

    # Check for dry-run flag
    dry_run = '--dry-run' in sys.argv

    if dry_run:
        print("⚠️ Running in DRY RUN mode (no changes will be made)")

    # Process CS database
    cs_detected, cs_updated = process_database(CS_DATABASE_ID, "CS", dry_run)

    # Process EM database
    em_detected, em_updated = process_database(EM_DATABASE_ID, "EM", dry_run)

    # Final summary
    print("\n" + "="*70)
    print("FINAL SUMMARY")
    print("="*70)
    print(f"CS Database: {cs_detected} entries with citations, {cs_updated} tagged")
    print(f"EM Database: {em_detected} entries with citations, {em_updated} tagged")
    print(f"Total: {cs_detected + em_detected} entries detected, {cs_updated + em_updated} successfully tagged")

    if dry_run:
        print(f"\n💡 This was a dry run. Run without --dry-run to apply changes.")
    else:
        print(f"\n✅ Voktere auto-tagging complete!")

    print("="*70 + "\n")

if __name__ == '__main__':
    main()
