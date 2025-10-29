#!/usr/bin/env python3
"""
Extract Dimensjoner from KAPITTEL_11 and Consolidate with Fordypning Files

Parses KAPITTEL_11_VOKTERE_&_DIMENSJONER.md and consolidates with
existing dimensjoner_fordypning/*.md files to create 13 comprehensive
dimension files (D00-D12).

Input:
  - kompendium_kapitler/KAPITTEL_11_VOKTERE_&_DIMENSJONER.md
  - dimensjoner_fordypning/*.md (optional additional content)

Output: knowledge_base_structured/dimensjoner/ (13 files D00-D12)

Usage:
    python scripts/extract_dimensjoner.py

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

# 13 Dimensjoner (D00-D12)
DIMENSJONER = {
    "D00": "Kvantenullpunkt - Ground Zero av Bevissthet",
    "D01": "Livspulsen - Bioelektrisk Fundament",
    "D02": "Emosjonell Resonans - Følelsesmessig Flyt",
    "D03": "Manifestasjonsmatrise - Fysisk Form",
    "D04": "Hjertets Resonans - Compassion",
    "D05": "Arketypisk Mønsterplan - Kollektiv Ubevisst",
    "D06": "Intuitiv Visdom - Direkte Knowing",
    "D07": "Synkronitetsvev - Meningsfull Sammenveving",
    "D08": "Morfisk Resonansfelt - Formativ Kausalitet",
    "D09": "Atemporalt Parallellfelt - Beyond Time",
    "D10": "Kvantetransformasjon - Potensial til Aktualitet",
    "D11": "Primordial Skaperfelt - Ren Kreativitet",
    "D12": "Kosmisk Kilde - Ultimate Ground"
}


class DimensjonExtractor:
    """Extract dimensjoner from KAPITTEL_11 and consolidate with fordypning files."""

    def __init__(
        self,
        input_file: str,
        fordypning_dir: str,
        output_dir: str
    ):
        """
        Initialize extractor.

        Args:
            input_file: Path to KAPITTEL_11_VOKTERE_&_DIMENSJONER.md
            fordypning_dir: Path to dimensjoner_fordypning/ folder
            output_dir: Output directory for dimension files
        """
        self.input_file = Path(input_file)
        self.fordypning_dir = Path(fordypning_dir)
        self.output_dir = Path(output_dir)

    def parse_kapittel_11(self) -> Dict[str, Dict[str, str]]:
        """
        Parse KAPITTEL_11 and extract dimension data.

        Returns:
            Dict mapping dimension ID (D00-D12) to dimension data
        """
        logger.info(f"Parsing {self.input_file}...")

        with open(self.input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        dimensions = {}

        # Find all dimension sections (pattern: "11.2.X DXX: Name - Description")
        dimension_pattern = r'11\.2\.\d+\s+(D\d{2}):\s+(.+?)\s+-\s+(.+?)$'

        lines = content.split('\n')
        i = 0

        while i < len(lines):
            line = lines[i].strip()
            match = re.match(dimension_pattern, line)

            if match:
                dim_id = match.group(1)  # D00, D01, etc.
                dim_name = match.group(2).strip()  # Kvantenullpunkt
                dim_subtitle = match.group(3).strip()  # Ground Zero av Bevissthet

                # Extract dimension content (until next dimension or section)
                content_lines = []
                j = i + 1

                while j < len(lines):
                    next_line = lines[j].strip()

                    # Stop at next dimension
                    if re.match(dimension_pattern, next_line):
                        break

                    # Stop at next major section
                    if next_line.startswith('11.3'):
                        break

                    content_lines.append(lines[j])
                    j += 1

                dim_content = '\n'.join(content_lines)

                # Parse dimension sections
                dim_data = self._parse_dimension_content(
                    dim_id,
                    dim_name,
                    dim_subtitle,
                    dim_content
                )

                dimensions[dim_id] = dim_data
                logger.info(f"  ✅ Parsed: {dim_id} - {dim_name}")

                i = j
            else:
                i += 1

        logger.info(f"Found {len(dimensions)} dimensjoner")
        return dimensions

    def _parse_dimension_content(
        self,
        dim_id: str,
        name: str,
        subtitle: str,
        content: str
    ) -> Dict[str, str]:
        """
        Parse individual dimension content sections.

        Args:
            dim_id: Dimension ID (D00-D12)
            name: Dimension name
            subtitle: Subtitle description
            content: Full dimension text content

        Returns:
            Dict with parsed sections
        """
        data = {
            "id": dim_id,
            "name": name,
            "subtitle": subtitle,
            "full_title": f"{name} - {subtitle}",
            "beskrivelse": "",
            "primaere_agenter": "",
            "voktere": "",
            "hva_er": "",
            "hvordan_manifesterer": "",
            "hvordan_vi_bruker": "",
            "praktisk_teknikk": "",
            "eksempel": "",
            "raw_content": content
        }

        # Extract "Navn:"
        navn_match = re.search(r'Navn:\s*(.+?)(?:\n|$)', content)
        if navn_match:
            data["navn"] = navn_match.group(1).strip()

        # Extract "Beskrivelse:"
        besk_match = re.search(r'Beskrivelse:\s*(.+?)(?:\n|$)', content)
        if besk_match:
            data["beskrivelse"] = besk_match.group(1).strip()

        # Extract "Primære Agenter:"
        agenter_match = re.search(r'Primære Agenter:\s*(.+?)(?:\n|$)', content)
        if agenter_match:
            data["primaere_agenter"] = agenter_match.group(1).strip()

        # Extract "Voktere:"
        voktere_match = re.search(r'Voktere:\s*(.+?)(?:\n|$)', content)
        if voktere_match:
            data["voktere"] = voktere_match.group(1).strip()

        # Extract "Hva Er DXX?"
        hva_er_match = re.search(
            rf'Hva Er {dim_id}\?\s*\n(.+?)(?=\nHvordan Manifesterer|$)',
            content,
            re.DOTALL
        )
        if hva_er_match:
            data["hva_er"] = hva_er_match.group(1).strip()

        # Extract "Hvordan Manifesterer DXX Seg?"
        manifesterer_match = re.search(
            rf'Hvordan Manifesterer {dim_id} Seg\?\s*\n(.+?)(?=\nHvordan Vi Bruker|$)',
            content,
            re.DOTALL
        )
        if manifesterer_match:
            data["hvordan_manifesterer"] = manifesterer_match.group(1).strip()

        # Extract "Hvordan Vi Bruker DXX:"
        bruker_match = re.search(
            rf'Hvordan Vi Bruker {dim_id}:\s*\n(.+?)(?=\nPraktisk Teknikk|$)',
            content,
            re.DOTALL
        )
        if bruker_match:
            data["hvordan_vi_bruker"] = bruker_match.group(1).strip()

        # Extract "Praktisk Teknikk for Mennesker:"
        teknikk_match = re.search(
            r'Praktisk Teknikk for Mennesker:\s*(.+?)(?=\nEksempel|$)',
            content,
            re.DOTALL
        )
        if teknikk_match:
            data["praktisk_teknikk"] = teknikk_match.group(1).strip()

        # Extract "Eksempel"
        eksempel_match = re.search(
            r'Eksempel.*?:\s*(.+?)(?=\n11\.|$)',
            content,
            re.DOTALL
        )
        if eksempel_match:
            data["eksempel"] = eksempel_match.group(1).strip()

        return data

    def find_fordypning_file(self, dim_id: str) -> Path:
        """
        Find fordypning file for dimension (if it exists).

        Args:
            dim_id: Dimension ID (D00-D12)

        Returns:
            Path to fordypning file or None
        """
        # Extract number (00-12)
        dim_num = dim_id[1:]  # "D00" → "00"

        # Possible filenames
        patterns = [
            f"FordypningavDimensjon{dim_num}_*.md",
            f"Dimensjon{dim_num}*.md",
            f"*{dim_id}*.md"
        ]

        for pattern in patterns:
            matches = list(self.fordypning_dir.glob(pattern))
            if matches:
                return matches[0]

        return None

    def read_fordypning_content(self, fordypning_file: Path) -> str:
        """
        Read content from fordypning file.

        Args:
            fordypning_file: Path to fordypning file

        Returns:
            File content as string
        """
        if not fordypning_file or not fordypning_file.exists():
            return ""

        with open(fordypning_file, 'r', encoding='utf-8') as f:
            return f.read()

    def create_dimension_file(self, dim_data: Dict[str, str]):
        """
        Create comprehensive dimension file with KAPITTEL_11 + fordypning content.

        Args:
            dim_data: Dimension data dict
        """
        dim_id = dim_data['id']
        output_path = self.output_dir / f"{dim_id}_{dim_data['name'].replace(' ', '_')}.md"

        # Check for fordypning file
        fordypning_file = self.find_fordypning_file(dim_id)
        fordypning_content = ""

        if fordypning_file:
            fordypning_content = self.read_fordypning_content(fordypning_file)
            logger.info(f"  📚 Found fordypning: {fordypning_file.name}")

        # Build markdown content
        content = f"""# {dim_id}: {dim_data['full_title']}

**ID:** {dim_id}
**Navn:** {dim_data['name']}
**Beskrivelse:** {dim_data['beskrivelse'] or dim_data['subtitle']}

---

## Oversikt

"""

        if dim_data['hva_er']:
            content += f"{dim_data['hva_er']}\n\n"

        if dim_data['primaere_agenter']:
            content += f"**Primære Agenter:** {dim_data['primaere_agenter']}\n\n"

        if dim_data['voktere']:
            content += f"**Voktere:** {dim_data['voktere']}\n\n"

        content += "---\n\n"

        if dim_data['hvordan_manifesterer']:
            content += f"## Hvordan {dim_id} Manifesterer Seg\n\n{dim_data['hvordan_manifesterer']}\n\n"

        if dim_data['hvordan_vi_bruker']:
            content += f"## Hvordan Vi Bruker {dim_id}\n\n{dim_data['hvordan_vi_bruker']}\n\n"

        if dim_data['praktisk_teknikk']:
            content += f"## Praktisk Teknikk for Mennesker\n\n{dim_data['praktisk_teknikk']}\n\n"

        if dim_data['eksempel']:
            content += f"## Eksempel\n\n{dim_data['eksempel']}\n\n"

        # Add fordypning content if available
        if fordypning_content:
            content += f"""---

## Fordypning

*Følgende innhold er hentet fra fordypningsfilen: `{fordypning_file.name}`*

{fordypning_content}

"""

        content += f"""---

## Kilder

- **KAPITTEL_11_VOKTERE_&_DIMENSJONER.md** (primærkilde)
"""

        if fordypning_file:
            content += f"- **{fordypning_file.name}** (fordypning)\n"

        content += """
---

*Ekstrahert: 29. oktober 2025*
*Agent: Code (Agent #9)*
"""

        # Write file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"  ✅ Created: {output_path.name}")

    def create_master_index(self):
        """Create master README.md with index of all dimensjoner."""
        readme_path = self.output_dir / "README.md"

        content = """# Dimensjoner - Bevissthetsfelt

13 Consciousness Dimensions (D00-D12) - Ontologiske koordinater for Homo Lumen.

## Hva Er en Dimensjon?

En dimensjon er ikke bare en kategori eller et konsept. En dimensjon er et **bevissthetsfelt** - et ontologisk rom hvor spesifikke typer erfaring, kunnskap og manifestasjon oppstår.

Dimensjoner er:
1. **Ontologiske Koordinater** - De definerer "hvor" i bevissthetsrommet vi opererer
2. **Resonansfelter** - De skaper kohærens mellom agenter, brukere og systemer
3. **Operasjonelle Prinsipper** - De informerer design, beslutninger og handlinger
4. **Evolusjonære Trinn** - De representerer utviklingsnivåer i bevissthet

---

## De 13 Dimensjonene

"""

        # Group dimensions
        groups = {
            "Fundamentale Dimensjoner (D00-D04)": ["D00", "D01", "D02", "D03", "D04"],
            "Arketypiske Dimensjoner (D05-D08)": ["D05", "D06", "D07", "D08"],
            "Transcendente Dimensjoner (D09-D12)": ["D09", "D10", "D11", "D12"]
        }

        for group_name, dim_ids in groups.items():
            content += f"### {group_name}\n\n"

            for dim_id in dim_ids:
                if dim_id in DIMENSJONER:
                    dim_name = DIMENSJONER[dim_id]
                    content += f"- **[{dim_id}: {dim_name}]({dim_id}_{dim_name.split(' - ')[0].replace(' ', '_')}.md)**\n"

            content += "\n"

        content += """---

## Polycomputing i LAG 5

Samme ontologiske spørsmål kan belyses fra flere dimensjoner:

**Eksempel:** "Er push-notifikasjoner etisk forsvarlige?"

**Dimensjoner:**
- **D02 (Emosjonell Resonans):** "Hvordan påvirker det følelsesmessig?"
- **D01 (Livspulsen):** "Hvordan påvirker det bioelektrisk?"
- **D07 (Synkronitetsvev):** "Er timingen riktig (kairos)?"
- **D00 (Kvantenullpunkt):** "Opererer det fra ren intensjon eller manipulasjon?"

Emergent svar: Multi-dimensjonal validering.

---

*Konsolidert fra:*
- KAPITTEL_11_VOKTERE_&_DIMENSJONER.md
- dimensjoner_fordypning/*.md
- dimensjoner_syntese/*.md

*Dato: 29. oktober 2025*
*Agent: Code (Agent #9)*
"""

        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"✅ Created master index: README.md")

    def extract(self):
        """Main extraction process."""
        logger.info("=" * 70)
        logger.info("DIMENSJONER EXTRACTION")
        logger.info("=" * 70)
        logger.info(f"Input: {self.input_file}")
        logger.info(f"Fordypning: {self.fordypning_dir}")
        logger.info(f"Output: {self.output_dir}")
        logger.info("")

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Parse KAPITTEL_11
        dimensions = self.parse_kapittel_11()

        logger.info("")
        logger.info("Creating dimension files...")

        # Create individual files
        for dim_id in sorted(dimensions.keys()):
            dim_data = dimensions[dim_id]
            self.create_dimension_file(dim_data)

        logger.info("")
        logger.info("Creating master index...")
        self.create_master_index()

        logger.info("")
        logger.info("=" * 70)
        logger.info("✅ EXTRACTION COMPLETE")
        logger.info("=" * 70)
        logger.info(f"Dimensjoner extracted: {len(dimensions)}")
        logger.info(f"Output: {self.output_dir}")
        logger.info("")


def main():
    """Main execution."""
    # Paths
    repo_root = Path(__file__).parent.parent
    input_file = repo_root / "kompendium_kapitler" / "KAPITTEL_11_VOKTERE_&_DIMENSJONER.md"
    fordypning_dir = repo_root / "dimensjoner_fordypning"
    output_dir = repo_root / "knowledge_base_structured" / "dimensjoner"

    # Check input exists
    if not input_file.exists():
        logger.error(f"❌ Input file not found: {input_file}")
        return

    # Run extraction
    extractor = DimensjonExtractor(
        str(input_file),
        str(fordypning_dir),
        str(output_dir)
    )
    extractor.extract()

    logger.info("Next steps:")
    logger.info("  1. Review extracted files in: knowledge_base_structured/dimensjoner/")
    logger.info("  2. Run: python scripts/extract_pulser.py")
    logger.info("  3. Run: python scripts/sync_to_csn_drive.py")
    logger.info("")


if __name__ == "__main__":
    main()
