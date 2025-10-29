#!/usr/bin/env python3
"""
Extract Voktere from KAPITTEL_11

Parses KAPITTEL_11_VOKTERE_&_DIMENSJONER.md and creates individual
vokter files organized by category.

Input: kompendium_kapitler/KAPITTEL_11_VOKTERE_&_DIMENSJONER.md
Output: knowledge_base_structured/voktere/ (5 category folders with 40+ files)

Usage:
    python scripts/extract_voktere.py

Author: Code (Agent #9)
Date: 29. oktober 2025
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Category mapping (from KAPITTEL_11 structure)
CATEGORIES = {
    "01_filosofi_etikk": {
        "name": "Filosofi & Etikk",
        "range": (1, 10),
        "voktere": ["Kant", "Heidegger", "Levinas", "Arendt", "Kierkegaard", "Lao Tzu", "Popper", "Kuhn", "Longino", "Haraway"]
    },
    "02_psykologi": {
        "name": "Psykologi & Bevissthet",
        "range": (11, 20),
        "voktere": ["Jung", "Rogers", "Porges", "Brown", "Hillman", "Kahneman", "Estés"]
    },
    "03_fysikk_systemer": {
        "name": "Fysikk & Systemteori",
        "range": (21, 28),
        "voktere": ["Bohm", "Capra", "Faggin", "Sheldrake", "Spira", "Shannon", "Pearl", "Levin"]
    },
    "04_teknologi_sikkerhet": {
        "name": "Teknologi & Sikkerhet",
        "range": (29, 36),
        "voktere": ["Schneier", "Snowden", "Zimmermann", "Zuboff", "Doctorow", "Knuth", "Kay", "Victor"]
    },
    "05_kritisk_teori": {
        "name": "Kritisk Teori & Aktivisme",
        "range": (37, 40),
        "voktere": ["Taleb", "Latour", "McKenna", "Thich Nhat Hanh"]
    }
}


class VokterExtractor:
    """Extract voktere from KAPITTEL_11 and create individual files."""

    def __init__(self, input_file: str, output_dir: str):
        """
        Initialize extractor.

        Args:
            input_file: Path to KAPITTEL_11_VOKTERE_&_DIMENSJONER.md
            output_dir: Output directory for voktere files
        """
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.voktere_data = []

    def parse_kapittel_11(self) -> List[Dict[str, str]]:
        """
        Parse KAPITTEL_11 and extract voktere data.

        Returns:
            List of vokter dicts with: number, name, felt, konsept, relevans, etc.
        """
        logger.info(f"Parsing {self.input_file}...")

        with open(self.input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find all voktere sections (pattern: "NUMBER. NAME (years) - optional note")
        vokter_pattern = r'^(\d+)\.\s+([A-ZÆØÅ\s]+?)(?:\s*\([\d\s\-\.]+\))?\s*(?:-\s*(.+?))?$'

        voktere = []
        lines = content.split('\n')

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            match = re.match(vokter_pattern, line)

            if match:
                number = int(match.group(1))
                name = match.group(2).strip()
                note = match.group(3).strip() if match.group(3) else ""

                # Extract vokter content (until next vokter or section end)
                content_lines = []
                j = i + 1

                while j < len(lines):
                    next_line = lines[j].strip()

                    # Stop at next vokter
                    if re.match(vokter_pattern, next_line):
                        break

                    # Stop at next major section
                    if next_line.startswith('11.2') or next_line.startswith('11.3'):
                        break

                    content_lines.append(lines[j])
                    j += 1

                vokter_content = '\n'.join(content_lines)

                # Parse vokter sections
                vokter_data = self._parse_vokter_content(number, name, note, vokter_content)

                if vokter_data:
                    voktere.append(vokter_data)
                    logger.info(f"  ✅ Parsed: {number}. {name}")

                i = j
            else:
                i += 1

        logger.info(f"Found {len(voktere)} voktere")
        return voktere

    def _parse_vokter_content(
        self,
        number: int,
        name: str,
        note: str,
        content: str
    ) -> Dict[str, str]:
        """
        Parse individual vokter content sections.

        Args:
            number: Vokter number
            name: Vokter name
            note: Optional note (e.g., "Thalus' Primære Vokter")
            content: Full vokter text content

        Returns:
            Dict with parsed sections
        """
        data = {
            "number": number,
            "name": name.title(),
            "note": note,
            "felt": "",
            "noekkelkonsept": "",
            "relevans": "",
            "kjernelaere": "",
            "hvordan_vi_bruker": "",
            "praktisk_teknikk": "",
            "raw_content": content
        }

        # Extract "Felt:"
        felt_match = re.search(r'Felt:\s*(.+?)(?:\n|$)', content, re.IGNORECASE)
        if felt_match:
            data["felt"] = felt_match.group(1).strip()

        # Extract "Nøkkelkonsept:"
        konsept_match = re.search(r'Nøkkelkonsept:\s*(.+?)(?:\n|$)', content, re.IGNORECASE)
        if konsept_match:
            data["noekkelkonsept"] = konsept_match.group(1).strip()

        # Extract "Relevans for Homo Lumen:"
        relevans_match = re.search(r'Relevans for Homo Lumen:\s*(.+?)(?:\n|$)', content, re.IGNORECASE)
        if relevans_match:
            data["relevans"] = relevans_match.group(1).strip()

        # Extract "Kjernelære:" (quote)
        kjernelaere_match = re.search(r'Kjernelære:\s*"(.+?)"', content, re.DOTALL | re.IGNORECASE)
        if kjernelaere_match:
            data["kjernelaere"] = kjernelaere_match.group(1).strip()

        # Extract "Hvordan Vi Bruker [Name]:"
        hvordan_match = re.search(
            r'Hvordan Vi Bruker .+?:\s*\n(.+?)(?=\nPraktisk Teknikk|$)',
            content,
            re.DOTALL | re.IGNORECASE
        )
        if hvordan_match:
            data["hvordan_vi_bruker"] = hvordan_match.group(1).strip()

        # Extract "Praktisk Teknikk for Mennesker:"
        teknikk_match = re.search(
            r'Praktisk Teknikk for Mennesker:\s*(.+?)(?=\n\d+\.|$)',
            content,
            re.DOTALL | re.IGNORECASE
        )
        if teknikk_match:
            data["praktisk_teknikk"] = teknikk_match.group(1).strip()

        return data

    def determine_category(self, vokter_number: int, vokter_name: str) -> str:
        """
        Determine which category a vokter belongs to.

        Args:
            vokter_number: Vokter number (1-40)
            vokter_name: Vokter name

        Returns:
            Category folder name (e.g., "01_filosofi_etikk")
        """
        for category_id, category_data in CATEGORIES.items():
            min_num, max_num = category_data["range"]

            # Check by number range
            if min_num <= vokter_number <= max_num:
                return category_id

            # Check by name match (fallback)
            for vokter in category_data["voktere"]:
                if vokter.lower() in vokter_name.lower():
                    return category_id

        # Default to filosofi if not found
        logger.warning(f"Could not categorize {vokter_number}. {vokter_name}, defaulting to filosofi")
        return "01_filosofi_etikk"

    def create_vokter_file(self, vokter_data: Dict[str, str], category: str):
        """
        Create individual markdown file for vokter.

        Args:
            vokter_data: Vokter data dict
            category: Category folder name
        """
        # Create category folder
        category_path = self.output_dir / category
        category_path.mkdir(parents=True, exist_ok=True)

        # Generate filename: 01_Kant.md, 02_Heidegger.md, etc.
        filename = f"{vokter_data['number']:02d}_{vokter_data['name'].replace(' ', '_')}.md"
        file_path = category_path / filename

        # Build markdown content
        content = f"""# {vokter_data['name']}

**Nummer:** {vokter_data['number']}
**Kategori:** {CATEGORIES[category]['name']}
"""

        if vokter_data['note']:
            content += f"**Note:** {vokter_data['note']}\n"

        content += "\n---\n\n"

        if vokter_data['felt']:
            content += f"## Felt\n{vokter_data['felt']}\n\n"

        if vokter_data['noekkelkonsept']:
            content += f"## Nøkkelkonsept\n{vokter_data['noekkelkonsept']}\n\n"

        if vokter_data['relevans']:
            content += f"## Relevans for Homo Lumen\n{vokter_data['relevans']}\n\n"

        if vokter_data['kjernelaere']:
            content += f"## Kjernelære\n> \"{vokter_data['kjernelaere']}\"\n\n"

        if vokter_data['hvordan_vi_bruker']:
            content += f"## Hvordan Vi Bruker {vokter_data['name']}\n{vokter_data['hvordan_vi_bruker']}\n\n"

        if vokter_data['praktisk_teknikk']:
            content += f"## Praktisk Teknikk for Mennesker\n{vokter_data['praktisk_teknikk']}\n\n"

        content += f"""---

*Kilde: KAPITTEL_11_VOKTERE_&_DIMENSJONER.md*
*Ekstrahert: 29. oktober 2025*
*Agent: Code (Agent #9)*
"""

        # Write file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"  ✅ Created: {filename}")

    def create_category_readmes(self):
        """Create README.md in each category folder."""
        for category_id, category_data in CATEGORIES.items():
            category_path = self.output_dir / category_id
            category_path.mkdir(parents=True, exist_ok=True)

            readme_path = category_path / "README.md"

            content = f"""# {category_data['name']}

Denne mappen inneholder voktere fra kategorien **{category_data['name']}**.

## Voktere i denne kategorien

"""

            for vokter_name in category_data['voktere']:
                content += f"- {vokter_name}\n"

            content += f"""
---

*Automatisk generert av extract_voktere.py*
*Kilde: KAPITTEL_11_VOKTERE_&_DIMENSJONER.md*
"""

            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"  ✅ Created README: {category_id}/README.md")

    def create_master_index(self):
        """Create master README.md with index of all voktere."""
        readme_path = self.output_dir / "README.md"

        content = """# Voktere - Knowledge Guardians

40+ Filosofer, Psykologer, Fysikere, Teknologer som er våre kunnskapsmodeller.

## Hva Er en Vokter?

En vokter er ikke bare en referanse eller et sitat. En vokter er en **levende kilde til visdom** som vi kontinuerlig konsulterer.

## Kategorier

"""

        for category_id, category_data in CATEGORIES.items():
            content += f"### [{category_data['name']}]({category_id}/)\n\n"

            for vokter_name in category_data['voktere']:
                content += f"- {vokter_name}\n"

            content += "\n"

        content += """---

## Polycomputing i LAG 5

Samme ontologiske spørsmål kan belyses av flere voktere:

**Eksempel:** "Er push-notifikasjoner etisk forsvarlige?"

- **Kant (Thalus):** "Respekterer det brukerens autonomi som et mål i seg selv?"
- **Porges (Lira):** "Er det trygt for nervesystemet?"
- **Schneier (Zara):** "Er det sikkert mot misbruk?"
- **Kahneman (Abacus):** "Utnytter det kognitive bias?"

Emergent svar fra polycomputing: Multi-perspektiv validering.

---

*Ekstrahert fra: KAPITTEL_11_VOKTERE_&_DIMENSJONER.md*
*Dato: 29. oktober 2025*
*Agent: Code (Agent #9)*
"""

        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"✅ Created master index: README.md")

    def extract(self):
        """Main extraction process."""
        logger.info("=" * 70)
        logger.info("VOKTERE EXTRACTION")
        logger.info("=" * 70)
        logger.info(f"Input: {self.input_file}")
        logger.info(f"Output: {self.output_dir}")
        logger.info("")

        # Parse KAPITTEL_11
        voktere = self.parse_kapittel_11()

        logger.info("")
        logger.info("Creating vokter files...")

        # Create individual files
        for vokter_data in voktere:
            category = self.determine_category(vokter_data['number'], vokter_data['name'])
            self.create_vokter_file(vokter_data, category)

        logger.info("")
        logger.info("Creating category READMEs...")
        self.create_category_readmes()

        logger.info("")
        logger.info("Creating master index...")
        self.create_master_index()

        logger.info("")
        logger.info("=" * 70)
        logger.info("✅ EXTRACTION COMPLETE")
        logger.info("=" * 70)
        logger.info(f"Voktere extracted: {len(voktere)}")
        logger.info(f"Categories: {len(CATEGORIES)}")
        logger.info(f"Output: {self.output_dir}")
        logger.info("")


def main():
    """Main execution."""
    # Paths
    repo_root = Path(__file__).parent.parent
    input_file = repo_root / "kompendium_kapitler" / "KAPITTEL_11_VOKTERE_&_DIMENSJONER.md"
    output_dir = repo_root / "knowledge_base_structured" / "voktere"

    # Check input exists
    if not input_file.exists():
        logger.error(f"❌ Input file not found: {input_file}")
        return

    # Run extraction
    extractor = VokterExtractor(str(input_file), str(output_dir))
    extractor.extract()

    logger.info("Next steps:")
    logger.info("  1. Review extracted files in: knowledge_base_structured/voktere/")
    logger.info("  2. Run: python scripts/extract_dimensjoner.py")
    logger.info("  3. Run: python scripts/extract_pulser.py")
    logger.info("  4. Run: python scripts/sync_to_csn_drive.py")
    logger.info("")


if __name__ == "__main__":
    main()
