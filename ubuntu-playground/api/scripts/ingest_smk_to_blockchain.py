#!/usr/bin/env python3
"""
GENOMOS Phase 3: SMK Ingestion Script

Ingests all SMK (Systemisk Minne Kompendium) files from the SMK/ directory
into the GENOMOS Agent DNA Blockchain.

Each SMK becomes a permanent gene in the blockchain, creating an immutable
knowledge base that can be queried via the DNA API.

Usage:
    python scripts/ingest_smk_to_blockchain.py [--blockchain-db PATH] [--smk-dir PATH]

Example:
    python scripts/ingest_smk_to_blockchain.py --blockchain-db ./data/genomos.db --smk-dir ../../SMK
"""

import sys
import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, date
import yaml
import logging

# Add parent directory to path to import blockchain modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from blockchain.agent_dna_chain import AgentDNAChain
from blockchain.dna_block import GeneType

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)


class SMKParser:
    """Parser for SMK files with support for both YAML frontmatter and markdown headers."""

    @staticmethod
    def parse_smk_file(file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Parse a SMK markdown file and extract metadata and content.

        Supports two formats:
        1. YAML frontmatter (enclosed in ---)
        2. Markdown header with metadata fields

        Returns:
            Dictionary with SMK metadata and content, or None if parsing fails
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Try parsing YAML frontmatter first
            frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)

            if frontmatter_match:
                # YAML frontmatter present
                yaml_content = frontmatter_match.group(1)
                markdown_content = frontmatter_match.group(2)

                try:
                    metadata = yaml.safe_load(yaml_content) or {}
                except yaml.YAMLError as e:
                    logger.warning(f"Failed to parse YAML frontmatter in {file_path.name}: {e}")
                    metadata = {}
            else:
                # No frontmatter, parse markdown header
                metadata = {}
                markdown_content = content

            # Extract SMK number from filename
            smk_number_match = re.search(r'SMK[#_]?(\d+)', file_path.name)
            if smk_number_match:
                smk_number = smk_number_match.group(1).zfill(3)
            else:
                logger.warning(f"Could not extract SMK number from {file_path.name}")
                return None

            # Parse markdown header for additional metadata
            header_metadata = SMKParser._parse_markdown_header(markdown_content)
            metadata.update(header_metadata)

            # Extract title from content if not in metadata
            if 'title' not in metadata or not metadata['title']:
                title_match = re.search(r'^#\s+SMK\s+#?\d+:?\s*(.+)$', markdown_content, re.MULTILINE)
                if title_match:
                    metadata['title'] = title_match.group(1).strip()

            # Build SMK data structure (with full metadata serialization)
            smk_data = {
                'type': 'smk_document',
                'smk_number': smk_number,
                'title': metadata.get('title', file_path.stem),
                'agent': metadata.get('agent', 'Unknown'),
                'date': SMKParser._serialize_date(metadata.get('date')),
                'tags': metadata.get('tags', []),
                'status': metadata.get('status', 'DOCUMENTED'),
                'significance': metadata.get('significance', ''),
                'related_smk': metadata.get('related_smk', []),
                'related_lk': metadata.get('related_lk', []),
                'content_preview': markdown_content[:500],  # First 500 chars
                'file_path': str(file_path.relative_to(file_path.parent.parent)),
                'metadata': SMKParser._serialize_metadata(metadata),
            }

            # Extract key sections
            sections = SMKParser._extract_sections(markdown_content)
            if sections:
                smk_data['sections'] = sections

            return smk_data

        except Exception as e:
            logger.error(f"Error parsing {file_path}: {e}")
            return None

    @staticmethod
    def _parse_markdown_header(content: str) -> Dict[str, Any]:
        """Extract metadata from markdown header (first 20 lines)."""
        metadata = {}
        lines = content.split('\n')[:20]

        for line in lines:
            # Match patterns like "**Dato:** 28. oktober 2025"
            match = re.match(r'\*\*(.+?):\*\*\s*(.+)', line)
            if match:
                key = match.group(1).lower()
                value = match.group(2).strip()

                if key in ['dato', 'date']:
                    metadata['date'] = value
                elif key == 'agent':
                    metadata['agent'] = value
                elif key == 'type':
                    metadata['type'] = value
                elif key == 'status':
                    metadata['status'] = value

        return metadata

    @staticmethod
    def _extract_sections(content: str) -> List[Dict[str, str]]:
        """Extract main sections from markdown content."""
        sections = []

        # Find all H2 headers (## Section Title)
        section_pattern = re.finditer(r'^##\s+(.+)$', content, re.MULTILINE)
        section_positions = [(match.group(1), match.start()) for match in section_pattern]

        for i, (title, start) in enumerate(section_positions):
            # Get content until next section or end of file
            if i < len(section_positions) - 1:
                end = section_positions[i + 1][1]
            else:
                end = len(content)

            section_content = content[start:end].strip()

            sections.append({
                'title': title.strip(),
                'preview': section_content[:200]  # First 200 chars of section
            })

        return sections

    @staticmethod
    def _serialize_date(date_value: Any) -> Optional[str]:
        """Convert date to ISO format string."""
        if isinstance(date_value, (date, datetime)):
            return date_value.isoformat()
        elif isinstance(date_value, str):
            return date_value
        return None

    @staticmethod
    def _serialize_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively serialize metadata to ensure JSON compatibility."""
        serialized = {}
        for key, value in metadata.items():
            if isinstance(value, (date, datetime)):
                serialized[key] = value.isoformat()
            elif isinstance(value, dict):
                serialized[key] = SMKParser._serialize_metadata(value)
            elif isinstance(value, list):
                serialized[key] = [
                    SMKParser._serialize_metadata(item) if isinstance(item, dict)
                    else item.isoformat() if isinstance(item, (date, datetime))
                    else item
                    for item in value
                ]
            else:
                serialized[key] = value
        return serialized


class SMKIngestionPipeline:
    """Pipeline for ingesting SMK files into the GENOMOS blockchain."""

    def __init__(self, blockchain_db_path: str, smk_directory: str):
        """
        Initialize the ingestion pipeline.

        Args:
            blockchain_db_path: Path to GENOMOS blockchain database
            smk_directory: Path to directory containing SMK markdown files
        """
        self.blockchain = AgentDNAChain(db_path=blockchain_db_path)
        self.smk_directory = Path(smk_directory)
        self.parser = SMKParser()

        logger.info(f"📂 SMK Directory: {self.smk_directory}")
        logger.info(f"🧬 Blockchain: {blockchain_db_path}")

    def ingest_all_smks(self) -> Dict[str, Any]:
        """
        Ingest all SMK files from the directory into the blockchain.

        Returns:
            Dictionary with ingestion statistics
        """
        # Find all SMK markdown files
        smk_files = sorted(self.smk_directory.glob('SMK*.md'))

        logger.info(f"📝 Found {len(smk_files)} SMK files")

        stats = {
            'total_files': len(smk_files),
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'errors': []
        }

        for smk_file in smk_files:
            try:
                # Check if SMK already exists in blockchain
                smk_number = self._extract_smk_number(smk_file.name)
                if self._smk_exists(smk_number):
                    logger.info(f"⏭️  SMK #{smk_number} already in blockchain, skipping")
                    stats['skipped'] += 1
                    continue

                # Parse SMK file
                smk_data = self.parser.parse_smk_file(smk_file)

                if not smk_data:
                    logger.error(f"❌ Failed to parse {smk_file.name}")
                    stats['failed'] += 1
                    stats['errors'].append(f"Parse failed: {smk_file.name}")
                    continue

                # Add to blockchain
                block = self.blockchain.add_gene(
                    gene_type=GeneType.SMK,
                    data=smk_data,
                    agent=smk_data['agent'].lower(),
                    tags=['smk', f"smk-{smk_data['smk_number']}"] + smk_data.get('tags', [])
                )

                logger.info(f"✅ SMK #{smk_data['smk_number']}: {smk_data['title']}")
                logger.info(f"   Block #{block.index} | Hash: {block.hash[:16]}...")

                stats['successful'] += 1

            except Exception as e:
                logger.error(f"❌ Error processing {smk_file.name}: {e}")
                stats['failed'] += 1
                stats['errors'].append(f"{smk_file.name}: {str(e)}")

        return stats

    def _extract_smk_number(self, filename: str) -> str:
        """Extract SMK number from filename."""
        match = re.search(r'SMK[#_]?(\d+)', filename)
        if match:
            return match.group(1).zfill(3)
        return None

    def _smk_exists(self, smk_number: str) -> bool:
        """Check if SMK already exists in blockchain."""
        for block in self.blockchain.chain:
            if block.gene_type == GeneType.SMK:
                existing_number = block.data.get('smk_number', '')
                if existing_number == smk_number:
                    return True
        return False

    def print_summary(self, stats: Dict[str, Any]):
        """Print ingestion summary."""
        logger.info("\n" + "="*60)
        logger.info("🧬 GENOMOS Phase 3: SMK Ingestion Summary")
        logger.info("="*60)
        logger.info(f"Total SMK files found: {stats['total_files']}")
        logger.info(f"✅ Successfully ingested: {stats['successful']}")
        logger.info(f"⏭️  Skipped (already exists): {stats['skipped']}")
        logger.info(f"❌ Failed: {stats['failed']}")

        if stats['errors']:
            logger.info("\nErrors:")
            for error in stats['errors']:
                logger.info(f"  - {error}")

        logger.info("\n📊 Blockchain Statistics:")
        info = self.blockchain.get_chain_info()
        logger.info(f"Total genes: {info['total_blocks']}")
        logger.info(f"Genesis hash: {info['genesis_block'][:16]}...")
        logger.info(f"Latest hash: {info['latest_block'][:16]}...")
        logger.info(f"Is valid: {info['chain_valid']}")

        # Count genes by type
        gene_counts = {}
        for block in self.blockchain.chain:
            gene_type = block.gene_type.value
            gene_counts[gene_type] = gene_counts.get(gene_type, 0) + 1

        logger.info("\nGene distribution:")
        for gene_type, count in sorted(gene_counts.items()):
            logger.info(f"  {gene_type}: {count}")

        logger.info("="*60)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Ingest SMK files into GENOMOS blockchain')
    parser.add_argument(
        '--blockchain-db',
        default='./data/genomos.db',
        help='Path to GENOMOS blockchain database (default: ./data/genomos.db)'
    )
    parser.add_argument(
        '--smk-dir',
        default='../../SMK',
        help='Path to SMK directory (default: ../../SMK)'
    )

    args = parser.parse_args()

    # Initialize pipeline
    pipeline = SMKIngestionPipeline(
        blockchain_db_path=args.blockchain_db,
        smk_directory=args.smk_dir
    )

    # Ingest all SMKs
    logger.info("🚀 Starting SMK ingestion...")
    stats = pipeline.ingest_all_smks()

    # Print summary
    pipeline.print_summary(stats)

    # Exit with error code if any failures
    if stats['failed'] > 0:
        sys.exit(1)

    logger.info("✨ SMK ingestion complete!")
    sys.exit(0)


if __name__ == '__main__':
    main()
