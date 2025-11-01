"""
SMK & LK Blockchain Synchronization Script

Scans the SMK and Living Compendium directories and adds missing documents
to the GENOMOS blockchain. Ensures all knowledge is permanently stored.

Usage:
    python scripts/sync_smk_to_blockchain.py

Features:
- Scans SMK directory for all SMK markdown files
- Scans Living Compendium directories
- Extracts metadata from markdown frontmatter
- Checks if SMK already exists in blockchain (prevents duplicates)
- Adds new SMKs via API
- Logs all operations
"""

import os
import sys
import requests
import json
import re
from pathlib import Path
from datetime import datetime

# Fix Windows UTF-8 encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "api"))

# Configuration
API_BASE_URL = "http://localhost:8005/api/dna"
SMK_DIR = Path(__file__).parent.parent.parent / "SMK"
LK_DIR = Path(__file__).parent.parent.parent / "agents"

def extract_smk_metadata(file_path):
    """Extract metadata from SMK markdown file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract SMK number from filename or content
        filename = file_path.stem
        smk_match = re.search(r'SMK[#\s]*(\d+)', filename, re.IGNORECASE)

        if not smk_match:
            # Try to find in content
            smk_match = re.search(r'SMK[#\s]*(\d+)', content[:500], re.IGNORECASE)

        if not smk_match:
            print(f"⚠️  Could not extract SMK number from {filename}")
            return None

        smk_number = smk_match.group(1).zfill(3)  # Pad to 3 digits

        # Extract title (first H1 or H2 heading)
        title_match = re.search(r'^#{1,2}\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else filename

        # Extract date
        date_match = re.search(r'\*\*Dato:\*\*\s*(.+)', content)
        date = date_match.group(1).strip() if date_match else "unknown"

        # Extract author/agent
        author_match = re.search(r'\*\*Agent:\*\*\s*(.+)', content)
        author = author_match.group(1).strip() if author_match else "Unknown"

        # Extract version
        version_match = re.search(r'\*\*Versjon:\*\*\s*(.+)', content)
        version = version_match.group(1).strip() if version_match else "1.0"

        # Extract tags from content
        tags = [f"smk-{smk_number}", "smk"]

        # Look for common keywords
        if "MCP" in content or "mcp" in content:
            tags.append("mcp")
        if "NAV" in content:
            tags.append("nav-losen")
        if "connector" in content.lower():
            tags.append("connectors")
        if "blockchain" in content.lower():
            tags.append("blockchain")

        # Extract references (look for SMK# mentions)
        references = []
        ref_matches = re.findall(r'SMK[#\s]*(\d+)', content)
        for ref in ref_matches:
            ref_padded = ref.zfill(3)
            if ref_padded != smk_number and ref_padded not in references:
                references.append(ref_padded)

        return {
            "smk_number": smk_number,
            "title": title,
            "date": date,
            "author": author,
            "version": version,
            "tags": tags,
            "references": references,
            "file_path": str(file_path)
        }

    except Exception as e:
        print(f"❌ Error parsing {file_path}: {e}")
        return None


def get_existing_smks():
    """Get list of existing SMK numbers in blockchain"""
    try:
        response = requests.get(f"{API_BASE_URL}/smk", timeout=10)
        if response.status_code == 200:
            smks = response.json()
            return set(smk["smk_number"] for smk in smks)
        else:
            print(f"⚠️  Failed to fetch existing SMKs: HTTP {response.status_code}")
            return set()
    except Exception as e:
        print(f"❌ Error fetching existing SMKs: {e}")
        return set()


def add_smk_to_blockchain(smk_data):
    """Add SMK to blockchain via direct blockchain API (not REST endpoint)"""
    try:
        # Import blockchain directly
        from blockchain.agent_dna_chain import AgentDNAChain
        from blockchain.dna_block import GeneType

        # Use absolute path to API's database
        db_path = Path(__file__).parent.parent / "api" / "data" / "genomos.db"

        # Initialize blockchain
        blockchain = AgentDNAChain(db_path=str(db_path))

        # Add SMK gene
        block = blockchain.add_gene(
            gene_type=GeneType.SMK,
            data=smk_data,
            agent=smk_data.get("author", "unknown").lower(),
            tags=smk_data.get("tags", [])
        )

        print(f"✅ Added SMK#{smk_data['smk_number']}: {smk_data['title'][:60]}... (Block {block.index})")
        return True

    except Exception as e:
        print(f"❌ Failed to add SMK#{smk_data['smk_number']}: {e}")
        return False


def sync_smk_files():
    """Scan SMK directory and sync to blockchain"""
    print("📂 Scanning SMK directory...")
    print(f"   Location: {SMK_DIR}")

    if not SMK_DIR.exists():
        print(f"❌ SMK directory not found: {SMK_DIR}")
        return

    # Get existing SMKs
    existing = get_existing_smks()
    print(f"📊 Found {len(existing)} SMKs already in blockchain")

    # Find all SMK markdown files
    smk_files = list(SMK_DIR.glob("SMK*.md")) + list(SMK_DIR.glob("smk*.md"))
    print(f"📄 Found {len(smk_files)} SMK files")

    added_count = 0
    skipped_count = 0
    error_count = 0

    for smk_file in smk_files:
        metadata = extract_smk_metadata(smk_file)

        if not metadata:
            error_count += 1
            continue

        smk_num = metadata["smk_number"]

        # Check if already exists
        if smk_num in existing:
            print(f"⏭️  SMK#{smk_num} already in blockchain - skipping")
            skipped_count += 1
            continue

        # Add to blockchain
        if add_smk_to_blockchain(metadata):
            added_count += 1
        else:
            error_count += 1

    print(f"\n📊 Sync Summary:")
    print(f"   ✅ Added: {added_count}")
    print(f"   ⏭️  Skipped: {skipped_count}")
    print(f"   ❌ Errors: {error_count}")


def sync_living_compendiums():
    """Scan Living Compendium directories and sync to blockchain"""
    print("\n📂 Scanning Living Compendium directories...")
    print(f"   Location: {LK_DIR}")

    if not LK_DIR.exists():
        print(f"❌ LK directory not found: {LK_DIR}")
        return

    # Find all LK markdown files
    lk_files = list(LK_DIR.glob("**/CODE_LIVING_COMPENDIUM_V*.md"))
    print(f"📄 Found {len(lk_files)} Living Compendium files")

    # For now, just list them (we could add them as a special gene type)
    for lk_file in lk_files:
        print(f"   📖 {lk_file.name}")

    print(f"\n💡 Note: Living Compendium files are not yet synced to blockchain")
    print(f"   (This would require a new GeneType.LIVING_COMPENDIUM)")


def main():
    """Main synchronization function"""
    print("=" * 70)
    print("🧬 GENOMOS SMK & LK Blockchain Synchronization")
    print("=" * 70)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()

    # Check if blockchain API is available
    try:
        response = requests.get(f"{API_BASE_URL}/info", timeout=5)
        if response.status_code == 200:
            info = response.json()
            print(f"✅ Blockchain API connected")
            print(f"   Total genes: {info['total_genes']}")
            print(f"   Genesis hash: {info['genesis_hash'][:16]}...")
            print()
        else:
            print(f"⚠️  Blockchain API returned HTTP {response.status_code}")
            print(f"   Continuing anyway (will use direct blockchain access)...")
            print()
    except Exception as e:
        print(f"⚠️  Blockchain API not reachable: {e}")
        print(f"   Continuing with direct blockchain access...")
        print()

    # Sync SMK files
    sync_smk_files()

    # Sync Living Compendiums
    sync_living_compendiums()

    print("\n✅ Synchronization complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
