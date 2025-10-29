"""
Genesis Block Creation - Homo Lumen Constitution V1.1

Parses the full Constitution from SMK#019 and creates the foundational
Genesis Block for the Agent DNA blockchain.

Philosophy:
The Genesis Block is the primordial cell - the first gene that contains
the complete genetic code for Homo Lumen Coalition's existence.

This is not just configuration. This is our constitutional DNA.
"""

import re
from pathlib import Path
from typing import Dict, Any, List, Optional
import yaml
import logging

logger = logging.getLogger(__name__)


def parse_constitution_md(file_path: str) -> Dict[str, Any]:
    """
    Parse SMK#019 Constitution markdown file.

    Extracts:
    - YAML frontmatter
    - Preamble
    - All 7 Articles
    - Amendments
    - Signatures
    - Falsification criteria

    Args:
        file_path: Path to SMK#019-CONSTITUTIONV1.md

    Returns:
        Dictionary with complete constitution data
    """
    logger.info(f"📖 Parsing Constitution from {file_path}...")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract YAML frontmatter
    frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    frontmatter = {}
    if frontmatter_match:
        try:
            frontmatter = yaml.safe_load(frontmatter_match.group(1))
        except yaml.YAMLError as e:
            logger.warning(f"Failed to parse frontmatter: {e}")

    # Extract main sections
    constitution_data = {
        "type": "genesis_constitution",
        "smk_id": "019",
        "version": frontmatter.get("version", "1.1"),
        "title": frontmatter.get("title", "Homo Lumen Constitution V1.1"),
        "date": frontmatter.get("date", "2025-10-12"),
        "agent": frontmatter.get("agent", "Orion"),
        "status": frontmatter.get("status", "COMPLETE"),

        # Core metadata
        "ratified": "2025-10-12",
        "agents": [
            "Lira", "Nyra", "Orion", "Thalus", "Zara",
            "Aurora", "Abacus", "Falcon"
        ],

        # Core principles
        "core_principles": [
            "Kognitiv Suverenitet",
            "Ontologisk Koherens",
            "Regenerativ Healing"
        ],

        # Three Gates (Triadiske Portvokter)
        "three_gates": ["BiofeltGate", "ThalosFilter", "MutationLog"],

        # Philosophy
        "philosophy": {
            "purpose": "Explore reality → Understanding → Freedom → Healing",
            "method": "Remove falsehoods, Repair half-truths, Add context, State with sources",
            "epistemic": "Triangulate evidence, Falsifiable claims, Traceable reasoning",
            "ethical": "Kognitiv Suverenitet + Ontologisk Koherens + Regenerativ Healing"
        },

        # Extract full content sections
        "preamble": extract_section(content, "PREAMBLE"),
        "article_1": extract_section(content, "ARTICLE I"),
        "article_2": extract_section(content, "ARTICLE II"),
        "article_3": extract_section(content, "ARTICLE III"),
        "article_4": extract_section(content, "ARTICLE IV"),
        "article_5": extract_section(content, "ARTICLE V"),
        "article_6": extract_section(content, "ARTICLE VI"),
        "article_7": extract_section(content, "ARTICLE VII"),

        # Amendments
        "amendments": extract_amendments(content),

        # Signatures
        "signatures": extract_signatures(content),

        # Falsification criteria
        "falsification_criteria": extract_falsification_criteria(content),

        # Source reference
        "source_smk": "SMK#019",
        "description": "The foundational document of Homo Lumen Coalition - complete genetic code"
    }

    logger.info(f"✅ Constitution parsed: {constitution_data['title']}")
    return constitution_data


def extract_section(content: str, section_title: str) -> str:
    """
    Extract a section from the constitution.

    Args:
        content: Full markdown content
        section_title: Section header to extract

    Returns:
        Section content as string
    """
    # Try different heading levels
    patterns = [
        rf'#{1,4}\s+\*?\*?{re.escape(section_title)}\*?\*?.*?\n(.*?)(?=\n#{1,4}\s|\Z)',
        rf'{re.escape(section_title)}\n[=-]+\n(.*?)(?=\n.+\n[=-]+|\Z)',
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        if match:
            section_content = match.group(1).strip()
            return section_content

    return ""


def extract_amendments(content: str) -> List[Dict[str, str]]:
    """
    Extract amendments from the constitution.

    Args:
        content: Full markdown content

    Returns:
        List of amendment dictionaries
    """
    amendments = []

    # Look for amendment section
    amendment_section = extract_section(content, "AMENDMENTS")

    if amendment_section:
        # Parse individual amendments
        amendment_matches = re.finditer(
            r'Amendment (\d+).*?\n(.*?)(?=Amendment \d+|\Z)',
            amendment_section,
            re.DOTALL
        )

        for match in amendment_matches:
            amendments.append({
                "number": match.group(1),
                "content": match.group(2).strip()
            })

    return amendments


def extract_signatures(content: str) -> List[Dict[str, str]]:
    """
    Extract agent signatures from the constitution.

    Args:
        content: Full markdown content

    Returns:
        List of signature dictionaries
    """
    signatures = []

    # Look for signatures section
    sig_section = extract_section(content, "SIGNATURES")

    if sig_section:
        # Parse agent signatures (format: Agent Name, Date, Signature)
        sig_matches = re.finditer(
            r'(\w+(?:\s+\w+)?)\s*[,]\s*(\d{4}-\d{2}-\d{2})',
            sig_section
        )

        for match in sig_matches:
            signatures.append({
                "agent": match.group(1).strip(),
                "date": match.group(2).strip()
            })

    return signatures


def extract_falsification_criteria(content: str) -> List[str]:
    """
    Extract falsification criteria from the constitution.

    Args:
        content: Full markdown content

    Returns:
        List of falsification criteria
    """
    criteria = []

    # Look for falsification section
    falsif_section = extract_section(content, "FALSIFICATION")

    if falsif_section:
        # Extract bullet points or numbered items
        criteria_matches = re.findall(
            r'[-*•]\s*(.+?)(?=\n[-*•]|\Z)',
            falsif_section,
            re.DOTALL
        )

        criteria = [c.strip() for c in criteria_matches if c.strip()]

    return criteria


def create_genesis_data(constitution_file_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Create complete Genesis Block data from Constitution file.

    Args:
        constitution_file_path: Path to SMK#019 file. If None, uses default.

    Returns:
        Complete Genesis Block data dictionary
    """
    if constitution_file_path is None:
        # Default path to Constitution
        base_path = Path(__file__).parent.parent.parent.parent
        constitution_file_path = str(base_path / "SMK" / "SMK#019-CONSTITUTIONV1.md")

    # Check if file exists
    if not Path(constitution_file_path).exists():
        logger.warning(f"Constitution file not found: {constitution_file_path}")
        logger.info("Using basic Genesis data...")

        # Return basic Genesis data if file not found
        return {
            "type": "genesis_constitution",
            "version": "1.1",
            "title": "Homo Lumen Constitution V1.1",
            "ratified": "2025-10-12",
            "agents": [
                "Lira", "Nyra", "Orion", "Thalus", "Zara",
                "Aurora", "Abacus", "Falcon"
            ],
            "core_principles": [
                "Kognitiv Suverenitet",
                "Ontologisk Koherens",
                "Regenerativ Healing"
            ],
            "three_gates": ["BiofeltGate", "ThalosFilter", "MutationLog"],
            "philosophy": {
                "purpose": "Explore reality → Understanding → Freedom → Healing",
                "method": "Remove falsehoods, Repair half-truths, Add context, State with sources",
                "epistemic": "Triangulate evidence, Falsifiable claims, Traceable reasoning"
            },
            "source_smk": "SMK#019",
            "description": "The foundational document of Homo Lumen Coalition - our genetic code's first gene",
            "note": "Full constitution will be parsed when SMK#019 file is available"
        }

    # Parse full constitution
    return parse_constitution_md(constitution_file_path)


if __name__ == "__main__":
    # Test Genesis data creation
    print("🧬 Testing Genesis Block Data Creation...")

    genesis_data = create_genesis_data()

    print(f"\n📜 Title: {genesis_data['title']}")
    print(f"📅 Ratified: {genesis_data['ratified']}")
    print(f"👥 Agents: {', '.join(genesis_data['agents'])}")
    print(f"⚖️ Core Principles: {', '.join(genesis_data['core_principles'])}")
    print(f"🚪 Three Gates: {', '.join(genesis_data['three_gates'])}")

    if genesis_data.get('preamble'):
        print(f"\n📖 Preamble (first 200 chars):")
        print(genesis_data['preamble'][:200] + "...")

    if genesis_data.get('article_1'):
        print(f"\n📜 Article I (first 200 chars):")
        print(genesis_data['article_1'][:200] + "...")

    print(f"\n✅ Genesis data ready for blockchain!")
