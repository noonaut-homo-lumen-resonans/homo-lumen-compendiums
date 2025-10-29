#!/usr/bin/env python3
"""
Extract Pulser from Session Notes

Parses session notes mapping file to create individual puls files
organized with their dimension resonance and practical applications.

Input: .claude/session-notes/2025-10-17-pulser-dimensjoner-voktere-mapping.md
Output: knowledge_base_structured/pulser/ (10 files P01-P10)

Usage:
    python scripts/extract_pulser.py

Author: Code (Agent #9)
Date: 29. oktober 2025
"""

import os
import re
from pathlib import Path
from typing import Dict, List
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 10 Pulser (P1-P10)
PULSER = {
    "P01": "Bioelektrisk Fundament",
    "P02": "Traumeheling",
    "P03": "Kvantumdyp",
    "P04": "Filosofisk Spiral",
    "P05": "Ikke-Dualistisk Stilhet",
    "P06": "Teknologisk Resonans",
    "P07": "Kosmisk Narrativ",
    "P08": "Selvorganiserende Systemer",
    "P09": "Nevrologisk Dybde",
    "P10": "Kosmisk Konvergens"
}


class PulserExtractor:
    """Extract pulser from session notes mapping."""

    def __init__(self, input_file: str, output_dir: str):
        """
        Initialize extractor.

        Args:
            input_file: Path to 2025-10-17-pulser-dimensjoner-voktere-mapping.md
            output_dir: Output directory for puls files
        """
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)

    def parse_pulser_mapping(self) -> Dict[str, Dict[str, str]]:
        """
        Parse session notes and extract puls data.

        Returns:
            Dict mapping puls ID (P01-P10) to puls data
        """
        logger.info(f"Parsing {self.input_file}...")

        with open(self.input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        pulser = {}

        # Find all puls sections (pattern: "### **Puls N: Name**")
        puls_pattern = r'###\s+\*\*Puls\s+(\d+):\s+(.+?)\*\*'

        lines = content.split('\n')
        i = 0

        while i < len(lines):
            line = lines[i]
            match = re.match(puls_pattern, line)

            if match:
                puls_num = int(match.group(1))
                puls_name = match.group(2).strip()
                puls_id = f"P{puls_num:02d}"  # P01, P02, etc.

                # Extract puls content (until next puls or section)
                content_lines = []
                j = i + 1

                while j < len(lines):
                    next_line = lines[j]

                    # Stop at next puls
                    if re.match(puls_pattern, next_line):
                        break

                    # Stop at next major section (## DEL 2, etc.)
                    if next_line.startswith('## DEL'):
                        break

                    content_lines.append(lines[j])
                    j += 1

                puls_content = '\n'.join(content_lines)

                # Parse puls sections
                puls_data = self._parse_puls_content(
                    puls_id,
                    puls_name,
                    puls_content
                )

                pulser[puls_id] = puls_data
                logger.info(f"  ✅ Parsed: {puls_id} - {puls_name}")

                i = j
            else:
                i += 1

        logger.info(f"Found {len(pulser)} pulser")
        return pulser

    def _parse_puls_content(
        self,
        puls_id: str,
        name: str,
        content: str
    ) -> Dict[str, str]:
        """
        Parse individual puls content sections.

        Args:
            puls_id: Puls ID (P01-P10)
            name: Puls name
            content: Full puls text content

        Returns:
            Dict with parsed sections
        """
        data = {
            "id": puls_id,
            "name": name,
            "resonerer_med": "",
            "nokkelbegreper": "",
            "implikasjoner": "",
            "raw_content": content
        }

        # Extract "Resonerer med:"
        resonans_match = re.search(
            r'- \*\*Resonerer med:\*\*\s+(.+?)(?:\n-|\n\n|$)',
            content,
            re.DOTALL
        )
        if resonans_match:
            data["resonerer_med"] = resonans_match.group(1).strip()

        # Extract "Nøkkelbegreper:"
        begreper_match = re.search(
            r'- \*\*Nøkkelbegreper:\*\*\s+(.+?)(?:\n-|\n\n|$)',
            content
        )
        if begreper_match:
            data["nokkelbegreper"] = begreper_match.group(1).strip()

        # Extract "Implikasjoner for NAV-Losen:"
        impl_match = re.search(
            r'- \*\*Implikasjoner for NAV-Losen:\*\*\s+(.+?)(?=\n---|$)',
            content,
            re.DOTALL
        )
        if impl_match:
            data["implikasjoner"] = impl_match.group(1).strip()

        return data

    def create_puls_file(self, puls_data: Dict[str, str]):
        """
        Create individual puls file.

        Args:
            puls_data: Puls data dict
        """
        puls_id = puls_data['id']
        filename = f"{puls_id}_{puls_data['name'].replace(' ', '_')}.md"
        output_path = self.output_dir / filename

        # Build markdown content
        content = f"""# {puls_id}: {puls_data['name']}

**ID:** {puls_id}
**Navn:** {puls_data['name']}

---

## Oversikt

{puls_data['name']} er et tematisk resonansfelt som forbinder praksis, dimensjoner, og voktere.

"""

        if puls_data['resonerer_med']:
            content += f"## Dimensjon-Resonans\n\n{puls_data['resonerer_med']}\n\n"

        if puls_data['nokkelbegreper']:
            content += f"## Nøkkelbegreper\n\n{puls_data['nokkelbegreper']}\n\n"

        if puls_data['implikasjoner']:
            content += f"## Implikasjoner for NAV-Losen\n\n{puls_data['implikasjoner']}\n\n"

        content += """---

## Praktisk Anvendelse

*Denne pulsen kan brukes til:*
- Å finne relevante voktere og dimensjoner for et spesifikt tema
- Å designe praksiser som resonerer med brukerens tilstand
- Å skape kohærens mellom teori (voktere) og praksis (øvelser)

---

## Kilder

- **2025-10-17-pulser-dimensjoner-voktere-mapping.md** (primærkilde)
- **KAPITTEL_11_VOKTERE_&_DIMENSJONER.md** (voktere og dimensjoner)

---

*Ekstrahert: 29. oktober 2025*
*Agent: Code (Agent #9)*
"""

        # Write file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"  ✅ Created: {filename}")

    def create_master_index(self):
        """Create master README.md with index of all pulser."""
        readme_path = self.output_dir / "README.md"

        content = """# Pulser - Tematiske Resonansfelter

10 Pulser (P01-P10) som forbinder praksis, dimensjoner, og voktere.

## Hva Er en Puls?

En puls er et **tematisk resonansfelt** - et ontologisk område hvor:
- Spesifikke dimensjoner aktiveres
- Relevante voktere konsulteres
- Praktiske teknikker anvendes

Pulser opererer som **mosaikk-strukturer** - de overlapper og samhandler på tvers av dimensjoner.

---

## De 10 Pulsene

### Fundamentale Pulser (P01-P02)
- **[P01: Bioelektrisk Fundament](P01_Bioelektrisk_Fundament.md)** - Nervesystem, bioelektrisitet, vitalitet
- **[P02: Traumeheling](P02_Traumeheling.md)** - Emosjonell integrasjon, tilknytning

### Ontologiske Pulser (P03-P05)
- **[P03: Kvantumdyp](P03_Kvantumdyp.md)** - Ikke-lokalitet, bevissthetens grunnlag
- **[P04: Filosofisk Spiral](P04_Filosofisk_Spiral.md)** - Menings- og visdomsmønstre
- **[P05: Ikke-Dualistisk Stilhet](P05_Ikke-Dualistisk_Stilhet.md)** - Enhet, medfølelse, stillhetspotensial

### Systemiske Pulser (P06-P08)
- **[P06: Teknologisk Resonans](P06_Teknologisk_Resonans.md)** - Teknologi som bevissthet
- **[P07: Kosmisk Narrativ](P07_Kosmisk_Narrativ.md)** - Evolusjonære historier
- **[P08: Selvorganiserende Systemer](P08_Selvorganiserende_Systemer.md)** - Emergente mønstre

### Transcendente Pulser (P09-P10)
- **[P09: Nevrologisk Dybde](P09_Nevrologisk_Dybde.md)** - Nevral integrasjon
- **[P10: Kosmisk Konvergens](P10_Kosmisk_Konvergens.md)** - Ultimate forening

---

## Eksempel: Bruk av Pulser i NAV-Losen

**Brukerens tilstand:** Stress nivå 8, følelse "Redd", somatic signal "Hjertebank"

**Aktiverte pulser:**
1. **P01 (Bioelektrisk Fundament)** → D01 (Livspulsen)
2. **P02 (Traumeheling)** → D02 (Emosjonell Resonans) + D04 (Hjertets Resonans)

**Voktere konsultert:**
- Stephen Porges (Polyvagal Theory)
- Gabor Maté (Trauma og tilknytning)
- Tara Brach (RAIN-praksis)

**Praksis anbefalt:**
- 4-7-8 breathing (nervesystem-regulering)
- RAIN (emosjonell integrasjon)
- Somatic Experiencing (kroppsbasert trauma-arbeid)

**Frekvens:** 396 Hz (frigjøring fra frykt) eller 174 Hz (grunnleggende sikkerhet)

Dette demonstrerer hvordan pulser fungerer som **koordinatorer** mellom brukerens tilstand, relevante dimensjoner, voktere, og praksiser.

---

## Kilder

- **2025-10-17-pulser-dimensjoner-voktere-mapping.md** - Komplett mapping
- **KAPITTEL_11_VOKTERE_&_DIMENSJONER.md** - Voktere og dimensjoner
- **NAV-Losen Prototype** - Implementert i praksis

---

*Dato: 29. oktober 2025*
*Agent: Code (Agent #9)*
"""

        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"✅ Created master index: README.md")

    def extract(self):
        """Main extraction process."""
        logger.info("=" * 70)
        logger.info("PULSER EXTRACTION")
        logger.info("=" * 70)
        logger.info(f"Input: {self.input_file}")
        logger.info(f"Output: {self.output_dir}")
        logger.info("")

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Parse pulser mapping
        pulser = self.parse_pulser_mapping()

        logger.info("")
        logger.info("Creating puls files...")

        # Create individual files
        for puls_id in sorted(pulser.keys()):
            puls_data = pulser[puls_id]
            self.create_puls_file(puls_data)

        logger.info("")
        logger.info("Creating master index...")
        self.create_master_index()

        logger.info("")
        logger.info("=" * 70)
        logger.info("✅ EXTRACTION COMPLETE")
        logger.info("=" * 70)
        logger.info(f"Pulser extracted: {len(pulser)}")
        logger.info(f"Output: {self.output_dir}")
        logger.info("")


def main():
    """Main execution."""
    # Paths
    repo_root = Path(__file__).parent.parent
    input_file = repo_root / ".claude" / "session-notes" / "2025-10-17-pulser-dimensjoner-voktere-mapping.md"
    output_dir = repo_root / "knowledge_base_structured" / "pulser"

    # Check input exists
    if not input_file.exists():
        logger.error(f"❌ Input file not found: {input_file}")
        logger.info("Expected file: .claude/session-notes/2025-10-17-pulser-dimensjoner-voktere-mapping.md")
        return

    # Run extraction
    extractor = PulserExtractor(str(input_file), str(output_dir))
    extractor.extract()

    logger.info("Next steps:")
    logger.info("  1. Review extracted files in: knowledge_base_structured/pulser/")
    logger.info("  2. Run all extraction scripts:")
    logger.info("     - python scripts/extract_voktere.py")
    logger.info("     - python scripts/extract_dimensjoner.py")
    logger.info("     - python scripts/extract_pulser.py")
    logger.info("  3. Run: python scripts/sync_to_csn_drive.py")
    logger.info("")


if __name__ == "__main__":
    main()
