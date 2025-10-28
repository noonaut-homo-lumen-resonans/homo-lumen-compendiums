#!/usr/bin/env python3
"""
Parse LK (Levende Kompendium) files with YAML frontmatter and extract metadata for Notion sync.

Agent: Claude Code
Date: 26. oktober 2025
"""

import os
import re
import json
import yaml
from pathlib import Path
from datetime import date, datetime

def parse_yaml_frontmatter(content):
    """
    Extract YAML frontmatter from markdown content.

    Expected format:
    ---
    agent: Orion
    version: V3.7
    date: 2025-10-20
    status: ACTIVE
    tags: [meta-coordinator, learning]
    ---
    """
    # Check if content starts with YAML frontmatter
    if not content.strip().startswith('---'):
        return None

    # Extract YAML block
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None

    yaml_content = parts[1].strip()

    try:
        metadata = yaml.safe_load(yaml_content)
        return metadata
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return None

def extract_agent_from_filename(filename):
    """Extract agent name from LK filename."""
    # Pattern: <Agent>_LK_V<version>.md
    match = re.match(r'([A-Z][a-z]+)_LK_V([\d\.]+)', filename)
    if match:
        return match.group(1), match.group(2)
    return None, None

def extract_learning_points(content, agent, lk_filename, github_url):
    """
    Extract all LP (Learning Points) entries from LK content.

    Pattern:
    ### **LP #001 - Title**
    **Dato:** 3. oktober 2025
    **Kontekst:** Context text
    **Innsikt:** Insight text

    Returns: Array of LP entry dictionaries
    """
    learning_points = []

    # Pattern to match LP entries
    # Handles both ### **LP #XXX and ### LP #XXX formats
    pattern = r'###\s+\*?\*?LP\s+#(\d+)\s*[-–]\s*(.+?)\*?\*?\n\*\*Dato:\*\*\s*(.+?)\n\*\*Kontekst:\*\*\s*(.+?)\n\*\*Innsikt:\*\*\s*(.+?)(?=\n###|\n##|\Z)'

    matches = re.findall(pattern, content, re.DOTALL)

    for match in matches:
        lp_id, title, dato, kontekst, innsikt = match

        # Clean up text (remove extra whitespace, asterisks)
        title = title.strip().strip('*').strip()
        dato = dato.strip()
        kontekst = kontekst.strip()
        innsikt = innsikt.strip()

        learning_points.append({
            "id": f"LP #{lp_id.zfill(3)}",  # Pad to 3 digits: LP #001
            "category": "Learning Point",
            "title": title,
            "date": dato,
            "context": kontekst,
            "content": f"**Kontekst:** {kontekst}\n\n**Innsikt:** {innsikt}",
            "agent": agent,
            "source_lk": lk_filename,
            "github_url": github_url
        })

    return learning_points

def extract_case_studies(content, agent, lk_filename, github_url):
    """
    Extract all CS (Case Studies) entries from LK content.

    Pattern:
    ### **CS #001 - Title**
    **Dato:** 3. oktober 2025
    **Situasjon:** Situation text
    **Tilnærming:** Approach text
    **Resultat:** Result text

    Returns: Array of CS entry dictionaries
    """
    case_studies = []

    pattern = r'###\s+\*?\*?CS\s+#(\d+)\s*[-–]\s*(.+?)\*?\*?\n\*\*Dato:\*\*\s*(.+?)\n\*\*Situasjon:\*\*\s*(.+?)\n\*\*Tilnærming:\*\*\s*(.+?)\n\*\*Resultat:\*\*\s*(.+?)(?=\n###|\n##|\Z)'

    matches = re.findall(pattern, content, re.DOTALL)

    for match in matches:
        cs_id, title, dato, situasjon, tilnaerming, resultat = match

        title = title.strip().strip('*').strip()
        dato = dato.strip()
        situasjon = situasjon.strip()
        tilnaerming = tilnaerming.strip()
        resultat = resultat.strip()

        case_studies.append({
            "id": f"CS #{cs_id.zfill(3)}",
            "category": "Case Study",
            "title": title,
            "date": dato,
            "content": f"**Situasjon:** {situasjon}\n\n**Tilnærming:** {tilnaerming}\n\n**Resultat:** {resultat}",
            "agent": agent,
            "source_lk": lk_filename,
            "github_url": github_url
        })

    return case_studies

def extract_shadow_logs(content, agent, lk_filename, github_url):
    """
    Extract all SL (Shadow Logs) entries from LK content.

    Pattern:
    ### **SL #001 - Title**
    **Dato:** 3. oktober 2025
    **Manifestasjon:** Manifestation text
    **Integrasjon:** Integration text
    **Status:** Status text

    Returns: Array of SL entry dictionaries
    """
    shadow_logs = []

    pattern = r'###\s+\*?\*?SL\s+#(\d+)\s*[-–]\s*(.+?)\*?\*?\n\*\*Dato:\*\*\s*(.+?)\n\*\*Manifestasjon:\*\*\s*(.+?)\n\*\*Integrasjon:\*\*\s*(.+?)\n\*\*Status:\*\*\s*(.+?)(?=\n###|\n##|\Z)'

    matches = re.findall(pattern, content, re.DOTALL)

    for match in matches:
        sl_id, title, dato, manifestasjon, integrasjon, status = match

        title = title.strip().strip('*').strip()
        dato = dato.strip()
        manifestasjon = manifestasjon.strip()
        integrasjon = integrasjon.strip()
        status = status.strip()

        shadow_logs.append({
            "id": f"SL #{sl_id.zfill(3)}",
            "category": "Shadow Log",
            "title": title,
            "date": dato,
            "content": f"**Manifestasjon:** {manifestasjon}\n\n**Integrasjon:** {integrasjon}\n\n**Status:** {status}",
            "agent": agent,
            "source_lk": lk_filename,
            "github_url": github_url
        })

    return shadow_logs

def extract_critical_decisions(content, agent, lk_filename, github_url):
    """
    Extract all KD (Critical Decisions) entries from LK content.

    Pattern:
    ### **KD #001 - Title**
    **Dato:** 3. oktober 2025
    **Beslutning:** Decision text

    Returns: Array of KD entry dictionaries
    """
    critical_decisions = []

    pattern = r'###\s+\*?\*?KD\s+#(\d+)\s*[-–]\s*(.+?)\*?\*?\n\*\*Dato:\*\*\s*(.+?)\n\*\*Beslutning:\*\*\s*(.+?)(?=\n###|\n##|\Z)'

    matches = re.findall(pattern, content, re.DOTALL)

    for match in matches:
        kd_id, title, dato, beslutning = match

        title = title.strip().strip('*').strip()
        dato = dato.strip()
        beslutning = beslutning.strip()

        critical_decisions.append({
            "id": f"KD #{kd_id.zfill(3)}",
            "category": "Critical Decision",
            "title": title,
            "date": dato,
            "content": f"**Beslutning:** {beslutning}",
            "agent": agent,
            "source_lk": lk_filename,
            "github_url": github_url
        })

    return critical_decisions

def extract_emergent_patterns(content, agent, lk_filename, github_url):
    """
    Extract Emergent Patterns from LK content.

    Pattern:
    1. **Pattern Title** - Description
    2. **Another Pattern** - Description

    Returns: Array of EM entry dictionaries

    NOTE: These patterns can be synced to the Emergent Patterns Database in Notion
    Database ID: 2988fec9293180509658e93447b3b259
    See: .github/workflows/sync-em-to-notion.yml (if exists)
    """
    emergent_patterns = []

    # Find the "Emergente Mønstre" section
    section_pattern = r'##\s+\*?\*?SEKSJON 5: EMERGENTE MØNSTRE\*?\*?(.+?)(?=\n##|\Z)'
    section_match = re.search(section_pattern, content, re.DOTALL)

    if not section_match:
        return emergent_patterns

    section_content = section_match.group(1)

    # Extract numbered patterns
    pattern = r'(\d+)\.\s+\*\*(.+?)\*\*\s*[-–]\s*(.+?)(?=\n\d+\.|\n##|\Z)'
    matches = re.findall(pattern, section_content, re.DOTALL)

    for match in matches:
        em_number, title, description = match

        title = title.strip()
        description = description.strip()

        emergent_patterns.append({
            "id": f"EM #{em_number.zfill(3)}",
            "category": "Emergent Pattern",
            "title": title,
            "date": None,  # Emergent patterns don't have dates
            "content": description,
            "agent": agent,
            "source_lk": lk_filename,
            "github_url": github_url
        })

    return emergent_patterns

def parse_lk_file(filepath, extract_content=False):
    """
    Parse a single LK file and extract metadata.

    Args:
        filepath: Path to LK file
        extract_content: If True, also extract LP/CS/SL/KD/EM entries

    Returns:
        Dictionary with metadata and optionally content entries
    """
    try:
        print(f"Parsing: {filepath.name}")
    except UnicodeEncodeError:
        print(f"Parsing: [filename with special characters]")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    metadata = parse_yaml_frontmatter(content)

    # If no YAML frontmatter, try to extract from filename
    if not metadata:
        metadata = {}
        agent, version = extract_agent_from_filename(filepath.name)
        if agent:
            metadata['agent'] = agent
            metadata['version'] = version
            print(f"  [INFO] No YAML frontmatter, extracted from filename")
        else:
            print(f"  [WARN] No YAML frontmatter and couldn't parse filename")
            return None

    # Extract title from content if not in YAML
    if 'title' not in metadata or not metadata['title']:
        # Try to find first # heading
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            metadata['title'] = title_match.group(1).strip()
        else:
            # Default title from agent name and version
            agent = metadata.get('agent', 'Unknown')
            version = metadata.get('version', 'Unknown')
            metadata['title'] = f"{agent} Levende Kompendium {version}"

    # Convert date objects to strings for JSON serialization
    if 'date' in metadata and isinstance(metadata['date'], (date, datetime)):
        metadata['date'] = metadata['date'].isoformat()

    # Add file metadata
    metadata['filename'] = filepath.name
    metadata['filepath'] = str(filepath)

    # Generate GitHub URL
    repo = os.getenv('GITHUB_REPOSITORY', 'noonaut-homo-lumen-resonans/homo-lumen-compendiums')
    branch = 'main'
    # Convert to absolute path first, then get relative to cwd
    try:
        abs_path = filepath.resolve()
        cwd = Path.cwd().resolve()
        relative_path = abs_path.relative_to(cwd)
    except ValueError:
        # If relative_to fails, just use the filepath as-is
        relative_path = filepath
    github_url = f"https://github.com/{repo}/blob/{branch}/{relative_path}".replace('\\', '/')
    metadata['github_url'] = github_url

    # Extract structured content if requested
    if extract_content:
        agent = metadata.get('agent', 'Unknown')
        lk_filename = filepath.name

        learning_points = extract_learning_points(content, agent, lk_filename, github_url)
        case_studies = extract_case_studies(content, agent, lk_filename, github_url)
        shadow_logs = extract_shadow_logs(content, agent, lk_filename, github_url)
        critical_decisions = extract_critical_decisions(content, agent, lk_filename, github_url)
        emergent_patterns = extract_emergent_patterns(content, agent, lk_filename, github_url)

        metadata['learning_points'] = learning_points
        metadata['case_studies'] = case_studies
        metadata['shadow_logs'] = shadow_logs
        metadata['critical_decisions'] = critical_decisions
        metadata['emergent_patterns'] = emergent_patterns

        total_entries = len(learning_points) + len(case_studies) + len(shadow_logs) + len(critical_decisions) + len(emergent_patterns)

        try:
            print(f"  [OK] Parsed: {agent} LK {metadata.get('version', '?')}")
            if total_entries > 0:
                print(f"       Extracted {total_entries} entries: {len(learning_points)} LP, {len(case_studies)} CS, {len(shadow_logs)} SL, {len(critical_decisions)} KD, {len(emergent_patterns)} EM")
        except UnicodeEncodeError:
            print(f"  [OK] Parsed: {agent} LK {metadata.get('version', '?')} - {total_entries} entries")
    else:
        try:
            print(f"  [OK] Parsed: {metadata.get('agent', '?')} LK {metadata.get('version', '?')} - {metadata.get('title', 'Untitled')}")
        except UnicodeEncodeError:
            print(f"  [OK] Parsed: {metadata.get('agent', '?')} LK {metadata.get('version', '?')}")

    return metadata

def main():
    """Main parsing process."""
    print("=" * 60)
    print("LK File Parser for Notion Sync")
    print("Agent: Claude Code")
    print("=" * 60)

    # Find all LK files in root directory
    root_dir = Path('.')
    lk_files = list(root_dir.glob('*_LK_*.md'))

    # Also check agents/ subdirectory
    agents_dir = Path('agents')
    if agents_dir.exists():
        lk_files.extend(agents_dir.glob('**/*kompendium*.md'))
        lk_files.extend(agents_dir.glob('**/*_LK_*.md'))

    # Sort by name
    lk_files = sorted(lk_files)

    if not lk_files:
        print("No LK files found")
        print("::set-output name=has_lks::false")
        return

    print(f"\nFound {len(lk_files)} LK files")

    # Parse all files
    lk_data = []
    for filepath in lk_files:
        metadata = parse_lk_file(filepath)
        if metadata:
            lk_data.append(metadata)

    if not lk_data:
        print("\nNo valid LK files to sync")
        print("::set-output name=has_lks::false")
        return

    # Output for next step
    print(f"\n[OK] Parsed {len(lk_data)} LK files successfully")
    print("::set-output name=has_lks::true")
    print(f"::set-output name=lk_count::{len(lk_data)}")
    print(f"::set-output name=lk_data::{json.dumps(lk_data)}")

if __name__ == '__main__':
    main()
