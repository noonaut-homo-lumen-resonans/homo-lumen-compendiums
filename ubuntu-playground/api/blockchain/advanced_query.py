"""
GENOMOS Advanced Query Builder - Phase 11: Comprehensive Query API

Advanced querying capabilities for the Agent DNA Blockchain.
Supports full-text search, complex filtering, and aggregations.

Philosophy: "Query the genome with precision - find patterns in the collective memory"
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import re
import logging
from blockchain.agent_dna_chain import AgentDNAChain
from blockchain.dna_block import DNABlock, GeneType

logger = logging.getLogger(__name__)


class AdvancedQueryBuilder:
    """
    Advanced query builder for GENOMOS blockchain.

    Features:
    - Full-text search across all gene data
    - Complex filtering (AND/OR conditions)
    - Date range queries
    - Aggregations (count, group by)
    - Sorting and limiting
    """

    def __init__(self, blockchain: AgentDNAChain):
        """
        Initialize query builder.

        Args:
            blockchain: AgentDNAChain instance to query
        """
        self.blockchain = blockchain
        self.logger = logging.getLogger(__name__)

    def full_text_search(
        self,
        query: str,
        gene_types: Optional[List[str]] = None,
        case_sensitive: bool = False,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Perform full-text search across all gene data.

        Args:
            query: Search query string
            gene_types: Filter by specific gene types (None = all)
            case_sensitive: Whether search is case-sensitive
            limit: Maximum results to return

        Returns:
            List of matching blocks with relevance scores
        """
        results = []

        # Prepare search pattern
        if not case_sensitive:
            pattern = re.compile(re.escape(query), re.IGNORECASE)
        else:
            pattern = re.compile(re.escape(query))

        for block in self.blockchain.chain:
            # Skip genesis if not relevant
            if block.index == 0 and gene_types and "genesis" not in gene_types:
                continue

            # Filter by gene type
            if gene_types and block.gene_type not in gene_types:
                continue

            # Search in block data
            block_text = str(block.data)
            matches = pattern.findall(block_text)

            if matches:
                relevance_score = len(matches)  # Simple relevance: count of matches

                results.append({
                    "block_index": block.index,
                    "gene_type": block.gene_type,
                    "agent": block.agent,
                    "timestamp": block.timestamp,
                    "hash": block.hash,
                    "relevance_score": relevance_score,
                    "match_count": len(matches),
                    "preview": self._generate_preview(block_text, query, 150)
                })

            if len(results) >= limit:
                break

        # Sort by relevance score (highest first)
        results.sort(key=lambda x: x["relevance_score"], reverse=True)

        self.logger.info(f"🔍 Full-text search: '{query}' - Found {len(results)} results")
        return results

    def complex_query(
        self,
        filters: Dict[str, Any],
        sort_by: Optional[str] = "timestamp",
        sort_order: str = "desc",
        limit: int = 100,
        offset: int = 0
    ) -> Tuple[List[DNABlock], int]:
        """
        Execute complex query with multiple filters.

        Args:
            filters: Dictionary of filter conditions
                - gene_types: List[str] - Filter by gene types
                - agents: List[str] - Filter by agents
                - tags: List[str] - Filter by tags (any match)
                - date_from: str - ISO date string (inclusive)
                - date_to: str - ISO date string (inclusive)
                - has_field: str - Check if data contains field
                - field_equals: Dict[str, Any] - Field exact match
            sort_by: Field to sort by (timestamp, index, gene_type)
            sort_order: 'asc' or 'desc'
            limit: Maximum results
            offset: Skip first N results

        Returns:
            Tuple of (matching blocks, total count)
        """
        matching_blocks = []

        for block in self.blockchain.chain:
            if self._matches_filters(block, filters):
                matching_blocks.append(block)

        # Total count before pagination
        total_count = len(matching_blocks)

        # Sort results
        matching_blocks = self._sort_blocks(matching_blocks, sort_by, sort_order)

        # Apply pagination
        paginated_results = matching_blocks[offset:offset + limit]

        self.logger.info(f"📊 Complex query: {len(paginated_results)}/{total_count} results (offset: {offset})")
        return paginated_results, total_count

    def aggregate(
        self,
        group_by: str,
        filters: Optional[Dict[str, Any]] = None,
        agg_functions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Aggregate blockchain data.

        Args:
            group_by: Field to group by (gene_type, agent, date, etc.)
            filters: Optional filters to apply before aggregating
            agg_functions: Aggregation functions ['count', 'first_date', 'last_date']

        Returns:
            Aggregation results
        """
        if agg_functions is None:
            agg_functions = ["count"]

        # Apply filters if provided
        if filters:
            blocks, _ = self.complex_query(filters, limit=len(self.blockchain.chain))
        else:
            blocks = self.blockchain.chain

        # Group blocks
        groups: Dict[str, List[DNABlock]] = {}

        for block in blocks:
            key = self._get_group_key(block, group_by)
            if key not in groups:
                groups[key] = []
            groups[key].append(block)

        # Apply aggregation functions
        results = {}
        for key, group_blocks in groups.items():
            results[key] = self._apply_aggregations(group_blocks, agg_functions)

        self.logger.info(f"📈 Aggregation by '{group_by}': {len(results)} groups")
        return {
            "group_by": group_by,
            "total_groups": len(results),
            "groups": results
        }

    def get_block_range(
        self,
        start_index: int,
        end_index: int,
        include_data: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get a range of blocks by index.

        Args:
            start_index: Starting block index (inclusive)
            end_index: Ending block index (inclusive)
            include_data: Whether to include full block data

        Returns:
            List of blocks in range
        """
        if start_index < 0 or end_index >= len(self.blockchain.chain):
            raise ValueError(f"Invalid range: {start_index}-{end_index} (chain length: {len(self.blockchain.chain)})")

        if start_index > end_index:
            raise ValueError(f"Start index ({start_index}) must be <= end index ({end_index})")

        results = []
        for i in range(start_index, end_index + 1):
            block = self.blockchain.chain[i]
            block_dict = {
                "index": block.index,
                "gene_type": block.gene_type,
                "agent": block.agent,
                "timestamp": block.timestamp,
                "hash": block.hash
            }

            if include_data:
                block_dict["data"] = block.data
                block_dict["tags"] = block.tags

            results.append(block_dict)

        return results

    def batch_query(
        self,
        queries: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Execute multiple queries in a single request.

        Args:
            queries: List of query specifications
                Each query should have: {"type": "search"|"complex"|"aggregate", "params": {...}}

        Returns:
            List of query results
        """
        results = []

        for i, query_spec in enumerate(queries):
            query_type = query_spec.get("type")
            params = query_spec.get("params", {})

            try:
                if query_type == "search":
                    result = self.full_text_search(**params)
                elif query_type == "complex":
                    blocks, total = self.complex_query(**params)
                    result = {
                        "blocks": [self._block_to_dict(b) for b in blocks],
                        "total": total
                    }
                elif query_type == "aggregate":
                    result = self.aggregate(**params)
                else:
                    result = {"error": f"Unknown query type: {query_type}"}

                results.append({
                    "query_index": i,
                    "success": True,
                    "result": result
                })

            except Exception as e:
                self.logger.error(f"Batch query {i} failed: {str(e)}")
                results.append({
                    "query_index": i,
                    "success": False,
                    "error": str(e)
                })

        return results

    # Helper methods

    def _matches_filters(self, block: DNABlock, filters: Dict[str, Any]) -> bool:
        """Check if block matches all filters."""

        # Gene type filter
        if "gene_types" in filters:
            if block.gene_type not in filters["gene_types"]:
                return False

        # Agent filter
        if "agents" in filters:
            if block.agent not in filters["agents"]:
                return False

        # Tags filter (any match)
        if "tags" in filters:
            if not any(tag in block.tags for tag in filters["tags"]):
                return False

        # Date range filters
        if "date_from" in filters:
            block_date = datetime.fromisoformat(block.timestamp.replace('Z', '+00:00'))
            filter_date = datetime.fromisoformat(filters["date_from"])
            if block_date < filter_date:
                return False

        if "date_to" in filters:
            block_date = datetime.fromisoformat(block.timestamp.replace('Z', '+00:00'))
            filter_date = datetime.fromisoformat(filters["date_to"])
            if block_date > filter_date:
                return False

        # Field existence check
        if "has_field" in filters:
            if filters["has_field"] not in block.data:
                return False

        # Field exact match
        if "field_equals" in filters:
            for field, value in filters["field_equals"].items():
                if block.data.get(field) != value:
                    return False

        return True

    def _sort_blocks(
        self,
        blocks: List[DNABlock],
        sort_by: str,
        sort_order: str
    ) -> List[DNABlock]:
        """Sort blocks by specified field."""
        reverse = (sort_order.lower() == "desc")

        if sort_by == "index":
            return sorted(blocks, key=lambda b: b.index, reverse=reverse)
        elif sort_by == "timestamp":
            return sorted(blocks, key=lambda b: b.timestamp, reverse=reverse)
        elif sort_by == "gene_type":
            return sorted(blocks, key=lambda b: b.gene_type, reverse=reverse)
        else:
            return blocks  # No sorting

    def _get_group_key(self, block: DNABlock, group_by: str) -> str:
        """Get grouping key for block."""
        if group_by == "gene_type":
            return block.gene_type
        elif group_by == "agent":
            return block.agent or "unknown"
        elif group_by == "date":
            # Group by date (YYYY-MM-DD)
            return block.timestamp[:10]
        elif group_by == "year":
            return block.timestamp[:4]
        elif group_by == "month":
            return block.timestamp[:7]  # YYYY-MM
        else:
            return "all"

    def _apply_aggregations(
        self,
        blocks: List[DNABlock],
        agg_functions: List[str]
    ) -> Dict[str, Any]:
        """Apply aggregation functions to block group."""
        result = {}

        if "count" in agg_functions:
            result["count"] = len(blocks)

        if "first_date" in agg_functions:
            result["first_date"] = min(b.timestamp for b in blocks)

        if "last_date" in agg_functions:
            result["last_date"] = max(b.timestamp for b in blocks)

        return result

    def _generate_preview(self, text: str, query: str, max_length: int = 150) -> str:
        """Generate preview snippet with highlighted query."""
        # Find first occurrence
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        match = pattern.search(text)

        if not match:
            return text[:max_length] + "..." if len(text) > max_length else text

        start = max(0, match.start() - 50)
        end = min(len(text), match.end() + max_length - 50)

        preview = text[start:end]
        if start > 0:
            preview = "..." + preview
        if end < len(text):
            preview = preview + "..."

        return preview

    def _block_to_dict(self, block: DNABlock) -> Dict[str, Any]:
        """Convert DNABlock to dictionary."""
        return {
            "index": block.index,
            "timestamp": block.timestamp,
            "gene_type": block.gene_type,
            "agent": block.agent,
            "tags": block.tags,
            "hash": block.hash,
            "previous_hash": block.previous_hash,
            "data": block.data
        }
