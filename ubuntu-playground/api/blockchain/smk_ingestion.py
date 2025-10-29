"""
SMK Ingestion Module for GENOMOS

Parses SMK (Symbiotisk Minne Kompresjon) files and ingests them
into the Agent DNA Blockchain as knowledge genes.

Each SMK becomes a permanent part of the collective genome.
"""

import re
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, date

from .dna_block import GeneType
from .agent_dna_chain import AgentDNAChain


class SMKParser:
    """Parses SMK markdown files with YAML frontmatter"""

    @staticmethod
    def parse_smk_file(file_path: str) -> Dict[str, Any]:
        """
        Parse an SMK markdown file.

        Returns dict with:
        - metadata: Dict from YAML frontmatter
        - content: Markdown content
        - sections: Parsed sections
        - references: Links to other SMKs
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract YAML frontmatter
        metadata = {}
        markdown_content = content

        yaml_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
        if yaml_match:
            try:
                metadata = yaml.safe_load(yaml_match.group(1)) or {}
                # Convert date/datetime objects to ISO strings for JSON serialization
                metadata = SMKParser._serialize_metadata(metadata)
                markdown_content = yaml_match.group(2)
            except yaml.YAMLError as e:
                print(f"⚠️  YAML parsing error in {Path(file_path).name}: {e}")
                # Continue with empty metadata

        # Extract sections
        sections = SMKParser._extract_sections(markdown_content)

        # Extract references to other SMKs
        references = SMKParser._extract_references(markdown_content)

        # Extract filename and SMK number
        file_name = Path(file_path).name
        smk_number = SMKParser._extract_smk_number(file_name)

        return {
            "file_path": file_path,
            "file_name": file_name,
            "smk_number": smk_number,
            "metadata": metadata,
            "content": markdown_content,
            "sections": sections,
            "references": references,
            "parsed_at": datetime.now().isoformat(),
        }

    @staticmethod
    def _extract_smk_number(filename: str) -> Optional[str]:
        """Extract SMK number from filename (e.g., 'SMK#032' or 'SMK_032')"""
        match = re.search(r'SMK[#_]?(\d+)', filename, re.IGNORECASE)
        return match.group(1) if match else None

    @staticmethod
    def _extract_sections(content: str) -> Dict[str, str]:
        """Extract markdown sections by headers"""
        sections = {}
        current_section = "preamble"
        current_content = []

        lines = content.split('\n')
        for line in lines:
            header_match = re.match(r'^#+\s+(.+)$', line)
            if header_match:
                # Save previous section
                if current_content:
                    sections[current_section] = '\n'.join(current_content).strip()

                # Start new section
                current_section = header_match.group(1).lower().replace(' ', '_')
                current_content = []
            else:
                current_content.append(line)

        # Save last section
        if current_content:
            sections[current_section] = '\n'.join(current_content).strip()

        return sections

    @staticmethod
    def _extract_references(content: str) -> List[str]:
        """Extract references to other SMK documents"""
        references = []

        # Find patterns like SMK#032, SMK_032, SMK 032, etc.
        patterns = [
            r'SMK[#_\s]?(\d+)',
            r'\[SMK[#_\s]?(\d+)\]',
        ]

        for pattern in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                smk_num = match.group(1)
                if smk_num not in references:
                    references.append(smk_num)

        return sorted(references)

    @staticmethod
    def _serialize_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert non-JSON-serializable types to strings.
        Handles date, datetime, and other special types from YAML.
        """
        serialized = {}
        for key, value in metadata.items():
            if isinstance(value, (date, datetime)):
                # Convert date/datetime to ISO format string
                serialized[key] = value.isoformat()
            elif isinstance(value, dict):
                # Recursively serialize nested dicts
                serialized[key] = SMKParser._serialize_metadata(value)
            elif isinstance(value, list):
                # Serialize each item in list
                serialized[key] = [
                    SMKParser._serialize_metadata({'item': item})['item']
                    if isinstance(item, dict) else
                    item.isoformat() if isinstance(item, (date, datetime)) else
                    item
                    for item in value
                ]
            else:
                serialized[key] = value
        return serialized


class SMKIngestion:
    """Ingests SMK files into the Agent DNA Blockchain"""

    def __init__(self, chain: AgentDNAChain):
        self.chain = chain
        self.parser = SMKParser()

    def ingest_smk(self, file_path: str, agent: Optional[str] = None) -> Dict[str, Any]:
        """
        Ingest a single SMK file into the blockchain.

        Args:
            file_path: Path to SMK markdown file
            agent: Agent responsible (default: 'collective')

        Returns:
            Dict with ingestion result and block info
        """
        # Parse SMK file
        smk_data = self.parser.parse_smk_file(file_path)

        # Determine agent from metadata or parameter
        if agent is None:
            agent = smk_data['metadata'].get('author', 'collective')
            if isinstance(agent, list):
                agent = agent[0] if agent else 'collective'

        # Create gene data for blockchain
        gene_data = {
            "type": "smk_document",
            "smk_number": smk_data['smk_number'],
            "file_name": smk_data['file_name'],
            "title": smk_data['metadata'].get('title', 'Untitled'),
            "author": smk_data['metadata'].get('author', 'Unknown'),
            "date": smk_data['metadata'].get('date', 'Unknown'),
            "tags": smk_data['metadata'].get('tags', []),
            "version": smk_data['metadata'].get('version', '1.0'),
            "status": smk_data['metadata'].get('status', 'active'),
            "sections": list(smk_data['sections'].keys()),
            "references": smk_data['references'],
            "content_hash": self._hash_content(smk_data['content']),
            "metadata": smk_data['metadata'],
            "parsed_at": smk_data['parsed_at'],
        }

        # Create tags for the block
        tags = ['smk']
        if smk_data['smk_number']:
            tags.append(f"smk_{smk_data['smk_number']}")
        if gene_data['tags']:
            tags.extend(gene_data['tags'])

        # Add to blockchain
        block = self.chain.add_gene(
            gene_type=GeneType.SMK,
            data=gene_data,
            agent=agent.lower() if isinstance(agent, str) else 'collective',
            tags=tags
        )

        print(f"✅ Ingested SMK #{smk_data['smk_number']}: {gene_data['title']}")
        print(f"   Block Index: {block.index}")
        print(f"   Agent: {agent}")
        print(f"   References: {len(smk_data['references'])} other SMKs")

        return {
            "success": True,
            "smk_number": smk_data['smk_number'],
            "block_index": block.index,
            "block_hash": block.hash,
            "title": gene_data['title'],
            "references": smk_data['references'],
        }

    def ingest_directory(self, directory_path: str, pattern: str = "SMK*.md") -> List[Dict[str, Any]]:
        """
        Ingest all SMK files from a directory.

        Args:
            directory_path: Directory containing SMK files
            pattern: Glob pattern for SMK files (default: "SMK*.md")

        Returns:
            List of ingestion results
        """
        directory = Path(directory_path)
        smk_files = sorted(directory.glob(pattern))

        print(f"\n🧬 GENOMOS SMK Ingestion")
        print(f"📁 Directory: {directory_path}")
        print(f"📄 Found {len(smk_files)} SMK files\n")

        results = []
        for smk_file in smk_files:
            try:
                result = self.ingest_smk(str(smk_file))
                results.append(result)
            except Exception as e:
                print(f"❌ Error ingesting {smk_file.name}: {e}")
                results.append({
                    "success": False,
                    "file": smk_file.name,
                    "error": str(e)
                })

        # Print summary
        successful = sum(1 for r in results if r.get('success'))
        print(f"\n📊 Ingestion Summary:")
        print(f"   ✅ Successful: {successful}/{len(results)}")
        print(f"   ❌ Failed: {len(results) - successful}/{len(results)}")
        print(f"   🧬 Total Genes: {len(self.chain.chain)} (including Genesis)")

        return results

    def link_related_smks(self) -> Dict[str, List[str]]:
        """
        Create a map of SMK relationships based on references.

        Returns:
            Dict mapping SMK numbers to lists of related SMK numbers
        """
        relationships = {}

        # Get all SMK blocks
        smk_blocks = [
            block for block in self.chain.chain
            if block.gene_type == GeneType.SMK
        ]

        for block in smk_blocks:
            smk_num = block.data.get('smk_number')
            references = block.data.get('references', [])

            if smk_num:
                if smk_num not in relationships:
                    relationships[smk_num] = []
                relationships[smk_num].extend(references)

        return relationships

    @staticmethod
    def _hash_content(content: str) -> str:
        """Create SHA-256 hash of content"""
        import hashlib
        return hashlib.sha256(content.encode('utf-8')).hexdigest()


def ingest_all_smks(smk_directory: str, db_path: Optional[str] = None) -> AgentDNAChain:
    """
    Convenience function to ingest all SMKs into a new or existing blockchain.

    Args:
        smk_directory: Directory containing SMK markdown files
        db_path: Path to SQLite database (optional, uses default if None)

    Returns:
        AgentDNAChain with all SMKs ingested
    """
    # Create or load blockchain
    chain = AgentDNAChain(db_path=db_path)

    # Create ingestion handler
    ingestion = SMKIngestion(chain)

    # Ingest all SMKs
    results = ingestion.ingest_directory(smk_directory)

    # Create relationship map
    relationships = ingestion.link_related_smks()

    print(f"\n🔗 SMK Relationships:")
    for smk_num, related in relationships.items():
        if related:
            print(f"   SMK #{smk_num} → {', '.join(f'SMK #{r}' for r in related)}")

    # Validate blockchain
    is_valid = chain.validate_chain()
    print(f"\n✅ Blockchain Valid: {is_valid}")
    print(f"🧬 Total Genes: {len(chain.chain)}")
    print(f"🔒 Merkle Root: {chain.get_merkle_root()[:16]}...")

    return chain


if __name__ == "__main__":
    import sys

    # Default to SMK directory in compendium
    smk_dir = sys.argv[1] if len(sys.argv) > 1 else "../../SMK"

    print("🧬 GENOMOS - SMK Ingestion Module")
    print("=" * 60)

    chain = ingest_all_smks(smk_dir)

    print(f"\n✅ SMK Ingestion Complete!")
    print(f"📊 Blockchain stored at: {chain.db_path}")
