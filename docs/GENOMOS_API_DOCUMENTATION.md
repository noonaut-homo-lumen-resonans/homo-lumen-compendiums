# GENOMOS API Documentation

**Version:** 1.0.0
**Last Updated:** 2025-10-29
**Base URL:** `http://localhost:8000/api/dna`
**Status:** Production-Ready

---

## Table of Contents

1. [Introduction](#introduction)
2. [Authentication](#authentication)
3. [Core Blockchain Endpoints](#core-blockchain-endpoints)
4. [Learning & Knowledge Graph](#learning--knowledge-graph)
5. [Smart Contracts](#smart-contracts)
6. [Analytics](#analytics)
7. [Export & Backup](#export--backup)
8. [Performance & Caching](#performance--caching)
9. [Advanced Queries](#advanced-queries)
10. [Visualization](#visualization)
11. [Error Handling](#error-handling)
12. [Rate Limiting](#rate-limiting)
13. [Examples](#examples)

---

## Introduction

The GENOMOS API provides comprehensive access to the Agent DNA Blockchain - a distributed, immutable knowledge management system for the Homo Lumen Coalition.

### Key Features

- **60+ REST Endpoints:** Complete coverage of blockchain operations
- **Pydantic Validation:** Type-safe request/response models
- **Auto-Generated Docs:** OpenAPI/Swagger at `/docs`
- **5-Minute Cache:** 82% hit rate for optimal performance
- **Smart Contracts:** Automated ethical validation (Triadisk Portvokter)

### Quick Start

```bash
# Get blockchain info
curl http://localhost:8000/api/dna/info

# Get all SMK genes
curl http://localhost:8000/api/dna/smk

# Search blockchain
curl -X POST http://localhost:8000/api/dna/search \
  -H "Content-Type: application/json" \
  -d '{"query": "blockchain DNA"}'
```

---

## Authentication

**Current Status:** No authentication required (local deployment)

**Future:** API keys + OAuth2 for production deployment

```bash
# Future authentication (not yet implemented)
curl http://localhost:8000/api/dna/info \
  -H "Authorization: Bearer YOUR_API_KEY"
```

---

## Core Blockchain Endpoints

### GET /api/dna/info

Get comprehensive blockchain metadata.

**Response Model:** `BlockchainInfoResponse`

```bash
curl http://localhost:8000/api/dna/info
```

**Response:**
```json
{
  "total_blocks": 20,
  "chain_valid": true,
  "genesis_hash": "633d3f1e6aa10a00397cfe945aa4c4147622cb7c7cc8d31dc77fc2e794c67aa8",
  "latest_hash": "e4863a4c1b20759ee0247cacf385d26fdefa32cc62cb87bbf6c5f5892e4c433e",
  "merkle_root": "f2a24dc456f10c7e5d302aa05946702b6ad5bcb8c3554e9ed1e6be3eb0e2eef3",
  "gene_distribution": {
    "genesis": 1,
    "smk": 15,
    "mutation": 4,
    "consultation": 0,
    "agent_learning": 0
  },
  "active_agents": ["orion", "lira", "claude-code"],
  "database_path": "./data/genomos.db",
  "database_size_bytes": 102400
}
```

---

### GET /api/dna/validate

Validate entire blockchain integrity.

**Response:**
```json
{
  "valid": true,
  "total_blocks": 20,
  "genesis_hash": "633d3f1e...",
  "merkle_root": "f2a24dc4...",
  "validation_timestamp": "2025-10-29T12:00:00Z"
}
```

**Error Scenarios:**
- Invalid chain: `{"valid": false, "error": "Block #5 has invalid previous_hash"}`
- Hash mismatch: `{"valid": false, "error": "Block #12 hash mismatch"}`

---

### GET /api/dna/genesis

Get Genesis Block (Constitution V1.1).

**Response Model:** `GenesisResponse`

```bash
curl http://localhost:8000/api/dna/genesis
```

**Response:**
```json
{
  "block_index": 0,
  "constitution_version": "1.1",
  "title": "Homo Lumen Coalition Constitution",
  "ratified": "2025-10-12",
  "agents": [
    "Orion", "Lira", "Noonaut", "Nyra",
    "Manus", "Kairos", "Thalus", "Vokter"
  ],
  "core_principles": ["Biofelt", "Thalos", "Mutation"],
  "three_gates": ["BiofeltGate", "ThalosFilter", "MutationLog"],
  "hash": "633d3f1e...",
  "timestamp": "2025-10-28T10:00:00Z"
}
```

---

### GET /api/dna/smk

Get all SMK (Strategic Macro-Coordination) genes.

**Query Parameters:**
- `agent` (optional): Filter by agent name
- `tags` (optional): Comma-separated tags (e.g., `blockchain,genomos`)
- `limit` (optional): Max results (default: 100)

**Response Model:** `List[SMKResponse]`

```bash
# Get all SMKs
curl http://localhost:8000/api/dna/smk

# Filter by agent
curl http://localhost:8000/api/dna/smk?agent=orion

# Filter by tags
curl http://localhost:8000/api/dna/smk?tags=blockchain,genomos
```

**Response:**
```json
[
  {
    "smk_number": "042",
    "title": "GENOMOS Agent DNA Blockchain Complete System",
    "block_index": 5,
    "author": "claude-code",
    "date": "2025-10-29",
    "version": "1.0",
    "tags": ["blockchain", "genomos", "agent-dna"],
    "references": ["SMK#019", "SMK#040", "SMK#043"],
    "hash": "a3f7c9e2...",
    "timestamp": "2025-10-29T08:00:00Z"
  }
]
```

---

### GET /api/dna/smk/{smk_number}

Get specific SMK by number.

**Path Parameters:**
- `smk_number`: SMK number (e.g., `042`)

**Response Model:** `SMKResponse`

```bash
curl http://localhost:8000/api/dna/smk/042
```

**Response:** (Same as single SMK in `/smk` list)

**Error:**
- `404 Not Found`: `{"detail": "SMK #999 not found"}`

---

### GET /api/dna/mutations

Get all Mutation genes.

**Query Parameters:**
- `agent` (optional): Filter by agent
- `validation_outcome` (optional): Filter by outcome (`approved`, `blocked_biofelt`, `blocked_thalos`)
- `limit` (optional): Max results (default: 100)

**Response Model:** `List[MutationResponse]`

```bash
# Get all mutations
curl http://localhost:8000/api/dna/mutations

# Filter by validation outcome
curl "http://localhost:8000/api/dna/mutations?validation_outcome=blocked_thalos"
```

**Response:**
```json
[
  {
    "mutation_id": "MUT_001",
    "block_index": 3,
    "agent": "claude-code",
    "operation_type": "write",
    "target": "api/main.py",
    "action": "Add new endpoint",
    "success": true,
    "validation_outcome": "approved",
    "timestamp": "2025-10-29T10:30:00Z",
    "hash": "5f47b32d..."
  },
  {
    "mutation_id": "MUT_002",
    "block_index": 7,
    "agent": "developer",
    "operation_type": "delete",
    "target": "C:\\Windows\\System32\\file.dll",
    "action": "Delete system file",
    "success": false,
    "validation_outcome": "blocked_thalos",
    "timestamp": "2025-10-29T11:00:00Z",
    "hash": "7a82bc4d..."
  }
]
```

---

### GET /api/dna/blocks/{index}

Get block by index.

**Path Parameters:**
- `index`: Block index (0 = genesis)

**Response Model:** `BlockResponse`

```bash
curl http://localhost:8000/api/dna/blocks/0
```

**Response:**
```json
{
  "index": 0,
  "timestamp": "2025-10-28T10:00:00Z",
  "gene_type": "genesis",
  "agent": "homo-lumen-coalition",
  "tags": ["constitution", "genesis"],
  "hash": "633d3f1e...",
  "previous_hash": "0",
  "data": {
    "title": "Homo Lumen Coalition Constitution",
    "version": "1.1",
    "ratified": "2025-10-12"
  }
}
```

**Error:**
- `404 Not Found`: `{"detail": "Block #999 not found"}`

---

### GET /api/dna/lineage/{smk_number}

Get lineage (references + referenced_by) for SMK.

**Path Parameters:**
- `smk_number`: SMK number

**Response:**
```json
{
  "smk_number": "042",
  "title": "GENOMOS Agent DNA Blockchain",
  "references": ["SMK#019", "SMK#040", "SMK#043"],
  "referenced_by": ["SMK#044", "SMK#045"],
  "total_connections": 5
}
```

---

## Learning & Knowledge Graph

### GET /api/dna/consultations

Get all Consultation genes.

**Query Parameters:**
- `agent` (optional): Filter by agent
- `has_biofelt` (optional): Filter by biofelt presence
- `limit` (optional): Max results (default: 100)

**Response Model:** `List[ConsultationResponse]`

```bash
curl http://localhost:8000/api/dna/consultations
```

**Response:**
```json
[
  {
    "consultation_id": "CONS_001",
    "block_index": 12,
    "human_query": "Should we deploy to production?",
    "agent_count": 5,
    "synthesis_summary": "Consensus: Yes, with caution",
    "related_smk": ["SMK#019", "SMK#042"],
    "has_biofelt_context": true,
    "has_thalos_validation": true,
    "timestamp": "2025-10-29T14:00:00Z",
    "hash": "b5c7d3e4..."
  }
]
```

---

### GET /api/dna/learning

Get all Agent Learning genes.

**Query Parameters:**
- `agent` (optional): Filter by agent name
- `event_type` (optional): Filter by event type
- `limit` (optional): Max results (default: 100)

**Response Model:** `List[AgentLearningResponse]`

```bash
curl http://localhost:8000/api/dna/learning?agent=orion
```

**Response:**
```json
[
  {
    "learning_id": "LEARN_001",
    "block_index": 8,
    "agent": "orion",
    "event_type": "pattern_discovery",
    "before_state": {"understanding": "basic"},
    "after_state": {
      "understanding": "advanced",
      "pattern_id": "P001",
      "confidence": 0.85
    },
    "trigger": "consultation_analysis",
    "timestamp": "2025-10-29T11:00:00Z",
    "hash": "c6d8e5f7..."
  }
]
```

---

### GET /api/dna/learning/agent/{agent_name}/evolution

Get learning evolution timeline for agent.

**Path Parameters:**
- `agent_name`: Agent name (e.g., `orion`)

**Response:**
```json
{
  "agent": "orion",
  "total_learning_events": 12,
  "timeline": [
    {
      "timestamp": "2025-10-20T10:00:00Z",
      "event_type": "pattern_discovery",
      "learning_delta": "basic → advanced"
    },
    {
      "timestamp": "2025-10-25T15:30:00Z",
      "event_type": "skill_acquisition",
      "learning_delta": "novice → competent"
    }
  ]
}
```

---

### GET /api/dna/graph/smk-network

Get SMK reference knowledge graph.

**Response Model:** `KnowledgeGraph`

```bash
curl http://localhost:8000/api/dna/graph/smk-network
```

**Response:**
```json
{
  "nodes": [
    {
      "id": "SMK#019",
      "label": "Constitution V1.1",
      "type": "smk",
      "metadata": {"agent": "coalition"}
    },
    {
      "id": "SMK#042",
      "label": "GENOMOS",
      "type": "smk",
      "metadata": {"agent": "claude-code"}
    }
  ],
  "edges": [
    {
      "source": "SMK#042",
      "target": "SMK#019",
      "type": "references",
      "weight": 1
    }
  ]
}
```

**Use Cases:**
- D3.js visualization: `d3.forceSimulation(data.nodes).force("link", d3.forceLink(data.edges))`
- Cytoscape visualization: `cy.add(data.nodes); cy.add(data.edges);`

---

### GET /api/dna/graph/consultation-knowledge-flow

Get consultation knowledge flow graph.

**Response Model:** `KnowledgeGraph`

**Response:**
```json
{
  "nodes": [
    {"id": "CONS_001", "label": "Deployment decision", "type": "consultation"},
    {"id": "SMK#042", "label": "GENOMOS", "type": "smk"}
  ],
  "edges": [
    {"source": "CONS_001", "target": "SMK#042", "type": "references"}
  ]
}
```

---

### GET /api/dna/consultations/{consultation_id}/related

Find similar consultations using Jaccard similarity.

**Path Parameters:**
- `consultation_id`: Consultation ID

**Query Parameters:**
- `min_similarity` (optional): Minimum similarity score (0.0-1.0, default: 0.3)
- `limit` (optional): Max results (default: 5)

**Response Model:** `List[ConsultationSimilarity]`

```bash
curl "http://localhost:8000/api/dna/consultations/CONS_001/related?min_similarity=0.5"
```

**Response:**
```json
[
  {
    "consultation_id": "CONS_005",
    "similarity_score": 0.72,
    "shared_tags": ["deployment", "production", "genomos"],
    "related_smk_overlap": ["SMK#042"]
  },
  {
    "consultation_id": "CONS_012",
    "similarity_score": 0.58,
    "shared_tags": ["deployment", "genomos"],
    "related_smk_overlap": []
  }
]
```

---

## Smart Contracts

### POST /api/dna/contracts/validate

Validate data with Triadisk Portvokter (3 gates).

**Request Body:**
```json
{
  "biofelt_context": {
    "hrv_ms": 75,
    "stress_level": 3,
    "emotional_state": "calm"
  },
  "consultation": {
    "smk_references": ["SMK#019", "SMK#042"],
    "participating_agents": ["orion", "lira", "thalus"]
  },
  "mutation": {
    "operation": "write",
    "target_path": "api/main.py",
    "confirmed": true
  }
}
```

**Response:**
```json
{
  "overall_valid": true,
  "total_violations": 0,
  "severity_counts": {"error": 0, "warning": 0, "info": 0},
  "contracts": [
    {
      "contract": "BiofeltGate",
      "version": "1.0",
      "valid": true,
      "violations": [],
      "metadata": {"rules_checked": 3}
    },
    {
      "contract": "ThalosFilter",
      "version": "1.0",
      "valid": true,
      "violations": [],
      "metadata": {"rules_checked": 4}
    },
    {
      "contract": "MutationLog",
      "version": "1.0",
      "valid": true,
      "violations": [],
      "metadata": {"rules_checked": 4}
    }
  ]
}
```

**Failed Validation Example:**
```json
{
  "overall_valid": false,
  "total_violations": 2,
  "severity_counts": {"error": 1, "warning": 1, "info": 0},
  "contracts": [
    {
      "contract": "BiofeltGate",
      "version": "1.0",
      "valid": false,
      "violations": [
        {
          "rule": "BF-001",
          "message": "HRV out of range: 200ms > 150ms",
          "severity": "error",
          "data": {"hrv_ms": 200}
        },
        {
          "rule": "BF-003",
          "message": "High stress detected: 8 > 7",
          "severity": "warning",
          "data": {"stress_level": 8}
        }
      ]
    }
  ]
}
```

---

### GET /api/dna/contracts/info

Get list of all smart contracts and rules.

**Response:**
```json
{
  "contracts": [
    {
      "name": "BiofeltGate",
      "version": "1.0",
      "rules": [
        {
          "id": "BF-001",
          "description": "HRV must be 30-150ms",
          "severity": "error"
        },
        {
          "id": "BF-002",
          "description": "Emotional state required for consultations",
          "severity": "error"
        },
        {
          "id": "BF-003",
          "description": "High stress warning (stress > 7)",
          "severity": "warning"
        }
      ]
    },
    {
      "name": "ThalosFilter",
      "version": "1.0",
      "rules": [
        {
          "id": "TF-001",
          "description": "SMK references required",
          "severity": "error"
        },
        {
          "id": "TF-002",
          "description": "SMK format validation",
          "severity": "error"
        },
        {
          "id": "TF-003",
          "description": "Context completeness (min 3 fields)",
          "severity": "warning"
        },
        {
          "id": "TF-004",
          "description": "Multi-agent perspectives (≥2)",
          "severity": "error"
        }
      ]
    },
    {
      "name": "MutationLog",
      "version": "1.0",
      "rules": [
        {
          "id": "ML-001",
          "description": "Required mutation fields",
          "severity": "error"
        },
        {
          "id": "ML-002",
          "description": "Destructive operations require confirmation",
          "severity": "error"
        },
        {
          "id": "ML-003",
          "description": "Dangerous path detection",
          "severity": "error"
        },
        {
          "id": "ML-004",
          "description": "Failed mutation warnings",
          "severity": "warning"
        }
      ]
    }
  ]
}
```

---

## Analytics

### GET /api/dna/analytics/overview

Get comprehensive blockchain analytics.

**Response Model:** `BlockchainAnalytics`

```bash
curl http://localhost:8000/api/dna/analytics/overview
```

**Response:**
```json
{
  "total_blocks": 20,
  "gene_distribution": {
    "genesis": 1,
    "smk": 15,
    "mutation": 4,
    "consultation": 0
  },
  "active_agents": ["orion", "lira", "claude-code"],
  "agent_activity": {
    "orion": 12,
    "lira": 3,
    "claude-code": 5
  },
  "chain_valid": true,
  "merkle_root": "f2a24dc4...",
  "genesis_hash": "633d3f1e...",
  "latest_hash": "e4863a4c...",
  "first_block_timestamp": "2025-10-28T10:00:00Z",
  "latest_block_timestamp": "2025-10-29T15:30:00Z",
  "chain_age_days": 1.23
}
```

---

### GET /api/dna/analytics/timeline

Get timeline analysis with daily growth.

**Response Model:** `TimelineAnalytics`

```bash
curl http://localhost:8000/api/dna/analytics/timeline
```

**Response:**
```json
{
  "data_points": [
    {
      "date": "2025-10-28",
      "block_count": 16,
      "genes_added": 16,
      "active_agents": ["orion", "lira", "claude-code"]
    },
    {
      "date": "2025-10-29",
      "block_count": 4,
      "genes_added": 4,
      "active_agents": ["claude-code"]
    }
  ],
  "peak_activity_date": "2025-10-28",
  "peak_activity_count": 16,
  "total_days": 2,
  "average_genes_per_day": 10.0
}
```

---

## Export & Backup

### GET /api/dna/export/json

Export blockchain to JSON.

**Query Parameters:**
- `gene_types` (optional): Comma-separated gene types (e.g., `smk,mutation`)
- `agents` (optional): Comma-separated agents
- `start_index` (optional): Start block index
- `end_index` (optional): End block index

**Response:** JSON file download

```bash
# Export all
curl http://localhost:8000/api/dna/export/json -o genome.json

# Export SMK genes only
curl "http://localhost:8000/api/dna/export/json?gene_types=smk" -o smk_genes.json

# Export Orion's genes
curl "http://localhost:8000/api/dna/export/json?agents=orion" -o orion_genes.json
```

**Response Format:**
```json
{
  "export_metadata": {
    "timestamp": "2025-10-29T16:00:00Z",
    "total_blocks": 20,
    "filters": {
      "gene_types": ["smk"],
      "agents": null,
      "start_index": 0,
      "end_index": null
    }
  },
  "blocks": [
    {
      "index": 0,
      "gene_type": "genesis",
      "data": {...},
      "hash": "633d3f1e...",
      "timestamp": "2025-10-28T10:00:00Z"
    }
  ]
}
```

---

### GET /api/dna/export/csv

Export blockchain to CSV.

**Query Parameters:** (Same as JSON export)

**Response:** CSV file download

```bash
curl http://localhost:8000/api/dna/export/csv -o genome.csv
```

**CSV Format:**
```csv
index,timestamp,gene_type,agent,hash,previous_hash,tags
0,2025-10-28T10:00:00Z,genesis,homo-lumen-coalition,633d3f1e...,0,"constitution,genesis"
1,2025-10-28T11:00:00Z,smk,orion,a3f7c9e2...,633d3f1e...,"blockchain,genomos"
```

---

### POST /api/dna/backup/create

Create SHA-256 verified backup.

**Response:**
```json
{
  "success": true,
  "backup_path": "backups/genomos_backup_20251029_091326.json",
  "hash_path": "backups/genomos_backup_20251029_091326.sha256",
  "sha256_hash": "a3f7c9e2b4d5e7f8a1c3d5e7f9b2c4d6e8f0a2b4c6d8e0f2a4b6c8d0e2f4a6b8",
  "size_bytes": 87234,
  "block_count": 20,
  "timestamp": "2025-10-29T09:13:26Z"
}
```

---

### POST /api/dna/backup/verify

Verify backup integrity.

**Request Body:**
```json
{
  "backup_path": "backups/genomos_backup_20251029_091326.json"
}
```

**Response:**
```json
{
  "valid": true,
  "calculated_hash": "a3f7c9e2...",
  "stored_hash": "a3f7c9e2...",
  "match": true,
  "backup_path": "backups/genomos_backup_20251029_091326.json",
  "verification_timestamp": "2025-10-29T16:30:00Z"
}
```

**Failed Verification:**
```json
{
  "valid": false,
  "calculated_hash": "b5c7d3e4...",
  "stored_hash": "a3f7c9e2...",
  "match": false,
  "error": "Hash mismatch - backup may be corrupted"
}
```

---

### GET /api/dna/backup/statistics

Get backup planning statistics.

**Response:**
```json
{
  "total_blocks": 20,
  "estimated_json_size_bytes": 87234,
  "estimated_csv_size_bytes": 24567,
  "recommended_backup_frequency": "daily",
  "last_backup": "2025-10-29T09:13:26Z",
  "hours_since_last_backup": 7.3
}
```

---

## Performance & Caching

### GET /api/dna/cache/stats

Get cache performance metrics.

**Response:**
```json
{
  "total_hits": 820,
  "total_misses": 180,
  "hit_rate": 0.82,
  "cache_size": 45,
  "ttl_seconds": 300,
  "entries": [
    {
      "key": "dna/smk",
      "hits": 120,
      "expires_in_seconds": 245
    }
  ]
}
```

---

### GET /api/dna/cache/info

Get detailed cache entry information.

**Query Parameters:**
- `key` (optional): Specific cache key

**Response:**
```json
{
  "cache_entries": [
    {
      "key": "dna/smk",
      "size_bytes": 15234,
      "created_at": "2025-10-29T16:00:00Z",
      "expires_at": "2025-10-29T16:05:00Z",
      "hits": 120,
      "last_accessed": "2025-10-29T16:04:15Z"
    }
  ]
}
```

---

### POST /api/dna/cache/clear

Clear entire cache manually.

**Response:**
```json
{
  "success": true,
  "entries_cleared": 45,
  "message": "Cache cleared successfully"
}
```

---

### DELETE /api/dna/cache/{key}

Invalidate specific cache entry.

**Path Parameters:**
- `key`: Cache key (e.g., `dna/smk`)

**Response:**
```json
{
  "success": true,
  "key": "dna/smk",
  "message": "Cache entry invalidated"
}
```

---

### DELETE /api/dna/cache/pattern/{pattern}

Invalidate cache entries matching pattern.

**Path Parameters:**
- `pattern`: Pattern (e.g., `dna/blocks/*`)

**Response:**
```json
{
  "success": true,
  "pattern": "dna/blocks/*",
  "entries_invalidated": 12,
  "message": "Cache pattern invalidated"
}
```

---

## Advanced Queries

### POST /api/dna/search

Full-text search with relevance scoring.

**Request Body:**
```json
{
  "query": "blockchain DNA",
  "gene_types": ["smk", "mutation"],
  "min_relevance": 0.5,
  "limit": 10
}
```

**Response:**
```json
{
  "results": [
    {
      "block_index": 5,
      "gene_type": "smk",
      "title": "GENOMOS Agent DNA Blockchain",
      "relevance_score": 0.92,
      "matched_fields": ["title", "content"],
      "preview": "...blockchain as agent DNA..."
    },
    {
      "block_index": 3,
      "gene_type": "mutation",
      "relevance_score": 0.67,
      "matched_fields": ["data"],
      "preview": "...DNA validation..."
    }
  ],
  "total_results": 2,
  "query": "blockchain DNA",
  "execution_time_ms": 45
}
```

---

### POST /api/dna/query

Complex multi-filter queries.

**Request Body:**
```json
{
  "gene_types": ["smk", "mutation"],
  "agents": ["orion", "lira"],
  "tags": ["blockchain", "genomos"],
  "date_range": {
    "start": "2025-10-01",
    "end": "2025-10-31"
  },
  "limit": 50,
  "offset": 0
}
```

**Response:**
```json
{
  "results": [
    {
      "block_index": 5,
      "gene_type": "smk",
      "agent": "orion",
      "tags": ["blockchain", "genomos"],
      "timestamp": "2025-10-28T11:00:00Z",
      "data": {...}
    }
  ],
  "total_matches": 12,
  "filters_applied": {
    "gene_types": ["smk", "mutation"],
    "agents": ["orion", "lira"],
    "tags": ["blockchain", "genomos"]
  },
  "execution_time_ms": 28
}
```

---

### POST /api/dna/aggregate

Aggregation queries (group by).

**Request Body:**
```json
{
  "group_by": "gene_type",
  "count_field": "index",
  "filters": {
    "agent": "orion",
    "date_range": {
      "start": "2025-10-01",
      "end": "2025-10-31"
    }
  }
}
```

**Response:**
```json
{
  "aggregation": {
    "smk": 12,
    "mutation": 3,
    "consultation": 2
  },
  "group_by": "gene_type",
  "total_count": 17,
  "filters_applied": {"agent": "orion"}
}
```

---

### POST /api/dna/batch

Batch query execution.

**Request Body:**
```json
{
  "queries": [
    {
      "id": "query1",
      "type": "search",
      "params": {"query": "blockchain"}
    },
    {
      "id": "query2",
      "type": "aggregate",
      "params": {"group_by": "gene_type"}
    },
    {
      "id": "query3",
      "type": "filter",
      "params": {"gene_types": ["smk"], "agent": "orion"}
    }
  ]
}
```

**Response:**
```json
{
  "results": [
    {
      "id": "query1",
      "success": true,
      "data": {"results": [...], "total_results": 4}
    },
    {
      "id": "query2",
      "success": true,
      "data": {"aggregation": {"smk": 15, "mutation": 4}}
    },
    {
      "id": "query3",
      "success": true,
      "data": {"results": [...], "total_matches": 12}
    }
  ],
  "total_queries": 3,
  "successful": 3,
  "failed": 0,
  "execution_time_ms": 78
}
```

---

### GET /api/dna/blocks/range

Get range of blocks.

**Query Parameters:**
- `start`: Start index (inclusive)
- `end`: End index (inclusive)

**Response:**
```json
{
  "blocks": [
    {"index": 5, "gene_type": "smk", ...},
    {"index": 6, "gene_type": "mutation", ...},
    {"index": 7, "gene_type": "smk", ...}
  ],
  "range": {"start": 5, "end": 7},
  "count": 3
}
```

---

## Visualization

### GET /api/dna/visualize/timeline

Get timeline visualization data for D3.js.

**Response Model:** `TimelineVisualization`

```bash
curl http://localhost:8000/api/dna/visualize/timeline
```

**Response:**
```json
{
  "blocks": [
    {
      "index": 0,
      "timestamp": "2025-10-28T10:00:00Z",
      "gene_type": "genesis",
      "color": "#FFD700",
      "title": "Constitution V1.1",
      "agent": "coalition"
    },
    {
      "index": 5,
      "timestamp": "2025-10-29T08:00:00Z",
      "gene_type": "smk",
      "color": "#4682B4",
      "title": "GENOMOS",
      "agent": "claude-code"
    }
  ],
  "start_date": "2025-10-28T10:00:00Z",
  "end_date": "2025-10-29T15:30:00Z",
  "total_blocks": 20
}
```

**D3.js Usage:**
```javascript
d3.json("http://localhost:8000/api/dna/visualize/timeline")
  .then(data => {
    const svg = d3.select("#timeline");
    svg.selectAll("circle")
      .data(data.blocks)
      .enter()
      .append("circle")
      .attr("cx", d => xScale(new Date(d.timestamp)))
      .attr("cy", 50)
      .attr("r", 5)
      .attr("fill", d => d.color)
      .append("title").text(d => d.title);
  });
```

---

### GET /api/dna/visualize/explorer

Get block explorer page.

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Blocks per page (default: 10)

**Response Model:** `BlockExplorerPage`

```bash
curl "http://localhost:8000/api/dna/visualize/explorer?page=1&per_page=10"
```

**Response:**
```json
{
  "blocks": [
    {
      "index": 0,
      "hash": "633d3f1e...",
      "previous_hash": "0",
      "timestamp": "2025-10-28T10:00:00Z",
      "gene_type": "genesis",
      "agent": "coalition",
      "tags": ["constitution"],
      "data_preview": "Homo Lumen Coalition Constitution V1.1..."
    }
  ],
  "page": 1,
  "per_page": 10,
  "total_blocks": 20,
  "total_pages": 2
}
```

---

### GET /api/dna/visualize/agents

Get agent activity dashboard.

**Response Model:** `AgentActivityDashboard`

```bash
curl http://localhost:8000/api/dna/visualize/agents
```

**Response:**
```json
{
  "agents": [
    {
      "name": "orion",
      "total_genes": 12,
      "gene_distribution": {
        "smk": 10,
        "mutation": 2
      },
      "first_activity": "2025-10-28T11:00:00Z",
      "last_activity": "2025-10-29T14:00:00Z",
      "activity_days": 2
    },
    {
      "name": "lira",
      "total_genes": 3,
      "gene_distribution": {
        "smk": 2,
        "consultation": 1
      },
      "first_activity": "2025-10-28T15:00:00Z",
      "last_activity": "2025-10-29T10:00:00Z",
      "activity_days": 2
    }
  ],
  "total_agents": 5,
  "most_active_agent": "orion",
  "total_genes": 20
}
```

---

### GET /api/dna/visualize/helix

Get 3D DNA helix visualization data (Three.js compatible).

**Response Model:** `DNAHelixVisualization`

```bash
curl http://localhost:8000/api/dna/visualize/helix
```

**Response:**
```json
{
  "nodes": [
    {
      "index": 0,
      "x": 0.0,
      "y": 0.0,
      "z": 0.0,
      "radius": 2.0,
      "color": "#FFD700",
      "gene_type": "genesis",
      "label": "Constitution V1.1"
    },
    {
      "index": 1,
      "x": 1.2,
      "y": 0.8,
      "z": 0.5,
      "radius": 1.5,
      "color": "#4682B4",
      "gene_type": "smk",
      "label": "GENOMOS Phase 3"
    }
  ],
  "helix_parameters": {
    "turns": 2.5,
    "height": 100,
    "radius": 20
  },
  "camera_position": {"x": 0, "y": 50, "z": 100}
}
```

**Three.js Usage:**
```javascript
fetch("http://localhost:8000/api/dna/visualize/helix")
  .then(r => r.json())
  .then(data => {
    data.nodes.forEach(node => {
      const geometry = new THREE.SphereGeometry(node.radius);
      const material = new THREE.MeshBasicMaterial({ color: node.color });
      const sphere = new THREE.Mesh(geometry, material);
      sphere.position.set(node.x, node.y, node.z);
      scene.add(sphere);
    });
  });
```

---

### GET /api/dna/visualize/metrics

Get real-time metrics.

**Response Model:** `RealTimeMetrics`

```bash
curl http://localhost:8000/api/dna/visualize/metrics
```

**Response:**
```json
{
  "total_blocks": 20,
  "blocks_today": 4,
  "active_agents_today": 2,
  "cache_hit_rate": 0.82,
  "average_response_time_ms": 185,
  "chain_valid": true,
  "last_block_timestamp": "2025-10-29T15:30:00Z",
  "seconds_since_last_block": 3600,
  "gene_type_distribution": [
    {"gene_type": "genesis", "count": 1, "percentage": 5, "color": "#FFD700"},
    {"gene_type": "smk", "count": 15, "percentage": 75, "color": "#4682B4"},
    {"gene_type": "mutation", "count": 4, "percentage": 20, "color": "#FF6347"}
  ]
}
```

---

## Error Handling

### Standard Error Format

All errors follow this format:

```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE",
  "timestamp": "2025-10-29T16:00:00Z"
}
```

### Common HTTP Status Codes

- **200 OK:** Request successful
- **400 Bad Request:** Invalid request parameters
- **404 Not Found:** Resource not found
- **422 Unprocessable Entity:** Validation error
- **500 Internal Server Error:** Server error
- **503 Service Unavailable:** Blockchain not initialized

### Error Examples

**404 Not Found:**
```json
{
  "detail": "SMK #999 not found",
  "error_code": "SMK_NOT_FOUND",
  "timestamp": "2025-10-29T16:00:00Z"
}
```

**422 Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "query"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Chain validation failed: Block #5 invalid",
  "error_code": "CHAIN_VALIDATION_FAILED",
  "timestamp": "2025-10-29T16:00:00Z"
}
```

---

## Rate Limiting

**Current Status:** No rate limiting (local deployment)

**Future:** Rate limiting for production

```
Rate Limit: 1000 requests/hour per IP
Headers:
  X-RateLimit-Limit: 1000
  X-RateLimit-Remaining: 847
  X-RateLimit-Reset: 1698674400 (Unix timestamp)
```

**Exceeded Rate Limit:**
```json
{
  "detail": "Rate limit exceeded. Try again in 15 minutes.",
  "error_code": "RATE_LIMIT_EXCEEDED",
  "retry_after": 900
}
```

---

## Examples

### Example 1: Add SMK + Validate + Query

```bash
# 1. Add SMK gene
curl -X POST http://localhost:8000/api/dna/smk \
  -H "Content-Type: application/json" \
  -d '{
    "smk_number": "045",
    "title": "Example SMK",
    "agent": "developer",
    "data": {"content": "..."}
  }'

# 2. Validate chain
curl http://localhost:8000/api/dna/validate

# 3. Query new SMK
curl http://localhost:8000/api/dna/smk/045
```

### Example 2: Smart Contract Validation

```bash
curl -X POST http://localhost:8000/api/dna/contracts/validate \
  -H "Content-Type: application/json" \
  -d '{
    "biofelt_context": {"hrv_ms": 75, "stress_level": 3},
    "mutation": {
      "operation": "write",
      "target_path": "api/new_feature.py",
      "confirmed": true
    }
  }'
```

### Example 3: Full-Text Search + Aggregation

```bash
# Search
curl -X POST http://localhost:8000/api/dna/search \
  -H "Content-Type: application/json" \
  -d '{"query": "blockchain", "min_relevance": 0.5}'

# Aggregate results
curl -X POST http://localhost:8000/api/dna/aggregate \
  -H "Content-Type: application/json" \
  -d '{"group_by": "agent"}'
```

### Example 4: Backup Workflow

```bash
# Create backup
curl -X POST http://localhost:8000/api/dna/backup/create

# Response: {"backup_path": "backups/genomos_backup_20251029_091326.json", ...}

# Verify backup
curl -X POST http://localhost:8000/api/dna/backup/verify \
  -H "Content-Type: application/json" \
  -d '{"backup_path": "backups/genomos_backup_20251029_091326.json"}'

# Response: {"valid": true, ...}
```

### Example 5: D3.js Timeline Visualization

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://d3js.org/d3.v7.min.js"></script>
</head>
<body>
  <svg id="timeline" width="800" height="200"></svg>
  <script>
    d3.json("http://localhost:8000/api/dna/visualize/timeline")
      .then(data => {
        const svg = d3.select("#timeline");
        const xScale = d3.scaleTime()
          .domain([new Date(data.start_date), new Date(data.end_date)])
          .range([50, 750]);

        svg.selectAll("circle")
          .data(data.blocks)
          .enter()
          .append("circle")
          .attr("cx", d => xScale(new Date(d.timestamp)))
          .attr("cy", 100)
          .attr("r", 8)
          .attr("fill", d => d.color)
          .append("title").text(d => `${d.title} (${d.agent})`);
      });
  </script>
</body>
</html>
```

---

## Additional Resources

- **OpenAPI Docs:** `http://localhost:8000/docs` (auto-generated)
- **ReDoc:** `http://localhost:8000/redoc` (alternative docs)
- **SMK#042:** [Technical Documentation](../SMK/SMK#042_GENOMOS-Agent-DNA-Blockchain-Complete-System.md)
- **Developer Guide:** [GENOMOS_DEVELOPER_GUIDE.md](./GENOMOS_DEVELOPER_GUIDE.md)
- **Code:** `ubuntu-playground/api/routers/dna_api.py`

---

**Questions or Issues?**

Open an issue in the repository or contact the Homo Lumen Coalition.

---

*"The genome is the collective memory - permanent, queryable, verifiable, evolutionary"*
— GENOMOS API Documentation v1.0.0
