#!/usr/bin/env python3
"""
SMK YAML Frontmatter Conversion Script

Purpose: Convert all SMK files to standardized YAML frontmatter format
Agent: Manus
Date: 26. oktober 2025

Handles 3 naming formats:
1. SMK#019-CONSTITUTIONV1.md (old format)
2. SMK_027_SUPERPOSISJON_ARKITEKTUR.md (numbered format)
3. SMK_2025_10_20_QDA_DEPLOYMENT_VALIDATION.md (date-based format)
"""

import os
import re
from pathlib import Path
from datetime import datetime

# SMK directory
SMK_DIR = Path(__file__).parent.parent / "SMK"

def extract_smk_number(filename):
    """Extract SMK number from filename."""
    # Pattern 1: SMK#019 or SMK#028
    match = re.search(r'SMK#(\d+)', filename)
    if match:
        return int(match.group(1))
    
    # Pattern 2: SMK_027 or SMK_030
    match = re.search(r'SMK_(\d+)_', filename)
    if match:
        return int(match.group(1))
    
    # Pattern 3: SMK_2025_10_20 (date-based) - needs manual mapping
    date_to_number = {
        '2025_10_20': 33,  # QDA Deployment Validation
        '2025_10_21': 29,  # Vercel Deployment Success
        '2025_10_22': 35,  # HOMO/AI LUMEN RESONANS MANIFESTATION
    }
    for date_pattern, number in date_to_number.items():
        if date_pattern in filename:
            return number
    
    return None

def extract_metadata(content, filename):
    """Extract metadata from SMK content."""
    metadata = {
        'smk_number': extract_smk_number(filename),
        'title': '',
        'date': '',
        'agent': '',
        'tags': [],
        'status': 'COMPLETE'
    }
    
    # Extract title (first # heading)
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        metadata['title'] = title_match.group(1).strip()
    
    # Extract date
    date_patterns = [
        r'\*\*Dato:\*\*\s*(\d+)\.\s*(\w+)\s*(\d+)',  # **Dato:** 12. oktober 2025
        r'date:\s*(\d{4}-\d{2}-\d{2})',  # date: 2025-10-20
        r'SMK_(\d{4})_(\d{2})_(\d{2})',  # SMK_2025_10_20
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, content)
        if match:
            if len(match.groups()) == 3:
                if match.group(1).isdigit() and len(match.group(1)) == 4:
                    # Format: YYYY-MM-DD
                    metadata['date'] = f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
                else:
                    # Format: DD. måned YYYY
                    day = match.group(1)
                    month_map = {
                        'januar': '01', 'februar': '02', 'mars': '03', 'april': '04',
                        'mai': '05', 'juni': '06', 'juli': '07', 'august': '08',
                        'september': '09', 'oktober': '10', 'november': '11', 'desember': '12'
                    }
                    month = month_map.get(match.group(2).lower(), '01')
                    year = match.group(3)
                    metadata['date'] = f"{year}-{month}-{day.zfill(2)}"
            else:
                metadata['date'] = match.group(1)
            break
    
    # Extract agent
    agent_patterns = [
        r'\*\*Agent:\*\*\s*[🔨🌟🎨🧠🔬📊🌅💻🦅⚡]*\s*(\w+)',  # **Agent:** 🔨 Manus
        r'agent:\s*(\w+)',  # agent: Manus
    ]
    
    for pattern in agent_patterns:
        match = re.search(pattern, content)
        if match:
            metadata['agent'] = match.group(1)
            break
    
    # Extract tags
    tags_match = re.search(r'tags:\s*\[([^\]]+)\]', content)
    if tags_match:
        metadata['tags'] = [tag.strip() for tag in tags_match.group(1).split(',')]
    else:
        # Infer tags from content
        tag_keywords = {
            'constitution': ['constitution', 'constitutional'],
            'mcp': ['mcp', 'multi-agent'],
            'nav-losen': ['nav-losen', 'nav losen'],
            'ubuntu-playground': ['ubuntu playground', 'ubuntu-playground'],
            'deployment': ['deployment', 'deploy'],
            'vercel': ['vercel'],
            'netlify': ['netlify'],
        }
        
        content_lower = content.lower()
        for tag, keywords in tag_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                metadata['tags'].append(tag)
    
    return metadata

def has_yaml_frontmatter(content):
    """Check if content already has YAML frontmatter."""
    return content.strip().startswith('---\n')

def create_yaml_frontmatter(metadata):
    """Create YAML frontmatter from metadata."""
    yaml = "---\n"
    
    if metadata['smk_number']:
        yaml += f"smk_number: {metadata['smk_number']}\n"
    
    if metadata['title']:
        yaml += f"title: \"{metadata['title']}\"\n"
    
    if metadata['date']:
        yaml += f"date: {metadata['date']}\n"
    
    if metadata['agent']:
        yaml += f"agent: {metadata['agent']}\n"
    
    yaml += "type: Strategic Macro-Coordination\n"
    
    if metadata['tags']:
        yaml += f"tags: [{', '.join(metadata['tags'])}]\n"
    
    yaml += f"status: {metadata['status']}\n"
    yaml += "---\n\n"
    
    return yaml

def convert_smk_file(filepath):
    """Convert a single SMK file to YAML frontmatter format."""
    print(f"\nProcessing: {filepath.name}")
    
    # Read content
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has YAML
    if has_yaml_frontmatter(content):
        print(f"  [OK] Already has YAML frontmatter - skipping")
        return False

    # Extract metadata
    metadata = extract_metadata(content, filepath.name)
    print(f"  [INFO] Extracted metadata:")
    print(f"     SMK #: {metadata['smk_number']}")
    print(f"     Agent: {metadata['agent']}")
    print(f"     Date: {metadata['date']}")
    print(f"     Tags: {metadata['tags']}")

    # Create YAML frontmatter
    yaml = create_yaml_frontmatter(metadata)

    # Combine YAML + original content
    new_content = yaml + content

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  [OK] Converted successfully!")
    return True

def main():
    """Main conversion process."""
    print("=" * 60)
    print("SMK YAML Frontmatter Conversion Script")
    print("Agent: Manus")
    print("Date: 26. oktober 2025")
    print("=" * 60)
    
    # Find all SMK files
    smk_files = sorted(SMK_DIR.glob("SMK*.md"))
    
    print(f"\nFound {len(smk_files)} SMK files")
    
    # Convert each file
    converted = 0
    skipped = 0
    
    for filepath in smk_files:
        if convert_smk_file(filepath):
            converted += 1
        else:
            skipped += 1
    
    # Summary
    print("\n" + "=" * 60)
    print("CONVERSION COMPLETE")
    print("=" * 60)
    print(f"[OK] Converted: {converted}")
    print(f"[SKIP] Skipped: {skipped}")
    print(f"[TOTAL] Files: {len(smk_files)}")
    print("\nAll SMK files now have standardized YAML frontmatter!")

if __name__ == "__main__":
    main()

