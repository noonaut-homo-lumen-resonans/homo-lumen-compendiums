"""
Test MutationLog Blockchain Integration (GENOMOS Phase 4)

Tests the integration between MutationLog and GENOMOS blockchain:
- Dual persistence (JSONL + Blockchain)
- Migration of historical mutations
- Blockchain validation
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from gates.mutation_log import MutationLog, MutationLevel, ValidationOutcome
from blockchain.agent_dna_chain import AgentDNAChain
from blockchain.dna_block import GeneType


def test_mutationlog_blockchain_integration():
    """Test MutationLog with blockchain enabled"""
    print("\n" + "=" * 60)
    print("TEST 1: MutationLog Blockchain Integration")
    print("=" * 60)

    # Initialize MutationLog with blockchain
    MutationLog.initialize(
        log_file_path="./data/test_mutation_log.jsonl",
        blockchain_db_path="./data/test_genomos_mutations.db"
    )

    print("\n✅ MutationLog initialized with blockchain")

    # Log a test mutation
    entry = MutationLog.log_approved_operation(
        agent="orion",
        operation_type=MutationLevel.WRITE,
        target="/workspace/orion/test.txt",
        action="Create test file for blockchain integration",
        biofelt_resonance="optimal",
        thalos_severity="INFO",
        intent="Test GENOMOS Phase 4",
        justification="Testing MutationLog→Blockchain integration"
    )

    print(f"\n✅ Mutation logged:")
    print(f"   Mutation ID: {entry.mutation_id}")
    print(f"   Agent: {entry.agent}")
    print(f"   Operation: {entry.operation_type.value}")
    print(f"   Success: {entry.success}")

    # Verify blockchain has the mutation
    if MutationLog._blockchain:
        mutation_genes = [
            block for block in MutationLog._blockchain.chain
            if block.gene_type == GeneType.MUTATION
        ]

        print(f"\n✅ Blockchain verification:")
        print(f"   Total genes in chain: {len(MutationLog._blockchain.chain)}")
        print(f"   Mutation genes: {len(mutation_genes)}")

        if mutation_genes:
            latest_mutation = mutation_genes[-1]
            print(f"   Latest mutation block: {latest_mutation.index}")
            print(f"   Agent: {latest_mutation.agent}")
            print(f"   Hash: {latest_mutation.hash[:16]}...")

        # Validate chain
        is_valid = MutationLog._blockchain.validate_chain()
        print(f"   Blockchain valid: {is_valid}")

        return is_valid
    else:
        print("⚠️ Blockchain not available")
        return False


def test_jsonl_migration():
    """Test migration of historical mutations from JSONL to blockchain"""
    print("\n" + "=" * 60)
    print("TEST 2: JSONL → Blockchain Migration")
    print("=" * 60)

    # Check if we have existing mutation_log.jsonl
    jsonl_path = "./data/mutation_log.jsonl"
    if not os.path.exists(jsonl_path):
        print(f"⚠️ No existing JSONL file to migrate: {jsonl_path}")
        return True

    # Initialize fresh blockchain for migration test
    MutationLog.initialize(
        log_file_path=jsonl_path,
        blockchain_db_path="./data/genomos_migrated.db"
    )

    # Run migration
    result = MutationLog.migrate_jsonl_to_blockchain(jsonl_path)

    print(f"\n✅ Migration Result:")
    print(f"   Success: {result['success']}")
    print(f"   Mutations migrated: {result.get('migrated', 0)}")
    print(f"   Errors: {len(result.get('errors', []))}")

    if result.get('blockchain_valid'):
        print(f"   Blockchain valid: {result['blockchain_valid']}")
        print(f"   Total genes: {result.get('total_genes', 0)}")
        print(f"   Merkle root: {result.get('merkle_root', '')[:16]}...")

    if result.get('errors'):
        print(f"\n⚠️ Migration errors:")
        for error in result['errors'][:5]:  # Show first 5 errors
            print(f"   - {error}")

    return result['success']


def test_dual_persistence():
    """Test that mutations are saved to both JSONL and blockchain"""
    print("\n" + "=" * 60)
    print("TEST 3: Dual Persistence (JSONL + Blockchain)")
    print("=" * 60)

    # Initialize with both systems
    MutationLog.initialize(
        log_file_path="./data/test_dual_mutation.jsonl",
        blockchain_db_path="./data/test_dual_blockchain.db"
    )

    # Log 3 different operations
    operations = [
        ("lira", MutationLevel.READ, "/workspace/lira/data.json", "Read user data"),
        ("nyra", MutationLevel.WRITE, "/workspace/nyra/output.png", "Save visualization"),
        ("thalus", MutationLevel.EXECUTE, "/scripts/analyze.py", "Run analysis script"),
    ]

    for agent, op_type, target, action in operations:
        MutationLog.log_approved_operation(
            agent=agent,
            operation_type=op_type,
            target=target,
            action=action,
            biofelt_resonance="balanced",
            thalos_severity="INFO"
        )

    print(f"\n✅ Logged {len(operations)} mutations")

    # Verify JSONL
    jsonl_path = "./data/test_dual_mutation.jsonl"
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        jsonl_lines = f.readlines()

    print(f"   JSONL entries: {len(jsonl_lines)}")

    # Verify Blockchain
    if MutationLog._blockchain:
        mutation_genes = [
            block for block in MutationLog._blockchain.chain
            if block.gene_type == GeneType.MUTATION
        ]
        print(f"   Blockchain mutations: {len(mutation_genes)}")

        # Verify both have same count
        if len(jsonl_lines) == len(mutation_genes):
            print(f"   ✅ Dual persistence verified: {len(jsonl_lines)} entries in both systems")
            return True
        else:
            print(f"   ❌ Mismatch: JSONL={len(jsonl_lines)}, Blockchain={len(mutation_genes)}")
            return False
    else:
        print("⚠️ Blockchain not available")
        return False


def test_blockchain_query():
    """Test querying mutations from blockchain"""
    print("\n" + "=" * 60)
    print("TEST 4: Blockchain Query & Statistics")
    print("=" * 60)

    # Initialize with existing test blockchain
    MutationLog.initialize(
        blockchain_db_path="./data/test_dual_blockchain.db"
    )

    if not MutationLog._blockchain:
        print("⚠️ Blockchain not available")
        return False

    # Get mutation statistics
    mutation_genes = [
        block for block in MutationLog._blockchain.chain
        if block.gene_type == GeneType.MUTATION
    ]

    print(f"\n✅ Blockchain Statistics:")
    print(f"   Total blocks: {len(MutationLog._blockchain.chain)}")
    print(f"   Mutation genes: {len(mutation_genes)}")

    # Group by agent
    by_agent = {}
    for block in mutation_genes:
        agent = block.agent or "unknown"
        by_agent[agent] = by_agent.get(agent, 0) + 1

    print(f"\n   Mutations by agent:")
    for agent, count in sorted(by_agent.items()):
        print(f"   - {agent}: {count}")

    # Validate integrity
    is_valid = MutationLog._blockchain.validate_chain()
    merkle_root = MutationLog._blockchain.get_merkle_root()

    print(f"\n   Blockchain integrity:")
    print(f"   - Valid: {is_valid}")
    print(f"   - Merkle root: {merkle_root[:16]}...")

    return is_valid


def main():
    """Run all tests"""
    print("\n🧬 GENOMOS Phase 4: MutationLog Blockchain Integration Tests")
    print("=" * 60)

    # Ensure Windows UTF-8 encoding
    if sys.platform == 'win32':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass

    results = []

    # Test 1: Basic integration
    results.append(("Blockchain Integration", test_mutationlog_blockchain_integration()))

    # Test 2: Migration
    results.append(("JSONL Migration", test_jsonl_migration()))

    # Test 3: Dual persistence
    results.append(("Dual Persistence", test_dual_persistence()))

    # Test 4: Queries
    results.append(("Blockchain Query", test_blockchain_query()))

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
