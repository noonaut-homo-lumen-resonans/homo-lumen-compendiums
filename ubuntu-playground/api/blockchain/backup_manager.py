"""
Backup Manager for GENOMOS Phase 9

Provides export, backup, and verification functionality for the blockchain.
Includes cryptographic verification and snapshot management.
"""

import json
import csv
import hashlib
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
from blockchain.agent_dna_chain import AgentDNAChain
from blockchain.dna_block import GeneType


class BackupManager:
    """
    Manages blockchain exports, backups, and verification.

    GENOMOS Phase 9: Export & Backup Systems
    """

    def __init__(self, blockchain: Optional[AgentDNAChain] = None, db_path: str = "./data/genomos.db"):
        """
        Initialize backup manager.

        Args:
            blockchain: Pre-loaded blockchain instance (optional)
            db_path: Path to GENOMOS database if blockchain not provided
        """
        if blockchain is None:
            blockchain = AgentDNAChain(db_path=db_path)
        self.blockchain = blockchain

    def export_to_json(
        self,
        include_genesis: bool = True,
        gene_types: Optional[List[str]] = None,
        pretty: bool = True
    ) -> Dict[str, Any]:
        """
        Export blockchain to JSON format.

        Args:
            include_genesis: Whether to include genesis block
            gene_types: Filter by specific gene types (None = all)
            pretty: Pretty-print JSON (vs compact)

        Returns:
            Dict with blockchain data ready for JSON serialization
        """
        blocks_data = []
        start_idx = 0 if include_genesis else 1

        for block in self.blockchain.chain[start_idx:]:
            # Filter by gene type if specified
            if gene_types:
                gene_type_str = block.gene_type.value if hasattr(block.gene_type, 'value') else str(block.gene_type)
                if gene_type_str not in gene_types:
                    continue

            block_data = {
                "index": block.index,
                "timestamp": block.timestamp,
                "gene_type": block.gene_type.value if hasattr(block.gene_type, 'value') else str(block.gene_type),
                "data": block.data,
                "agent": block.agent if hasattr(block, 'agent') else None,
                "tags": block.tags if hasattr(block, 'tags') else [],
                "hash": block.hash,
                "previous_hash": block.previous_hash
            }
            blocks_data.append(block_data)

        export_data = {
            "export_metadata": {
                "export_timestamp": datetime.now().isoformat(),
                "total_blocks": len(blocks_data),
                "genesis_included": include_genesis,
                "gene_type_filter": gene_types,
                "blockchain_db_path": self.blockchain.db_path if hasattr(self.blockchain, 'db_path') else None
            },
            "blockchain_info": {
                "total_blocks_in_chain": len(self.blockchain.chain),
                "genesis_hash": self.blockchain.chain[0].hash,
                "latest_hash": self.blockchain.chain[-1].hash,
                "is_valid": self.blockchain.validate_chain()
            },
            "blocks": blocks_data
        }

        return export_data

    def export_to_csv(
        self,
        output_path: Optional[str] = None,
        include_genesis: bool = True,
        gene_types: Optional[List[str]] = None
    ) -> str:
        """
        Export blockchain to CSV format.

        Args:
            output_path: Path to save CSV file (None = return CSV string)
            include_genesis: Whether to include genesis block
            gene_types: Filter by specific gene types

        Returns:
            CSV content as string
        """
        import io

        csv_buffer = io.StringIO()
        csv_writer = csv.writer(csv_buffer)

        # CSV headers
        csv_writer.writerow([
            "index",
            "timestamp",
            "gene_type",
            "agent",
            "tags",
            "hash",
            "previous_hash",
            "data_json"
        ])

        start_idx = 0 if include_genesis else 1

        for block in self.blockchain.chain[start_idx:]:
            # Filter by gene type
            if gene_types:
                gene_type_str = block.gene_type.value if hasattr(block.gene_type, 'value') else str(block.gene_type)
                if gene_type_str not in gene_types:
                    continue

            csv_writer.writerow([
                block.index,
                block.timestamp,
                block.gene_type.value if hasattr(block.gene_type, 'value') else str(block.gene_type),
                block.agent if hasattr(block, 'agent') else "",
                ",".join(block.tags) if hasattr(block, 'tags') else "",
                block.hash,
                block.previous_hash,
                json.dumps(block.data)  # Data as JSON string
            ])

        csv_content = csv_buffer.getvalue()
        csv_buffer.close()

        # Optionally save to file
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(csv_content)

        return csv_content

    def create_backup(
        self,
        backup_dir: str = "./backups",
        include_metadata: bool = True
    ) -> Dict[str, Any]:
        """
        Create a complete blockchain backup with cryptographic verification.

        Args:
            backup_dir: Directory to store backup files
            include_metadata: Include blockchain metadata

        Returns:
            Dict with backup information
        """
        backup_path = Path(backup_dir)
        backup_path.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"genomos_backup_{timestamp}.json"
        backup_filepath = backup_path / backup_filename

        # Export blockchain to JSON
        export_data = self.export_to_json(include_genesis=True, pretty=True)

        # Add backup-specific metadata
        export_data["backup_metadata"] = {
            "backup_timestamp": datetime.now().isoformat(),
            "backup_filename": backup_filename,
            "backup_version": "1.0"
        }

        # Calculate backup hash (for verification)
        backup_json = json.dumps(export_data, sort_keys=True, indent=2)
        backup_hash = hashlib.sha256(backup_json.encode('utf-8')).hexdigest()

        # Save backup file
        with open(backup_filepath, 'w', encoding='utf-8') as f:
            f.write(backup_json)

        # Create verification file
        verification_filepath = backup_path / f"{backup_filename}.sha256"
        with open(verification_filepath, 'w', encoding='utf-8') as f:
            f.write(f"{backup_hash}  {backup_filename}\n")

        return {
            "success": True,
            "backup_file": str(backup_filepath),
            "verification_file": str(verification_filepath),
            "backup_hash": backup_hash,
            "total_blocks": export_data["export_metadata"]["total_blocks"],
            "file_size_bytes": backup_filepath.stat().st_size,
            "timestamp": datetime.now().isoformat()
        }

    def verify_backup(self, backup_filepath: str) -> Dict[str, Any]:
        """
        Verify backup integrity using SHA-256 checksum.

        Args:
            backup_filepath: Path to backup JSON file

        Returns:
            Dict with verification results
        """
        backup_path = Path(backup_filepath)

        if not backup_path.exists():
            return {
                "valid": False,
                "error": f"Backup file not found: {backup_filepath}"
            }

        # Read backup file
        with open(backup_path, 'r', encoding='utf-8') as f:
            backup_content = f.read()

        # Calculate current hash
        current_hash = hashlib.sha256(backup_content.encode('utf-8')).hexdigest()

        # Check for verification file
        verification_path = backup_path.parent / f"{backup_path.name}.sha256"

        if verification_path.exists():
            with open(verification_path, 'r', encoding='utf-8') as f:
                stored_hash = f.read().strip().split()[0]

            hash_match = (current_hash == stored_hash)

            return {
                "valid": hash_match,
                "current_hash": current_hash,
                "stored_hash": stored_hash,
                "verification_file": str(verification_path),
                "backup_file": str(backup_path),
                "file_size_bytes": backup_path.stat().st_size
            }
        else:
            return {
                "valid": None,  # Cannot verify without hash file
                "current_hash": current_hash,
                "warning": "No verification file found (.sha256)",
                "backup_file": str(backup_path)
            }

    def get_backup_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about blockchain suitable for backup planning.

        Returns:
            Dict with blockchain statistics
        """
        total_blocks = len(self.blockchain.chain)

        # Gene type distribution
        gene_distribution = {}
        total_data_size = 0

        for block in self.blockchain.chain[1:]:  # Skip genesis
            gene_type = block.gene_type.value if hasattr(block.gene_type, 'value') else str(block.gene_type)
            gene_distribution[gene_type] = gene_distribution.get(gene_type, 0) + 1

            # Estimate data size
            data_size = len(json.dumps(block.data))
            total_data_size += data_size

        # Calculate estimated backup size
        estimated_backup_size = total_data_size + (total_blocks * 500)  # +500 bytes metadata per block

        return {
            "total_blocks": total_blocks,
            "gene_distribution": gene_distribution,
            "estimated_backup_size_bytes": estimated_backup_size,
            "estimated_backup_size_kb": round(estimated_backup_size / 1024, 2),
            "estimated_backup_size_mb": round(estimated_backup_size / (1024 * 1024), 2),
            "blockchain_valid": self.blockchain.validate_chain(),
            "genesis_hash": self.blockchain.chain[0].hash,
            "latest_hash": self.blockchain.chain[-1].hash
        }
