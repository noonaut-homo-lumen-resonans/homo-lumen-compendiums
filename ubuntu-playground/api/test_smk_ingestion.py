"""
Test SMK Ingestion into GENOMOS Blockchain

Tests Phase 3 of GENOMOS implementation:
- SMK file parsing
- Blockchain ingestion
- Relationship linking
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from blockchain.smk_ingestion import SMKIngestion, SMKParser, ingest_all_smks
from blockchain.agent_dna_chain import AgentDNAChain
from blockchain.dna_block import GeneType

def test_smk_parser():
    """Test SMK file parsing"""
    print("\n" + "=" * 60)
    print("TEST 1: SMK Parser")
    print("=" * 60)

    # Test with SMK#019 (Constitution)
    smk_path = "../../SMK/SMK#019-CONSTITUTIONV1.md"
    if not os.path.exists(smk_path):
        print(f"⚠️  SMK file not found: {smk_path}")
        return False

    parser = SMKParser()
    smk_data = parser.parse_smk_file(smk_path)

    print(f"✅ Parsed: {smk_data['file_name']}")
    print(f"   SMK Number: #{smk_data['smk_number']}")
    print(f"   Title: {smk_data['metadata'].get('title', 'N/A')}")
    print(f"   Sections: {len(smk_data['sections'])}")
    print(f"   References: {len(smk_data['references'])}")

    if smk_data['sections']:
        print(f"   Section Names: {', '.join(list(smk_data['sections'].keys())[:5])}")

    return True


def test_single_smk_ingestion():
    """Test ingesting a single SMK"""
    print("\n" + "=" * 60)
    print("TEST 2: Single SMK Ingestion")
    print("=" * 60)

    # Create a test blockchain
    chain = AgentDNAChain(db_path="./data/test_genomos.db")

    # Create ingestion handler
    ingestion = SMKIngestion(chain)

    # Ingest SMK#019
    smk_path = "../../SMK/SMK#019-CONSTITUTIONV1.md"
    if not os.path.exists(smk_path):
        print(f"⚠️  SMK file not found: {smk_path}")
        return False

    result = ingestion.ingest_smk(smk_path, agent='collective')

    print(f"\n✅ Ingestion Result:")
    print(f"   Success: {result['success']}")
    print(f"   Block Index: {result['block_index']}")
    print(f"   Block Hash: {result['block_hash'][:16]}...")
    print(f"   Title: {result['title']}")

    # Verify blockchain
    is_valid = chain.validate_chain()
    print(f"\n✅ Blockchain Valid: {is_valid}")
    print(f"🧬 Total Genes: {len(chain.chain)} (Genesis + 1 SMK)")

    return is_valid


def test_multiple_smk_ingestion():
    """Test ingesting multiple SMKs from directory"""
    print("\n" + "=" * 60)
    print("TEST 3: Multiple SMK Ingestion")
    print("=" * 60)

    # Use the main SMK directory
    smk_dir = "../../SMK"
    if not os.path.exists(smk_dir):
        print(f"⚠️  SMK directory not found: {smk_dir}")
        return False

    # Create new blockchain for this test
    chain = ingest_all_smks(smk_dir, db_path="./data/genomos_full.db")

    # Validate
    is_valid = chain.validate_chain()

    print(f"\n✅ Final Blockchain State:")
    print(f"   Valid: {is_valid}")
    print(f"   Total Blocks: {len(chain.chain)}")
    print(f"   Genesis: {chain.chain[0].gene_type}")
    print(f"   SMK Genes: {sum(1 for b in chain.chain if b.gene_type == GeneType.SMK)}")
    print(f"   Merkle Root: {chain.get_merkle_root()[:16]}...")

    # Show first few SMK blocks
    smk_blocks = [b for b in chain.chain if b.gene_type == GeneType.SMK][:5]
    print(f"\n📄 First {len(smk_blocks)} SMK Genes:")
    for block in smk_blocks:
        print(f"   Block {block.index}: SMK #{block.data['smk_number']} - {block.data['title']}")

    return is_valid


def test_smk_relationships():
    """Test SMK relationship linking"""
    print("\n" + "=" * 60)
    print("TEST 4: SMK Relationships")
    print("=" * 60)

    # Load blockchain with SMKs
    chain = AgentDNAChain(db_path="./data/genomos_full.db")
    ingestion = SMKIngestion(chain)

    # Get relationships
    relationships = ingestion.link_related_smks()

    print(f"✅ Found {len(relationships)} SMKs with relationships")

    # Show some examples
    count = 0
    for smk_num, related in relationships.items():
        if related and count < 5:
            print(f"   SMK #{smk_num} → {', '.join(f'SMK #{r}' for r in related[:3])}")
            count += 1

    return True


def main():
    """Run all tests"""
    print("\n🧬 GENOMOS Phase 3: SMK Ingestion Tests")
    print("=" * 60)

    # Ensure Windows UTF-8 encoding
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass

    results = []

    # Test 1: Parser
    results.append(("SMK Parser", test_smk_parser()))

    # Test 2: Single ingestion
    results.append(("Single Ingestion", test_single_smk_ingestion()))

    # Test 3: Multiple ingestion
    results.append(("Multiple Ingestion", test_multiple_smk_ingestion()))

    # Test 4: Relationships
    results.append(("SMK Relationships", test_smk_relationships()))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")

    passed_count = sum(1 for _, passed in results if passed)
    print(f"\n📊 {passed_count}/{len(results)} tests passed")

    return passed_count == len(results)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
