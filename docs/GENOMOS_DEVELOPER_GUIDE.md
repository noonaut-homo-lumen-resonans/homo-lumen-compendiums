# GENOMOS Developer Guide

**Version:** 1.0.0
**Last Updated:** 2025-10-29
**Status:** Production-Ready
**Target Audience:** Developers contributing to GENOMOS

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Architecture Overview](#architecture-overview)
4. [Adding New Gene Types](#adding-new-gene-types)
5. [Extending Smart Contracts](#extending-smart-contracts)
6. [Querying the Blockchain](#querying-the-blockchain)
7. [Contributing Patterns](#contributing-patterns)
8. [Backup & Restore](#backup--restore)
9. [Testing](#testing)
10. [Common Patterns](#common-patterns)
11. [Troubleshooting](#troubleshooting)
12. [Contributing Guidelines](#contributing-guidelines)

---

## Introduction

### What is GENOMOS?

**GENOMOS** (Genetic Ontological Memory Operational System) is a blockchain-based immutable memory system for the Homo Lumen Coalition. It treats knowledge as "genetic code" - permanent, verifiable, and inheritable.

### Key Concepts

- **Gene:** A block in the blockchain (e.g., SMK document, mutation, consultation)
- **Genome:** The complete blockchain (all genes linked together)
- **Gene Type:** Category of knowledge (10 types: Genesis, SMK, Mutation, etc.)
- **Smart Contract:** Validation rules (Triadisk Portvokter: BiofeltGate, ThalosFilter, MutationLog)
- **Merkle Root:** Cryptographic fingerprint of entire chain

### Philosophy

> *"If we treat knowledge as DNA, we enable evolutionary epistemology - knowledge that can mutate, recombine, and evolve while maintaining integrity."*

---

## Getting Started

### Prerequisites

- Python 3.13+
- FastAPI
- SQLite
- Git

### Installation

```bash
# Clone repository
cd homo-lumen-compendiums/ubuntu-playground

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from api.blockchain import AgentDNAChain; AgentDNAChain()"

# Start server
uvicorn api.main:app --reload --port 8000
```

### Verify Installation

```bash
# Check blockchain info
curl http://localhost:8000/api/dna/info

# Expected response:
{
  "total_blocks": 1,
  "chain_valid": true,
  "genesis_hash": "633d3f1e...",
  "merkle_root": "..."
}
```

---

## Architecture Overview

### Directory Structure

```
ubuntu-playground/api/
├── blockchain/
│   ├── __init__.py              # Gene types
│   ├── dna_block.py             # Individual gene (block)
│   ├── agent_dna_chain.py       # Complete blockchain
│   ├── genesis.py               # Constitution parsing
│   ├── smk_ingestion.py         # SMK file parser
│   ├── reference_extractor.py   # Knowledge graph
│   ├── consultation_recommender.py  # Similarity scoring
│   ├── advanced_query.py        # Complex queries
│   ├── backup_manager.py        # Backups with SHA-256
│   ├── cache_manager.py         # LRU cache
│   └── smart_contracts/
│       ├── base_contract.py     # Base contract class
│       ├── biofelt_contract.py  # BiofeltGate
│       ├── thalos_contract.py   # ThalosFilter
│       ├── mutation_contract.py # MutationLog
│       └── contract_engine.py   # Contract executor
├── models/
│   ├── knowledge_graph.py       # Graph models
│   └── visualization.py         # Visualization data models
├── routers/
│   └── dna_api.py               # 60+ REST API endpoints
├── data/
│   └── genomos.db               # SQLite database
└── main.py                      # FastAPI app
```

### Data Flow

```
User Request → FastAPI Router → Blockchain Layer → SQLite/Cache → Response
                                      ↓
                              Smart Contracts (validation)
                                      ↓
                              Knowledge Graph (relationships)
```

---

## Adding New Gene Types

### Step 1: Define Gene Type

Edit `blockchain/__init__.py`:

```python
class GeneType(str, Enum):
    # Existing types...
    NEW_TYPE = "new_type"  # Add your gene type
```

### Step 2: Create Helper Function

Edit `blockchain/dna_block.py`:

```python
def create_new_type_gene(
    index: int,
    previous_hash: str,
    data: Dict[str, Any],
    agent: str,
    tags: Optional[List[str]] = None
) -> DNABlock:
    """
    Create a NEW_TYPE gene block.

    Args:
        index: Block index in chain
        previous_hash: Hash of previous block
        data: Your custom data structure
        agent: Agent creating this gene
        tags: Optional tags for filtering

    Returns:
        DNABlock with NEW_TYPE gene
    """
    return DNABlock(
        index=index,
        gene_type=GeneType.NEW_TYPE,
        data=data,
        previous_hash=previous_hash,
        agent=agent,
        tags=tags or []
    )
```

### Step 3: Add API Endpoint

Edit `routers/dna_api.py`:

```python
from pydantic import BaseModel

class NewTypeResponse(BaseModel):
    index: int
    timestamp: str
    data: dict
    block_hash: str

@app.get("/api/dna/new-type", response_model=List[NewTypeResponse])
def get_new_type_genes():
    """Get all NEW_TYPE genes from blockchain."""
    genes = blockchain.get_genes_by_type(GeneType.NEW_TYPE)
    return [
        NewTypeResponse(
            index=gene.index,
            timestamp=gene.timestamp,
            data=gene.data,
            block_hash=gene.block_hash
        )
        for gene in genes
    ]

@app.post("/api/dna/new-type")
def create_new_type_gene(data: dict):
    """Add NEW_TYPE gene to blockchain."""
    block = blockchain.add_gene(
        gene_type=GeneType.NEW_TYPE,
        data=data,
        agent="your-agent-name",
        tags=["new-type", "custom"]
    )
    return {"success": True, "block_index": block.index}
```

### Step 4: Test Your Gene Type

```python
# Test script: test_new_gene_type.py
from blockchain import AgentDNAChain, GeneType

chain = AgentDNAChain()

# Add new gene
block = chain.add_gene(
    gene_type=GeneType.NEW_TYPE,
    data={"key": "value", "metadata": "example"},
    agent="developer",
    tags=["test"]
)

print(f"✅ Gene added: Block #{block.index}")

# Query new genes
genes = chain.get_genes_by_type(GeneType.NEW_TYPE)
print(f"✅ Found {len(genes)} NEW_TYPE genes")

# Validate chain
assert chain.validate_chain()
print(f"✅ Chain valid: {chain.get_merkle_root()}")
```

### Example: Adding "Agent Performance" Gene

```python
# Step 1: Add to GeneType enum
class GeneType(str, Enum):
    # ...
    AGENT_PERFORMANCE = "agent_performance"

# Step 2: Helper function
def create_performance_gene(
    index: int,
    previous_hash: str,
    agent: str,
    metrics: dict
) -> DNABlock:
    return DNABlock(
        index=index,
        gene_type=GeneType.AGENT_PERFORMANCE,
        data={
            "agent": agent,
            "response_time_ms": metrics["response_time"],
            "success_rate": metrics["success_rate"],
            "total_operations": metrics["total_ops"],
            "timestamp": datetime.now().isoformat()
        },
        previous_hash=previous_hash,
        agent=agent,
        tags=["performance", agent]
    )

# Step 3: API endpoint
@app.get("/api/dna/performance/{agent}")
def get_agent_performance(agent: str):
    genes = blockchain.get_genes_by_agent(agent)
    perf_genes = [g for g in genes if g.gene_type == GeneType.AGENT_PERFORMANCE]
    return {"agent": agent, "performance_history": perf_genes}
```

---

## Extending Smart Contracts

### Understanding Triadisk Portvokter

GENOMOS has 3 smart contract layers:

1. **BiofeltGate:** Physiological validation (HRV, stress)
2. **ThalosFilter:** Wisdom validation (SMK references, multi-agent)
3. **MutationLog:** Safety validation (destructive ops, dangerous paths)

### Adding New Contract Rules

#### Example: Add "Time-Based Validation" to BiofeltGate

Edit `blockchain/smart_contracts/biofelt_contract.py`:

```python
class BiofeltGateContract(BaseContract):
    contract_name = "BiofeltGate"
    version = "1.1"  # Increment version

    def validate(self, data: Dict[str, Any]) -> ContractResult:
        violations = []

        # Existing rules (BF-001, BF-002, BF-003)...

        # NEW RULE: BF-004 - Time-based validation
        if "biofelt_context" in data:
            ctx = data["biofelt_context"]
            current_hour = datetime.now().hour

            # Block high-risk operations late at night (11 PM - 5 AM)
            if 23 <= current_hour or current_hour <= 5:
                if ctx.get("operation_risk", "low") == "high":
                    violations.append(ContractViolation(
                        rule="BF-004",
                        message="High-risk operations blocked during night hours (11 PM - 5 AM)",
                        severity="warning",
                        data={"current_hour": current_hour}
                    ))

        return ContractResult(
            valid=len([v for v in violations if v.severity == "error"]) == 0,
            violations=violations,
            metadata={"contract": self.contract_name, "version": self.version}
        )
```

### Creating a New Smart Contract

#### Example: "Resource Limit Contract"

Create `blockchain/smart_contracts/resource_contract.py`:

```python
from .base_contract import BaseContract, ContractResult, ContractViolation
from typing import Dict, Any

class ResourceLimitContract(BaseContract):
    """
    Contract that enforces resource usage limits.

    Rules:
    - RL-001: Memory usage must be < 1GB
    - RL-002: CPU usage must be < 80%
    - RL-003: Disk usage must be < 90%
    """

    contract_name = "ResourceLimit"
    version = "1.0"

    def validate(self, data: Dict[str, Any]) -> ContractResult:
        violations = []

        if "resource_usage" not in data:
            # No resource data = skip validation
            return ContractResult(valid=True, violations=[], metadata={})

        usage = data["resource_usage"]

        # RL-001: Memory limit
        if usage.get("memory_mb", 0) > 1024:
            violations.append(ContractViolation(
                rule="RL-001",
                message=f"Memory usage too high: {usage['memory_mb']}MB > 1024MB",
                severity="error",
                data={"memory_mb": usage["memory_mb"]}
            ))

        # RL-002: CPU limit
        if usage.get("cpu_percent", 0) > 80:
            violations.append(ContractViolation(
                rule="RL-002",
                message=f"CPU usage too high: {usage['cpu_percent']}% > 80%",
                severity="warning",
                data={"cpu_percent": usage["cpu_percent"]}
            ))

        # RL-003: Disk limit
        if usage.get("disk_percent", 0) > 90:
            violations.append(ContractViolation(
                rule="RL-003",
                message=f"Disk usage critical: {usage['disk_percent']}% > 90%",
                severity="error",
                data={"disk_percent": usage["disk_percent"]}
            ))

        return ContractResult(
            valid=len([v for v in violations if v.severity == "error"]) == 0,
            violations=violations,
            metadata={"contract": self.contract_name, "version": self.version}
        )
```

### Register New Contract in Engine

Edit `blockchain/smart_contracts/contract_engine.py`:

```python
from .resource_contract import ResourceLimitContract

class ContractEngine:
    def __init__(self):
        self.contracts: List[BaseContract] = [
            BiofeltGateContract(),
            ThalosFilterContract(),
            MutationLogContract(),
            ResourceLimitContract()  # Add your contract
        ]
```

### Test Your Contract

```python
# test_resource_contract.py
from blockchain.smart_contracts import ContractEngine

engine = ContractEngine()

# Test passing validation
data_ok = {
    "resource_usage": {
        "memory_mb": 512,
        "cpu_percent": 45,
        "disk_percent": 60
    }
}
result = engine.validate_all(data_ok)
assert result["overall_valid"] == True
print("✅ Passed: Resource usage within limits")

# Test failing validation
data_fail = {
    "resource_usage": {
        "memory_mb": 2048,  # > 1024MB
        "cpu_percent": 90,  # > 80%
        "disk_percent": 95  # > 90%
    }
}
result = engine.validate_all(data_fail)
assert result["overall_valid"] == False
print(f"❌ Failed: {result['total_violations']} violations")
for contract in result["contracts"]:
    if contract["contract"] == "ResourceLimit":
        for violation in contract["violations"]:
            print(f"  - {violation['rule']}: {violation['message']}")
```

---

## Querying the Blockchain

### Basic Queries

```python
from blockchain import AgentDNAChain, GeneType

chain = AgentDNAChain()

# 1. Get blockchain info
info = chain.get_chain_info()
print(f"Total blocks: {info['total_blocks']}")
print(f"Chain valid: {chain.validate_chain()}")

# 2. Get genes by type
smk_genes = chain.get_genes_by_type(GeneType.SMK)
print(f"Found {len(smk_genes)} SMK genes")

# 3. Get genes by agent
orion_genes = chain.get_genes_by_agent("orion")
print(f"Orion has {len(orion_genes)} genes")

# 4. Get genes by tag
blockchain_genes = chain.get_genes_by_tag("blockchain")
print(f"Found {len(blockchain_genes)} genes tagged 'blockchain'")

# 5. Get specific block
genesis = chain.get_block_by_index(0)
print(f"Genesis: {genesis.data['title']}")

# 6. Get block by hash
block = chain.get_block_by_hash("633d3f1e...")
print(f"Block #{block.index}: {block.gene_type}")
```

### Advanced Queries

```python
from blockchain.advanced_query import AdvancedQueryBuilder

builder = AdvancedQueryBuilder(chain)

# Complex filter query
results = builder.complex_query(
    gene_types=[GeneType.SMK, GeneType.MUTATION],
    agents=["orion", "lira"],
    date_range=("2025-10-01", "2025-10-31"),
    tags=["blockchain", "genomos"],
    limit=50
)
print(f"Found {len(results)} matching genes")

# Full-text search
search_results = builder.full_text_search(
    query="blockchain DNA",
    gene_types=[GeneType.SMK],
    min_relevance=0.5
)
for result in search_results:
    print(f"  - {result['title']} (relevance: {result['score']})")

# Aggregation query
aggregated = builder.aggregate(
    group_by="gene_type",
    count_field="index",
    filter={"agent": "orion"}
)
print("Gene distribution for Orion:")
for gene_type, count in aggregated.items():
    print(f"  {gene_type}: {count}")
```

### REST API Queries

```bash
# 1. Get all SMK genes
curl http://localhost:8000/api/dna/smk

# 2. Filter by agent
curl http://localhost:8000/api/dna/smk?agent=orion

# 3. Full-text search
curl -X POST http://localhost:8000/api/dna/search \
  -H "Content-Type: application/json" \
  -d '{"query": "blockchain DNA", "min_relevance": 0.5}'

# 4. Complex query
curl -X POST http://localhost:8000/api/dna/query \
  -H "Content-Type: application/json" \
  -d '{
    "gene_types": ["smk", "mutation"],
    "agents": ["orion"],
    "tags": ["blockchain"],
    "limit": 50
  }'

# 5. Aggregation
curl -X POST http://localhost:8000/api/dna/aggregate \
  -H "Content-Type: application/json" \
  -d '{"group_by": "gene_type", "count_field": "index"}'
```

---

## Contributing Patterns

### What are Patterns?

Patterns are discovered regularities in blockchain data (e.g., "HRV drops Monday mornings" or "Lira emphasizes empathy in consultations").

### Detecting Patterns

Create `detect_patterns.py`:

```python
from blockchain import AgentDNAChain, GeneType
from collections import Counter
from datetime import datetime

chain = AgentDNAChain()

# Pattern 1: Agent activity distribution
agents = [gene.agent for gene in chain.get_genes_by_type(GeneType.SMK)]
agent_counts = Counter(agents)
print("Agent Activity Pattern:")
for agent, count in agent_counts.most_common():
    print(f"  {agent}: {count} SMKs")

# Pattern 2: Temporal activity
genes = chain.get_all_blocks()
hour_counts = Counter([
    datetime.fromisoformat(gene.timestamp).hour
    for gene in genes
])
print("\nTemporal Pattern (activity by hour):")
for hour in sorted(hour_counts.keys()):
    print(f"  {hour:02d}:00 - {hour_counts[hour]} genes")

# Pattern 3: Tag co-occurrence
all_tags = []
for gene in genes:
    all_tags.extend(gene.tags)
tag_counts = Counter(all_tags)
print("\nTag Pattern:")
for tag, count in tag_counts.most_common(10):
    print(f"  {tag}: {count} occurrences")
```

### Storing Patterns as Genes

```python
# Store discovered pattern
pattern_data = {
    "pattern_id": "P001",
    "pattern_type": "agent_activity",
    "description": "Orion contributes most SMK genes (12/15 = 80%)",
    "confidence": 0.92,
    "data": {"orion": 12, "lira": 2, "manus": 1},
    "discovered_at": datetime.now().isoformat()
}

pattern_block = chain.add_gene(
    gene_type=GeneType.PATTERN,
    data=pattern_data,
    agent="pattern-detector",
    tags=["pattern", "agent-activity"]
)

print(f"✅ Pattern stored as Block #{pattern_block.index}")
```

### Querying Patterns

```python
# Get all discovered patterns
patterns = chain.get_genes_by_type(GeneType.PATTERN)
print(f"Found {len(patterns)} patterns")

for pattern in patterns:
    data = pattern.data
    print(f"Pattern {data['pattern_id']}: {data['description']}")
    print(f"  Confidence: {data['confidence']}")
    print(f"  Type: {data['pattern_type']}")
```

---

## Backup & Restore

### Creating Backups

```python
from blockchain import AgentDNAChain
from blockchain.backup_manager import BackupManager

chain = AgentDNAChain()
backup_mgr = BackupManager()

# Create backup with SHA-256 verification
backup_info = backup_mgr.create_backup(chain)

print(f"✅ Backup created:")
print(f"  Path: {backup_info['backup_path']}")
print(f"  SHA-256: {backup_info['hash']}")
print(f"  Size: {backup_info['size_bytes']} bytes")
print(f"  Blocks: {backup_info['block_count']}")
```

### Verifying Backups

```python
# Verify backup integrity
result = backup_mgr.verify_backup("backups/genomos_backup_20251029_091326.json")

if result["valid"]:
    print("✅ Backup verified: SHA-256 match")
else:
    print("❌ Backup corrupted: Hash mismatch")
    print(f"  Expected: {result['stored_hash']}")
    print(f"  Got: {result['calculated_hash']}")
```

### Restoring from Backup

```python
# Restore chain from backup
chain.import_chain("backups/genomos_backup_20251029_091326.json")

# Verify restored chain
assert chain.validate_chain()
print(f"✅ Chain restored: {len(chain.chain)} blocks")
print(f"  Merkle root: {chain.get_merkle_root()}")
```

### Automated Backup Schedule

Create `backup_scheduler.py`:

```python
import schedule
import time
from blockchain import AgentDNAChain
from blockchain.backup_manager import BackupManager

chain = AgentDNAChain()
backup_mgr = BackupManager()

def backup_job():
    """Run backup and print result."""
    try:
        info = backup_mgr.create_backup(chain)
        print(f"✅ Backup created: {info['backup_path']}")
    except Exception as e:
        print(f"❌ Backup failed: {str(e)}")

# Schedule backups every day at 2 AM
schedule.every().day.at("02:00").do(backup_job)

print("Backup scheduler started (daily at 2 AM)")
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
```

### REST API Backup

```bash
# Create backup via API
curl -X POST http://localhost:8000/api/dna/backup/create

# Response:
{
  "backup_path": "backups/genomos_backup_20251029_091326.json",
  "hash": "a3f7c9e2...",
  "size_bytes": 87234,
  "block_count": 20
}

# Verify backup via API
curl -X POST http://localhost:8000/api/dna/backup/verify \
  -H "Content-Type: application/json" \
  -d '{"backup_path": "backups/genomos_backup_20251029_091326.json"}'

# Response:
{
  "valid": true,
  "calculated_hash": "a3f7c9e2...",
  "stored_hash": "a3f7c9e2..."
}
```

---

## Testing

### Unit Tests

Create `tests/test_new_feature.py`:

```python
import pytest
from blockchain import AgentDNAChain, GeneType

@pytest.fixture
def chain():
    """Fixture: Fresh blockchain for each test."""
    return AgentDNAChain(db_path=":memory:")  # In-memory for speed

def test_add_gene(chain):
    """Test adding gene to chain."""
    block = chain.add_gene(
        gene_type=GeneType.SMK,
        data={"title": "Test SMK"},
        agent="test-agent"
    )
    assert block.index == 1  # Genesis = 0, this = 1
    assert block.gene_type == GeneType.SMK
    assert chain.validate_chain()

def test_query_by_type(chain):
    """Test querying genes by type."""
    chain.add_gene(GeneType.SMK, {"title": "SMK 1"}, "agent1")
    chain.add_gene(GeneType.SMK, {"title": "SMK 2"}, "agent2")
    chain.add_gene(GeneType.MUTATION, {"op": "write"}, "agent1")

    smks = chain.get_genes_by_type(GeneType.SMK)
    assert len(smks) == 2

    mutations = chain.get_genes_by_type(GeneType.MUTATION)
    assert len(mutations) == 1

def test_chain_validation(chain):
    """Test chain integrity after multiple additions."""
    for i in range(10):
        chain.add_gene(GeneType.SMK, {"n": i}, "agent")

    assert chain.validate_chain()
    assert len(chain.chain) == 11  # Genesis + 10
```

### Integration Tests

Create `tests/test_integration.py`:

```python
import pytest
import requests

BASE_URL = "http://localhost:8000"

def test_full_workflow():
    """Test complete workflow: add gene → query → verify."""

    # 1. Add gene via API
    response = requests.post(f"{BASE_URL}/api/dna/smk", json={
        "smk_number": "999",
        "title": "Integration Test SMK",
        "agent": "test-agent"
    })
    assert response.status_code == 200
    block_index = response.json()["block_index"]

    # 2. Query gene via API
    response = requests.get(f"{BASE_URL}/api/dna/smk/999")
    assert response.status_code == 200
    smk = response.json()
    assert smk["title"] == "Integration Test SMK"

    # 3. Validate chain via API
    response = requests.get(f"{BASE_URL}/api/dna/validate")
    assert response.status_code == 200
    assert response.json()["valid"] == True
```

### Running Tests

```bash
# Install pytest
pip install pytest pytest-cov

# Run all tests
pytest tests/

# Run with coverage
pytest --cov=blockchain --cov-report=html tests/

# Run specific test file
pytest tests/test_new_feature.py

# Run specific test function
pytest tests/test_new_feature.py::test_add_gene
```

---

## Common Patterns

### Pattern 1: Add Gene with Validation

```python
from blockchain import AgentDNAChain, GeneType
from blockchain.smart_contracts import ContractEngine

chain = AgentDNAChain()
engine = ContractEngine()

# Validate data before adding
data = {
    "biofelt_context": {"hrv_ms": 75, "stress_level": 3},
    "mutation": {"operation": "write", "target": "code.py"}
}

validation = engine.validate_all(data)

if validation["overall_valid"]:
    # Add gene if validation passes
    block = chain.add_gene(
        gene_type=GeneType.MUTATION,
        data=data["mutation"],
        agent="developer"
    )
    print(f"✅ Gene added: Block #{block.index}")
else:
    # Log violations
    print(f"❌ Validation failed: {validation['total_violations']} violations")
    for contract in validation["contracts"]:
        for violation in contract["violations"]:
            print(f"  - {violation['rule']}: {violation['message']}")
```

### Pattern 2: Paginated Query

```python
def get_genes_paginated(gene_type: GeneType, page: int = 1, per_page: int = 10):
    """Get genes with pagination."""
    all_genes = chain.get_genes_by_type(gene_type)
    start = (page - 1) * per_page
    end = start + per_page
    return {
        "genes": all_genes[start:end],
        "page": page,
        "per_page": per_page,
        "total": len(all_genes),
        "total_pages": (len(all_genes) + per_page - 1) // per_page
    }

# Usage
result = get_genes_paginated(GeneType.SMK, page=1, per_page=5)
print(f"Showing {len(result['genes'])} of {result['total']} SMKs")
```

### Pattern 3: Cache-Aside

```python
from blockchain.cache_manager import CacheManager

cache = CacheManager(ttl_seconds=300)

def get_gene_cached(gene_type: GeneType, use_cache: bool = True):
    """Get genes with cache-aside pattern."""
    cache_key = f"genes:{gene_type}"

    if use_cache:
        # Try cache first
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

    # Cache miss - query blockchain
    genes = chain.get_genes_by_type(gene_type)

    # Store in cache
    cache.set(cache_key, genes)

    return genes
```

---

## Troubleshooting

### Chain Validation Fails

```python
# Symptom: chain.validate_chain() returns False

# Debug: Check each block
for i, block in enumerate(chain.chain):
    if i == 0:
        continue  # Skip genesis

    prev_block = chain.chain[i - 1]
    if block.previous_hash != prev_block.block_hash:
        print(f"❌ Block #{i} has invalid previous_hash")
        print(f"  Expected: {prev_block.block_hash}")
        print(f"  Got: {block.previous_hash}")
        break

    # Recalculate hash
    calculated_hash = block.calculate_hash()
    if calculated_hash != block.block_hash:
        print(f"❌ Block #{i} has invalid hash")
        print(f"  Expected: {block.block_hash}")
        print(f"  Got: {calculated_hash}")
        break
```

### Database Locked Error

```python
# Symptom: "sqlite3.OperationalError: database is locked"

# Solution: Close existing connections
import sqlite3

# Check open connections
connections = sqlite3.connect(chain.db_path)
connections.close()

# Or: Use WAL mode (Write-Ahead Logging)
conn = sqlite3.connect(chain.db_path)
conn.execute("PRAGMA journal_mode=WAL")
conn.close()
```

### Cache Not Invalidating

```python
# Symptom: Stale data returned from cache

# Solution: Invalidate cache after chain modifications
chain.add_gene(...)  # Modify chain

# Invalidate related caches
cache.invalidate_pattern("dna/blocks/*")
cache.invalidate_pattern("dna/smk")
cache.invalidate_pattern("dna/analytics/*")
```

### Memory Usage Growing

```python
# Symptom: High memory usage with large chains

# Solution: Use pagination + generators
def get_genes_generator(gene_type: GeneType):
    """Generator to yield genes one at a time."""
    conn = sqlite3.connect(chain.db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM dna_blocks WHERE gene_type = ?",
        (gene_type,)
    )

    for row in cursor:
        yield DNABlock.from_db_row(row)

    conn.close()

# Usage (doesn't load all into memory)
for gene in get_genes_generator(GeneType.SMK):
    process(gene)
```

---

## Contributing Guidelines

### Code Style

- **Python:** PEP 8 (use `black` formatter)
- **Docstrings:** Google style
- **Type Hints:** Required for all functions

```python
from typing import List, Dict, Optional

def example_function(
    param1: str,
    param2: int,
    optional: Optional[Dict] = None
) -> List[str]:
    """
    Short description of function.

    Args:
        param1: Description of param1
        param2: Description of param2
        optional: Description of optional param

    Returns:
        List of strings with results

    Raises:
        ValueError: If param2 is negative
    """
    if param2 < 0:
        raise ValueError("param2 must be non-negative")

    return [param1] * param2
```

### Testing Requirements

- **Unit Tests:** Required for all new functions
- **Coverage:** Minimum 80%
- **Integration Tests:** Required for API endpoints

### Git Workflow

```bash
# 1. Create feature branch
git checkout -b feature/new-gene-type

# 2. Make changes
# ... edit files ...

# 3. Run tests
pytest tests/

# 4. Commit
git add .
git commit -m "feat: Add NEW_TYPE gene support

- Add GeneType.NEW_TYPE to enum
- Create helper function create_new_type_gene()
- Add API endpoint GET /api/dna/new-type
- Add tests (coverage: 85%)"

# 5. Push
git push origin feature/new-gene-type

# 6. Create PR
# ... via GitHub UI ...
```

### Commit Message Format

```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions/changes
- `refactor`: Code refactoring
- `perf`: Performance improvements

**Example:**
```
feat: Add ResourceLimitContract for memory/CPU validation

- Implement RL-001 (memory < 1GB)
- Implement RL-002 (CPU < 80%)
- Implement RL-003 (disk < 90%)
- Add tests (100% coverage)
- Update ContractEngine to include new contract

Related: SMK#042, LP#084
```

### Review Checklist

- [ ] Code follows PEP 8
- [ ] Type hints added
- [ ] Docstrings added (Google style)
- [ ] Tests added (coverage ≥ 80%)
- [ ] Tests pass (`pytest tests/`)
- [ ] Chain validation passes after changes
- [ ] Documentation updated (if needed)
- [ ] Commit messages follow format

---

## Additional Resources

### Documentation

- [SMK#042: GENOMOS Technical Documentation](../SMK/SMK#042_GENOMOS-Agent-DNA-Blockchain-Complete-System.md)
- [CODE_LK_V1725: Learning Points #083-090](../CODE_LK_V1725_UPDATE.md)
- [GENOMOS API Documentation](./GENOMOS_API_DOCUMENTATION.md)

### Related SMKs

- [SMK#019: Constitution V1.1](../SMK/SMK#019-CONSTITUTIONV1.md)
- [SMK#040: Triadiske Portvokter](../SMK/SMK#040_TriadiskePortvokter-CompleteImplementation.md)
- [SMK#043: GENOMOS Phase 3](../SMK/SMK#043_GENOMOS-Phase3-SMK-Ingestion-DNA-Blockchain.md)

### Code Examples

- `ubuntu-playground/api/tests/test_genomos_comprehensive.py` - 26 comprehensive tests
- `ubuntu-playground/api/blockchain/` - Complete implementation
- `ubuntu-playground/api/routers/dna_api.py` - API examples

---

**Questions or Issues?**

Open an issue in the repository or contact the Homo Lumen Coalition.

---

*"The genome is the collective memory - permanent, queryable, verifiable, evolutionary"*
— GENOMOS Developer Guide v1.0.0
